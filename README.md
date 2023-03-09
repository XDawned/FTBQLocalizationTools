# ftbquestsAutoTrans
### 介绍:

一个辅助翻译ftbquests任务的python脚本

你可以用它:
1. 使用百度API翻译ftbquests任务 
2. 生成lang文件，辅助任务汉化工作（如果你想获取机翻后的lang，你可以先机翻再使用机翻后任务生成lang文件）
### 使用:

 1. 复制粘贴`config_example.py`并将新文件重命名为`config.py`，配置`APPID`、`APPKEY`、以及`WORK_PATH`
 2. 将`ftbquest文件夹`放到程序同级目录下运行程序

### 效果：
![image](https://img2023.cnblogs.com/blog/2192803/202301/2192803-20230107125912964-39430206.png)

### Tips
1. 为了获取更好的翻译效果，建议先在百度翻译api中扩充自己的术语库，原版术语可以参考[CFPA术语库](https://github.com/CFPAOrg/Glossary)

2. 如果你有更好的思路或者发现了某些bug，欢迎在此pr！
