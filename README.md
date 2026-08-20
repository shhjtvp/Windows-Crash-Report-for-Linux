# Windows' Crash Report for Linux (cCrash Simulator)

解决了Linux不能向微软发送错误报告的bug

**(English)[README.en.md]** | 
**(简体中文)[README.md]** | 
**(文言)[README.lzh.md]** | 
**(Русский язык)[README.ru.md]**

> **声明**
> 我不太熟悉Linux
> 本项目属于“赤石科技”范畴，是个AI项目
> **请勿在生产环境或重要工作设备上运行**。

<p align="center">
  <img src="assets/demo-preview.png" alt="Crash Simulator Demo" width="600">
  <br>
  <em>以假乱真的 WER 弹窗</em>
</p>

## 特性

-   **像素级还原**：基于 Qt 实现，精确复刻 Win11 风格的圆角、阴影、字体与交互动效
-   **跨平台支持**：在 Windows / Linux (X11/Wayland) 下自动适配窗口标志与样式
-   **进程监控模拟**：可选的后台守护模式，当指定进程退出时自动触发弹窗
-   **安全防呆设计**：所有弹窗均带有 `[模拟]` 水印标识，避免误认为真实系统故障

## 开始

### 安装

```bash
pip install Windows-Crash-Report-for-Linux
```

### 首次运行

```bash
crash-simulator
```

> 首次运行时，程序会在终端显示安全警告并要求手动输入 `YES` 确认。
> 这是为了确保您已了解本项目的娱乐性质及潜在影响。非交互式环境下将拒绝启动

### 常用命令

```bash
# 立即弹出一次模拟错误窗口
crash-simulator pop

# 启动后台监控模式（监控指定 PID）
crash-simulator monitor --pid 12345

# 生成/移除开机自启动项
crash-simulator autostart --enable
crash-simulator autostart --disable

# 一键清理所有配置与残留文件
crash-simulator cleanup --yes
```

### 开发

```bash
# 克隆仓库(名字长也是计划的一部分)
git clone https://github.com/shhjtvp/Windows-Crash-Report-for-Linux.git
cd crash-simulator

# 创建虚拟环境并安装开发依赖
python -m venv .venv && source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate                            # Windows
pip install -e ".[dev]"

# 本地运行
python -m crash_simulator
```

### 结构

```text
crash_simulator/
├── gui_app.py
├── monitor.py
├── setup_utils.py
└── __main__.py
```

## 贡献
os：真的会有人为史做些什么吗