import os
import sys
import time
import signal
import logging
import importlib
from typing import Set, Tuple, Optional, List
import psutil
import subprocess

logger = logging.getLogger(__name__)

class ProcessMonitor:
    def __init__(self, blacklist: Optional[List[str]] = None, poll_interval: float = 1.5):
        self.blacklist = set(b.lower() for b in (blacklist or []))
        self.poll_interval = poll_interval
        self.running = True
        
        # 自身进程及子进程排除
        self.self_pids = self._get_self_and_children_pids()
        
        # 已知进程快照: Set[Tuple[int, float, str]] -> (pid, create_time, name)
        self.known_processes: Set[Tuple[int, float, str]] = set()
        
        # 注册信号处理器，确保 Ctrl+C 或 systemctl stop 能优雅退出
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _get_self_and_children_pids(self) -> Set[int]:
        """获取自身及所有子进程的 PID 集合"""
        try:
            parent = psutil.Process(os.getpid())
            children = parent.children(recursive=True)
            return {p.pid for p in children} | {parent.pid}
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return {os.getpid()}

    def _signal_handler(self, signum, frame):
        logger.info(f"接收到信号 {signum}，正在停止监控...")
        self.running = False

    def _get_process_snapshot(self) -> Set[Tuple[int, float, str]]:
        """获取当前系统进程快照，过滤黑名单和自身进程"""
        snapshot = set()
        for proc in psutil.process_iter(['pid', 'name', 'create_time']):
            try:
                pid = proc.info['pid']
                if pid in self.self_pids:
                    continue
                
                name = proc.info['name']
                if name and name.lower() in self.blacklist:
                    continue
                
                # 使用 (pid, create_time) 防止 PID 复用误判
                snapshot.add((pid, proc.info['create_time'], name))
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        return snapshot

    def run(self):
        """启动监控主循环"""
        self.known_processes = self._get_process_snapshot()
        logger.info(f"开始监控 {len(self.known_processes)} 个进程... (轮询间隔: {self.poll_interval}s)")
        
        while self.running:
            time.sleep(self.poll_interval)
            if not self.running:
                break
                
            try:
                current_processes = self._get_process_snapshot()
                
                # 找出消失的进程 (在 known 中但不在 current 中)
                dead_processes = self.known_processes - current_processes
                
                for pid, ctime, name in dead_processes:
                    self._handle_crash(pid, name)
                    
                self.known_processes = current_processes
                
            except Exception as e:
                logger.error(f"轮询出错: {e}", exc_info=True)

    def _handle_crash(self, pid: int, name: str):
        """处理进程崩溃事件"""
        logger.warning(f"检测到进程崩溃: [PID {pid}] {name}")
        self._launch_gui(pid, name)

    def _launch_gui(self, pid: int, name: str):
        subprocess.Popen(
            [sys.executable, "-c", 
             f"from crash_simulator.gui_app import start_gui; start_gui({pid}, '{name}')"],
            start_new_session=True  # 脱离父进程，避免被 SIGTERM 连带杀死
        )