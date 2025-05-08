from func.base import *
from tqdm import tqdm

def get_lang(input_path: Path):
    with open(input_path, 'r', encoding="utf-8") as fin:
        quest = fin.read()
        try:
            if input_path.parts[-1].endswith('.snbt'):
                quest = snbtlib.loads(quest)  # 转化为json格式并读取
            else:
                quest = json.loads(quest)  # 转化为json格式并读取
            return quest
        except TypeError:
            print(TextStyle.RED, 'lang文件读取出错，可能是所读取的文件格式错误或其它问题！', TextStyle.RESET)


def update_lang_file(input_path: Path, output_path: Path):
    print('读取成功，正在翻译lang文件:', TextStyle.LIGHT_YELLOW, input_path, TextStyle.RESET)
    lang = get_lang(input_path)
    lang = update_lang(lang)  # 翻译相应内容
    with open(output_path, 'w', encoding="utf-8") as fout:
        print(TextStyle.GREEN, '翻译完成\n')
        if input_path.parts[-1].endswith('.snbt'):
            processed_text = snbtlib.dumps(lang)
        else:
            processed_text = json.dumps(lang, indent=1, ensure_ascii=False)
        fout.write(processed_text)


def update_lang(lang: dict) -> dict:
    KEEP_ORIGINAL = global_var.get_value('KEEP_ORIGINAL')
    for key in tqdm(lang):
        try:
            if isinstance(lang[key], list):
                translated_lines = []
                for index, line in enumerate(lang[key]):
                    pre_processed_line = pre_process(line)
                    if pre_processed_line:
                        translate = translate_line(pre_processed_line)
                        post_translate = post_process(line, translate)
                        translated_lines.append(post_translate)
                        print(f"\r文本翻译完成：\n原文：" + TextStyle.YELLOW + line + TextStyle.RESET)
                        print("\r译文：" + TextStyle.GREEN + post_translate + TextStyle.RESET)
                        if KEEP_ORIGINAL:
                            lang[key][index] = f"{post_translate}[--{line}--]"
                        else:
                            lang[key][index] = post_translate
            else:
                line = lang[key]
                pre_processed_line = pre_process(line)
                translate = translate_line(pre_processed_line) if pre_processed_line else line
                post_translate = post_process(line, translate)
                print(f"\r文本翻译完成：\n原文：" + TextStyle.YELLOW + line + TextStyle.RESET)
                print("\r译文：" + TextStyle.GREEN + post_translate + TextStyle.RESET)
                if KEEP_ORIGINAL:
                    lang[key] = f"{post_translate}[--{line}--]"
                else:
                    lang[key] = post_translate
        except Exception as e:
            print(TextStyle.RED + f'key：{key}项遇到错误{e}，请手动处理' + TextStyle.RESET)
            continue
    return lang


def make_output_path(path: Path) -> Path:
    parts = list(path.parts)
    parts[-1] = 'zh_cn'+ '.' + parts[-1].split('.')[-1]
    output_path = Path(*parts)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    return output_path


def lang_trans():
    get_config()
    LANG_PATH = global_var.get_value('LANG_PATH')
    input_path = Path(LANG_PATH)  # 要翻译的目录
    output_path = make_output_path(input_path)  # 生成输出目录路径
    update_lang_file(input_path, output_path)  # 更新任务文件
    print(TextStyle.CYAN, "你可以在en_us同级目录下的trans文件夹中找到翻译后的zh_cn lang文件.", TextStyle.RESET)
    print("************lang文件翻译完成************")
