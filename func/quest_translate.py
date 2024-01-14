import logging
from copy import copy

from nbt import nbt
from tqdm import tqdm
from func.base import *

LOW = False


def trans_field_snbt(quest: dict) -> dict:
    """
    翻译此层关键字段（不涉及内部）
    :param quest:任务dict
    :return:完成指定的部分翻译的dict
    """
    trans_key = ['title', 'subtitle', 'text', 'description']
    KEEP_ORIGINAL = global_var.get_value('KEEP_ORIGINAL')
    for key in quest:
        try:
            if key in trans_key:  # 匹配到关键key才进行翻译
                if isinstance(quest[key], list):  # 文本可能多行，以list形式为判断
                    line_list = quest[key]
                    post_translate_list = []
                    for index in range(0, len(line_list)):
                        if bool(re.search('[a-zA-Z]', line_list[index])):  # 忽略无字母的无效行
                            print(f"\r翻译中：\n{TextStyle.YELLOW + line_list[index] + TextStyle.RESET}")
                            pre_line = pre_process(line_list[index])
                            if pre_line:  # 空返回为图片，保留，不处理
                                translate = translate_line(pre_line)
                                post_translate = post_process(pre_line, translate)
                                post_translate_list.append(post_translate)
                            else:
                                post_translate_list.append(line_list[index])
                            print(f"{TextStyle.GREEN + post_translate_list[-1] + TextStyle.RESET}")
                    if KEEP_ORIGINAL:
                        quest[key] = post_translate_list + quest[key]
                    else:
                        quest[key] = post_translate_list
                else:  # 单行文本
                    text = pre_process(quest[key])
                    if text:
                        translate = translate_line(text)
                        post_translate = post_process(quest[key], translate)
                        print(f"\r翻译中：\n{TextStyle.YELLOW+text}\n{TextStyle.GREEN+post_translate+TextStyle.RESET}")
                        if KEEP_ORIGINAL:
                            quest[key] = f"{post_translate}[--{quest[key]}--]"
                        else:
                            quest[key] = post_translate
        except Exception as e:
            logging.exception(e)
            print(TextStyle.RED + f'值为{quest[key]}的项遇到错误{e}，请手动处理' + TextStyle.RESET)
            continue
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
    quest, LOW = get_snbt_quest(input_path)
    quest = update_snbt(quest)  # 翻译相应内容
    with open(output_path, 'w', encoding="utf-8") as fout:
        fout.write(snbtlib.dumps(quest, compact=LOW))


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
    KEEP_ORIGINAL = global_var.get_value('KEEP_ORIGINAL')
    for key in quest.keys():
        try:
            if key in trans_key:  # 匹配到关键key才进行翻译
                if type(quest[key]) == nbt.TAG_List:  # 文本可能多行，以list形式为判断
                    line_list = quest[key]
                    post_translate_list = []
                    for index in range(0, len(line_list)):
                        if bool(re.search('[a-zA-Z]', line_list[index].value)):  # 忽略无字母的无效行
                            pre_line = pre_process(line_list[index].value)
                            if pre_line:  # 空返回为图片，保留，不处理
                                translate = translate_line(pre_line)
                                post_translate = post_process(pre_line, translate)
                                post_translate_list.append(post_translate)
                                print(f"\r翻译中：\n{TextStyle.YELLOW+pre_line}\n{TextStyle.GREEN+post_translate+TextStyle.RESET}")
                    if KEEP_ORIGINAL:
                        quest[key].value = post_translate_list + quest[key].value
                    else:
                        quest[key].value = post_translate_list
                else:  # 单行文本
                    line = quest[key].value
                    pre_line = pre_process(line)
                    if pre_line:
                        translate = translate_line(pre_line)
                        post_translate = post_process(quest[key].value, translate)
                        print(f"\r翻译中：\n{TextStyle.YELLOW+line}\n{TextStyle.GREEN+post_translate+TextStyle.RESET}")
                        if KEEP_ORIGINAL:
                            quest[key].value = f"{line}[--{post_translate}--]"
                        else:
                            quest[key].value = post_translate
        except Exception as e:
            print(TextStyle.RED + f'值为{quest[key]}的项遇到错误{e}，请手动处理' + TextStyle.RESET)
            continue
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
        try:
            input_path = t[i]
            output_path = make_output_path(input_path)  # 生成输出目录路径
            update_snbt_file(input_path, output_path)  # 更新任务文件
        except Exception as ex:
            print(TextStyle.RED, f"{i}在翻译时遇到错误:{ex}", TextStyle.RESET)
            continue
    t = list(quest_path.rglob("*.nbt"))
    for i in tqdm(range(0, len(t)), colour='#0396FF'):
        try:
            input_path = t[i]
            output_path = make_output_path(input_path)  # 生成输出目录路径
            update_nbt_file(input_path, output_path)  # 更新任务文件
        except Exception as ex:
            print(TextStyle.RED, f"{i}在翻译时遇到错误:{ex}", TextStyle.RESET)
            continue

    print("************翻译任务完成************")
