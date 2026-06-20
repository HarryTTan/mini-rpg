from fpdf import FPDF

pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_font("cn", "", r"C:\Windows\Fonts\msyh.ttc")
pdf.add_font("cn", "B", r"C:\Windows\Fonts\msyhbd.ttc")

def title_page():
    pdf.add_page()
    pdf.ln(60)
    pdf.set_font("cn", "B", 28)
    pdf.cell(0, 15, "Mini RPG", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(8)
    pdf.set_font("cn", "", 16)
    pdf.cell(0, 10, "2D像素角色扮演游戏", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(6)
    pdf.cell(0, 10, "数据结构与算法课程大作业", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(20)
    pdf.set_font("cn", "", 14)
    pdf.cell(0, 10, "数算B — 2026春季学期", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)
    pdf.cell(0, 10, "GitHub: https://github.com/HarryTTan/mini-rpg", align="C", new_x="LMARGIN", new_y="NEXT")

def section(title):
    pdf.ln(4)
    pdf.set_font("cn", "B", 16)
    pdf.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

def body(text):
    pdf.set_font("cn", "", 10)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(w=pdf.epw, h=6, text=text)

def bullet(text):
    pdf.set_font("cn", "", 10)
    pdf.cell(8)
    pdf.cell(0, 6, "• " + text, new_x="LMARGIN", new_y="NEXT")

# ====== 封面 ======
title_page()

# ====== 项目概述 ======
section("一、项目概述")
body(
    "Mini RPG 是一款基于 Python 和 pygame-ce 开发的2D俯视角像素风角色扮演游戏。"
    "本项目的核心目标是将课程所学的数据结构与算法（N叉树、A*寻路）融入一个完整的游戏系统中，"
    "通过实际应用加深对算法原理和工程设计流程的理解。"
)
body(
    "游戏包含村庄与山洞两张地图，玩家可与NPC进行多分支对话（N叉树结构），"
    "怪物使用A*寻路算法追踪玩家并有完整的攻击状态机。"
)

# ====== 核心算法 ======
section("二、核心算法与数据结构")

pdf.set_font("cn", "B", 13)
pdf.cell(0, 8, "1. 对话系统 — N叉树 (N-ary Tree)", new_x="LMARGIN", new_y="NEXT")
body(
    "文件 src/dialogue.py 从零实现了通用N叉树结构。DialogueNode 为树节点，包含对话文本text、"
    "回应选项列表responses、子节点列表children，is_leaf()判断叶子。"
    "DialogueTree 从JSON文件递归构建完整N叉树，_build_from_dict() 方法深度优先遍历JSON结构，"
    "每个节点可含任意数量子分支。DialogueManager 为树遍历控制器，"
    "遇单子节点自动推进(advance)，遇分支等待玩家选择(select_choice)，至叶子节点结束对话。"
    "时间复杂度：树构建O(n)，每次对话推进O(1)。"
)

pdf.ln(2)
pdf.set_font("cn", "B", 13)
pdf.cell(0, 8, "2. 怪物AI — A*寻路算法", new_x="LMARGIN", new_y="NEXT")
body(
    "文件 src/pathfinding.py 实现了经典A*最短路径搜索算法。评价函数 f(n)=g(n)+h(n)，"
    "其中g为从起点已走步数，h为当前节点到终点的曼哈顿距离。"
    "使用 heapq 最小堆实现优先队列，按f值排序保证每次扩展最优点；"
    "visited 字典（hash table）记录已探索节点及父节点，用于最终路径回溯。"
    "四方向邻域扩展，排除不可走瓦片（墙壁、水域、树木）和动态障碍（其他怪物、NPC位置）。"
    "曼哈顿距离在四方向网格上是可接受的启发函数，保证找到最短路径。"
    "时间复杂度最坏O(b^d)，实际远小于此因为启发函数提供方向性剪枝。"
)
body(
    "怪物行为状态机：待机（超出5格视野）→ 追踪（每30帧A*寻路并移动一步）→ "
    "蓄力（相邻，闪橙色25帧前摇）→ 攻击（造成伤害+进入60帧冷却）→ 循环。"
    "玩家攻击可打断蓄力。"
)

pdf.ln(2)
pdf.set_font("cn", "B", 13)
pdf.cell(0, 8, "3. 背包系统 — 哈希表", new_x="LMARGIN", new_y="NEXT")
body(
    "src/inventory.py 基于 Python defaultdict（哈希表）实现物品管理。O(1) 物品查找与存取，"
    "支持装备类（武器替换逻辑）、消耗类（回血）、突破上限类（提升最大生命值）三种物品类型。"
)

# ====== 系统架构 ======
section("三、系统架构")
body(
    "游戏主循环为60FPS标准循环：事件处理 → 更新（移动/怪物AI/状态检测）→ 渲染（地图/实体/UI）。"
    "实体采用面向对象继承体系：Entity基类（位置、闪光系统）→ "
    "Player（移动、碰撞、战斗）、NPC（对话树）、Monster（AI、蓄力、攻击）。"
    "场景管理通过 current_map / current_npcs / current_monsters 变量动态切换，"
    "踩上特定瓦片(TILE_CAVE=6)触发村庄与山洞之间的地图传送。"
)

body("文件结构：")
bullet("main.py — 游戏主入口与主循环")
bullet("src/constants.py — 全局常量（屏幕/瓦片/颜色/怪物参数）")
bullet("src/entity.py — Entity基类 + Player + NPC + Monster")
bullet("src/map_data.py — 瓦片地形判定 + 地图加载与碰撞检测")
bullet("src/dialogue.py — N叉树对话系统（节点+树+管理器+UI渲染）")
bullet("src/inventory.py — 背包系统（物品+哈希表存储+UI面板）")
bullet("src/pathfinding.py — A*寻路算法（优先队列+曼哈顿启发）")
bullet("assets/maps/ — 两张30x20纯文本地图（村庄+山洞）")
bullet("assets/dialogues/ — NPC对话树JSON数据")

# ====== 操作说明 ======
section("四、操作说明")
body("环境要求：Python 3.10+，唯一外部依赖 pygame-ce>=2.5.0，其余全部使用Python标准库。")
body("运行步骤：pip install -r requirements.txt && python main.py")

bullet("方向键 ↑↓←→ — 网格移动（按住可连续移动）")
bullet("Z键 — 与相邻NPC对话（曼哈顿距离=1）/ 背包内确认使用")
bullet("↑↓ — 对话中选择回应选项 / 背包中选择物品")
bullet("I键 — 开关背包面板")
bullet("空格键 — 攻击相邻怪物")
bullet("ESC键 — 退出游戏")

# ====== 游戏截图 ======
section("五、游戏截图")
body("【请在此处插入实际游戏截图】")
body("建议截图内容：")
bullet("村庄全景")
bullet("与村长对话界面（展示分支选项）")
bullet("山洞地图与怪物")
bullet("战斗场景（怪物蓄力橙色闪光）")
bullet("背包面板")
bullet("Game Over / Victory 界面")

section("六、AI工具声明")
body(
    "本项目在开发过程中使用了 Claude Code（Anthropic）辅助开发。"
    "AI辅助部分：UI渲染代码（对话框、背包面板、Game Over界面）、地图文件设计、"
    "对话文本润色、README与本文档撰写、部分辅助逻辑（场景切换、闪光效果、死亡/胜利检测）。"
    "自主实现部分：N叉树数据结构核心设计、A*寻路算法的完整实现、"
    "Monster AI状态机逻辑、碰撞检测系统由开发者主导设计并逐行理解后写入。"
    "所有AI生成代码均经开发者逐行审查、修改并测试通过。"
)

# 保存
pdf.output(r"C:\Users\LEGION\Desktop\xiangmu\rpg_game\docs\report.pdf")
print("PDF saved to docs/report.pdf")
