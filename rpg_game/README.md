# Mini RPG — 2D像素RPG游戏

数算B课程大作业。基于 Python + pygame-ce 的俯视角2D像素风角色扮演游戏，核心数据结构与算法：N叉树对话系统、A*寻路、双向链表背包。

## 项目背景

传统课堂中的数据结构（树、图、链表）通常以孤立习题形式出现。本项目将它们融入一个可玩的RPG游戏，探索"数据结构如何驱动游戏逻辑"。玩家在一个有NPC、怪物、山洞的像素世界中探索，对话系统底层是N叉树，怪物追踪使用A*寻路，背包物品管理基于双向链表。

## 核心算法与数据结构

### 1. 对话系统 — N叉树 (N-ary Tree)

`src/dialogue.py` 实现了通用的N叉树结构：

- **`DialogueNode`**：树节点，含对话文本 `text`、回应选项 `responses`、子节点 `children`
- **`DialogueTree`**：从JSON递归构建N叉树（`_build_from_dict`），支持BFS/DFS遍历
- **`DialogueManager`**：树遍历状态管理器，处理单子节点自动推进、多分支选项选择

对话数据存储在 `assets/dialogues/*.json`，每个节点可包含任意数量的子分支。

**树结构示例**（村长对话）：
```
"欢迎来到村庄"
  ├── "怪物在骚扰村庄，能帮忙吗？"
  │     ├── "我这就去" → "小心！"（叶子）
  │     └── "晚点再来" → "随时等你"（叶子）
  └── "我路过而已" → "一路小心"（叶子）
```

### 2. 怪物AI — A*寻路算法

`src/pathfinding.py` 实现A*最短路径搜索：

- **评价函数**：`f(n) = g(n) + h(n)`，其中 `g` 为已走步数，`h` 为曼哈顿距离启发函数
- **数据结构**：优先队列（`heapq` 最小堆）按f值排序，字典 `visited` 记录父节点用于路径回溯
- **障碍处理**：区分静态障碍（地图瓦片）和动态障碍（其他怪物、NPC）

怪物行为：5格视野内检测玩家 → A*计算路径 → 每30帧移动一步 → 相邻时蓄力攻击（25帧前摇）

### 3. 背包系统 — 双向链表 (Doubly Linked List)

`src/inventory.py` 基于自定义双向链表实现物品存储：

- **`ItemNode`**：链表节点，含 `item`（物品对象）、`prev`、`next` 指针
- **`Inventory`**：链表管理器，支持 `insert_front`、`find`、`remove` 操作
- 物品使用遍历链表查找，装备/消耗/堆叠逻辑构建于链表操作之上

---

## 运行指南

```bash
# 克隆仓库
git clone https://github.com/HarryTTan/mini-rpg.git
cd mini-rpg

# 创建虚拟环境并安装依赖
python -m venv .venv
source .venv/bin/activate      # macOS/Linux
# .venv\Scripts\activate       # Windows

pip install -r requirements.txt

# 运行游戏
python main.py
```

**操作说明：**

| 按键 | 功能 |
|------|------|
| ↑↓←→ | 移动 |
| Z | 对话 / 确认 |
| I | 开关背包 |
| 空格 | 攻击 |
| ESC | 退出 |

---

## 项目结构

```
mini-rpg/
├── main.py                      # 游戏主循环 (60FPS)
├── requirements.txt             # 依赖: pygame-ce>=2.5.0
├── README.md
├── LICENSE
├── src/
│   ├── constants.py             # 全局常量（屏幕/瓦片/颜色/方向）
│   ├── entity.py                # Entity基类 + Player + NPC + Monster
│   ├── map_data.py              # Tile(地形判定) + MapLoader(地图加载)
│   ├── dialogue.py              # N叉树对话系统（树+管理器+UI）
│   ├── inventory.py             # 双向链表背包系统
│   └── pathfinding.py           # A*寻路算法
└── assets/
    ├── maps/                    # 地图文件（纯文本网格）
    │   ├── village_map.txt      # 30×20村庄地图
    │   └── cave_map.txt         # 30×20山洞地图
    └── dialogues/               # NPC对话树JSON
        ├── elder_dialogue.json
        └── younger_dialogue.json
```

---

## 游戏截图

```
村庄                               山洞
■■■■■■■■■■■■■■■■■■■■    ■■■■■■■■■■■■■■■■■■■■
■  🏠🏠      🌳🌳🌳  ■    ■                    ■
■  🏠🏠 👴      🌳C■    ■  🦇                 ■
■                 🌳■    ■                    ■
■  🧑                    ■    ■■■■■■■■■■■■■■■■■■■■■■
■              👦🟢 ■    ■         🦴 🟣      ■
■   🟢                  ■    ■                    ■
■■■■■■■■■■■■■■■■■■■■    ■■■■■■■■■■■■■■■■■■■■
```
> 蓝色=玩家  金色=NPC  红色=怪物  绿色=草地  棕色=墙

---

## AI 工具声明

本项目在开发过程中使用了 **Claude Code**（Anthropic）辅助：

- **AI 辅助部分**：GUI框架代码（对话框渲染、背包面板、Game Over界面）、地图文件设计、对话文本润色、README文档撰写
- **自主实现部分**：N叉树数据结构核心逻辑、A*寻路算法、双向链表背包、怪物AI状态机、场景切换系统由开发者主导设计并逐行理解后写入
- 所有由AI生成的代码均经过开发者逐行审查、修改并测试通过

## 许可

MIT License
