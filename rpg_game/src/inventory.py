from collections import defaultdict
import pygame
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT

#基本背包信息
items_info={
    "sword":(5, "attack", "equip"),
    "potion":(20, "heal", "consume"),
    "giant_sword":(10, "attack", "equip"),
    "big_potion":(20, "heal_over_max", "consume")
}

#物品类，用于存储物品信息
class Item:
    def __init__(self,name):
        info=items_info[name]
        self.name=name
        self.effect_value=info[0]
        self.effect_type=info[1]
        self.consume_type=info[2]

#背包类，实现所有背包功能
class Inventory:
    def __init__(self):
        self.items=defaultdict(lambda:0)
        self.weapon=False
        self.add_attack=0

    def add(self,name,count=1):
        self.items[name]+=count

    def remove(self,name,target=None):
        if name not in self.items:
            return
        self.items[name]-=1
        if self.items[name]<=0:
            del self.items[name]

    def use(self,name,target):
        if name not in self.items:
            return
        item=Item(name)

        if item.effect_type=="attack":
            cur_add_attack=self.add_attack
            if self.weapon:
                self.weapon=False
                target.attack-=self.add_attack
                self.add_attack=0
            if item.effect_value != cur_add_attack:
                target.attack+=item.effect_value
                self.add_attack=item.effect_value
                self.weapon=True

        elif item.effect_type=="heal":
            if target.hp == target.max_hp:
                return
            target.hp=min(target.hp+item.effect_value,target.max_hp)
            self.remove(name)

        elif item.effect_type=="heal_over_max":
            target.max_hp+=item.effect_value
            target.hp+=item.effect_value
            self.remove(name)

    def get_list(self):
        return [(name,count) for name,count in self.items.items()]

#背包界面渲染
class InventoryBox:
    def __init__(self):
        self.font = pygame.font.Font(None,24)
        panel_width,panel_height = 640,480
        self.rect = pygame.Rect(
            (SCREEN_WIDTH-panel_width)//2,
            (SCREEN_HEIGHT-panel_height)//2,
            panel_width,panel_height
        )

    def render(self, screen, inventory, player, selected_index):
        bg = pygame.Surface((self.rect.width,self.rect.height), pygame.SRCALPHA)
        bg.fill((0,0,0,220))
        screen.blit(bg,(self.rect.x,self.rect.y))
        pygame.draw.rect(screen,(255,255,255),self.rect,2)

        y = self.rect.y + 10
        status = self.font.render(
            f"HP: {player.hp}/{player.max_hp}  ATK: {player.attack}",
            True,(255,255,255)
        )
        screen.blit(status,(self.rect.x + 15,y))

        y+=35
        pygame.draw.line(screen, (100,100,100),
                         (self.rect.x+10, y),
                         (self.rect.x+self.rect.width-10, y))

        y+=10

        items =inventory.get_list()
        for i, (name,count) in enumerate(items):
            prefix = "> " if i==selected_index else "  "
            color = (255,255,0) if i == selected_index else (255,255,255)
            text=self.font.render(f"{prefix}{name} x{count}",True,color)
            screen.blit(text,(self.rect.x + 15,y))
            y+=30
