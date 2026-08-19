import os
import logging
from typing import Set, Dict, Optional

try:
    import psutil
except ImportError:
    psutil = None  # 降级处理，后续给出明确提示

logger = logging.getLogger(__name__)


class ProcessMonitor:
    """健壮的进程监控器，支持黑名单过滤与安全退出检测"""

    def __init__(self, blacklist: Optional[Set[str]] = None):
        self.blacklist = blacklist or set()
        self._known_pids: Dict[int, str] = {}
        self._running = False

        if psutil is None:
            raise RuntimeError(
                "psutil is required for process monitoring. "
                "Install it via: pip install psutil"
            )

    def start(self):
        """启动监控，记录当前所有进程快照"""
        try:
            for proc in psutil.process_iter(['pid', 'name']):
                self._known_pids[proc.info['pid']] = proc.info['name']
            self._running = True
            logger.info(f"Monitoring started. Tracking {len(self._known_pids)} processes.")
        except (psutil.AccessDenied, psutil.NoSuchProcess) as e:
            logger.warning(f"Partial process snapshot due to permission: {e}")
            self._running = True  # 部分失败仍继续运行

    def check_exited(self) -> list:
        """
        检查已退出的进程，返回 (pid, name) 列表
        ✅ 修复：变量作用域、黑名单过滤位置、异常兜底
        """
        if not self._running:
            return []

        exited = []
        current_pids = set()
        try:
            for proc in psutil.process_iter(['pid']):
                current_pids.add(proc.info['pid'])
        except Exception as e:
            logger.error(f"Failed to enumerate processes: {e}")
            return []

        # 计算差集得到已退出 PID
        exited_pids = set(self._known_pids.keys()) - current_pids

        for pid in exited_pids:
            name = self._known_pids.get(pid, "Unknown")
            # ✅ 跳过自身进程
            if pid == os.getpid():
                continue
            # ✅ 黑名单过滤必须在获取 name 之后、加入结果之前
            if name in self.blacklist:
                continue
            exited.append((pid, name))
            logger.debug(f"Process exited: {name} (PID {pid})")

        # 清理已知进程表，避免内存泄漏
        for pid in exited_pids:
            self._known_pids.pop(pid, None)

        return exited

    def stop(self):
        self._running = False
        self._known_pids.clear()
        logger.info("Monitoring stopped.")