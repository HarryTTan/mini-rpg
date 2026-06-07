from src.constants import TILE_GRASS, TILE_PATH, TILE_DOOR


class Tile:
    @staticmethod
    def is_walkable(tile_id):
        return tile_id in (TILE_GRASS, TILE_PATH, TILE_DOOR)


class MapLoader:
    def __init__(self, path):
        self.grid = []
        self.width = 0
        self.height = 0
        self._load(path)

    #地图加载
    def _load(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                row = [int(n) for n in line.split()]
                self.grid.append(row)
        self.height = len(self.grid)
        self.width = len(self.grid[0]) if self.grid else 0

    #获取tile坐标对应的tile_id
    def get_tile(self, col, row):
        if 0 <= row < self.height and 0 <= col < self.width:
            return self.grid[row][col]
        return -1

    #基本方块碰撞判定
    def is_walkable(self, col, row):
        tile_id = self.get_tile(col, row)
        return Tile.is_walkable(tile_id)

    #npc与怪物碰撞判定，写成静态方法似乎方便一点
    @staticmethod
    def is_npc_at(npc_list, tile_x, tile_y):
        for npc in npc_list:
            if npc.tile_x == tile_x and npc.tile_y == tile_y:
                return True
        return False
