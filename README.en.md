# Windows Crash Report for Linux  
*Fixed the bug where Linux couldn't send error reports to Microsoft*  

[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)  
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)  
[![Platform: Linux](https://img.shields.io/badge/platform-Linux-lightgrey.svg)]()

**[README: English](README.en.md)** | 
**[README: 简体中文](README.md)** | 
**[README: 文言](README.lzh.md)** | 
**[README: Русский язык](README.ru.md)**

---

## ⚠️ Warning

**I'm not familiar with the Linux development environment, so expect unexpected bugs (doge).**  
**For technical demonstration and entertainment purposes only.**

- Use this script at your own risk.  
- **Not recommended for production environments or critical work machines.**  
- The author is not responsible for any data loss or psychological fright caused by this tool (will anyone actually get scared?).

---

## Introduction

a Python program that runs on Linux desktop environments. It does the following:

1. **Monitors** processes started by the current user and detects when they exit.  
2. When a process exits, it **pops up a Windows‑style “Microsoft Windows Error Reporting” window**.  
3. When the user clicks **“Send”**, it simulates sending an error report (actually just runs `ping microsoft.com` once).  
4. Perfectly recreates the Windows “crash experience” — great for trolling your friends.

---

## How to Install

### Dependencies

- Python 3.6 or higher  
- pip (Python package manager)  
- A desktop environment (GNOME / KDE / XFCE, etc., with support for `~/.config/autostart`)

### Online Installation

Install the latest version directly from GitHub:
```bash
pip install git+https://github.com/shhjtvp/Windows-Crash-Report-for-Linux.git
```

If you prefer not to use `sudo`, add the `--user` flag to install for the current user only:
```bash
pip install --user git+https://github.com/shhjtvp/Windows-Crash-Report-for-Linux.git
```

After installation, you get two command‑line tools:  
- `crash-sim` – starts the main program  
- `crash-sim-setup` – configuration wizard (shows warnings, sets up autostart)

### Local Installation

If you have cloned the source repository:
```bash
git clone https://github.com/shhjtvp/Windows-Crash-Report-for-Linux.git
cd Windows-Crash-Report-for-Linux
pip install .
```
Again, you can add `--user` if needed.

### Verify Installation
```bash
which crash-sim
```
If the command path is shown, installation succeeded.

---

## First‑Time Setup

**Important!** After installation, you must run the configuration command to confirm that you have read the warning and choose whether to enable autostart:
```bash
crash-sim-setup
```
You should see:
```text
============================================================
  WARNING: This script is for technical demonstration
  and entertainment purposes only, nya~
  Use at your own risk, meow~
  Do NOT run this on physical hardware!
============================================================
```
- Type `y` or `yes` → enable autostart (for the current user only)  
- Type `n` or `no`, or just press Enter → do not enable autostart, only confirm the warning

---

## How to Use

### Start Monitoring
```bash
crash-sim
```
Once started, the program monitors all processes of the current user in the background. Whenever you close any application (e.g., Firefox, Chrome, terminal, etc.), a fake Windows error reporting window will pop up immediately.

### Stop Monitoring
Press `Ctrl + C` to exit the monitoring program, or simply close the terminal window.

### Autostart
If you enabled autostart during setup, `crash-sim` will run automatically in the background every time you log into your desktop. You can see the `crash-sim` process in your system monitor, or manually stop it at any time with:
```bash
killall crash-sim
```

---

## Uninstallation

### 1. Remove Autostart Entry
```bash
crash-sim-setup --uninstall
```
This deletes the `~/.config/autostart/crash-sim.desktop` file (if it exists).

### 2. Uninstall the Python Package
```bash
pip uninstall crash-simulator
```
If you installed with `--user`, add that flag as well:
```bash
pip uninstall crash-simulator --user
```

### Complete Cleanup
To remove all related files, you may also delete these directories (if they exist):
```bash
rm -rf ~/.cache/crash-sim          # cache directory
rm -rf ~/.config/crash-sim         # config directory
```

> 💡 Tip: Use `pip show crash-simulator` to see where the package is installed.

---

## Desktop Environment Compatibility

*So that every Linux user can enjoy this piece of 💩*

By default, we use the `~/.config/autostart/` directory (freedesktop.org standard) for autostart, which is supported by most mainstream Linux desktop environments.

### Supported Desktop Environments

| Desktop Environment | Autostart Support | Notes |
|---------------------|-------------------|-------|
| **GNOME** (3.x/40+) | ✅ Full | Uses standard `autostart` directory |
| **KDE Plasma**      | ✅ Full | Same |
| **XFCE**            | ✅ Full | Same |
| **Cinnamon**        | ✅ Full | Same |
| **MATE**            | ✅ Full | Same |
| **LXDE / LXQt**     | ✅ Full | Same |
| **i3 / Sway / Awesome** (WM) | ⚠️ Limited | Manual config required, see below |
| **Deepin / Unity**  | ✅ Full | Same |

### Tiling Window Managers (i3 / Sway / Awesome, etc.)
If you use a pure window manager (not a full desktop environment), `.desktop` files in `~/.config/autostart` **will not be executed automatically**. You need to add the launch command to your window manager's configuration file manually.

**Example (i3):** Edit `~/.config/i3/config` and add:
```
exec --no-startup-id crash-sim
```

**Example (Sway):** Edit `~/.config/sway/config` and add:
```
exec crash-sim
```

**Example (Awesome WM):** Edit `~/.config/awesome/rc.lua` and add:
```lua
awful.spawn.with_shell("crash-sim")
```

### Manual Autostart Management (Universal)
If you prefer full manual control:
1. Run `crash-sim-setup` and choose **not** to enable autostart.  
2. Start it manually whenever you want with `crash-sim &` to run it in the background.  
3. You could also add `crash-sim` to your shell config (e.g., `~/.bashrc`), but this is **not recommended** because it will start a new monitor process for every terminal you open, wasting resources.

---

## Frequently Asked Questions

> **Q: How do I temporarily disable monitoring?**  
> **A:** Press `Ctrl + C` to terminate the program. If you want to pause monitoring without restarting, you can kill the Python process, or add a `pause()` method to `ProcessMonitor` (not built into the current version).

> **Q: Autostart doesn't work?**  
> **A:** Please check:  
> 1. Confirm that `~/.config/autostart/crash-sim.desktop` exists and contains the correct content.  
> 2. Make sure the file has execute permission (usually not required, but you can `chmod +x` just in case).  
> 3. Verify that your desktop environment supports the `autostart` standard (see table above).  
> 4. Try restarting your desktop session (or logging out and back in) – some environments only scan the autostart directory at login.  
> 5. Run `crash-sim` manually to ensure the command itself works.

> **Q: The autostart entry remains after uninstallation?**  
> **A:** Make sure to run `crash-sim-setup --uninstall` **before** uninstalling the package. If you already removed the package, delete the autostart file manually:
> ```bash
> rm -f ~/.config/autostart/crash-sim.desktop
> ```

> **Q: Does it work under Wayland?**  
> **A:** Yes, the program itself does not depend on X11. However, note that the `ping` command may require `CAP_NET_RAW` capability or the setuid bit. If `ping` fails, the program will report “send failed”, but the popup window will still work fine.

---

## Contributing (Contribute Nothing??? )

Issues and pull requests are welcome!
