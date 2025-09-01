import json
import re
import snbtlib
from abc import ABC
from pathlib import Path
from nbt import nbt
from enum import Enum


class LangType(Enum):
    LANG = 0
    SNBT = 1
    JSON = 2

class FTBQuestType(Enum):
    SNBT = 0
    SNBT_OLD = 1
    NBT = 2


class BaseSerializer(ABC):
    """
    Use the same serializer to parse and dumps !!!
    """
    file_path:Path = None
    @staticmethod
    def load(file_path):
        pass

    @staticmethod
    def save(file_path):
        pass

    @staticmethod
    def make_output_path(path: Path) -> Path:
        """
        生成输出目录，为原文件夹+trans
        :param path:输入目录路径
        :return:自动生成的输出目录路径
        """
        if not path:
            raise AttributeError('No output path given')
        parts = list(path.parts)
        parts.insert(0, './output')
        output_path = Path(*parts)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        return output_path


class NbtSerializer(BaseSerializer):

    def load(self, file_path:Path)->nbt.NBTFile:
        if not file_path.suffix == '.nbt':
            raise TypeError(f'{file_path} must be a .nbt file')
        self.file_path = file_path
        return nbt.NBTFile(file_path, 'rb')

    def save(self, data:nbt.NBTFile, output_path:Path=None):
        output_path = output_path if output_path else self.make_output_path(self.file_path)
        data.write_file(output_path)


class SnbtSerializer(BaseSerializer):
    is_low_version = False

    def load(self, file_path:Path)->dict|list:
        if not file_path.suffix == '.snbt':
            raise TypeError(f'{file_path} must be a .snbt file')
        with open(file_path, 'r', encoding="utf-8") as fin:
            quest = fin.read()
            # check 1.12.2-old or lower version
            self.is_low_version = bool(re.search(r'\",$', quest, re.MULTILINE))
            self.file_path = file_path
            return snbtlib.loads(quest)

    def save(self, data:list|dict, output_path:Path=None):
        output_path = output_path if output_path else self.make_output_path(self.file_path)
        processed_text = snbtlib.dumps(data, compact=self.is_low_version)
        with open(output_path, 'w', encoding="utf-8") as f:
            f.write(processed_text)


class LangSerializer(BaseSerializer):
    def load(self, file_path:Path)-> dict | None:
        if not file_path.suffix  == '.lang' or file_path.suffix == '.json':
            raise TypeError(f'{file_path} must be a .lang or .json file')
        with open(file_path, 'r', encoding="utf-8") as fin:
            text = fin.read()
            self.file_path = file_path
            try:
                _res = json.loads(text)
            except json.decoder.JSONDecodeError:
                _res = {}
                for line in text.splitlines():
                    if line.startswith("#") or not line:
                        continue
                    key, value = re.compile('(.*)=(.*)').match(line).groups()
                    _res[key] = value.replace("%n", "\n")
                return _res
            except Exception as e:
                raise TypeError(f"Can't decode lang file from {file_path}") from e


    def save(self, data:dict, output_path:Path=None):
        output_path = output_path if output_path else self.make_output_path(self.file_path)
        processed_text = json.dumps(data, indent=1, ensure_ascii=False)
        with open(output_path, 'w', encoding="utf-8") as f:
            f.write(processed_text)

