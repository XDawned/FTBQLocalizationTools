from hashlib import md5
from pathlib import Path
import random
import requests
from config import *
import re

MAGIC_WORD = r'{xdawned}'


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
        print("api调用出错")
        return line
        # return translate_line(line)


# magic方法，这样似乎就可以让baidu不翻译颜色代码
def bracket(m: re.Match):
    return "[&" + m.group(0) + "]"


def debracket(m: re.Match):
    return m.group(0)[2:-1]


def pre_process(line: str):
    # 情景1：图片介绍
    if line.find('.jpg') + line.find('.png') != -2:
        return None  # 新版ftbquest可以展示图片，遇到图片则略过
    # 情景2：\\&表and
    line = line.replace('\\\\&', 'PPP')
    # 情景3：彩色区域
    # 彩色格式保留，让百度api忽略&
    # 目前已知的彩色格式只有a~f,0~9全部依次录入即可）百度api大多可以返回包含&.的汉化结果。
    pattern = re.compile(r'&([a-z,0-9]|#[0-9,A-F]{6})')
    line = pattern.sub(bracket, line)
    # 情景4：物品引用
    # 比如#minecraft:coals需要保留,打破此格式将会导致此章任务无法读取！！！
    # 这里给出的方案是先将引用替换为临时词MAGIC_WORD，术语库中设置MAGIC_WORD-MAGIC_WORD来保留此关键词，然后借此在翻译后的句子中定位MAGIC_WORD用先前引用词换回
    line = re.sub(r'#\w+:\w+\b', MAGIC_WORD, re.sub(r'\\"', '\"', line))  # 辅助忽略转义符

    return line


def post_process(line, translate):
    # 将方括号替换回来
    pattern = re.compile(r'\[&&([a-z,0-9]|#[0-9,A-F]{6})\]')
    translate = pattern.sub(debracket, translate)
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

