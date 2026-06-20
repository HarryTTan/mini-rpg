from src.constants import MONSTER_WINDUP_DURATION, COLOR_MONSTER_WINDUP, TILE_SIZE, COLOR_FLASH_HURT, COLOR_MONSTER, COLOR_PLAYER, COLOR_NPC, DIRECTIONS, FLASH_DURATION, MONSTER_DETECTION_RANGE, MONSTER_MOVE_COOLDOWN, MONSTER_ATTACK_COOLDOWN
from src.dialogue import DialogueTree
from src.pathfinding import astar
import pygame

#实体类，包含怪物与玩家与NPC。
class Entity:
    def __init__(self, tile_x, tile_y, color):
        self.tile_x = tile_x
        self.tile_y = tile_y
        self.color = color
        self.flash_timer = 0
        self.flash_color = None

    @property #定义属性，据说可以自动更新像素坐标
    def pixel_x(self):
        return self.tile_x * TILE_SIZE

    @property
    def pixel_y(self):
        return self.tile_y * TILE_SIZE

    #将实体方格画在地图上，独立于地图作画
    def render(self, screen, camera_offset_x=0, camera_offset_y=0):
        #闪光期间用闪光色
        if self.flash_timer > 0:
            draw_color = self.flash_color
            self.flash_timer -= 1
        else:
            draw_color = self.color
        pygame.draw.rect(
            screen,
            draw_color,
            (self.pixel_x - camera_offset_x,
             self.pixel_y - camera_offset_y,
             TILE_SIZE, TILE_SIZE)
        )

    #触发闪光
    def trigger_flash(self, color, duration=FLASH_DURATION):
        self.flash_timer = duration
        self.flash_color = color

class Player(Entity):

    #玩家实体，特殊属性包括朝向等
    def __init__(self, tile_x, tile_y):
        super().__init__(tile_x, tile_y,COLOR_PLAYER)
        self.facing = "down"
        self.hp=70
        self.max_hp=100
        self.attack=5

    #移动
    def move(self, dx, dy, game_map, npc_list, monster_list):
        new_x, new_y= self.tile_x + dx, self.tile_y + dy
        if game_map.is_walkable(new_x, new_y) and not game_map.is_npc_at(npc_list+monster_list, new_x, new_y):
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

class Monster(Entity):

    #怪物实体，属性包括血量、攻击力等
    def __init__(self,tile_x, tile_y, name, hp, attack):
        super().__init__(tile_x, tile_y, COLOR_MONSTER)
        self.name = name
        self.hp = hp
        self.attack = attack
        self.on_attack=0
        self.alive = True
        self.windup_duration = MONSTER_WINDUP_DURATION
        self.windup_timer = MONSTER_WINDUP_DURATION
        self.detection_range = MONSTER_DETECTION_RANGE
        self.move_cooldown = MONSTER_MOVE_COOLDOWN
        self.move_timer = 0
        self.attack_cooldown = MONSTER_ATTACK_COOLDOWN
        self.attack_timer = 0
    def interrupt_attack(self):
        self.on_attack = 0
        self.attack_timer = self.attack_cooldown
        self.windup_timer = self.windup_duration
    def update(self, player, game_map, npc_list, monster_list):
        if not self.alive:
            return
        self.move_timer -= 1 if self.move_timer > 0 else 0
        self.attack_timer -= 1 if self.attack_timer > 0 else 0
        dist = abs(self.tile_x - player.tile_x) + abs(self.tile_y - player.tile_y)

        if self.on_attack:
            self.windup_timer -= 1
            if self.windup_timer <= 0:
                if dist==1:
                    player.hp -= self.attack
                    player.trigger_flash(COLOR_FLASH_HURT)
                self.attack_timer = self.attack_cooldown
                self.windup_timer = self.windup_duration
                self.on_attack = 0
            return
        if dist == 1:
            if self.attack_timer <= 0:
                self.on_attack = 1
                self.trigger_flash(COLOR_MONSTER_WINDUP, self.windup_duration)
            return
        if dist > self.detection_range:
            return
        if self.move_timer <= 0 and not self.on_attack:
            blocked=set()
            for m in monster_list:
                if m.alive and m is not self:
                    blocked.add((m.tile_x, m.tile_y))
            for n in npc_list:
                blocked.add((n.tile_x, n.tile_y))
            path = astar(
                (self.tile_x, self.tile_y),
                (player.tile_x, player.tile_y),
                game_map, blocked
            )
            if path:
                self.tile_x, self.tile_y = path[0]
            self.move_timer = self.move_cooldown
