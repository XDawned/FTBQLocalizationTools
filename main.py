from func.base import check_config_exists

VERSION = 'v1.4.8'

if __name__ == '__main__':
    try:
        check_config_exists()
        import func
        while True:
            print('**********FTBQ本地化小工具-%s**********' %VERSION)
            print('主功能引导\n1.翻译任务snbt\n2.生成lang文件(默认位置config中WORK_PATH)\n3.翻译lang文件\n4.回填lang文件\n5.退出')
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


