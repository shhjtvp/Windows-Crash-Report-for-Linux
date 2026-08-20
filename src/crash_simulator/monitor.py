import os
import sys
import json
import signal
import logging
import subprocess
import threading
from pathlib import Path
from typing import Optional

# ── 日志配置 ──────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("ProcessMonitor")


class ProcessMonitor:
    """
    监控指定进程，当目标进程退出时自动弹出 GUI 告警窗口。

    Parameters
    ----------
    pid : int
        要监控的目标进程 PID。
    name : str
        目标进程的可读名称（用于日志与 GUI 显示）。
    poll_interval : float
        轮询间隔（秒），默认 1.0。
    """

    def __init__(self, pid: int, name: str, poll_interval: float = 1.0):
        if pid <= 0:
            raise ValueError(f"无效的 PID: {pid}，必须为正整数")

        self.pid = pid
        self.name = name
        self.poll_interval = max(0.1, poll_interval)  # 防止过短轮询

        # 使用 Event 代替 bool，可被信号立即中断 wait()
        self._stop_event = threading.Event()
        # 保留 running 属性以兼容外部读取，但内部状态由 _stop_event 驱动
        self.running: bool = True

        self._gui_process: Optional[subprocess.Popen] = None
        self._register_signals()

    # ──────────────────────────────────────────────────────
    # 信号处理
    # ──────────────────────────────────────────────────────
    def _register_signals(self):
        """注册 SIGINT / SIGTERM 以便优雅退出"""
        for sig in (signal.SIGINT, signal.SIGTERM):
            try:
                signal.signal(sig, self._signal_handler)
            except (OSError, ValueError) as exc:
                # 非主线程或 Windows 不支持的信号会抛出异常
                logger.warning("无法注册信号 %s: %s", sig, exc)

    def _signal_handler(self, signum, frame):
        """信号回调：立即唤醒 stop_event，无需等待当前 sleep 结束"""
        sig_name = signal.Signals(signum).name if hasattr(signal, "Signals") else str(signum)
        logger.info("收到信号 %s，准备停止监控...", sig_name)
        self.running = False
        self._stop_event.set()

    # ──────────────────────────────────────────────────────
    # 进程存活检测（跨平台）
    # ──────────────────────────────────────────────────────
    @staticmethod
    def _is_process_alive(pid: int) -> bool:
        """
        跨平台判断进程是否存活。
        - POSIX: os.kill(pid, 0) 仅做存在性检查
        - Windows: ctypes.windll.kernel32.OpenProcess
        """
        if pid <= 0:
            return False
        try:
            if os.name == "posix":
                os.kill(pid, 0)
                return True
            else:
                import ctypes
                kernel32 = ctypes.windll.kernel32
                PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
                handle = kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
                if handle:
                    kernel32.CloseHandle(handle)
                    return True
                return False
        except ProcessLookupError:
            return False
        except PermissionError:
            # 进程存在但无权查询 → 视为存活
            return True
        except Exception as exc:
            logger.debug("检查进程 %d 存活状态时异常: %s", pid, exc)
            return False

    def check_health(self) -> bool:
        """检查目标进程是否仍在运行。返回 True=存活, False=已退出。"""
        alive = self._is_process_alive(self.pid)
        if not alive:
            logger.warning("进程 %s (PID=%d) 已不可达", self.name, self.pid)
        return alive

    def check_exited(self) -> bool:
        """check_health 的反向语义别名，方便外部循环使用。"""
        return not self.check_health()

    # ──────────────────────────────────────────────────────
    # GUI 告警子进程
    # ──────────────────────────────────────────────────────
    def _launch_gui(self):
        """
        以独立子进程启动 GUI 弹窗。
        参数通过 JSON 序列化传递，避免字符串拼接导致的注入风险。
        """
        # 如果 GUI 进程已在运行，不重复启动
        if self._gui_process is not None and self._gui_process.poll() is None:
            logger.debug("GUI 告警进程 (PID=%s) 仍在运行，跳过重复启动", self._gui_process.pid)
            return

        payload = json.dumps({"pid": self.pid, "name": self.name})
        cmd = [
            sys.executable, "-c",
            (
                "import sys, json; "
                "from gui_app import start_gui; "
                "d = json.loads(sys.argv[1]); "
                "start_gui(d['pid'], d['name'])"
            ),
            payload,
        ]

        try:
            self._gui_process = subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
                start_new_session=True,  # 脱离父进程组，避免被同一信号误杀
            )
            logger.info("已启动 GUI 告警子进程 (PID=%s)", self._gui_process.pid)
        except FileNotFoundError:
            logger.error("找不到 Python 解释器 (%s)，无法启动 GUI", sys.executable)
        except Exception as exc:
            logger.error("启动 GUI 告警子进程失败: %s", exc)

    # ──────────────────────────────────────────────────────
    # 主监控循环
    # ──────────────────────────────────────────────────────
    def run(self):
        """
        阻塞式监控主循环。
        推荐使用此方法代替外部手写 while 循环，
        内部已正确处理 poll_interval 与信号中断。
        """
        logger.info(
            "开始监控进程 '%s' (PID=%d)，轮询间隔 %.2fs",
            self.name, self.pid, self.poll_interval,
        )

        while not self._stop_event.is_set():
            if self.check_exited():
                logger.warning("✖ 检测到进程 '%s' (PID=%d) 已退出！", self.name, self.pid)
                self._launch_gui()
                break  # 目标进程已退出，监控任务完成

            # wait(timeout) 可被 _stop_event.set() 立即唤醒
            # 相比 time.sleep，响应信号的延迟从 poll_interval 降至近乎 0
            self._stop_event.wait(timeout=self.poll_interval)

        logger.info("监控循环已结束")

    # ──────────────────────────────────────────────────────
    # 资源清理
    # ──────────────────────────────────────────────────────
    def cleanup(self):
        """
        释放所有资源：
        1. 设置停止标志，唤醒可能阻塞在 wait() 中的线程
        2. 终止 GUI 告警子进程（先 TERM 后 KILL）
        3. 重置内部状态
        """
        logger.info("正在执行资源清理...")
        self._stop_event.set()
        self.running = False

        if self._gui_process is not None:
            if self._gui_process.poll() is None:
                logger.info("正在终止 GUI 告警子进程 (PID=%s)...", self._gui_process.pid)
                self._gui_process.terminate()
                try:
                    self._gui_process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    logger.warning("GUI 子进程未在 5s 内退出，强制杀死")
                    self._gui_process.kill()
                    self._gui_process.wait(timeout=3)
            self._gui_process = None

        logger.info("✅ 资源清理完成")

    # ──────────────────────────────────────────────────────
    # 上下文管理器支持
    # ──────────────────────────────────────────────────────
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()
        return False  # 不吞掉异常

    def __repr__(self) -> str:
        status = "running" if self.running else "stopped"
        return f"<ProcessMonitor pid={self.pid} name='{self.name}' status={status}>"