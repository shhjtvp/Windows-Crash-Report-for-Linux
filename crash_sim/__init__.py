#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#阿伟，你又在看代码了哦，歇歇好吗？
import sys
import time
import subprocess
import threading
import psutil
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QCheckBox, QProgressDialog, QMessageBox
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QObject
from PyQt5.QtGui import QIcon, QPixmap

# ---------- 警告信息 ----------
print("\033[93m" + "=" * 60)
print("  警告：此脚本仅供技术演示和娱乐用途喵~")
print("  使用本脚本产生的任何后果由要使用者自行承担nya~")
print("  不要在物理机上运行本脚本！")
print("=" * 60 + "\033[0m")

# ---------- 后台监控线程 ----------
class ProcessMonitor(QObject):
    # 信号：当检测到进程退出时发射 (pid, 进程名)
    process_exited = pyqtSignal(int, str)

    def __init__(self, parent=None):
        self.blacklist = ['sh', 'bash', 'sleep', 'cron', 'grep', 'awk', 'sed']
        super().__init__(parent)
        self._running = True
        self._known_pids = {}  # pid -> 进程名

    def start_monitor(self):
        """开始监控（在独立线程中运行）"""
        self._running = True
        # 获取当前用户所有进程快照
        self._known_pids = {}   # 注意这里改为 self._known_pids
        for proc in psutil.process_iter(['pid', 'name', 'uid']):
            try:
                if proc.info['uid'] == os.getuid():
                    self._known_pids[proc.info['pid']] = proc.info['name']
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        # 启动定时检查（每4066毫秒次）
        self.timer = QTimer()
        self.timer.timeout.connect(self._check)
        self.timer.start(5000)

    def stop_monitor(self):
        self._running = False
        if hasattr(self, 'timer'):
            self.timer.stop()

    def _check(self):
        if name not in self.blacklist:
            self.process_exited.emit(pid, name)
        if not self._running:
            return
        # 获取当前进程列表
        current_pids = {}
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                current_pids[proc.info['pid']] = proc.info['name']
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        # 检测哪些进程从之前快照中消失（即已退出）
        exited = set(self._known_pids.keys()) - set(current_pids.keys())
        for pid in exited:
            name = self._known_pids.get(pid, "Unknown")
            # 排除自身（当前脚本的进程）
            if pid == os.getpid():
                continue
            # 发射信号，在主线程中处理
            self.process_exited.emit(pid, name)

        # 更新快照
        self._known_pids = current_pids

# ---------- 错误报告窗口 ----------
class CrashReportWindow(QMainWindow):
    def __init__(self, pid, process_name):
        super().__init__()
        self.pid = pid
        self.process_name = process_name
        self.worker_thread = None
        self.progress_dialog = None
        self.init_ui()
        self.setAttribute(Qt.WA_DeleteOnClose, True)

    def init_ui(self):
        self.setWindowTitle("Microsoft Windows 错误报告")
        self.setFixedSize(480, 200)
        # 尝试设置Windows风格
        self.setStyle(QApplication.style().metaObject().className())

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # 提示文本
        layout.addWidget(QLabel(f"{self.process_name} (PID: {self.pid}) 遇到一个问题，需要关闭。"))
        layout.addWidget(QLabel("我们对此引起的不便表示抱歉。"))

        # 错误签名
        sig_label = QLabel("错误签名")
        sig_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(sig_label)

        details = QVBoxLayout()
        details.addWidget(QLabel(f"应用程序名: {self.process_name}"))
        details.addWidget(QLabel(f"应用程序版本: 1145.14.350234"))
        details.addWidget(QLabel(f"事件名称: APPCRASH"))
        layout.addLayout(details)

        # 底部按钮
        btn_layout = QHBoxLayout()
        self.checkbox = QCheckBox("发送错误报告")
        self.checkbox.setChecked(True)
        btn_layout.addWidget(self.checkbox)

        btn_layout.addStretch()

        send_btn = QPushButton("发送")
        send_btn.clicked.connect(self.on_send)
        btn_layout.addWidget(send_btn)

        close_btn = QPushButton("退出")
        close_btn.clicked.connect(self.close)
        btn_layout.addWidget(close_btn)

        layout.addLayout(btn_layout)

    def on_send(self):
        if not self.checkbox.isChecked():
            QMessageBox.information(self, "[Info]", "选择 退出")
            self.close()
            return

        # 弹出进度条窗口（位于屏幕左上角）
        self.progress_dialog = QProgressDialog("正在向 Microsoft 发送错误报告...", "取消", 0, 100, self)
        self.progress_dialog.setWindowTitle("请稍后")
        self.progress_dialog.setWindowModality(Qt.WindowModal)
        # 移动窗口到左上角
        screen_geo = QApplication.primaryScreen().geometry()
        self.progress_dialog.move(0, 0)
        self.progress_dialog.show()

        # 启动后台任务：执行ping命令
        self.worker = SendReportWorker()
        self.worker.progress_updated.connect(self.update_progress)
        self.worker.finished.connect(self.on_send_finished)
        self.worker.canceled.connect(self.on_send_canceled)
        self.worker.start()

    def update_progress(self, value):
        if self.progress_dialog:
            self.progress_dialog.setValue(value)

    def on_send_finished(self, success):
        if self.progress_dialog:
            self.progress_dialog.close()
        if success:
            QMessageBox.information(self, "发送成功", "错误报告已成功发送给 Microsoft。\n感谢您帮助我们改进产品！")
            print("[Info]微软：？")
            time.sleep(1)
        else:
            QMessageBox.warning(self, "发送失败", "发送报告时出现网络错误，请稍后重试。")
            print("\033[91m[error]网络问题\033[0m]")
        self.close()

    def on_send_canceled(self):
        if self.progress_dialog:
            self.progress_dialog.close()
        QMessageBox.warning(self, "已取消", "错误报告发送已取消。")
        self.close()

    def closeEvent(self, event):
        if hasattr(self, 'worker') and self.worker and self.worker.isRunning():
            self.worker.cancel()
            self.worker.wait()
        event.accept()

# ---------- 后台发送线程 ----------
class SendReportWorker(threading.Thread):
    progress_updated = pyqtSignal(int)
    finished = pyqtSignal(bool)
    canceled = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._cancel = False

    def cancel(self):
        self._cancel = True

    def run(self):
        try:
            # 模拟发送步骤，更新进度
            for i in range(1, 11):
                if self._cancel:
                    self.canceled.emit()
                    return
                time.sleep(0.3)
                self.progress_updated.emit(i * 10)

            # 执行 ping 命令（如果未取消）
            if not self._cancel:
                cmd = ['ping', '-c', '1', '-W', '2', 'microsoft.com']
                result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=5)
                success = (result.returncode == 0)   # 在这里定义 success
                # 如果过程中被取消，则不再发射完成信号
                if self._cancel:
                    self.canceled.emit()
                    return
                # 更新进度到100%
                self.progress_updated.emit(100)
                # 发射完成信号
                self.finished.emit(success)
            else:
                self.canceled.emit()
        except Exception as e:
            self.finished.emit(False)

# ---------- 主程序 ----------
import os

def main():
    app = QApplication(sys.argv)
    app.setStyle('Windows')  # 尝试Windows风格

    # 创建监控对象
    monitor = ProcessMonitor()

    # 信号绑定：当进程退出时，创建并显示错误报告窗口
    def on_process_exited(pid, name):
        # 确保在主线程中创建窗口
        window = CrashReportWindow(pid, name)
        window.show()

    monitor.process_exited.connect(on_process_exited)

    # 开始监控
    monitor.start_monitor()

    # 退出时停止监控
    app.aboutToQuit.connect(monitor.stop_monitor)

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
