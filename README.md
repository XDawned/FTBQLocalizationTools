<div align="center">
  <img width="115" height="115" src="https://i.postimg.cc/QtrcwLL7/icon.png">
</div>
<div align="center">
    <a href="https://github.com/XDawned/FTBQLocalizationTools/blob/main/LICENSE">
        <img src="https://img.shields.io/github/license/mashape/apistatus.svg" alt="license">
    </a>
    <a href="https://github.com/Tryanks/python-snbtlib">
        <img src="https://img.shields.io/badge/lib-snbtlib-brightgreen" alt="lib">
    </a>
    <a href="https://github.com/XDawned/FTBQLocalizationTools/releases/tag/v1.0">
        <img src="https://img.shields.io/badge/releases-1.0-blue" alt="releases">
    </a>

# FTB任务本地化工具
</div>

### 介绍:

一个辅助翻译ftbquests任务的python脚本

你可以用它:
1. 机翻ftbquests任务（机翻同时保留原文）
2. 为ftbquests生成lang文件，辅助任务汉化工作
### 使用:

1. 打开config.json，配置各项参数
    - `[APPID]`  百度api-appid(模型不选用百度api可随意修改)
    - `[APPKEY]` 百度api-appkey(模型不选用百度api可随意修改)
    - `QUESTS_PATH` 要翻译或生成lang的文件目录，此目录下所有snbt文件都会被翻译#
      【可选./ftbquests或./chapter，./chapter只翻译章节内容，./ftbquests额外包括战利品表名称、大章节标题等内容】
    - `LANG_PATH` 要翻译的lang中json文件相对目录，默认为程序运行目录下的en_us.json
    - `KEEP_ORIGINAL` 是否保留原文，可选`true、false`，默认为`true`(无需引号）
    - 如果你有一定的代码基础建议采用此项目分支model_trans，其支持本地CPU或GPU运行翻译模型 [model_trans](https://github.com/XDawned/FTBQLocalizationTools/tree/model_trans))
2. 将任务文件或语言文件放到指定位置(比如默认配置`QUESTS_PATH`为`./ftbquests`，即将从.minecraft/config下获取的ftbquests目录复制到程序同级目录下)
3. 运行程序，选择相应功能
### 效果：
![image](https://img2023.cnblogs.com/blog/2192803/202301/2192803-20230107125912964-39430206.png)

### 可能遇到的问题
1. 闪退，大概率为配置文件不正确或异常操作
2. API调用出错，网络环境不佳或者达到了速率限制

### 未来的计划
1.完善机器学习分支，并入主线，摆脱外部付费API限制

2.制作UI

### Tips
1. 如果你不想使用付费的翻译API可以选择branch中的model_trans分支，使用本地机翻模型版本！

2. 为了获取更好的翻译效果，如果使用百度翻译api建议先在百度翻译api中扩充自己的术语库，原版术语可以参考[CFPA术语库](https://github.com/CFPAOrg/Glossary)

3. 脚本使用了[snbtlib](https://github.com/Tryanks/python-snbtlib)，如果提示缺少此库你可以尝试`pip install snbtlib`

4. 这个脚本的实现并不复杂甚至可以说粗略，如果你有更好的思路或者发现了某些bug，欢迎在此发起issue或pr！

