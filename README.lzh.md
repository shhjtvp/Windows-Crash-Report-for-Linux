# 視窗崩潰報章擬器（Linux用）

補Linux不能傳誤報於微軟之闕也。

**[README:English](README.en.md)** | 
**[README:简体中文](README.md)** | 
**[README:文言](README.lzh.md)** | 
**[README:Русский язык](README.ru.md)** |
**[README:Shakespearean English](README.sp_en.md)** |
**[README:佛曰](README.zh_bu.md)**


## 戒辭

-   吾於Linux之道，未甚精熟。
-   此作乃「屎技」之屬（戲稱不經之技也），實為人工智能所造。
-   **慎勿用於生產之境，或關乎機要之器。**



## 特點

-   **毫釐畢肖：** 以Qt築之，舉凡Win11圓角、陰影、字體、互動動畫，皆纖悉無遺。
-   **跨域通行：** 無論視窗、Linux（X11/Wayland），窗幟樣式，皆能自適。
-   **擬監進程：** 可設守護於後臺，若所指進程既終，則彈窗自發。
-   **安穩防愚：** 凡彈窗必綴「[模擬]」水印，使人毋誤以為真災也。

## 入門

### 安裝

```bash
pip install Windows-Crash-Report-for-Linux
```

### 初啟

```bash
crash-simulator
```

初啟之時，終端必示安全之誡，須手書 `YES` 以證其意。
蓋欲使君明此作娛戲之本，及其潛患也。若非互動之境，則拒而不啟。

### 常用令

```bash
# 即刻觸發模擬錯誤之窗
crash-simulator pop

# 啟後臺監護模式（監視指定PID）
crash-simulator monitor --pid 12345

# 啟閉開機自啟
crash-simulator autostart --enable
crash-simulator autostart --disable

# 一鍵盡除配置及殘檔
crash-simulator cleanup --yes
```

## 開發

```bash
# 克隆倉庫（名長亦在計中）
git clone https://github.com/shhjtvp/Windows-Crash-Report-for-Linux.git
cd crash-simulator

# 建虛境並裝開發依賴
python -m venv .venv && source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate                            # Windows

pip install -e ".[dev]"

# 本地運行
python -m crash_simulator
```

## 結構

```text
crash_simulator/
├── gui_app.py
├── monitor.py
├── setup_utils.py
└── __main__.py
```