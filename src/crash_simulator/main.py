import sys
import os
import time
import json
import argparse
import subprocess
from pathlib import Path

# 确保能找到本地模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from monitor import ProcessMonitor
from gui_app import start_gui
from setup_utils import create_desktop_entry, remove_desktop_entry

# 用户同意标记路径
CONSENT_FLAG = Path.home() / ".crash_sim_consent"

def require_consent():
    """要求用户确认风险。如果已经确认过，则直接返回。"""
    if CONSENT_FLAG.exists():
        return True

    print("="*50)
    print("⚠️  [崩溃模拟器 - 风险警告] ⚠️")
    print("该项目用于模拟进程崩溃场景，仅用于测试和演示目的。")
    print("请勿在生产力环境或重要服务器上运行此工具。")
    print("继续运行即表示您同意自行承担所有风险。")
    print("="*50)
    
    ans = input("我已了解风险并同意继续使用 (输入 'yes' 确认): ").strip().lower()
    if ans in ('yes', 'y'):
        CONSENT_FLAG.write_text(json.dumps({"consent_time": time.time()}))
        return True
    
    print("❌ 用户取消操作，程序退出。")
    return False

def cmd_monitor(args):
    """启动监控守护进程"""
    # 示例：监控当前 CLI 进程本身，或者你可以通过 args 传入特定的 PID
    pid = os.getpid()
    name = "CrashSim-Main"
    
    print(f"🚀 启动监控守护进程... (目标 PID: {pid}, 名称: {name})")
    monitor = ProcessMonitor(pid, name)
    
    try:
        # 使用 monitor 内部配置的 poll_interval 进行循环
        while monitor.running:
            monitor.check_health()
            # 使用 threading.Event 的 wait 方法代替 time.sleep，以便能被信号立即中断
            if hasattr(monitor, 'stop_event'):
                monitor.stop_event.wait(timeout=monitor.poll_interval)
            else:
                time.sleep(monitor.poll_interval)
    except KeyboardInterrupt:
        print("\n🛑 收到中断信号，正在停止监控...")
    finally:
        monitor.cleanup()
        print("✅ 监控进程已安全退出。")

def cmd_gui(args):
    """启动图形界面"""
    # 修复：start_gui 需要 pid 和 name 参数
    # 如果用户通过命令行指定了 PID，则使用指定的；否则默认监控当前终端或一个虚拟进程
    target_pid = args.pid if args.pid else os.getpid()
    target_name = args.name if args.name else "CrashSim-GUI-Target"
    
    print(f"🖥️  正在启动 GUI 界面... (监控目标: {target_name} [{target_pid}])")
    
    # 注意：如果在独立进程中启动 GUI，应确保 PySide6 环境正确
    # 这里直接调用函数，因为 start_gui 内部会创建 QApplication
    try:
        start_gui(target_pid, target_name)
    except Exception as e:
        print(f"❌ GUI 启动失败: {e}")
        sys.exit(1)

def cmd_setup(args):
    """设置开机自启"""
    if args.remove:
        remove_desktop_entry()
        print("🗑️  已移除开机自启配置。")
    else:
        create_desktop_entry()
        print("✅ 已配置开机自启。")

def main():
    parser = argparse.ArgumentParser(
        prog="crash-sim",
        description="崩溃模拟器 - 进程监控与故障演示工具"
    )
    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # monitor 子命令
    p_mon = subparsers.add_parser("monitor", help="启动后台监控守护进程")
    p_mon.set_defaults(func=cmd_monitor)

    # gui 子命令
    p_gui = subparsers.add_parser("gui", help="启动图形监控界面")
    p_gui.add_argument("--pid", type=int, help="要监控的进程 PID (默认为当前进程)")
    p_gui.add_argument("--name", type=str, help="要监控的进程名称")
    p_gui.set_defaults(func=cmd_gui)

    # setup 子命令
    p_setup = subparsers.add_parser("setup", help="配置系统开机自启")
    p_setup.add_argument("--remove", action="store_true", help="移除开机自启配置")
    p_setup.set_defaults(func=cmd_setup)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    # 除了 setup 命令外，其他命令需要用户确认风险
    if args.command != "setup":
        if not require_consent():
            sys.exit(1)

    # 执行对应的子命令
    args.func(args)

if __name__ == "__main__":
    main()