from typing import Tuple
from func.base import *


def get_text_fields(quest: str) -> list:
    """
    截取翻译区域
    :param quest: 任务文本
    :return: 截取到的title,subtitle,description,text文本指针
    """
    title_line = re.findall(r'\stitle: "(.*)"', quest)
    subtitle_line = re.findall(r'\ssubtitle: "(.*)"', quest)

    decription_lines = re.findall(r'\sdescription: \[[\n]*([^]]*)\]', quest)  # 先指定以关键字打头，再进一步匹配到左括号略过换行再截取所有右括号前字符，下同
    decription_lines = [re.findall(r'"(.+)"', x) for x in decription_lines]
    decription_lines = [token for t in decription_lines for token in t]  # 双层遍历降维

    text_search = re.search(r'\stext: \[[\n]*([^]]*)\]', quest)
    text_lines = re.findall(r'"(.+)"', text_search.group(1)) if text_search else ()

    line = []
    line.extend(title_line)
    line.extend(subtitle_line)
    line.extend(decription_lines)
    line.extend(text_lines)

    return line


def update_quest(quest: str, text_fields: Tuple[str]) -> str:
    """
    更新任务中需要汉化的区域
    :param quest:任务
    :param text_fields:摘取出的替换文本
    :return:汉化后任务
    """
    for line in text_fields:
        pre_processed_line = pre_process(line)
        translate = translate_line(pre_processed_line)
        replacement = post_process(line, translate)
        print("替换中：" + replacement)
        quest = quest.replace('\"' + line + '\"',
                              '\"' + replacement + '\"')  # 用双引号卡一下因为多处文本可能相同，防止重复替换替换到其它位置；处理过的就为 "原文[--*--]" 不再参与替换
    return quest


def update_quest_file(input_path: Path, output_path: Path) -> None:
    """
    更新文件，将处理完的文本写回
    :param input_path:输入目录
    :param output_path:输输出目录
    :return:无
    """
    with open(input_path, 'r', encoding="utf-8") as fin:
        quest = fin.read()
        text_fields = get_text_fields(quest)  # 截取翻译内容
        if not text_fields:
            print('无需翻译，未找到截取关键词', input_path)
            print(quest)
        else:
            print('开始翻译 {input_path}.')
        new_text = update_quest(quest, text_fields)

    with open(output_path, 'w', encoding="utf-8") as fout:
        fout.write(new_text)


def make_output_path(path: Path) -> Path:
    """
    生成输出目录，为原文件夹+trans
    :param path:输入目录路径
    :return:自动生成的输出目录路径
    """
    parts = list(path.parts)
    parts[0] = parts[0] + "-trans"
    output_path = Path(*parts)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    return output_path


def regular_trans():
    quest_path = Path(QUESTS_PATH)  # 要翻译的目录
    for input_path in quest_path.rglob("*.snbt"):
        output_path = make_output_path(input_path)  # 生成输出目录路径
        update_quest_file(input_path, output_path)  # 更新任务文件
    print("************翻译任务完成************")
