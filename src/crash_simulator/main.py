import sys
import argparse
import logging
import sys, os


CONSENT_FLAG = os.path.expanduser("~/.config/crash_simulator/.consent_given")

def require_consent():
    if os.path.exists(CONSENT_FLAG):
        return

    # 检测是否为非交互式环境
    if not sys.stdin.isatty():
        print("[Info]检测到非交互式环境，为安全起见拒绝启动")
        print("请在手动终端中首次运行以完成风险确认")
        sys.exit(1)

    print("\n" + "=" * 60)
    print("[傻逼项目 | 赤石科技系列]")
    print("=" * 60)
    print("• 可能被杀毒软件/EDR 误判为恶意程序")
    print("• 可能在某些桌面环境下导致窗口管理器异常")
    print("• 绝对不适合在生产服务器/工作机上使用")
    print("-" * 60)

    try:
        answer = input("我已了解上述风险并自愿承担后果 (输入 YES 继续): ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\n已取消运行。")
        sys.exit(0)

    if answer != "YES":
        print("已取消运行。")
        sys.exit(0)

    os.makedirs(os.path.dirname(CONSENT_FLAG), exist_ok=True)
    with open(CONSENT_FLAG, "w") as f:
        f.write(f"consented_at={time.time()}\n")
    print("✅ 已记录同意，后续启动将不再提示。\n")

def main():
# main.py 的 main() 函数开头
    import os, json
    MARKER = os.path.expanduser("~/.config/crash_sim/.risk_acknowledged")
    require_consent()

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