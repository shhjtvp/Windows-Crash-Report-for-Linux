import sys
import argparse
import logging


def main():
# main.py 的 main() 函数开头
    import os, json
    MARKER = os.path.expanduser("~/.config/crash_sim/.risk_acknowledged")
    if not os.path.exists(MARKER):
        print("\n首次运行提醒：本项目为整活工具，可能干扰系统进程。")
        print("   请确保在非生产环境中使用。按 Enter 确认已知悉，后续不再提醒...")
        input()
        os.makedirs(os.path.dirname(MARKER), exist_ok=True)
        open(MARKER, "w").close()

    """CLI 入口点 - 绝不在此处初始化 GUI 或执行耗时操作"""
    parser = argparse.ArgumentParser(
        prog="crash-sim",
        description="Crash simulation and process monitoring tool"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # GUI 子命令
    gui_parser = subparsers.add_parser("gui", help="Launch graphical interface")
    gui_parser.add_argument("--verbose", action="store_true", help="Enable debug logging")

    # Monitor 子命令
    mon_parser = subparsers.add_parser("monitor", help="Run CLI process monitor")
    mon_parser.add_argument("--blacklist", nargs="*", default=[], help="Process names to ignore")

    args = parser.parse_args()

    # 配置日志
    log_level = logging.DEBUG if getattr(args, 'verbose', False) else logging.INFO
    logging.basicConfig(level=log_level, format="%(asctime)s [%(levelname)s] %(message)s")

    if args.command == "gui":
        # ✅ GUI 仅在用户明确要求时加载，pipx 验证不会触发此处
        try:
            from .gui_app import start_gui
            start_gui()
        except ImportError:
            print("ERROR: GUI dependencies not installed.", file=sys.stderr)
            print("Install with: pipx install 'crash-sim[gui]'", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            logging.exception(f"GUI startup failed: {e}")
            sys.exit(1)

    elif args.command == "monitor":
        from .monitor import ProcessMonitor
        monitor = ProcessMonitor(blacklist=set(args.blacklist))
        monitor.start()
        print("Monitoring... Press Ctrl+C to stop.")
        try:
            while True:
                exited = monitor.check_exited()
                for pid, name in exited:
                    print(f"[EXITED] {name} (PID {pid})")
                import time; time.sleep(1)
        except KeyboardInterrupt:
            monitor.stop()
            print("\nStopped.")
    else:
        parser.print_help()
        sys.exit(0)


if __name__ == "__main__":
    main()