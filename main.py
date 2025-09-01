import os
import sys
import textwrap
from typing import Callable

import func
from func.base import check_config_exists

VERSION = '1.4.9'

# ---------------- 工具函数 ----------------
def clear() -> None:
    """跨平台清屏"""
    os.system("cls" if os.name == "nt" else "clear")

def pause() -> None:
    """等待用户继续"""
    input("\n按 Enter 键继续...")

def safe_import(module_name: str) -> Callable | None:
    """懒加载功能模块，减少启动时间"""
    try:
        return __import__(module_name, fromlist=[""]).__dict__[module_name]
    except Exception as e:
        print(f"❌ 加载模块失败: {e}")
        return None

# ---------------- 菜单系统 ----------------
class Menu:
    def __init__(self, title: str, items: list[tuple[str, Callable | None, str]]):
        """
        :param title: 菜单标题
        :param items: [(按键, 函数, 描述), ...]
        """
        self.title = title
        self.items = items

    def run(self) -> None:
        while True:
            clear()
            print(self.title)
            for key, _, desc in self.items:
                print(f"  {key}  {desc}")
            choice = input("\n请选择：").strip()
            for key, func, _ in self.items:
                if choice == key and func:
                    try:
                        func()
                    except Exception as e:
                        print(f"运行出错：{e}")
                    pause()
                    break
            else:
                if choice.lower() in {"q", "quit", "exit"}:
                    return
                print("⚠️  无效输入，请重新选择。")


# ---------------- 主流程 ----------------
def main():
    # 1. 检查配置文件
    try:
        check_config_exists()
    except Exception as e:
        print("配置文件检查失败：", e)
        pause()
        return

    # 2. 版本提示
    if len(sys.argv) == 1:  # 没有命令行参数时才进入交互模式
        clear()
        print(
            textwrap.dedent(
                f"""
                ╔══════════════════════════════════════════╗
                         FTBQ 本地化小工具 v{VERSION}         
                ╚══════════════════════════════════════════╝

                使用前请确认：
                1. 已正确设置 config.py 中的 LANG_PATH 与 WORK_PATH
                2. 1.20+自带lang文件，请修改config中LANG_PATH后选择功能3, lang文件见/ftbquests/quests/lang/en_us.snbt)
                """
            )
        )
        pause()

    # 3. 主菜单
    main_menu = Menu(
        title=textwrap.dedent(
            """
            ╔══════════════════════════════════════════╗
            ║  主菜单                                  ║
            ╚══════════════════════════════════════════╝
            """
        ),
        items=[
            ("1", func.quest_trans, "翻译任务（旧版）"),
            ("2", func.trans2lang, "生成 lang 文件"),
            ("3", func.lang_trans, "翻译 lang 文件（低版本json,高版本snbt）"),
            ("4", func.back_fill, "回填 lang 文件（仅 .json）"),
            ("q", None, "退出"),
        ],
    )
    main_menu.run()

if __name__ == "__main__":
    main()


