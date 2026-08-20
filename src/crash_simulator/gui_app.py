import sys
import platform
import logging
from typing import Optional

logger = logging.getLogger(__name__)

def start_gui(pid: int, name: str):
    """
    GUI 启动入口（供 monitor.py 动态调用）
    内部处理所有 PyQt5 导入与异常，绝不向外抛出
    """
    try:
        from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
        from PyQt5.QtCore import Qt, QSize
        from PyQt5.QtGui import QIcon, QPixmap
        import os

        # 确保每个崩溃弹窗拥有独立的 QApplication 实例生命周期管理
        app = QApplication.instance() or QApplication(sys.argv)

        dialog = _CrashDialog(pid, name)
        dialog.show()
        
        # 使用 exec_ 阻塞当前线程直到弹窗关闭，避免被监控主循环回收
        # 注意：monitor.py 中应以子进程或非阻塞方式调用此函数，否则主循环会暂停
        sys.exit(app.exec_()) 
        
    except ImportError as e:
        logger.error(f"PyQt5 导入失败: {e}")
    except Exception as e:
        logger.error(f"GUI 渲染异常: {e}", exc_info=True)


class _CrashDialog(QWidget):
    def __init__(self, pid: int, process_name: str, parent=None):
        super().__init__(parent)
        self.pid = pid
        self.process_name = process_name
        
        # 1. 跨平台边框与窗口标志处理
        self._setup_window_flags()
        
        # 2. 绑定 QSS 对象名
        self.setObjectName("CrashDialog")
        
        # 3. 加载样式表
        self._load_style()
        
        # 4. 构建 UI 与信号连接
        self._setup_ui()
        
        # 5. 窗口居中与尺寸固定
        self.setFixedSize(480, 260)
        self._center_window()

    def _setup_window_flags(self):
        """根据操作系统动态设置窗口标志"""
        system = platform.system()
        
        if system == "Windows":
            # Windows: 无边框 + 透明背景以支持 QSS 圆角和阴影
            self.setWindowFlags(
                Qt.FramelessWindowHint | 
                Qt.WindowStaysOnTopHint |
                Qt.Tool  # 不在任务栏显示
            )
            self.setAttribute(Qt.WA_TranslucentBackground)
        else:
            # Linux/macOS: 保留原生边框以避免合成器兼容问题
            # 仅通过 QSS 控制内部控件样式
            self.setWindowFlags(
                Qt.Window | 
                Qt.WindowStaysOnTopHint |
                Qt.CustomizeWindowHint |
                Qt.WindowTitleHint |
                Qt.WindowCloseButtonHint
            )
            # Linux 下不使用透明背景，防止在某些 WM 下出现黑边
            self.setAttribute(Qt.WA_NoSystemBackground, False)

    def _load_style(self):
        """安全加载 Win11 QSS 样式表"""
        qss_path = os.path.join(os.path.dirname(__file__), "assets", "style.qss")
        try:
            with open(qss_path, "r", encoding="utf-8") as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            logger.warning(f"未找到 style.qss: {qss_path}，使用系统默认样式")
        except Exception as e:
            logger.error(f"加载 QSS 失败: {e}")

    def _setup_ui(self):
        """构建 UI 布局并绑定对象名与信号"""
        from PyQt5.QtWidgets import QSpacerItem, QSizePolicy
        
        # === 标题栏 ===
        title_bar = QWidget()
        title_bar.setObjectName("TitleBar")
        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(0, 0, 0, 0)
        
        title_label = QLabel(f"{self.process_name} 已停止工作")
        title_label.setObjectName("TitleLabel")
        title_layout.addWidget(title_label)
        title_layout.addStretch()

        # === 内容卡片 ===
        content_area = QWidget()
        content_area.setObjectName("ContentArea")
        content_layout = QHBoxLayout(content_area)
        
        # 图标占位 (实际使用时可替换为真实 .ico/.png)
        icon_label = QLabel()
        icon_label.setObjectName("IconLabel")
        # 尝试加载资源图标，失败则留空
        icon_path = os.path.join(os.path.dirname(__file__), "assets", "icon.png")
        if os.path.exists(icon_path):
            icon_label.setPixmap(QPixmap(icon_path).scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        
        # 文本区域
        text_layout = QVBoxLayout()
        msg_label = QLabel(f"程序 [{self.process_name}] (PID: {self.pid}) 遇到了未知错误并已终止。")
        msg_label.setObjectName("MessageLabel")
        
        detail_label = QLabel("您可以选择关闭此对话框，或查看技术详情以获取调试信息。")
        detail_label.setObjectName("DetailLabel")
        
        text_layout.addWidget(msg_label)
        text_layout.addWidget(detail_label)
        text_layout.addStretch()
        
        content_layout.addWidget(icon_label)
        content_layout.addLayout(text_layout)

        # === 按钮区域 ===
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        close_btn = QPushButton("关闭程序")
        close_btn.setObjectName("PrimaryButton")
        close_btn.clicked.connect(self.accept)  # 信号连接：点击关闭
        
        report_btn = QPushButton("查看详细信息")
        report_btn.clicked.connect(self._on_report_clicked)  # 信号连接：查看详情
        
        btn_layout.addWidget(report_btn)
        btn_layout.addWidget(close_btn)

        # === 主布局组装 ===
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 12)
        main_layout.addWidget(title_bar)
        main_layout.addWidget(content_area)
        main_layout.addLayout(btn_layout)

    def _center_window(self):
        """将窗口居中到屏幕中央"""
        from PyQt5.QtWidgets import QDesktopWidget
        screen = QDesktopWidget().availableGeometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

    def accept(self):
        """关闭弹窗"""
        self.close()

    def _on_report_clicked(self):
        """查看详情按钮槽函数"""
        logger.info(f"用户请求查看 PID {self.pid} ({self.process_name}) 的详细崩溃信息")
        # TODO: 在此处展开详情面板或打开日志文件
        # 当前仅作占位，不阻塞主交互