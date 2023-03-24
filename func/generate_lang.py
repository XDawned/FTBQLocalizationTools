import sys
from func.base import *
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


def get_value(prefix: str, text):
    """
    为key赋予value（多行与图片)
    :param text:文本
    :param prefix:键名前缀
    :return 键文dict和处理为键值后的原文
    """
    key_value = {}  # 用于存放新生成的键值及其对应的文本
    if isinstance(text, list):
        for i in range(0, len(text)):
            if bool(re.search(r'\S', text[i])):  # 非空行，为此行生成键值
                if text[i].find('{image:') == -1:  # 非图片
                    local_key = prefix + '.' + str(i)
                    key_value[local_key] = text[i]
                    text[i] = '{' + local_key + '}'
        return text, key_value
    else:
        if text.find('{image:') == -1:  # 非图片
            key_value[prefix] = text
            text = '{' + prefix + '}'
        return text, key_value


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
    get_config()
    QUESTS_PATH = global_var.get_value('QUESTS_PATH')
    quest_path = Path(QUESTS_PATH)  # 要翻译的目录
    key_value = {}  # 用于存放新生成的键值及其对应的文本

    for input_path in quest_path.rglob("*.snbt"):
        output_path = make_output_path(input_path)
        quest = get_quest(input_path)
        prefix = ''+list(input_path.parts)[-1].replace('.snbt', '')  # 以snbt文件名为key的前缀便于回溯
        # chapter_groups[title]
        if quest.get('chapter_groups'):
            chapter_groups = quest['chapter_groups']
            for i in range(0, len(chapter_groups)):
                local_key = 'ftbquests.chapter_groups.' + prefix + '.' + str(i) + '.title'
                text, new_key_value = get_value(local_key, chapter_groups[i]['title'])
                key_value.update(new_key_value)
                quest['chapter_groups'][i]['title'] = text
            # 写入更新后的quest
            with open(output_path, 'w', encoding="utf-8") as fout:
                print("************", output_path, "snbt替换结束************")
                fout.write(snbtlib.dumps(quest))
            continue

        # loot_table[title]
        if quest.get('loot_size'):  # 仅以键值判断是否是loot_table内容
            title = quest['title']
            local_key = 'ftbquests.loot_table.' + prefix + '.title'
            text, new_key_value = get_value(local_key, quest['title'])
            key_value.update(new_key_value)
            quest['title'] = text
            # 写入更新后的quest
            with open(output_path, 'w', encoding="utf-8") as fout:
                print("************", output_path, "snbt替换结束************")
                fout.write(snbtlib.dumps(quest))
            continue

        # chapter[title,subtitle]
        if quest.get('title'):
            title = quest['title']
            local_key = 'ftbquests.chapter.' + prefix + '.title'
            text, new_key_value = get_value(local_key, quest['title'])
            key_value.update(new_key_value)
            quest['title'] = text
        if quest.get('subtitle'):
            subtitle = quest['subtitle']
            if len(subtitle) > 0:
                local_key = 'ftbquests.chapter.' + prefix + '.subtitle'
                text, new_key_value = get_value(local_key, quest['subtitle'])
                key_value.update(new_key_value)
                quest['subtitle'] = text

        # chapter.images[i][hover]
        if quest.get('images'):
            images = quest['images']
            for i in range(0, len(images)):
                if images[i].get('hover'):
                    hover = images[i]['hover']
                    if len(hover) > 0:
                        local_key = 'ftbquests.chapter.' + prefix + '.images.' + str(i) + '.hover'
                        text, new_key_value = get_value(local_key, hover)
                        key_value.update(new_key_value)
                        quest['images'][i]['hover'] = text

        # chapter.quests[i][title,subtitle,description]
        # chapter.quests[i].tasks[j].[title,description]
        # chapter.quests[i].rewards[j].title
        if quest.get('quests'):
            quests = quest['quests']
            for i in range(0, len(quests)):
                # title
                if quests[i].get('title'):
                    title = quests[i]['title']
                    if len(title) > 0:
                        local_key = 'ftbquests.chapter.' + prefix + '.quests.' + str(i) + '.title'
                        text, new_key_value = get_value(local_key, title)
                        key_value.update(new_key_value)
                        quest['quests'][i]['title'] = text
                # subtitle
                if quests[i].get('subtitle'):
                    subtitle = quests[i]['subtitle']
                    if len(subtitle) > 0:
                        local_key = 'ftbquests.chapter.' + prefix + '.quests.' + str(i) + '.subtitle'
                        text, new_key_value = get_value(local_key, subtitle)
                        key_value.update(new_key_value)
                        quest['quests'][i]['subtitle'] = text
                # description
                if quests[i].get('description'):
                    description = quests[i]['description']
                    if len(description) > 0:
                        local_key = 'ftbquests.chapter.' + prefix + '.quests.' + str(i) + '.description'
                        text, new_key_value = get_value(local_key, description)
                        key_value.update(new_key_value)
                        quest['quests'][i]['description'] = text
                        
                # tasks[j].title
                if quests[i].get('tasks'):
                    tasks = quests[i]['tasks']
                    if len(tasks) > 0:
                        for j in range(0, len(tasks)):
                            if tasks[j].get('title'):
                                title = tasks[j]['title']
                                local_key = 'ftbquests.chapter.' + prefix + '.quests.' + str(i) + '.tasks.' + str(j) + '.title'
                                text, new_key_value = get_value(local_key, title)
                                key_value.update(new_key_value)
                                quest['quests'][i]['tasks'][j]['title'] = text

                # tasks[j].description
                if quests[i].get('tasks'):
                    tasks = quests[i]['tasks']
                    if len(tasks) > 0:
                        for j in range(0, len(tasks)):
                            if tasks[j].get('description'):
                                description = tasks[j]['description']
                                local_key = 'ftbquests.chapter.' + prefix + '.quests.' + str(i) + '.tasks.' + str(j) + '.description'
                                text, new_key_value = get_value(local_key, description)
                                key_value.update(new_key_value)
                                quest['quests'][i]['tasks'][j]['description'] = text

                # rewards[j].title
                if quests[i].get('rewards'):
                    rewards = quests[i]['rewards']
                    if len(rewards) > 0:
                        for j in range(0, len(rewards)):
                            if rewards[j].get('title'):
                                title = rewards[j]['title']
                                local_key = 'ftbquests.chapter.' + prefix + '.quests.' + str(i) + '.rewards.' + str(j) + '.title'
                                text, new_key_value = get_value(local_key, title)
                                key_value.update(new_key_value)
                                quest['quests'][i]['rewards'][j]['title'] = text
        # 写入更新后的quest
        with open(output_path, 'w', encoding="utf-8") as fout:
            print("************", output_path, "snbt替换结束************")
            fout.write(snbtlib.dumps(quest))
    # 生成json
    with open('./zh_cn.json', 'w', encoding="utf-8") as fout:
        fout.write(json.dumps(key_value, indent=1, ensure_ascii=False))
        print("************json生成结束************")
        print("键值生成格式为【ftbquests.任务部分.任务原文件名称.区域.区域序号(从0开始).n*子区域.子区域序号(从0开始).行号(单行则无)】")
        print("关于如何使用此文件有两种形式:")
        print("1.制作成resourcepack下资源包，可以参考https://www.mcmod.cn/post/2194.html")
        print("2.制作成kubejs下资源包(依赖kubejs)，"
              "可以参考https://www.reddit.com/r/feedthebeast/comments/qllnpq/how_to_translate_quests_in_a_modpack_and_my/")

