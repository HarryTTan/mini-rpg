# 像素RPG项目 — 进度记录

## 当前状态
- **完成阶段**: 阶段1、2、3
- **下一步**: 阶段4 — NPC + 对话系统

## 已完成文件

| 文件 | 状态 | 说明 |
|------|------|------|
| main.py | 完成 | 游戏窗口 + 地图渲染 + 玩家移动(方向键) + 退出(ESC) |
| constants.py | 完成 | 屏幕/瓦片/颜色/寻路/朝向 所有常量 + DIRECTIONS字典 |
| src/tile.py | 完成 | Tile.is_walkable() 判断可通行地形 |
| src/map_data.py | 完成 | MapLoader: 加载txt→2D数组, get_tile(), is_walkable() |
| src/entity.py | 完成 | Entity基类: 瓦片坐标 + pixel属性 + render() |
| src/player.py | 完成 | Player(Entity): move()含碰撞检测 + facing朝向 |
| assets/maps/village_map.txt | 完成 | 30×20地图: 村庄+房屋+小路+水域+树木边界 |

## 技术架构回顾

游戏循环结构(main.py):
  while running:
    ① 事件 → KEYDOWN: 上下左右移动 / ESC退出 / QUIT退出
    ② 渲染 → 遍历2D数组画瓦片 → player.render(screen)
    ③ flip() + clock.tick(60)

实体继承:
  Entity → Player (move + collision + facing)
  Entity → NPC (对话树, 待写)
  Entity → Monster (状态机 + 寻路 + 攻击, 待写)

碰撞检测:
  player.move(dx, dy, game_map) → game_map.is_walkable(new_x, new_y) → 查2D数组

## 阶段4: NPC + 对话系统 (明天继续)
需要创建:
  1. src/dsa/tree.py — DialogueNode + DialogueTree (N叉树 + BFS/DFS)
  2. src/npc.py — NPC类继承Entity, 持有DialogueTree
  3. assets/dialogues/elder_dialogue.json — 对话树数据
  4. src/dialogue_system.py — DialogueManager
  5. src/dialogue_ui.py — DialogBox渲染
  6. src/scenes/scene_base.py — 抽象Scene基类
  7. src/scenes/dialogue_scene.py — 对话场景
  8. 修改main.py — Z键触发对话

## 完整实现顺序
□ 阶段1: 项目搭建 + 基础窗口     ✓
□ 阶段2: 地图系统                 ✓
□ 阶段3: 玩家 + 碰撞检测          ✓
□ 阶段4: NPC + 对话系统           ← 下一步
□ 阶段5: 背包系统 (LinkedList)
□ 阶段6: 寻路 + 怪物 (A*/Dijkstra + 状态机)
□ 阶段7: 实时战斗 (攻击冷却 + 伤害)
□ 阶段8: 寻路对比 + 报告
