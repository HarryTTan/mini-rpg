from src.constants import TILE_SIZE, COLOR_PLAYER, COLOR_NPC, DIRECTIONS
from src.dialogue import DialogueTree
import pygame

#实体类，包含怪物与玩家与NPC。
class Entity:
    def __init__(self, tile_x, tile_y, color):
        self.tile_x = tile_x
        self.tile_y = tile_y
        self.color = color

    @property #定义属性，据说可以自动更新像素坐标
    def pixel_x(self):
        return self.tile_x * TILE_SIZE

    @property
    def pixel_y(self):
        return self.tile_y * TILE_SIZE

    #将实体方格画在地图上，独立于地图作画
    def render(self, screen, camera_offset_x=0, camera_offset_y=0):
        pygame.draw.rect(
            screen,
            self.color,
            (self.pixel_x - camera_offset_x,
             self.pixel_y - camera_offset_y,
             TILE_SIZE, TILE_SIZE)
        )

class Player(Entity):

    #玩家实体，特殊属性包括朝向
    def __init__(self, tile_x, tile_y):
        super().__init__(tile_x, tile_y,COLOR_PLAYER)
        self.facing = "down"

    #移动
    def move(self, dx, dy, game_map, npc_list):
        new_x, new_y= self.tile_x + dx, self.tile_y + dy
        if game_map.is_walkable(new_x, new_y) and not game_map.is_npc_at(npc_list, new_x, new_y):
            self.tile_x, self.tile_y = new_x, new_y
        self.facing= DIRECTIONS[(dx, dy)]

class NPC(Entity):

    #npc实体，特殊属性包括名字与对话树
    def __init__(self, tile_x, tile_y, name, dialogue_json_path):
        super().__init__(tile_x, tile_y, COLOR_NPC)
        self.name = name
        self.dialogue_tree = DialogueTree(dialogue_json_path)

    #开始对话时重置对话树
    def reset(self):
        self.dialogue_tree.current = self.dialogue_tree.root
