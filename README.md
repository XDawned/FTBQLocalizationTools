# FTBQLocalizationTools(FTB任务本地化工具)
### 这里是本地化机器翻译模型分支，[模型介绍](https://github.com/XDawned/minecraft-modpack-quests-transformer)
### 介绍:

一个辅助翻译ftbquests任务的python脚本

你可以用它:
1. 使用百度API或我托管于hugging-face平台的自训练模型机翻ftbquests任务 
2. 生成lang文件，辅助任务汉化工作（如果你想获取机翻后的lang，你可以先机翻再使用机翻后任务生成lang文件）
### 使用:

 1. 打开config.json，配置各项参数
    - `QUESTS_PATH` 要翻译或生成lang的文件目录，此目录下所有snbt文件都会被翻译#
    可选`./ftbquests`或`./chapter`，`./chapter`只翻译章节内容，`./ftbquests`额外包括战利品表名称、大章节标题等内容
    - `LANG_PATH` 要翻译的lang中json文件相对目录，默认为程序运行目录下的`en_us.json`
    - `DEVICE` 运行模型所使用的硬件，可选值`CPU`、`GPU`（GPU运行对环境要求更高，需要进行额外的配置）
 2. 下载并打开项目，安装依赖环境(如编辑器无法自动安装请手动`pip install`，建议采用conda环境)
 3. 将任务文件或语言文件放到指定位置(比如默认配置`QUESTS_PATH`为`./ftbquests`，即将从.minecraft/config下获取的ftbquests目录复制到程序同级目录下)
### 效果：
![image](https://img2023.cnblogs.com/blog/2192803/202301/2192803-20230107125912964-39430206.png)

### 可能遇到的问题
 1. 闪退，大概率为配置文件不正确或异常操作

### Tips
1. 模型仍处于开发阶段，效果有限，后续仍会更新，其目标是在基础翻译基础上润色对mc专有名词的翻译
2. 运行时请注意本地硬件散热，CPU高占用属正常情况
3. 脚本使用了[snbtlib](https://github.com/Tryanks/python-snbtlib)，如果提示缺少此库你可以尝试`pip install snbtlib`
4. 如果你有更好的思路或者发现了某些bug，欢迎在此pr！

