APPID = '2***************3'  # 百度api-appid(模型不选用百度api可随意修改)
APPKEY = 'L***************X'  # 百度api-appkey(模型不选用百度api可随意修改)

HUGGING_FACE_TOKEN = 'h**********************j'  # huggingface平台注册账号后免费获取(https://huggingface.co/settings/tokens)

QUESTS_PATH = './ftbquests'  # 要翻译或生成lang的文件目录，此目录下所有snbt文件都会被翻译
# 【可选./ftbquests或./chapter，./chapter只翻译章节内容，./ftbquests额外包括战利品表名称、大章节标题等内容】

LANG_PATH = './en_us.json'  # 要翻译的lang中json文件相对目录，默认为程序运行目录下的en_us.json

MODEL = 'baidu'  # 可选值baidu、transformer分别对应百度翻译API(额度内免费)和托管于hugging-face平台的自训练模型(免费但不稳定)
# 自训练模型介绍https://github.com/XDawned/minecraft-modpack-quests-transformer
