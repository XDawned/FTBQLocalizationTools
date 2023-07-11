import requests
from func.base import TextStyle
VERSION = 'v1.4.1'

if __name__ == '__main__':
    try:
        import func
        url = ''
        try:
            response = requests.get(url, timeout=8)
            if response.status_code == 200:
                result = response.json()
                latest_version = result[0]
                logs = result[1]
                link = result[2]
                if latest_version != VERSION:
                    print("检测到更新!\n最新版本：")
                    print(TextStyle.GREEN + latest_version + TextStyle.RESET)
                    print("更新日志")
                    print(TextStyle.YELLOW + logs + TextStyle.RESET)
                    print("下载链接")
                    print(TextStyle.GREEN + link + TextStyle.RESET)
        except Exception as e:
            print(TextStyle.RED + "更新检查失败,服务器貌似开小差了~" + TextStyle.RESET)
        while True:
            print('**********FTBQ本地化小工具-%s**********' %VERSION)
            print('主功能引导\n1.翻译任务snbt\n2.生成lang文件(默认位置config中WORK_PATH)\n3.翻译lang文件\n4.回填lang文件\n5.退出')
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
                func.back_fill()
            elif choice == '5':
                break
            else:
                print('无效输入')
    except Exception as e:
        print("程序发生了错误:", repr(e))
    finally:
        input("按任意键继续...")


