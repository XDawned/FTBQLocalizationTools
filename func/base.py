import os
from hashlib import md5
from pathlib import Path
import random
import requests
from transformers import pipeline
import global_var
import re
import json
import snbtlib

MAGIC_WORD = r'{xdawned}'

pipe = None


class TextStyle:
    # 定义常量，表示不同颜色和特殊样式
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    # 前景色
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    LIGHT_YELLOW = '\033[93m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    # 背景色
    BLACK_BG = '\033[40m'
    RED_BG = '\033[41m'
    GREEN_BG = '\033[42m'
    YELLOW_BG = '\033[43m'
    BLUE_BG = '\033[44m'
    MAGENTA_BG = '\033[45m'
    CYAN_BG = '\033[46m'
    WHITE_BG = '\033[47m'


def check_config_exists():
    filename = 'config.json'
    # 检查文件是否存在
    if not os.path.exists(filename):
        # 创建一个空的配置字典
        config = {
            "APPID": "20**********4",
            "APPKEY": "u**********R",
            "QUESTS_PATH": "./ftbquests",
            "LANG_PATH": "./en_us.json",
            "KEEP_ORIGINAL": True,
            "BACK_FILL_PATH": "./ftbquests-trans",
            "BACK_FILL_LANG_PATH": "./zh_cn.json",
            "API": "LOCAL"
        }
        try:
            # 打开文件并写入配置内容
            with open(filename, 'w') as file:
                json.dump(config, file, indent=1, ensure_ascii=False)
            print(f"配置文件已初始化于：{filename}")
        except Exception as e:
            print(f"未检测到配置文件,在尝试创建时出错,你可以手动创建：{e}")
    else:
        print(f"读取到配置文件：{filename}")


def get_config():
    with open('config.json', 'r', encoding="utf-8") as fin:
        config_data = json.loads(fin.read())
        global_var.set_value('APPID', config_data['APPID'])
        global_var.set_value('APPKEY', config_data['APPKEY'])
        global_var.set_value('QUESTS_PATH', config_data['QUESTS_PATH'])
        global_var.set_value('LANG_PATH', config_data['LANG_PATH'])
        global_var.set_value('KEEP_ORIGINAL', config_data['KEEP_ORIGINAL'])
        global_var.set_value('BACK_FILL_PATH', config_data['BACK_FILL_PATH'])
        global_var.set_value('BACK_FILL_LANG_PATH', config_data['BACK_FILL_LANG_PATH'])
        global_var.set_value('API', config_data['API'])


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


def check_low(text):
    match = re.search(r'\",$', text, re.MULTILINE)
    if match:
        print(TextStyle.BLUE, '检测到1.12.2老版本任务文件!!!', TextStyle.RESET)
    return match


def get_snbt_quest(input_path: Path):
    with open(input_path, 'r', encoding="utf-8") as fin:
        quest = fin.read()
        low = check_low(quest)
        try:
            quest = snbtlib.loads(quest)  # 转化为json格式并读取
            return quest, low
        except TypeError:
            print(TextStyle.RED, 'snbtlib调用出错，可能是python环境版本过低或其它问题！', TextStyle.RESET)


def translate_line(line: str) -> str:
    """
    翻译送来的字符串
    :param line:字符串
    :return:翻译结果字符串
    """
    APPID = global_var.get_value('APPID')
    APPKEY = global_var.get_value('APPKEY')
    API = global_var.get_value('API')
    if API == 'Baidu':
        try:
            # 关于语言选项参考文档 `https://api.fanyi.baidu.com/doc/21`
            # 百度appid/appkey.（PS：密钥随IP绑定，设置密钥时候注意设置正确的IP否则无法使用！！！）
            appid = APPID  # 请注册你自己的密钥
            appkey = APPKEY  # 请注册你自己的密钥
            from_lang = 'en'
            to_lang = 'zh'
            endpoint = 'http://api.fanyi.baidu.com'
            path = '/api/trans/vip/translate'
            url = endpoint + path

            def make_md5(s, encoding='utf-8'):
                return md5(s.encode(encoding)).hexdigest()

            salt = random.randint(32768, 65536)
            sign = make_md5(appid + line + str(salt) + appkey)

            # Build request
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            payload = {'appid': appid, 'q': line, 'from': from_lang, 'to': to_lang, 'salt': salt,
                       'sign': sign, 'action': 1}

            # Send request
            r = requests.post(url, params=payload, headers=headers)
            result = r.json()
            return result.get('trans_result')[0].get('dst')
        except TypeError:
            '''
            TypeError: 'NoneType' object is not subscriptable
            八成是appid和appkey不正确或申请的服务中绑定的IP设置错误，小概率网络波动原因
            '''
            print(TextStyle.RED, "api调用出错", TextStyle.RESET)
            return line
    else:
        try:
            output = pipe(line)[0]['translation_text']
            return output
        except:
            print(TextStyle.RED, "翻译模型调用出错！", TextStyle.RESET)
            return line


# magic方法，这样似乎就可以让baidu不翻译颜色代码
def bracket(m: re.Match):
    return "[&" + m.group(0) + "]"


def debracket(m: re.Match):
    return m.group(0)[2:-1]


def back_fill_magic_word(line, translate, pattern, type_info=''):
    quotes = re.findall(pattern, line)  # 找出所有引用词
    if len(quotes) > 0:
        print(TextStyle.YELLOW, f"在此行找到{type_info}", quotes, TextStyle.RESET)
        count = 0
        # 找出MAGIC_WORD出现的所有位置并替换为对应引用词
        index = translate.find(MAGIC_WORD)
        while index != -1:
            translate = re.sub(MAGIC_WORD, quotes[count], translate, 1)
            count = count + 1
            index = translate.find(MAGIC_WORD)
    return translate


def add_escape_quotes(text):
    pattern = r'(?<!\\)"'
    repl = r'\\"'
    result = re.sub(pattern, repl, text)
    return result


def pre_process(line: str):
    API = global_var.get_value('API')
    # 情景1：图片介绍
    if line.find('.jpg') + line.find('.png') != -2:
        print(TextStyle.YELLOW, '检测到图片', line, '已保留', TextStyle.RESET)
        return None  # 新版ftbquest可以展示图片，遇到图片则略过
    # 情景2：特殊事件，彩色或点击action等
    if line.find(r'{\"') != -1:
        print(TextStyle.YELLOW, '检测到特殊事件', line, '已保留', TextStyle.RESET)
        return None
    # 情景3：\\&表and
    line = line.replace('\\\\&', 'PPP')
    # 情景4：彩色区域
    # 彩色格式保留，让百度api忽略&
    # 目前已知的彩色格式只有a~f,0~9全部依次录入即可）百度api大多可以返回包含&.的汉化结果。
    pattern = re.compile(r'&([a-z,0-9]|#[0-9,A-F]{6})')
    # 将方括号替换回来
    if API == 'Baidu':
        line = pattern.sub(bracket, line)
    # 情景5：物品引用
    # 比如#minecraft:coals需要保留,打破此格式将会导致此章任务无法读取！！！
    # 这里给出的方案是先将引用替换为临时词MAGIC_WORD，术语库中设置MAGIC_WORD-MAGIC_WORD来保留此关键词，然后借此在翻译后的句子中定位MAGIC_WORD用先前引用词换回
    line = re.sub(r'#\w+:\w+\b', MAGIC_WORD, re.sub(r'\\"', '\"', line))  # 辅助忽略转义符
    # 情景6：超链接
    pattern = re.compile(r'(http|https)://(?:[-\w.]|(?:%[\da-fA-F]{2}))+')
    if re.search(pattern, line):
        print(TextStyle.YELLOW, '检测到超链接', line, '已保留', TextStyle.RESET)
        return None  # 某行包含超链接，保险策略，直接略过此行
    # 情景7：翻页{@pagebreak}
    if re.search(r'\{@\w+}', line):
        print(TextStyle.YELLOW, '检测到点击事件', line, '已保留', TextStyle.RESET)
        return None  # 某行包含点击事件，保险策略，直接略过此行
    return line


def post_process(line, translate):
    API = global_var.get_value('API')
    # 将方括号替换回来
    pattern = re.compile(r'\[&&([a-z,0-9]|#[0-9,A-F]{6})]')
    if API == 'Baidu':
        translate = pattern.sub(debracket, translate)
        line = pattern.sub(debracket, line)
    # 将物品引用换回
    translate = back_fill_magic_word(line=line, translate=translate, pattern=re.compile(r'#\w+:\w+\b'),
                                     type_info='物品引用')
    # translate = back_fill_magic_word(line=line, translate=translate, pattern=re.compile(r'\{@\w+}'), type_info='翻页')
    # 修补缺失转义符
    translate = add_escape_quotes(translate)
    return translate
