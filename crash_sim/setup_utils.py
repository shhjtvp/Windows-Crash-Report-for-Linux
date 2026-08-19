import json
import os
import logging

CONFIG_PATH = os.path.expanduser("~/.config/crash_sim/config.json")
logger = logging.getLogger(__name__)


def interactive_setup():
    """交互式配置向导，带完整异常防护"""
    print("=== Crash Sim Setup ===")
    config = {}

    try:
        # 安全读取已有配置
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                config = json.load(f)
            print(f"Loaded existing config from {CONFIG_PATH}")
    except (json.JSONDecodeError, OSError) as e:
        logger.warning(f"Could not load existing config: {e}. Starting fresh.")
        config = {}

    # 带验证的用户输入
    while True:
        raw = input(f"Blacklisted processes (comma-separated, current: {config.get('blacklist', [])}): ").strip()
        if raw:
            config["blacklist"] = [p.strip() for p in raw.split(",") if p.strip()]
        else:
            config.setdefault("blacklist", [])
        break  # 简化示例，实际可加格式校验

    # 安全写入配置
    try:
        os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        print(f"✅ Config saved to {CONFIG_PATH}")
    except OSError as e:
        print(f"❌ Failed to save config: {e}", file=sys.stderr)
        return 1

    return 0