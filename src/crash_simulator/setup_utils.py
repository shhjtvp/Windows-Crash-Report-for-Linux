import os
import json
import logging
import argparse
import tempfile
from pathlib import Path
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

# --- XDG 路径规范 ---
def get_xdg_config_home() -> Path:
    return Path(os.getenv("XDG_CONFIG_HOME", Path.home() / ".config"))

def get_xdg_state_home() -> Path:
    # 较新的 XDG 规范使用 ~/.local/state，旧版可能没有，这里做兼容
    return Path(os.getenv("XDG_STATE_HOME", Path.home() / ".local" / "state"))

CONFIG_DIR = get_xdg_config_home() / "crash_sim"
CONFIG_FILE = CONFIG_DIR / "config.json"

STATE_DIR = get_xdg_state_home() / "crash_sim"
STATE_FILE = STATE_DIR / "state.json"

AUTOSTART_DIR = get_xdg_config_home() / "autostart"
DESKTOP_FILE = AUTOSTART_DIR / "crash-sim.desktop"

DEFAULT_CONFIG = {
    "blacklist": ["systemd", "kworker", "bash", "sh", "zsh", "fish"],
    "poll_interval": 1.5
}

# --- 配置与状态管理 ---

def _ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)

def _validate_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """轻量级 Schema 校验，修复用户手动编辑导致的格式错误"""
    valid_config = DEFAULT_CONFIG.copy()
    
    if "blacklist" in config and isinstance(config["blacklist"], list):
        valid_config["blacklist"] = [str(x).lower() for x in config["blacklist"]]
        
    if "poll_interval" in config and isinstance(config["poll_interval"], (int, float)):
        valid_config["poll_interval"] = max(0.1, float(config["poll_interval"]))
        
    return valid_config

def load_config() -> Dict[str, Any]:
    if not CONFIG_FILE.exists():
        return DEFAULT_CONFIG.copy()
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return _validate_config(data)
    except (json.JSONDecodeError, IOError) as e:
        logger.warning(f"配置文件损坏，使用默认配置: {e}")
        return DEFAULT_CONFIG.copy()

def save_config(config: Dict[str, Any]):
    """原子写入配置，防止写入中断导致文件损坏"""
    _ensure_dir(CONFIG_DIR)
    validated = _validate_config(config)
    
    # 写入临时文件后重命名，保证原子性
    fd, tmp_path = tempfile.mkstemp(dir=CONFIG_DIR, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(validated, f, indent=4)
        os.replace(tmp_path, CONFIG_FILE)
    except Exception:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
        raise

def load_state() -> Dict[str, Any]:
    if not STATE_FILE.exists():
        return {}
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}

def save_state(state: Dict[str, Any]):
    _ensure_dir(STATE_DIR)
    fd, tmp_path = tempfile.mkstemp(dir=STATE_DIR, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=4)
        os.replace(tmp_path, STATE_FILE)
    except Exception:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
        raise

# --- 开机自启动管理 ---

def enable_autostart():
    _ensure_dir(AUTOSTART_DIR)
    desktop_content = f"""[Desktop Entry]
Type=Application
Name=Crash Simulator
Exec=crash-sim monitor
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
Comment=Simulates Windows crash reports for dead processes
"""
    with open(DESKTOP_FILE, "w", encoding="utf-8") as f:
        f.write(desktop_content)
    print(f"✅ 开机自启已启用: {DESKTOP_FILE}")

def disable_autostart():
    if DESKTOP_FILE.exists():
        DESKTOP_FILE.unlink()
        print(f"开机自启已卸载: {DESKTOP_FILE}")
    else:
        print("未找到自启动配置，无需卸载。")

# --- CLI 入口 (用于 crash-sim-setup) ---

def setup_main():
    parser = argparse.ArgumentParser(prog="crash-sim-setup", description="管理 Crash Simulator 配置与自启动")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--enable-autostart", action="store_true", help="启用开机自启动")
    group.add_argument("--disable-autostart", action="store_true", help="禁用开机自启动")
    group.add_argument("--show-config", action="store_true", help="显示当前配置")
    group.add_argument("--reset-config", action="store_true", help="重置为默认配置")
    
    args = parser.parse_args()
    
    if args.enable_autostart:
        enable_autostart()
    elif args.disable_autostart:
        disable_autostart()
    elif args.show_config:
        print(json.dumps(load_config(), indent=4))
    elif args.reset_config:
        save_config(DEFAULT_CONFIG)
        print("✅ 配置已重置为默认值。")

if __name__ == "__main__":
    setup_main()