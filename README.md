# FTBQLocalizationTools(FTB任务本地化工具)
### 介绍:

一个辅助翻译ftbquests任务的python脚本

你可以用它:
1. 使用百度API或我托管于hugging-face平台的自训练模型机翻ftbquests任务 
2. 生成lang文件，辅助任务汉化工作（如果你想获取机翻后的lang，你可以先机翻再使用机翻后任务生成lang文件）
### 使用:

 1. 打开config.json，配置各项参数
    - `[APPID]`  百度api-appid(模型不选用百度api可随意修改)
    - `[APPKEY]` 百度api-appkey(模型不选用百度api可随意修改)
    - `[HUGGING_FACE_TOKEN]` (模型不选用Hugging-Face api可随意修改) [获取token](https://huggingface.co/settings/tokens)
    - `QUESTS_PATH` 要翻译或生成lang的文件目录，此目录下所有snbt文件都会被翻译#
    【可选./ftbquests或./chapter，./chapter只翻译章节内容，./ftbquests额外包括战利品表名称、大章节标题等内容】
    - `LANG_PATH` 要翻译的lang中json文件相对目录，默认为程序运行目录下的en_us.json
    - `MODEL` 可选值baidu、transformer分别对应百度翻译API(额度内免费)和托管于hugging-face平台的自训练模型(免费但速率有限制，你在此项目分支model_trans中找到支持本地CPU或GPU运行翻译模型的版本[model_trans](https://github.com/XDawned/FTBQLocalizationTools/tree/model_trans))
 2. 将任务文件或语言文件放到指定位置(比如默认配置`QUESTS_PATH`为`./ftbquests`，即将从.minecraft/config下获取的ftbquests目录复制到程序同级目录下)
 3. 运行程序，选择相应功能
### 效果：
![image](https://img2023.cnblogs.com/blog/2192803/202301/2192803-20230107125912964-39430206.png)

### 可能遇到的问题
 1. 闪退，大概率为配置文件不正确或异常操作
 2. hugging-face API调用出错，网络环境不佳或者达到了速率限制

### 未来的计划
1.翻译接口对接chatgpt（它在翻译效果上可以说很出色，大多数mc专业术语都可以识别保留）

2.模型优化

### Tips
1. 如果你不想使用联网API可以选择branch中的model_trans分支，使用本地机翻模型版本

2. 为了获取更好的翻译效果，如果使用百度翻译api建议先在百度翻译api中扩充自己的术语库，原版术语可以参考[CFPA术语库](https://github.com/CFPAOrg/Glossary)

3. 脚本使用了[snbtlib](https://github.com/Tryanks/python-snbtlib)，如果提示缺少此库你可以尝试`pip install snbtlib`

4. 如果你有更好的思路或者发现了某些bug，欢迎在此pr！

