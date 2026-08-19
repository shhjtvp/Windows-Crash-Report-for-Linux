# Windows 崩溃报告·Linux 版  
正 Linux 不能向微软传错误报告之 bug  

[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)  
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)  
[![Platform: Linux](https://img.shields.io/badge/platform-Linux-lightgrey.svg)]()

(English)[README.en.md] | (简体中文 中国)[README.md] | **文言 华夏**

---

## ⚠️ 警

**余不习 Linux 开发之境，故或有意外之 bug（dog）。**  
**此物惟供戏玩与技术演示，慎之。**

- 用此脚本者，自担其责。  
- **勿用于生产机器或要务之机。**  
- 若因之失数据、受惊骇（岂真有人骇耶？），作者不任咎。

---

## 叙

**Crash Simulator** 者，行于 Linux 桌面之 Python 程序也。其能：

1. **监** 当前用户所启之进程，察其何时退出。  
2. 见进程退，则 **弹出** Windows 风格之“Microsoft Windows 错误报告”窗。  
3. 用户点“发送”，则仿发送误报之状（实则惟行 `ping microsoft.com` 一次）。  
4. 尽复 Windows 用户“崩溃之体验”，宜于友前弄巧。

---

## 如何安装

### 依赖

- Python 3.6 或更高  
- pip（Python 包管理器）  
- 桌面环境（GNOME / KDE / XFCE 等，须支持 `~/.config/autostart`）

### 在线安装

直从 GitHub 装最新版：
```bash
pip install git+https://github.com/shhjtvp/Windows-Crash-Report-for-Linux.git
```
若不欲用 sudo，可加 `--user` 以装于当前用户：
```bash
pip install --user git+https://github.com/shhjtvp/Windows-Crash-Report-for-Linux.git
```
装毕，得二命令行工具：  
- `crash-sim` —— 启主程序  
- `crash-sim-setup` —— 配置向导（示警、设自启）

### 本地安装

若已克隆源码：
```bash
git clone https://github.com/shhjtvp/Windows-Crash-Report-for-Linux.git
cd Windows-Crash-Report-for-Linux
pip install .
```
亦可加 `--user`。

### 验装
```bash
which crash-sim
```
若见路径，则装成。

---

## 初次配置

**要哉！** 装毕，必行配置令，以证汝已读警，并择是否自启：
```bash
crash-sim-setup
```
当见：
```text
============================================================
  警：此脚本惟供戏玩与技术演示，喵~
  用者自担其责，nya~
  勿于物理机行此脚本！
============================================================
```
- 输 `y` 或 `yes`：启自启（仅当前用户）  
- 输 `n` 或 `no` 或直按回车：不启自启，惟确认警言

---

## 食用之法

### 启监
```bash
crash-sim
```
启后，后台监当前用户诸进程。凡闭应用（如 Firefox、Chrome、终端等），即弹仿 Windows 误报窗。

### 停之
直按 `Ctrl + C` 可退监程序，或闭终端窗亦止。

### *自启*
若安装时启自启，则每登桌面，crash-sim 自于后台行。可于系统监视器见 `crash-sim` 进程，亦可随时 `killall crash-sim` 手止。

---

## 卸载

### 1. 清自启项
```bash
crash-sim-setup --uninstall
```
此令删 `~/.config/autostart/crash-sim.desktop`（若存）。

### 2. 卸 Python 包
```bash
pip uninstall crash-simulator
```
若初装用 `--user`，卸时亦加：
```bash
pip uninstall crash-simulator --user
```

### *尽清*
欲尽去相关文件，可并删以下目录（若有）：
```bash
rm -rf ~/.cache/crash-sim          # 缓存目录
rm -rf ~/.config/crash-sim         # 配置目录
```

> 💡 提示：用 `pip show crash-simulator` 可见包之所在。

---

## 诸桌面环境适配

*欲使诸 Linux 用户皆得尝此💩也*

默认用 `~/.config/autostart/` 目录（freedesktop.org 标准）以实自启，主流 Linux 桌面多支持。

### 所支持之桌面

| 桌面环境 | 自启支持 | 注 |
|---------|---------|---|
| **GNOME** (3.x/40+) | ✅ 全 | 用标准 `autostart` 目录 |
| **KDE Plasma** | ✅ 全 | 同上 |
| **XFCE** | ✅ 全 | 同上 |
| **Cinnamon** | ✅ 全 | 同上 |
| **MATE** | ✅ 全 | 同上 |
| **LXDE / LXQt** | ✅ 全 | 同上 |
| **i3 / Sway / Awesome** (WM) | ⚠️ 有限 | 须手动配置，见下 |
| **Deepin / Unity** | ✅ 全 | 同上 |

### 平铺窗口管理器（i3 / Sway / Awesome 等）

若用纯窗口管理器（非完整桌面），则 `~/.config/autostart` 下 `.desktop` 文件 **不会自动执行**。须手动将启令加入窗口管理器之配置文件。

**例（i3）：** 编辑 `~/.config/i3/config`，加：
```
exec --no-startup-id crash-sim
```

**例（Sway）：** 编辑 `~/.config/sway/config`，加：
```
exec crash-sim
```

**例（Awesome WM）：** 编辑 `~/.config/awesome/rc.lua`，加：
```lua
awful.spawn.with_shell("crash-sim")
```

### 手动自启（通用）

若欲于任何环境下手动控制，可：
1. 行 `crash-sim-setup` 时择 **不启** 自启。  
2. 欲启时，手行 `crash-sim &` 置于后台。  
3. 亦可加至 shell 配置文件（如 `~/.bashrc`），然不荐，盖每开终端辄启一监进程，徒费资源。

---

## 常问

> **问：如何暂止监控？**  
> **答：** 按 `Ctrl + C` 止之。若欲不重启而暂止，可杀 Python 进程，或自加 `pause()` 法于 `ProcessMonitor`（今版未内置）。

> **问：自启无效？**  
> **答：** 请检：  
> 1. `~/.config/autostart/crash-sim.desktop` 存在且内容正。  
> 2. 文件有执行权（通常不需，然可 `chmod +x` 试之）。  
> 3. 桌面环境支持 `autostart` 标准（见上表）。  
> 4. 重启桌面会话（或重登录），盖有环境惟登录时扫 autostart 一次。  
> 5. 手行 `crash-sim` 以验令自身可正常。

> **问：卸后自启项仍在？**  
> **答：** 务必先 `crash-sim-setup --uninstall` 再卸包。若已卸包，可手删自启文件：
> ```bash
> rm -f ~/.config/autostart/crash-sim.desktop
> ```

> **问：Wayland 下可用否？**  
> **答：** 可，程序本身不赖 X11。然 `ping` 令之权限须留意：Wayland 下网络权与 X11 无异，`ping` 通常需 `CAP_NET_RAW` 能力或 setuid 位。若 `ping` 不行，程序报“发送失败”，然弹窗无碍。

---

## 贡献（献一滚木？😸）

欢迎提 Issue 与 PR。