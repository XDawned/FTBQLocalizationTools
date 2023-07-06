<div align="center">
  <img width="115" height="115" src="https://i.postimg.cc/QtrcwLL7/icon.png">
</div>
<div align="center">
    <a href="https://github.com/XDawned/ModpackLocalizationTools/blob/main/LICENSE">
        <img src="https://img.shields.io/badge/license-GPL%203.0-yellow.svg" alt="license">
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

### 用途:
1. 处理FTBQuest、BetterQuesting任务文件
2. 处理lang文件
3. 为未做本地化的任务文本进行本地化转化
4. 为任务生成高质量机翻
#### 优势
##### 术语优化
和~~产卵者 暴徒~~说再见

离线翻译模型版本所使用的模型已针对MC术语做了大量微调优化，大部分的热门术语都可以正确翻译
##### 富文本机翻优化
在实际应用时不是简单的将任务文本送给翻译接口就好，游戏中的任务往往为为富文本，可能会出现诸如

- `动态物品ID：#minecraft:apple`
- `网址：www.minecraft.net`
- `彩色标记：Find an &aAPPLE`
- `点击事件：[\"\",{\"text\":\"Click here\",\"color\":\"light_purple\",\"clickEvent\":{\"action\":\"change_page\",\"value\":\"4FA6ADCA7857A92F\"},\"hoverEvent\":{\"action\":\"show_text\",\"contents\":[\"Botania chapter\"]}},\" to see the Botania quest chapter for help in making Mana Steel.\"]`
- ...
  
我们需要保留富文本特殊格式的同时保证翻译需翻部分

针对已知的将近十种富文本格式都做了考量，翻译时会在后台自动对相应文本做出处理

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
<img width=700 height=400 src="https://img2023.cnblogs.com/blog/2192803/202301/2192803-20230107125912964-39430206.png"/>

### 项目推荐
[整合包本地化工具](https://github.com/XDawned/ModpackLocalizationTools)

搭载FluentDesign风格UI界面，提供整合包汉化一条龙服务

为`mod、ftbq、bq、kubejs、contenttweaker、fancymenu`等整合包汉化相关提供自动化方案与简单cat辅助翻译平台
### 可能遇到的问题
1. 闪退，大概率为配置文件不正确或异常操作
2. API调用出错，网络环境不佳或者达到了速率限制
3. 没有离线翻译， 你需要下载搭载了机器翻译的full版本
### 未来的计划
1. 优化模型翻译效果，以及运行速度
2. 添加对更多富文本格式的支持



### Tips
1. 如果你不想使用付费的翻译API可以选择此项目分支[model_trans](https://github.com/XDawned/FTBQLocalizationTools/tree/model_trans)或releases中的full版本，在本地运行翻译模型！

2. 为了获取更好的翻译效果，如果使用百度翻译api建议先在百度翻译api中扩充自己的术语库，原版术语可以参考[CFPA术语库](https://github.com/CFPAOrg/Glossary)

3. 本项目由[snbtlib](https://github.com/Tryanks/python-snbtlib)提供snbt文本解析，如果提示缺少此库你可以尝试`pip install snbtlib`

4. 此项目代码结构简单明了且注释完整，欢迎各位一起参与到开发中来。如果你有更好的思路或者发现了某些bug，欢迎在此发起issue或pr！

