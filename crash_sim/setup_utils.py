# crash_sim/setup_utils.py
import os
import sys
import shutil
from pathlib import Path

def interactive_setup():
    print("\033[93m" + "=" * 60)
    print("  警告：此脚本仅供技术演示和娱乐用途喵~")
    print("  使用本脚本产生的任何后果由使用者自行承担nya~")
    print("  不要在物理机上运行本脚本！")
    print("=" * 60 + "\033[0m")
    
    # 询问自启动
    while True:
        choice = input("是否启用开机自启动？(y/N): ").strip().lower()
        if choice in ('y', 'yes'):
            enable_autostart()
            break
        elif choice in ('n', 'no', ''):
            disable_autostart()
            break
        else:
            print("请输入 y 或 n")

def enable_autostart():
    autostart_dir = Path.home() / ".config" / "autostart"
    autostart_dir.mkdir(parents=True, exist_ok=True)
    desktop_file = autostart_dir / "crash-sim.desktop"
    content = f"""[Desktop Entry]
Type=Application
Name=Crash Simulator
Exec=crash-sim
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
Comment=模拟Windows崩溃报告
"""
    desktop_file.write_text(content)
    print("已为当前用户开启开机自启动了喵~")

def disable_autostart():
    autostart_file = Path.home() / ".config" / "autostart" / "crash-sim.desktop"
    if autostart_file.exists():
        autostart_file.unlink()
        print("删除自启动项了喵~")
    else:
        print("ℹ未发现已存在的自启动项")
def uninstall_cleanup():
    disable_autostart()
    print("已清理所有配置，您可以使用 pip uninstall crash-simulator 移除程序")