import json

import func


if __name__ == '__main__':
    while True:
        print('********************')
        print('主功能引导\n1.翻译任务snbt\n2.生成lang文件(默认位置config中WORK_PATH)\n3.翻译lang文件\n4.生成配置文件\n5.退出')
        choice = input('请输入你要选择的功能：')
        if choice == '1':
            print('开始翻译，请确保你已提前完成配置！')
            while True:
                print('********************')
                print('选择翻译解析器\n1.snbtlib(推荐)\n2.正则表达式(稳定，但易漏翻)\n3.退出')
                choice = input('请输入你要选择的解析器：')
                if choice == '1':
                    func.snbtlib_trans()
                elif choice == '2':
                    func.regular_trans()
                elif choice == '3':
                    break
                else:
                    print('无效输入')
        elif choice == '2':
            func.trans2lang()
        elif choice == '3':
            func.lang_trans()
        elif choice == '4':
            with open('config.json', 'w', encoding="utf-8") as fout:
                QUESTS_PATH = input('翻译目录(比如相对路径./ftbquests或绝对路径*/ftbquests)')
                LANG_PATH = input('要翻译的lang中json文件相对目录，默认为程序运行目录下的en_us.json')
                DEVICE = input('可选值CPU,GPU')
                fout.write(json.dumps(
                    {'QUESTS_PATH': QUESTS_PATH, 'LANG_PATH': LANG_PATH,
                     'DEVICE': DEVICE}, indent=1, ensure_ascii=False))
            print('配置修改完成！')
        elif choice == '5':
            break
        else:
            print('无效输入')
