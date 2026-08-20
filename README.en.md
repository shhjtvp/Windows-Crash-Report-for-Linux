# Windows' Crash Report for Linux (cCrash Simulator)

Fixes the bug where Linux cannot send error reports to Microsoft.

**[README:English](README.en.md)** | 
**[README:简体中文](README.md)** | 
**[README:文言](README.lzh.md)** | 
**[README:Русский язык](README.ru.md)** |
**[README:Shakespearean English](README.sp_en.md)** |
**[README:佛曰](README.zh_bu.md)**


## Disclaimer

-   I am not very familiar with Linux.
-   This project falls under the category of "Shi Tech" (a humorous term for questionable tech projects) and is an AI-generated project.
-   **Do not run this in production environments or on critical work devices.**



## Features

-   **Pixel-Perfect Replica:** Built with Qt, accurately replicating Win11-style rounded corners, shadows, fonts, and interaction animations.
-   **Cross-Platform Support:** Automatically adapts window flags and styles on Windows / Linux (X11/Wayland).
-   **Process Monitoring Simulation:** Optional background daemon mode that automatically triggers the popup when a specified process exits.
-   **Safety & Foolproof Design:** All popups include a `[Simulation]` watermark to prevent them from being mistaken for real system failures.

## Getting Started

### Installation

```bash
pip install Windows-Crash-Report-for-Linux
```

### First Run

```bash
crash-simulator
```

On first run, the program will display a safety warning in the terminal and require manual input of `YES` to confirm.
This ensures you understand the entertainment nature and potential impact of this project. It will refuse to start in non-interactive environments.

### Common Commands

```bash
# Immediately trigger a simulated error window
crash-simulator pop

# Start background monitoring mode (monitor a specific PID)
crash-simulator monitor --pid 12345

# Enable/Disable startup entry
crash-simulator autostart --enable
crash-simulator autostart --disable

# One-click cleanup of all configs and residual files
crash-simulator cleanup --yes
```

## Development

```bash
# Clone the repository (the long name is part of the plan)
git clone https://github.com/shhjtvp/Windows-Crash-Report-for-Linux.git
cd crash-simulator

# Create a virtual environment and install dev dependencies
python -m venv .venv && source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate                            # Windows

pip install -e ".[dev]"

# Run locally
python -m crash_simulator
```

## Structure

```text
crash_simulator/
├── gui_app.py
├── monitor.py
├── setup_utils.py
└── __main__.py
```