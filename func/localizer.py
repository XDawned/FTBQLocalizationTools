import copy
import json
import re
from collections import OrderedDict
from pathlib import Path
from uuid import uuid4

from nbt import nbt

from func.serializer import LangSerializer, SnbtSerializer, LangType, FTBQuestType, NbtSerializer, BaseSerializer


class Lang:
    data = None
    serializer = None
    lang_type = None

    def __init__(self, data:dict=None, lang_type:LangType=LangType.JSON):
        self.data = data
        self.lang_type = lang_type

    def load_file(self, file_path: Path):
        if file_path.suffix == '.lang':
            self.lang_type = LangType.LANG
            self.serializer = LangSerializer()
        elif file_path.suffix == '.json':
            self.lang_type = LangType.JSON
            self.serializer = LangSerializer()
        elif file_path.suffix == '.snbt':
            self.lang_type = LangType.SNBT
            self.serializer = SnbtSerializer()
        else:
            raise TypeError(f'Unsupported lang type: {file_path.suffix}')
        self.data = self.serializer.load(file_path)

    def write_file(self, data:dict, output_file_path:Path=None):
        return self.serializer.save(data, output_file_path)

    def __len__(self):
        return len(self.data)

    def __add__(self, other):
        merged = self.data.copy() if self.data else {}
        if isinstance(other, Lang):
            other_data = other.data
        elif isinstance(other, dict):
            other_data = other
        else:
            raise TypeError(f'Unsupported lang type: {type(other)}')
        for key, value in other_data.items():
            if key in merged:
                merged[f"{uuid4()}.{key}"] = value  # 自定义操作：相加（可以改成 max/min/str 拼接等）
            else:
                merged[key] = value
        return Lang(data=merged, lang_type=self.lang_type)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.data})'



class FTBQuestLocalizer:
    lang:Lang = None
    data:dict|nbt.NBTFile = None  # resolved task (snbt:dict,nbt:NBTFile)
    locale_data:dict|nbt.NBTFile = None  # the task data that has been replaced with key-value pairs
    serializer:NbtSerializer|SnbtSerializer = None
    quest_path:Path = None
    quest_name:str = ''
    quest_type:FTBQuestType = None
    accept_tags = ['title', 'description', 'subtitle', 'text', 'hover', 'Lore', 'Name', 'tasks']
    escape_keyword = ['{image:', '{@pagebreak}']

    def __init__(
            self,
            quest_path:Path=None,
            data:dict|nbt.NBTFile=None,
            quest_name:str=None,
            quest_type:FTBQuestType=None
    ):
        if all([data, quest_name, quest_type]):
            self.quest_name = quest_name
            self.data = data
            self.quest_type = quest_type
        elif quest_path is not None:
            self.quest_path = quest_path
            self.quest_name = self.get_quest_name_from_path(quest_path)
            self._load_from_file(quest_path)
        else:
            raise ValueError('You need to specify data + quest_type + quest_name or quest_path.')
        self.lang = Lang()

    @staticmethod
    def get_quest_name_from_path(quest_path:Path):
        return (list(quest_path.parts)[-1].
                replace('.snbt', '').
                replace('.nbt', ''))

    def _load_from_file(self, file_path: Path):
        if file_path.suffix == '.snbt':
            self.serializer = SnbtSerializer()
            self.data = self.serializer.load(file_path)
            self.quest_type = FTBQuestType.SNBT_OLD if self.serializer.is_low_version else FTBQuestType.SNBT
        elif file_path.suffix == '.nbt':
            self.serializer = NbtSerializer()
            self.data = self.serializer.load(file_path)
            self.quest_type = FTBQuestType.NBT
        else:
            raise TypeError(f'Unsupported ftbquests file type: {file_path.suffix}')

    @staticmethod
    def get_key_pairs(quest_name:str, data:dict)->list:
        # init key parts
        prefix_list = ['ftbquests']
        if data.get('chapter_groups'):
            prefix_list.append('chapter_groups')
        elif data.get('loot_size'):
            prefix_list.append('reward_tables')
        elif data.get('disable_gui'):
            prefix_list.append('data')
        else:
            prefix_list.append('chapter')
        prefix_list.append(quest_name)
        return prefix_list

    def _filter(self, text: str) -> bool:
        if not text:
            return False
        if text.startswith("{") and text.endswith("}"):
            return False
        if text.startswith("[") and text.endswith("]"):
            return False
        if not bool(re.search(r'\S', text)):
            return False
        if any(tag in text for tag in self.escape_keyword):
            return False
        return True

    def _extract(self, data, prefix: list, subtext_flag=False):
        # get the text to be translated
        extracted_lang = OrderedDict()
        prefix_ = copy.deepcopy(prefix)
        if isinstance(data, (dict, nbt.TAG_Compound)):
            for k_, v_ in data.items():
                child, child_data = self._extract(v_, prefix_ + [k_])
                data[k_] = child_data
                extracted_lang.update(child)
        elif type(data) in [list, nbt.TAG_LIST]:
            length_ = len(data)
            for idx in range(length_):
                line_prefix = prefix_ + [str(idx + 1)] if length_ > 1 else prefix_
                child, child_data = self._extract(data[idx], line_prefix, True)
                data[idx] = child_data
                extracted_lang.update(child)
        elif isinstance(data, str):
            single_line_flag = prefix_[-1] in self.accept_tags
            multi_line_flag = (subtext_flag and prefix_[-2] in self.accept_tags)
            if single_line_flag or multi_line_flag:
                if self._filter(data):
                    key = f"{'.'.join(prefix_)}"
                    extracted_lang[key] = data
                    data = '{' + key + '}'
        elif isinstance(data, nbt.TAG) and data.id == nbt.TAG_STRING:
            if prefix_[-1] in self.accept_tags or subtext_flag:
                key = f"{'.'.join(prefix_)}"
                extracted_lang[key] = data.lang
                data.lang = '{' + key + '}'
        return extracted_lang, data

    def save_to_path(self, output_path: Path=None):
        if self.serializer:
            self.serializer.save(self.data, output_path)
        else:
            if not output_path:
                raise AttributeError('No output path given')
            elif self.quest_type == FTBQuestType.SNBT:
                SnbtSerializer().save(self.data, output_path)
            elif self.quest_type == FTBQuestType.SNBT_OLD:
                serializer = SnbtSerializer()
                serializer.is_low_version = True
                serializer.save(self.data, output_path)
            elif self.quest_type == FTBQuestType.NBT:
                NbtSerializer().save(self.data, output_path)


    def extract_to_lang(self, lang_type:LangType=LangType.JSON):
        lang, self.locale_data = self._extract(
            copy.deepcopy(self.data),
            self.get_key_pairs(self.quest_name, self.data)
        )
        self.lang = Lang(lang, lang_type)

    def get_back_fill_quest(self, fill_lang: Lang, quest_type:FTBQuestType):
        text_ = json.dumps(self.locale_data, ensure_ascii=False)
        for key, value in fill_lang.data.items():
            text_ = text_.replace('{' + key + '}', str(value))
        return FTBQuestLocalizer(
            data=json.loads(text_),
            quest_type=quest_type,
            quest_name=self.quest_name
        )


if __name__ == '__main__':
    quest_folder = Path(r"D:\Coding\Project\FTBQLocalizationTools\ftbquests")
    res = Lang()
    for i in list(quest_folder.rglob("*.snbt")):
        localizer = FTBQuestLocalizer(i)
        res += localizer.extract_to_lang(LangType.JSON)
    print(res)
    print(len(res))