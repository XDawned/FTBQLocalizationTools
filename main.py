from func.base import check_config_exists

VERSION = 'v1.4.8'

if __name__ == '__main__':
    try:
        check_config_exists()
        import func
        while True:
            print('**********FTBQ本地化小工具-%s**********' %VERSION)
            print('主功能引导\n'
                  '1.翻译任务\n  (1.20+自带lang文件，请修改config中LANG_PATH后选择功能3, lang文件见/ftbquests/quests/lang/en_us.snbt)\n'
                  '2.生成lang文件\n  (默认保存位置config中WORK_PATH)\n'
                  '3.翻译lang文件\n  (低版本json,高版本snbt)\n'
                  '4.回填lang文件\n  (不支持回填高版本snbt)\n'
                  '5.退出'
                  )
            choice = input('请输入你要选择的功能：')
            if choice == '1':
                func.quest_trans()
            elif choice == '2':
                func.trans2lang()
            elif choice == '3':
                func.lang_trans()
            elif choice == '4':
                func.back_fill()
            elif choice == '5':
                break
            else:
                print('无效输入')
    except Exception as e:
        print("程序发生了错误:", repr(e))
    finally:
        input("按任意键继续...")


