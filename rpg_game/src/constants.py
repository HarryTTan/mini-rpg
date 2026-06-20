# ============================
# 屏幕 & 瓦片
# ============================
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 640
TILE_SIZE = 32
MAP_COLS = 30
MAP_ROWS = 20
FPS = 60

# ============================
# 瓦片类型
# ============================
TILE_GRASS = 0    # 草地 (可走)
TILE_WALL = 1     # 墙壁 (不可走)
TILE_PATH = 2     # 小路 (可走)
TILE_WATER = 3    # 水   (不可走)
TILE_DOOR = 4     # 门   (可走)
TILE_TREE = 5     # 树   (不可走)
TILE_CAVE = 6          #洞穴入口（可走）
TILE_CAVE_FLOOR = 7     #洞穴地面（可走）
TILE_CAVE_WALL = 8      #洞穴岩壁（不可走）

# ============================
# 颜色
# ============================
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_PLAYER = (0, 100, 255)
COLOR_NPC = (255, 215, 0)
COLOR_MONSTER = (255, 60, 60)

# 瓦片颜色映射
TILE_COLORS = {
    TILE_GRASS: (34, 139, 34),
    TILE_WALL:  (139, 90, 43),
    TILE_PATH:  (210, 180, 140),
    TILE_WATER: (65, 105, 225),
    TILE_DOOR:  (160, 82, 45),
    TILE_TREE:  (0, 100, 0),
    TILE_CAVE: (100, 50, 150),
    TILE_CAVE_FLOOR: (95, 85, 75),
    TILE_CAVE_WALL:  (45, 38, 32),
}

# ============================
# 朝向
# ============================
DIRECTIONS = {(0,-1):"UP", (0,1):"DOWN", (1,0):"RIGHT", (-1,0):"LEFT"}

# ============================
# 怪物
# ============================
MONSTER_DETECTION_RANGE = 8  # 视野范围（曼哈顿距离）
MONSTER_MOVE_COOLDOWN = 30  # 移动间隔（帧数）
MONSTER_ATTACK_COOLDOWN = 60  # 攻击间隔（帧数）
MONSTER_WINDUP_DURATION = 25  # 攻击前摇帧数
COLOR_MONSTER_WINDUP = (255, 140, 0)  # 橙色 — 怪物蓄力

# ============================
# 闪光颜色（攻击/受击反馈）
# ============================
COLOR_MONSTER_HURT = (160, 30, 30)     # 暗红色 — 怪物受击
COLOR_FLASH_HURT   = (255, 255, 255)    # 白色 — 受到伤害
FLASH_DURATION = 10                     # 闪光持续帧数