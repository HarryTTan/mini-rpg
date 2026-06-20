# Mini RPG

数算B课程大作业。基于 Python + pygame-ce 的2D小游戏，核心数据结构与算法：N叉树对话系统、A\*寻路算法。

## 项目背景

传统课堂中的数据结构与算法通常以孤立习题形式出现。本项目将它们融入一个可玩的RPG游戏，探索"数据结构与算法如何驱动游戏逻辑"。玩家在村庄和山洞两张地图中探索，与NPC对话的底层是N叉树结构，怪物追踪玩家使用A*最短路径搜索。

## 核心算法与数据结构

### 1. 对话系统 — N叉树 (N-ary Tree)

`src/dialogue.py` 从零实现了通用的N叉树结构：

- **`DialogueNode`**：树节点，包含对话文本 `text`、回应选项列表 `responses`、子节点列表 `children`。`is_leaf()` 判断是否为叶子节点
- **`DialogueTree`**：从JSON文件递归构建完整N叉树，`_build_from_dict()` 方法深度优先遍历JSON结构，每个节点可含任意数量子分支
- **`DialogueManager`**：树遍历控制器 — 遇单子节点自动推进（`advance`），遇分支等待玩家选择（`select_choice`），至叶子节点结束对话

**时间复杂度**：树构建 O(n)，每次对话推进 O(1)。

**树结构示例**（村长对话）：
```
"欢迎来到村庄，我是村长"
├── "怪物最近出没，东边山洞似乎是源头，能帮忙吗？"
│   ├── "交给我" → "多谢！洞口在村庄东边，小心"（叶子）
│   └── "晚点再来" → "随时等你"（叶子）
└── "只是路过" → "一路小心，附近有怪物"（叶子）
```

### 2. 怪物AI — A\*寻路算法

`src/pathfinding.py` 实现了经典A\*最短路径搜索：

- **评价函数**：`f(n) = g(n) + h(n)` — `g` 为从起点已走步数，`h` 为当前节点到终点的曼哈顿距离（`|dx| + |dy|`）
- **数据结构**：
  - `heapq` 最小堆实现优先队列，按 `f` 值排序，保证每次扩展最优点
  - `visited` 字典（hash table）记录已探索节点及父节点，用于最终路径回溯
  - 四方向邻域扩展，排除不可走瓦片和动态障碍（其他怪物、NPC）
- **启发函数可接受性**：曼哈顿距离在四方向网格上不会高估实际代价，保证找到最优路径

**时间复杂度**：最坏 O(b^d)，实际远小于此因为有启发函数剪枝。

**怪物行为状态机**：待机（超出视野）→ 追踪（5格内，每30帧A*寻路并移动）→ 蓄力（相邻，闪橙25帧）→ 攻击（伤害+冷却60帧）→ 循环。玩家攻击可打断蓄力。

### 3. 背包系统 — 哈希表 (Hash Table / Dictionary)

`src/inventory.py` 基于 Python `defaultdict`（哈希表）实现物品管理：

- O(1) 物品查找与存取
- 物品分类：装备类（武器，替换逻辑）、消耗类（回血）、突破上限类（提升最大生命值）
- 状态管理：记录当前装备的武器和攻击加成

---

## 运行指南

**环境要求：** Python 3.10+（Windows / macOS / Linux 均可）

**依赖库：**

| 库 | 版本 | 用途 |
|----|------|------|
| `pygame-ce` | >=2.5.0 | 图形渲染、事件处理、游戏主循环 |

其余全部使用 Python 标准库：`heapq`（优先队列）、`json`（对话数据解析）、`collections`（背包哈希表）、`sys`（退出）。

```bash
# 克隆仓库
git clone https://github.com/HarryTTan/mini-rpg.git
cd mini-rpg

# 创建虚拟环境
python3 -m venv .venv

# 激活虚拟环境
source .venv/bin/activate      # macOS / Linux
# .venv\Scripts\activate       # Windows

# 安装依赖
pip install -r requirements.txt

# 运行游戏
python main.py
```

> macOS 注意：如 `python3` 不存在，改用 `python`。
> 注：以上指南为AI编写，没有经其它电脑验证，不保证可行。如果上述方法不行，也可以直接从库里下载main.py、assets与src三个文件，在IDE里运行main.py即可（仍需下载pygame）

**操作说明：**

| 按键 | 场景 | 功能 |
|------|------|------|
| ↑↓←→ | 一般 | 网格移动（按住可连续移动） |
| Z | 一般 | 与相邻NPC对话（曼哈顿距离=1） |
| ↑↓ | 对话中 | 选择回应选项 |
| Z | 对话中 | 确认选项 / 对话结束按Z关闭 |
| I | 一般 | 开关背包面板 |
| ↑↓ | 背包中 | 选择物品 |
| Z | 背包中 | 使用选中物品 |
| 空格 | 一般 | 攻击相邻怪物 |
| ESC | 任意 | 退出游戏 |

---

## 项目结构

```
mini-rpg/
├── main.py                      # 游戏主循环 (60FPS)
├── requirements.txt             # 依赖: pygame-ce>=2.5.0
├── README.md
├── LICENSE
├── src/
│   ├── constants.py             # 全局常量（屏幕/瓦片/颜色/朝向/怪物参数）
│   ├── entity.py                # Entity基类 + Player + NPC + Monster（含AI）
│   ├── map_data.py              # Tile(地形判定) + MapLoader(地图加载+碰撞)
│   ├── dialogue.py              # N叉树对话系统（树+管理器+UI渲染）
│   ├── inventory.py             # 背包系统（物品+哈希表存储+UI面板）
│   └── pathfinding.py           # A*寻路算法（heapq优先队列+曼哈顿启发）
└── assets/
    ├── maps/                    # 地图文件（30×20 纯文本网格）
    │   ├── village_map.txt
    │   └── cave_map.txt
    └── dialogues/               # NPC对话树（JSON格式）
        ├── elder_dialogue.json
        └── younger_dialogue.json
```

---

## AI 工具声明

本项目在开发过程中使用了 **Claude Code**辅助：

- **AI 辅助部分**：UI渲染代码（对话框、背包面板、Game Over界面）与部分辅助逻辑（场景切换、闪光效果、死亡/胜利检测）
- **自主实现部分**：N叉树数据结构的核心设计、A\*寻路算法的完整实现、Monster AI状态机逻辑、碰撞检测系统由开发者主导设计并写入
- 所有AI生成代码均经开发者逐行审查、修改并测试通过

