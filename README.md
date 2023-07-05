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
        <img src="https://img.shields.io/badge/releases-1.3-blue" alt="releases">
    </a>

# FTB任务本地化工具
</div>

### 介绍:

一个辅助翻译ftbquests任务的python脚本

你可以用它:
1. 生成机翻(借助本地机翻模型或者百度翻译API)
2. 生成lang文件
3. lang文件回填
### 使用:

1. 打开config.json，配置各项参数
    - `[APPID]`  百度api-appid
    - `[APPKEY]` 百度api-appkey
    - `QUESTS_PATH` 要翻译或生成lang的文件目录，此目录下所有snbt文件都会被翻译#
    - `LANG_PATH` 要翻译的lang文件相对路径，默认为`./en_us.json`
    - `KEEP_ORIGINAL` 是否保留原文，可选`true、false`，默认为`true`(无需引号）
    - `BACK_FILL_PATH` 回填源文件所在地即已经使用键值的任务所在文件夹，默认为`./ftbquests-trans`
    - `BACK_FILL_LANG_PATH` 回填的lang文件所在地，默认为`./zh_cn.json`
2. 将任务文件或语言文件放到指定位置(比如默认配置`QUESTS_PATH`为`./ftbquests`，即将从.minecraft/config下获取的ftbquests目录复制到程序同级目录下)
3. 运行程序，选择相应功能
### 效果：
![image](https://img2023.cnblogs.com/blog/2192803/202301/2192803-20230107125912964-39430206.png)

### 可能遇到的问题
1. 闪退，大概率为配置文件不正确或异常操作
2. API调用出错，网络环境不佳或者达到了速率限制

### 未来的计划
1.完善机器学习分支，并入主线，彻底摆脱外部付费API限制

2.制作UI，脱离游戏进行FTBQ任务简单编辑

### Tips
1. 如果你不想使用付费的翻译API可以选择此项目分支[model_trans](https://github.com/XDawned/FTBQLocalizationTools/tree/model_trans)或releases中的full版本，在本地运行翻译模型！

2. 为了获取更好的翻译效果，如果使用百度翻译api建议先在百度翻译api中扩充自己的术语库，原版术语可以参考[CFPA术语库](https://github.com/CFPAOrg/Glossary)

3. 本项目由[snbtlib](https://github.com/Tryanks/python-snbtlib)提供snbt文本解析，如果提示缺少此库你可以尝试`pip install snbtlib`

4. 这个脚本的实现并不复杂并且代码注释完整，如果你有更好的思路或者发现了某些bug，欢迎在此发起issue或pr！

