import json
from pathlib import Path
from func.base import *

from config import *


def get_quest(input_path: Path) -> str:
    with open(input_path, 'r', encoding="utf-8") as fin:
        quest = fin.read()
        try:
            quest = json.loads(quest)  # 转化为json格式并读取
            return quest
        except TypeError:
            print('lang文件读取出错，可能是所读取的json文件格式错误或其它问题！')


def update_quest_file(input_path: Path, output_path: Path) -> None:
    """
    更新文件，将处理完的文本写回
    :param input_path:输入目录
    :param output_path:输出目录
    :return:无
    """
    print('读取成功，正在翻译lang文件:', input_path)
    quest = get_quest(input_path)
    quest = update_quest(quest)  # 翻译相应内容
    with open(output_path, 'w', encoding="utf-8") as fout:
        print('翻译完成\n')
        fout.write(json.dumps(quest, indent=1, ensure_ascii=False))


def update_quest(quest: dict) -> dict:
    """
    更新任务中需要汉化的区域
    :param quest:任务dict
    :return:汉化后任务dict
    """
    for key in quest:
        line = quest[key]
        pre_processed_line = pre_process(line)
        translate = translate_line(pre_processed_line)
        replacement = post_process(line, translate)
        print("替换中：" + replacement)
        quest[key] = replacement
    return quest

def make_output_path(path: Path) -> Path:
    """
    生成输出目录，为原文件夹+trans
    :param path:输入目录路径
    :return:自动生成的输出目录路径
    """
    parts = list(path.parts)
    parts[0] = 'zh_cn.json'
    output_path = Path(*parts)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    return output_path


def lang_trans():
    input_path = Path(LANG_PATH)  # 要翻译的目录
    output_path = make_output_path(input_path)  # 生成输出目录路径
    quest = get_quest(input_path)
    update_quest_file(input_path, output_path)  # 更新任务文件
    print("你可以在en_us同级目录下的trans文件夹中找到翻译后的lang文件zh_cn.json.")
    print("************lang文件翻译完成************")

