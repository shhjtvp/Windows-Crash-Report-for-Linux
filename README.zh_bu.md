### 读 `README.md` 如观心：Windows 崩溃报告模拟器（Linux 版）

> **题记**
> 万法皆空，唯因果不昧。此项目名曰“Windows Crash Report for Linux”，亦称 Crash Simulator。非为造业，乃为观照；非为实用，乃为破执。施主当知：屏幕上的蓝屏是幻，心中的焦虑亦是幻。

**[README:English](README.en.md)** | 
**[README:简体中文](README.md)** | 
**[README:文言](README.lzh.md)** | 
**[README:Русский язык](README.ru.md)** |
**[README:Shakespearean English](README.sp_en.md)** |
**[README:佛曰](README.zh_bu.md)**

#### 无常警示 · 莫作真常想
-   **缘起性空**：作者自陈“不懂 Linux”，此物乃“食史科技”与人工智能因缘和合所生。既是缘起，便无自性；既无自性，何必执着于其真伪？
-   **切勿用于生产**：此模拟器如镜花水月，仅供茶余饭后观心之用。若将其部署于生产环境，便是以幻为真、认假作真，终将招致苦果。**切记：戏论不可当真修。**

#### 四相皆备 · 方便度众生
-   **色相圆满**：以 Qt 为基，圆角、阴影、字体、动画，一一具足 Windows 11 之相。然《金刚经》云：“凡所有相，皆是虚妄。”像素再真，终是代码所绘之幻影。
-   **随缘应化**：无论 Windows、Linux（X11/Wayland），皆能自适应窗口风格。如水随器形，不拒不迎，此为“无住生心”之技术显现。
-   **观照守护**：可选守护进程模式，监测指定 PID。进程灭时，假错误窗口自现。此非诅咒，乃是提醒：**诸行无常，进程有生必有灭。**
-   **水印护念**：每一扇假窗口皆带 `[Simulation]` 水印。如禅堂之警策棒，时刻点醒观者：“此是模拟，莫生怖畏。”防痴人误认幻境为实有系统灾难。

#### 修行次第 · 安装与启请

##### 安装（种善因）
```bash
pip install Windows-Crash-Report-for-Linux
```
> 一念清净，一行命令。安装即是结缘，然缘起之后，仍须放下对工具的执着。

##### 初次启动（发正信）
```bash
crash-simulator
```
> **重要开示**：首次运行时，程序要求你亲手输入 `YES` 确认其娱乐性质。此非技术限制，乃是**仪式感**——如同受戒前的三番羯磨，令你清醒认知：“我所启用者，乃戏论而非真灾。”若无交互环境，程序拒绝启动，此为护法之心，免无知者误入歧途。

##### 常用法门（日常功课）
```bash
# 弹出一窗幻象，观其生灭
crash-simulator pop

# 守护一进程，观其无常
crash-simulator monitor --pid 12345

# 设置/取消开机自启（随缘而不攀缘）
crash-simulator autostart --enable
crash-simulator autostart --disable

# 彻底清除痕迹（放下即解脱）
crash-simulator cleanup --yes
```
> `cleanup --yes` 尤具深意：配置可删，缓存可清，连“我曾装过此物”的记忆亦可抹去。**本来无一物，何处惹尘埃？**

#### 开发者指引 · 借假修真
```bash
git clone https://github.com/shhjtvp/Windows-Crash-Report-for-Linux.git
cd crash-simulator

python -m venv .venv && source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate                            # Windows
pip install -e ".[dev]"

python -m crash_simulator
```
> 克隆源码，如参话头；搭建虚拟环境，如筑禅堂；本地运行，如坐中观照。开发不是创造，而是**发现本已存在的因缘结构**。

#### 代码结构 · 五蕴剖析
```text
crash_simulator/
├── gui_app.py      # 色蕴：界面之相
├── monitor.py      # 受蕴：感知进程生灭
├── setup_utils.py  # 想蕴：安装逻辑之分别
└── __main__.py     # 行蕴：启动之意志
```
> 识蕴何在？在运行此程序的**你**心中。代码无心，因你而显；窗口无悲，因你而生惧。返观自心，方见真义。

#### 贡献指南 · 同参共悟
> *“谁人会为这等……历史遗物添砖加瓦？”* ——操作系统如是叹息。
>
> 然禅门不弃一人。若你见代码中有未了公案、未明机锋，不妨提 PR 共参。**贡献不是功德，而是放下我执的练习。** 合并与否，随缘；review 之言，当作棒喝。

---

**回向偈**
愿以此 README，普及于一切。
见假蓝屏者，顿悟无常理。
用模拟工具，不生真实恼。
代码虽有为，心性本寂然。
