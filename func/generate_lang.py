from config import *
from pathlib import Path
import re
import snbtlib
import json


def get_quest(input_path: Path) -> str:
    with open(input_path, 'r', encoding="utf-8") as fin:
        quest = fin.read()
        try:
            quest = snbtlib.loads(quest)  # 转化为json格式并读取
            return quest
        except TypeError:
            print('snbtlib调用出错，可能是python环境版本过低或其它问题！')
            sys.exit(0)


def all2line(text: list) -> str:
    """
    处理传来的文本：单行不处理，多行list则插换行符转为一行
    :param text:文本
    :return:单行文本
    """
    if isinstance(text, list):
        res = ''
        for line in text:
            if bool(re.search(r'\S', line)):  # 匹配到空行则插入换行
                res += line
            else:
                res += '\n'
        return res
    else:
        return text


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


def trans2lang():
    quest_path = Path(WORK_PATH)  # 要翻译的目录
    key_value = {}  # 用于存放新生成的键值及其对应的文本

    for input_path in quest_path.rglob("*.snbt"):
        output_path = make_output_path(input_path)
        quest = get_quest(input_path)
        prefix = ''+list(input_path.parts)[-1].replace('.snbt', '')  # 以snbt文件名为key的前缀便于回溯
        # chapter_groups[title]
        if quest.get('chapter_groups'):
            chapter_groups = quest['chapter_groups']
            for i in range(0, len(chapter_groups)):
                local_key = 'ftbquest.chapter_groups.' + prefix + str(i) + '.title'
                text = all2line(chapter_groups[i]['title'])
                key_value[local_key] = text
                quest['chapter_groups'][i]['title'] = '{' + local_key + '}'
            # 写入更新后的quest
            with open(output_path, 'w', encoding="utf-8") as fout:
                print("************", output_path, "snbt替换结束************")
                fout.write(snbtlib.dumps(quest))
            continue

        # loot_table[title]
        if quest.get('loot_size'):  # 仅以键值判断是否是loot_table内容
            title = quest['title']
            local_key = 'ftbquest.loot_table.' + prefix + '.title'
            text = all2line(quest['title'])
            key_value[local_key] = text
            quest['title'] = '{' + local_key + '}'
            # 写入更新后的quest
            with open(output_path, 'w', encoding="utf-8") as fout:
                print("************", output_path, "snbt替换结束************")
                fout.write(snbtlib.dumps(quest))
            continue

        # chapter[title,subtitle]
        if quest.get('title'):
            title = quest['title']
            local_key = 'ftbquest.chapter.' + prefix + '.title'
            text = all2line(quest['title'])
            key_value[local_key] = text
            quest['title'] =  '{' + local_key + '}'
        if quest.get('subtitle'):
            subtitle = quest['subtitle']
            if len(subtitle) > 0:
                local_key = 'ftbquest.chapter.' + prefix + '.subtitle'
                text = all2line(quest['subtitle'])
                key_value[local_key] = text
                quest['subtitle'] = '{' + local_key + '}'

        # chapter.images[i][hover]
        if quest.get('images'):
            images = quest['images']
            for i in range(0, len(images)):
                if images[i].get('hover'):
                    hover = images[i]['hover']
                    if len(hover) > 0:
                        local_key = 'ftbquest.chapter.' + prefix + '.images.' + str(i) + '.hover'
                        text = all2line(hover)
                        key_value[local_key] = text
                        quest['images'][i]['hover'] = '{' + local_key + '}'

        # chapter.quests[i][title,subtitle,description]
        # chapter.quests[i].tasks[j].title
        # chapter.quests[i].rewards[j].title
        if quest.get('quests'):
            quests = quest['quests']
            for i in range(0, len(quests)):
                # title
                if quests[i].get('title'):
                    title = quests[i]['title']
                    if len(title) > 0:
                        local_key = 'ftbquest.chapter.' + prefix + '.quests.' + str(i) + '.title'
                        text = all2line(title)
                        key_value[local_key] = text
                        quest['quests'][i]['title'] = '{' + local_key + '}'
                # subtitle
                if quests[i].get('subtitle'):
                    subtitle = quests[i]['subtitle']
                    if len(subtitle) > 0:
                        local_key = 'ftbquest.chapter.' + prefix + '.quests.' + str(i) + '.subtitle'
                        text = all2line(subtitle)
                        key_value[local_key] = text
                        quest['quests'][i]['subtitle'] = '{' + local_key + '}'
                # description
                if quests[i].get('description'):
                    description = quests[i]['description']
                    if len(description) > 0:
                        local_key = 'ftbquest.chapter.' + prefix + '.quests.' + str(i) + '.description'
                        text = all2line(description)
                        key_value[local_key] = text
                        quest['quests'][i]['description'] = '{' + local_key + '}'
                        
                # tasks[j].title
                if quests[i].get('tasks'):
                    tasks = quests[i]['tasks']
                    if len(tasks) > 0:
                        for j in range(0, len(tasks)):
                            if tasks[j].get('title'):
                                title = tasks[j]['title']
                                local_key = 'ftbquest.chapter.' + prefix + '.quests.' + str(i) + '.tasks.' + str(j) + '.title'
                                text = all2line(title)
                                key_value[local_key] = text
                                quest['quests'][i]['tasks'][j]['title'] = '{' + local_key + '}'

                # rewards[j].title
                if quests[i].get('rewards'):
                    rewards = quests[i]['rewards']
                    if len(rewards) > 0:
                        for j in range(0, len(rewards)):
                            if rewards[j].get('title'):
                                title = rewards[j]['title']
                                local_key = 'ftbquest.chapter.' + prefix + '.quests.' + str(i) + '.rewards.' + str(j) + '.title'
                                text = all2line(title)
                                key_value[local_key] = text
                                quest['quests'][i]['rewards'][j]['title'] = '{' + local_key + '}'
        # 写入更新后的quest
        with open(output_path, 'w', encoding="utf-8") as fout:
            print("************", output_path, "snbt替换结束************")
            fout.write(snbtlib.dumps(quest))
    # 生成json
    with open('./zh_cn.json', 'w', encoding="utf-8") as fout:
        fout.write(json.dumps(key_value, indent=1, ensure_ascii=False))
        print("************json生成结束************")
        print("键值生成格式为【ftbquest.任务部分.任务原文件名称.区域.区域序号(从0开始).子区域.子区域序号(从0开始)】")
        print("关于如何使用此文件有两种形式:")
        print("1.制作成resourcepack下资源包，可以参考https://www.mcmod.cn/post/2194.html")
        print("2.制作成kubejs下资源包(依赖kubejs)，"
              "可以参考https://www.reddit.com/r/feedthebeast/comments/qllnpq/how_to_translate_quests_in_a_modpack_and_my/")

