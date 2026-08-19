# Windows Crash Report for Linux
Fixed the issue where crash reports could not be sent to Microsoft on Linux.  =)


---
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![Platform: Linux](https://img.shields.io/badge/platform-Linux-lightgrey.svg)]()

---

## 警告

<span style="color: #ff0000">我不熟悉Linux开发环境，可能会出现意想不到的bug</span>

**本工具仅供技术演示和娱乐用途！**

- 使用本脚本产生的任何后果由使用者自行承担
- 本工具会监控当前用户的进程退出事件并弹窗
- **不建议在生产环境或重要工作机器上运行**
- 作者不对因使用本工具造成的任何数据丢失或心理惊吓负责（真的会有人被吓到吗） 

---

## 简介

Crash Simulator 是一个运行在 Linux 桌面环境下的 Python 程序，它会：

1. **监控** 当前用户启动的进程，检测它们何时退出
2. 当检测到进程退出时，**弹出一个 Windows 风格的「Microsoft Windows 错误报告」窗口**
3. 用户点击「发送」后，会模拟发送错误报告的过程（实际只执行一次 `ping microsoft.com`）
4. 完美复刻 Windows 用户的「崩溃体验」，适合在朋友面前整活

---

## 如何安装？

### 依赖

- Python 3.6 或更高版本
- pip（Python 包管理器）
- 桌面环境（GNOME / KDE / XFCE 等，支持 `~/.config/autostart` 即可）

### 在线安装

直接从 GitHub 安装最新版本：
```bash
pip install git+https://github.com/shhjtvp/Windows-Crash-Report-for-Linux.git
```

如果不想用 sudo，可以添加 --user 参数安装到当前用户目录：
```bash
pip install --user git+https://github.com/你的用户名/crash-simulator.git
```

安装完成后，你会获得两个命令行工具：
crash-sim —— 启动主程序
crash-sim-setup —— 配置向导（显示警告、设置开机自启动）

### 本地安装

如果你已经克隆了源码仓库：
```bash
git clone https://github.com/你的用户名/crash-simulator.git
cd crash-simulator
pip install .
```
