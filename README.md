# FTBQLocalizationTools(FTB任务本地化工具)
### 介绍:

一个辅助翻译ftbquests任务的python脚本

你可以用它:
1. 使用百度API机翻ftbquests任务 
2. 生成lang文件，辅助任务汉化工作（如果你想获取机翻后的lang，你可以先机翻再使用机翻后任务生成lang文件）
### 使用:

 1. 复制粘贴`config_example.py`并将新文件重命名为`config.py`，配置`APPID`、`APPKEY`、以及`WORK_PATH`
 2. 将`ftbquest文件夹`放到程序同级目录下运行程序

### 效果：
![image](https://img2023.cnblogs.com/blog/2192803/202301/2192803-20230107125912964-39430206.png)

### 未来的计划
1.翻译接口对接chatgpt（它在翻译效果上可以说很出色，大多数mc专业术语都可以识别保留）

2.未来可能会找个预训练模型，尝试自己针对mc进行调教。

### Tips
1. 为了获取更好的翻译效果，建议先在百度翻译api中扩充自己的术语库，原版术语可以参考[CFPA术语库](https://github.com/CFPAOrg/Glossary)

2. 脚本使用了[snbtlib](https://github.com/Tryanks/python-snbtlib)，如果提示缺少此库你可以尝试`pip install snbtlib`

3. 如果你有更好的思路或者发现了某些bug，欢迎在此pr！

