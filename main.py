import requests
from func.base import TextStyle, check_config_exists

VERSION = 'v1.4.6'

if __name__ == '__main__':
    try:
        check_config_exists()
        import func
        # url = 'https://mockapi.eolink.com/arvjB2Yc4668071e4e0351ac3a2e20131a45027fac017a0/ftbq/version'
        # try:
        #     response = requests.get(url, timeout=8)
        #     if response.status_code == 200:
        #         result = response.json()
        #         latest_version = result['version']
        #         logs = result['logs'].split('--')
        #         link = result['link']
        #         if latest_version != VERSION:
        #             print(TextStyle.RED + TextStyle.BOLD + TextStyle.UNDERLINE + "检测到更新!!!\n"
        #                   + TextStyle.RESET + "最新版本：")
        #             print(TextStyle.GREEN + latest_version + TextStyle.RESET)
        #             print("更新日志" + TextStyle.YELLOW)
        #             for log in logs:
        #                 print(log)
        #             print(TextStyle.RESET + "下载链接")
        #             print(TextStyle.GREEN + link + TextStyle.RESET)
        # except Exception as e:
        #     print(TextStyle.RED + "更新检查失败,服务器貌似开小差了~" + TextStyle.RESET)
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


