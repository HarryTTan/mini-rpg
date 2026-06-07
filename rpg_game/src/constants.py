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
}

# ============================
# 寻路
# ============================
PATHFINDING_ALGO = "astar"  # "astar" 或 "dijkstra"

# ============================
# 朝向
# ============================
DIRECTIONS = {(0,-1):"UP", (0,1):"DOWN", (1,0):"RIGHT", (-1,0):"LEFT"}

