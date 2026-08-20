"""
PySide6 GUI 应用程序
修复了以下问题：
1. 增加了参数默认值，使其更灵活。
2. 优化了 sys.exit 的使用，确保资源能更好释放。
3. 增强了 QSS 和图标加载的异常处理与 Fallback 机制。
"""

import sys
import os
import json
import logging
from pathlib import Path

# PySide6 导入
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame, QSystemTrayIcon, QMenu, QMessageBox
)
from PySide6.QtCore import Qt, QTimer, QSize, Signal
from PySide6.QtGui import QIcon, QAction, QFont, QColor, QPalette

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("CrashSimGUI")

class MainWindow(QMainWindow):
    """主窗口类"""
    
    # 定义信号，用于跨线程或组件通信
    crash_detected = Signal(int, str)

    def __init__(self, target_pid: int, target_name: str):
        super().__init__()
        self.target_pid = target_pid
        self.target_name = target_name
        
        self.setWindowTitle(f"崩溃模拟器 - 监控: {target_name} [{target_pid}]")
        self.setMinimumSize(600, 400)
        
        # 尝试加载样式和图标
        self._apply_stylesheet()
        self._setup_ui()
        self._setup_tray_icon()
        
        # 模拟心跳/状态检查定时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._check_status)
        self.timer.start(2000) # 每2秒检查一次

    def _apply_stylesheet(self):
        """加载并应用 QSS 样式表"""
        qss_path = Path(__file__).parent / "resources" / "style.qss"
        try:
            if qss_path.exists():
                with open(qss_path, "r", encoding="utf-8") as f:
                    self.setStyleSheet(f.read())
                logger.info("成功加载外部样式表。")
            else:
                logger.warning(f"未找到样式文件 {qss_path}，使用默认样式。")
                self._apply_fallback_style()
        except Exception as e:
            logger.error(f"加载样式表时出错: {e}")
            self._apply_fallback_style()

    def _apply_fallback_style(self):
        """内置的 Fallback 样式，确保在无外部 QSS 时界面依然整洁"""
        fallback_qss = """
            QMainWindow { background-color: #f0f2f5; }
            QLabel { color: #333333; font-size: 14px; }
            QPushButton { 
                background-color: #0078d7; color: white; 
                border: none; border-radius: 4px; padding: 8px 16px; 
                font-weight: bold; 
            }
            QPushButton:hover { background-color: #005a9e; }
            QPushButton:pressed { background-color: #004578; }
            .StatusCard { 
                background-color: white; border-radius: 8px; 
                border: 1px solid #dddddd; padding: 10px; 
            }
        """
        self.setStyleSheet(fallback_qss)

    def _setup_ui(self):
        """初始化用户界面"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # 标题
        title_label = QLabel("⚠️ 进程崩溃模拟器控制台")
        title_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        # 状态卡片
        status_frame = QFrame()
        status_frame.setProperty("class", "StatusCard")
        status_layout = QVBoxLayout(status_frame)
        
        self.pid_label = QLabel(f"目标 PID: <b>{self.target_pid}</b>")
        self.name_label = QLabel(f"进程名称: <b>{self.target_name}</b>")
        self.status_label = QLabel("当前状态: <font color='green'><b>运行中 (监控中)</b></font>")
        
        status_layout.addWidget(self.pid_label)
        status_layout.addWidget(self.name_label)
        status_layout.addWidget(self.status_label)
        layout.addWidget(status_frame)

        # 操作按钮区
        btn_layout = QHBoxLayout()
        
        self.btn_simulate_crash = QPushButton("💥 模拟崩溃 (Simulate Crash)")
        self.btn_simulate_crash.clicked.connect(self._trigger_crash)
        
        self.btn_reset = QPushButton("🔄 重置状态")
        self.btn_reset.clicked.connect(self._reset_status)
        
        btn_layout.addWidget(self.btn_simulate_crash)
        btn_layout.addWidget(self.btn_reset)
        layout.addLayout(btn_layout)

        # 底部信息
        info_label = QLabel("提示：点击“模拟崩溃”将强制结束目标进程并触发监控报警。")
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_label.setStyleSheet("color: #666; font-size: 12px;")
        layout.addWidget(info_label)

    def _setup_tray_icon(self):
        """设置系统托盘图标"""
        if not QSystemTrayIcon.isSystemTrayAvailable():
            logger.warning("当前系统不支持系统托盘。")
            return

        self.tray_icon = QSystemTrayIcon(self)
        
        # 尝试加载图标，提供 fallback
        icon_path = Path(__file__).parent / "resources" / "icon.png"
        if icon_path.exists():
            self.tray_icon.setIcon(QIcon(str(icon_path)))
        else:
            # 使用系统默认图标或应用程序图标
            self.tray_icon.setIcon(self.style().standardIcon(self.style().StandardPixmap.SP_MessageBoxInformation))

        # 托盘菜单
        tray_menu = QMenu()
        show_action = QAction("显示主窗口", self)
        show_action.triggered.connect(self.show)
        quit_action = QAction("退出程序", self)
        quit_action.triggered.connect(QApplication.instance().quit)
        
        tray_menu.addAction(show_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        
        self.tray_icon.show()
        self.tray_icon.showMessage(
            "崩溃模拟器", 
            f"已开始监控进程 {self.target_name}", 
            QSystemTrayIcon.MessageIcon.Information, 
            2000
        )

    def _check_status(self):
        """定时检查目标进程状态"""
        # 这里只是演示，实际逻辑应在 monitor.py 中实现并通过信号传递
        # 检查 /proc/{pid} 或使用 psutil
        is_alive = os.path.exists(f"/proc/{self.target_pid}") if os.name == 'posix' else True # 简化处理
        
        if not is_alive:
            self.status_label.setText("当前状态: <font color='red'><b>已崩溃 (Crashed)</b></font>")
            self.crash_detected.emit(self.target_pid, self.target_name)
            self.timer.stop()
        else:
            self.status_label.setText("当前状态: <font color='green'><b>运行中 (Running)</b></font>")

    def _trigger_crash(self):
        """执行模拟崩溃操作"""
        reply = QMessageBox.question(
            self, '确认操作', 
            f"确定要强制结束进程 {self.target_name} (PID: {self.target_pid}) 吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                import signal
                if os.path.exists(f"/proc/{self.target_pid}"):
                    os.kill(self.target_pid, signal.SIGKILL)
                    logger.info(f"已向进程 {self.target_pid} 发送 SIGKILL 信号。")
                else:
                    logger.warning(f"进程 {self.target_pid} 似乎已经不存在。")
                    self._reset_status()
            except ProcessLookupError:
                logger.warning(f"进程 {self.target_pid} 未找到。")
            except PermissionError:
                logger.error(f"权限不足，无法结束进程 {self.target_pid}。")
            except Exception as e:
                logger.error(f"模拟崩溃失败: {e}")

    def _reset_status(self):
        """重置界面状态"""
        self.status_label.setText("当前状态: <font color='green'><b>运行中 (监控中)</b></font>")
        if not self.timer.isActive():
            self.timer.start(2000)

    def closeEvent(self, event):
        """重写关闭事件，使其最小化到托盘而不是直接退出"""
        if self.tray_icon and self.tray_icon.isVisible():
            self.hide()
            self.tray_icon.showMessage(
                "崩溃模拟器", 
                "程序已最小化到系统托盘运行。", 
                QSystemTrayIcon.MessageIcon.Information, 
                2000
            )
            event.ignore()
        else:
            event.accept()

def start_gui(pid: int = 1, name: str = "System"):
    """
    启动 GUI 应用程序。
    修复：增加了参数默认值，优化了退出逻辑。
    """
    # 确保每个进程只有一个 QApplication
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    # 设置应用程序级别的属性
    app.setApplicationName("Crash Simulator")
    app.setOrganizationName("CrashSim Tech")
    
    # 阻止关闭最后一个窗口时自动退出应用（为了支持托盘运行）
    app.setQuitOnLastWindowClosed(False)

    window = MainWindow(pid, name)
    window.show()

    logger.info(f"GUI 启动成功，正在监控: {name} [{pid}]")
    
    # 执行事件循环
    exit_code = app.exec()
    
    # 清理工作
    logger.info("GUI 应用程序退出。")
    sys.exit(exit_code)

if __name__ == "__main__":
    # 方便单独调试 GUI
    start_gui(pid=os.getpid(), name="Debug-Mode")