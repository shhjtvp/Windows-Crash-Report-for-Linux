# Windows Crash Report for Linux
修复了Linux不能向微软发送错误报告的bug

[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![Platform: Linux](https://img.shields.io/badge/platform-Linux-lightgrey.svg)]()

---

## 警告

**我不熟悉Linux开发环境，可能会出现意想不到的bug（doge）
**仅供技术演示和娱乐用途**

- 使用本脚本产生的任何后果由使用者自行承担
- **不建议在生产环境或重要工作机器上运行**
- 作者不对因使用本工具造成的任何数据丢失或心理惊吓负责（真的会有人被吓到吗） 


## 简介

Crash Simulator 是一个运行在 Linux 桌面环境下的 Python 程序，它会：

1. **监控** 当前用户启动的进程，检测它们何时退出
2. 当检测到进程退出时，**弹出一个 Windows 风格的「Microsoft Windows 错误报告」窗口**
3. 用户点击「发送」后，会模拟发送错误报告的过程（实际只执行一次 `ping microsoft.com`）
4. 完美复刻 Windows 用户的「崩溃体验」，适合在朋友面前整活



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

如果不想用 sudo，可以添加 `--user` 参数安装到当前用户目录：
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
同样，可以加 --user 参数

### 验证安装
```bash
which crash-sim
```
如果能找到命令路径，则安装成功

## 首次配置
**重要！** 安装完成后，必须运行配置命令，以确认你已阅读警告并选择是否开机自启动：
```bash
crash-sim-setup
```
运行后你应该会看到：
```text
============================================================
  警告：此脚本仅供技术演示和娱乐用途喵~
  使用本脚本产生的任何后果由使用者自行承担nya~
  不要在物理机上运行本脚本！
============================================================
```
- 输入 `y` 或 `yes`：启用开机自启动（仅当前用户）
- 输入 `n` 或 `no` 或直接回车：不启用自启动，只确认警告

## 食用方法
### 启动监控

```bash
crash-sim
```
程序启动后，会在后台监控当前用户的所有进程。当你关闭任何应用程序（如 Firefox、Chrome、终端等）时，会立即弹出一个仿 Windows 错误报告窗口。

### 关闭
直接按 `Ctrl + C` 即可退出监控程序,或关闭终端窗口也会终止程序。

### *自启动*
如果安装时启用了开机自启动，每次登录桌面后 crash-sim 会自动在后台运行。你可以通过系统监视器查看名为 `crash-sim` 的进程，也可以随时在终端中 `killall crash-sim` 手动停止它

---

## 卸载
### 1.清理自启动项
```bash
crash-sim-setup --uninstall
```
这条命令会删除 ~/.config/autostart/crash-sim.desktop 文件（如果存在）
### 2.卸载程序 Python 包
```bash
pip uninstall crash-simulator
```
如果当初安装时用了 ``--user``，卸载时也要加上：
```bash
pip uninstall crash-simulator --user
```

### *完全清理*
如果你想彻底移除所有相关文件，可以额外删除以下目录（如果有）：
```bash
rm -rf ~/.cache/crash-sim          # 缓存目录
rm -rf ~/.config/crash-sim         # 配置文件目录
```

---

## 不同桌面环境的适配说明

本工具默认使用 ~/.config/autostart/ 目录来实现开机自启动（[freedesktop.org] 标准），大多数主流 Linux 桌面环境支持
