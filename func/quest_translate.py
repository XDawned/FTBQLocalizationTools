from copy import copy

from nbt import nbt
from tqdm import tqdm
import snbtlib
from func.base import *

LOW = False


def trans_field_snbt(quest: dict) -> dict:
    """
    翻译此层关键字段（不涉及内部）
    :param quest:任务dict
    :return:完成指定的部分翻译的dict
    """
    trans_key = ['title', 'subtitle', 'text', 'description']
    for key in quest:
        if key in trans_key:  # 匹配到关键key才进行翻译
            if isinstance(quest[key], list):  # 文本可能多行，以list形式为判断
                line_list = quest[key]
                for index in range(0, len(line_list)):
                    if bool(re.search('[a-zA-Z]', line_list[index])):  # 忽略无字母的无效行
                        pre_line = pre_process(line_list[index])
                        if pre_line is not None:  # 空返回为图片，保留，不处理
                            translate = translate_line(pre_line)
                            replacement = post_process(pre_line, translate)
                            print("\r替换中：" + TextStyle.GREEN + replacement + TextStyle.RESET)
                            line_list[index] = replacement
                quest.update({key: line_list})  # 更新dict中文本
            else:  # 单行文本
                text = pre_process(quest[key])
                if text:
                    translate = translate_line(text)
                    replacement = post_process(quest[key], translate)
                    print("\r替换中：" + TextStyle.GREEN + replacement + TextStyle.RESET)
                    quest.update({key: replacement})  # 更新dict中文本
    return quest


def update_snbt(quest: dict) -> dict:
    """
    更新任务中需要汉化的区域
    :param quest:任务dict
    :return:汉化后任务dict
    """
    quest = trans_field_snbt(quest)  # 章节内容翻译
    quest_child = ['quests', 'chapter_groups']  # 选择翻译的内层节点（quests为章节下任务,chapter_groups为目录）
    for child in quest_child:
        if quest.get(child):
            quests = quest[child]
            for index in range(0, len(quests)):
                quests[index] = trans_field_snbt(quests[index])
            quest.update({child: quests})  # 覆盖
    if quest.get('quests'):
        quests_child = ['tasks']  # 任务中子节点quests下还可能存在更细一层的子任务tasks
        for child in quests_child:
            for i in range(0, len(quest['quests'])):  # quests可能有多个
                if quest['quests'][i].get(child):
                    tasks = quest['quests'][i][child]
                    for index in range(0, len(tasks)):  # tasks可能有多个
                        tasks[index] = trans_field_snbt(tasks[index])
                    quest['quests'][i].update({child: tasks})  # 覆盖原先quests下tasks
    return quest


def update_snbt_file(input_path: Path, output_path: Path) -> None:
    """
    更新文件，将处理完的文本写回
    :param input_path:输入目录
    :param output_path:输出目录
    :return:无
    """
    global LOW
    print("正在处理:" + TextStyle.LIGHT_YELLOW + str(input_path) + TextStyle.RESET)
    quest = get_snbt_quest(input_path)
    quest = update_snbt(quest)  # 翻译相应内容
    with open(output_path, 'w', encoding="utf-8") as fout:
        fout.write(snbtlib.dumps(quest, compact=LOW))


def get_snbt_quest(input_path: Path) -> str:
    with open(input_path, 'r', encoding="utf-8") as fin:
        quest = fin.read()
        try:
            quest = snbtlib.loads(quest)  # 转化为json格式并读取
            return quest
        except TypeError:
            print(TextStyle.RED, 'snbtlib调用出错，可能是python环境版本过低或其它问题！', TextStyle.RESET)


def update_nbt(quest: nbt.NBTFile) -> nbt.NBTFile:
    quest = trans_field_snbt(quest)  # 章节内容翻译
    quest_child = ['quests', 'chapter_groups']  # 选择翻译的内层节点（quests为章节下任务,chapter_groups为目录）
    for child in quest_child:
        if quest.get(child):
            quests = quest[child]
            for index in range(0, len(quests)):
                quests[index] = trans_field_snbt(quests[index])
            quest.update({child: quests})  # 覆盖
    if quest.get('quests'):
        quests_child = ['tasks']  # 任务中子节点quests下还可能存在更细一层的子任务tasks
        for child in quests_child:
            for i in range(0, len(quest['quests'])):  # quests可能有多个
                if quest['quests'][i].get(child):
                    tasks = quest['quests'][i][child]
                    for index in range(0, len(tasks)):  # tasks可能有多个
                        tasks[index] = trans_field_snbt(tasks[index])
                    quest['quests'][i].update({child: tasks})  # 覆盖原先quests下tasks
    return quest


def trans_field_nbt(quest):
    quest = copy(quest)
    trans_key = ['title', 'description', 'text']
    for key in quest.keys():
        if key in trans_key:  # 匹配到关键key才进行翻译
            if type(quest[key]) == nbt.TAG_List:  # 文本可能多行，以list形式为判断
                line_list = quest[key]
                for index in range(0, len(line_list)):
                    if bool(re.search('[a-zA-Z]', line_list[index].value)):  # 忽略无字母的无效行
                        pre_line = pre_process(line_list[index].value)
                        if pre_line:  # 空返回为图片，保留，不处理
                            translate = translate_line(pre_line)
                            replacement = post_process(pre_line, translate)
                            print("\r替换中：" + TextStyle.GREEN + replacement + TextStyle.RESET)
                            quest[key][index].value = replacement
            else:  # 单行文本
                t = quest[key].value
                text = pre_process(t)
                if text:
                    translate = translate_line(text)
                    replacement = post_process(quest[key].value, translate)
                    print("\r替换中：" + TextStyle.GREEN + replacement + TextStyle.RESET)
                    quest[key].value = replacement  # 更新dict中文本
    return quest


def update_nbt_file(input_path: Path, output_path: Path) -> None:
    print("正在处理:" + TextStyle.LIGHT_YELLOW + str(input_path) + TextStyle.RESET)
    quest = get_nbt_quest(input_path)
    if quest.get('tasks'):
        for i in range(0, len(quest['tasks'])):
            quest['tasks'][i] = trans_field_nbt(quest['tasks'][i])
    quest = trans_field_nbt(quest)
    quest.write_file(output_path)


def get_nbt_quest(input_path: Path) -> nbt.NBTFile:
    try:
        nbtfile = nbt.NBTFile(input_path, 'rb')
        return nbtfile
    except Exception:
        print(TextStyle.RED, 'nbt读取出错！', TextStyle.RESET)


def quest_trans():
    get_config()
    QUESTS_PATH = global_var.get_value('QUESTS_PATH')
    quest_path = Path(QUESTS_PATH)  # 要翻译的目录
    t = list(quest_path.rglob("*.snbt"))
    for i in tqdm(range(0, len(t)), colour='#0396FF'):
        input_path = t[i]
        output_path = make_output_path(input_path)  # 生成输出目录路径
        update_snbt_file(input_path, output_path)  # 更新任务文件
    t = list(quest_path.rglob("*.nbt"))
    for i in tqdm(range(0, len(t)), colour='#0396FF'):
        input_path = t[i]
        output_path = make_output_path(input_path)  # 生成输出目录路径
        update_nbt_file(input_path, output_path)  # 更新任务文件
    print("************翻译任务完成************")
