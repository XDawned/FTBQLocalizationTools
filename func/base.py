import sys
from pathlib import Path
import re
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import json
import global_var


MAGIC_WORD = r'{xdawned}'


def get_config():
    with open('config.json', 'r', encoding="utf-8") as fin:
        config_data = json.loads(fin.read())
        global_var.set_value('QUESTS_PATH', config_data['QUESTS_PATH'])
        global_var.set_value('LANG_PATH', config_data['LANG_PATH'])
        global_var.set_value('DEVICE', config_data['DEVICE'])


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


def translate_line(line: str) -> str:
    """
    翻译送来的字符串
    :param line:字符串
    :return:翻译结果字符串
    """
    try:
        get_config()
        DEVICE = global_var.get_value('DEVICE')
        tokenizer = AutoTokenizer.from_pretrained("XDawned/minecraft-modpack-quests-transformer")

        if DEVICE == 'GPU':
            model = AutoModelForSeq2SeqLM.from_pretrained("XDawned/minecraft-modpack-quests-transformer").to('cuda')
            input_ids = tokenizer.encode(line, return_tensors="pt").to('cuda')
        elif DEVICE == 'CPU':
            model = AutoModelForSeq2SeqLM.from_pretrained("XDawned/minecraft-modpack-quests-transformer")
            input_ids = tokenizer.encode(line, return_tensors="pt")
        else:
            print('模型配置选择有误！')
            sys.exit(0)
        translated = model.generate(input_ids, max_length=128)
        output = tokenizer.decode(translated[0], skip_special_tokens=True)
        return output
    except TypeError:
        '''
        此模型基于CPU运行
        起步阶段，翻译效果可能不佳
        '''
        print("transformer模型调用出错")
        return line


def pre_process(line: str):
    # 情景1：图片介绍
    if line.find('.jpg') + line.find('.png') != -2:
        print('检测到图片', line, '已保留')
        return None  # 新版ftbquest可以展示图片，遇到图片则略过
    # 情景2：\\&表and
    line = line.replace('\\\\&', 'PPP')
    # 情景3：彩色区域
    # 彩色格式保留，让百度api忽略&
    # 目前已知的彩色格式只有a~f,0~9全部依次录入即可）百度api大多可以返回包含&.的汉化结果。

    # 本地模型本体分词器已包含

    # 情景4：物品引用
    # 比如#minecraft:coals需要保留,打破此格式将会导致此章任务无法读取！！！
    # 这里给出的方案是先将引用替换为临时词MAGIC_WORD，术语库中设置MAGIC_WORD-MAGIC_WORD来保留此关键词，然后借此在翻译后的句子中定位MAGIC_WORD用先前引用词换回
    line = re.sub(r'#\w+:\w+\b', MAGIC_WORD, re.sub(r'\\"', '\"', line))  # 辅助忽略转义符
    # 情景5：超链接
    pattern = re.compile(r'(http|https)://(?:[-\w.]|(?:%[\da-fA-F]{2}))+')
    if re.search(pattern, line):
        print('检测到超链接', line, '已保留')
        return None  # 某行包含超链接，保险策略，直接略过此行

    return line


def post_process(line, translate):
    # 将物品引用换回
    quotes = re.findall(r'#\w+:\w+\b', line)  # 找出所有引用词

    if len(quotes) > 0:
        print('在此行找到引用', quotes)
        count = 0
        # 找出MAGIC_WORD出现的所有位置并替换为对应引用词
        index = translate.find(MAGIC_WORD)
        while index != -1:
            translate = re.sub(MAGIC_WORD, quotes[count], translate, 1)
            count = count + 1
            index = translate.find(MAGIC_WORD)
        print(translate)
    replacement = translate + "[--" + line + "--]"  # 原文保留
    return replacement
