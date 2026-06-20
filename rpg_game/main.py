import pygame
import sys

from src.constants import TILE_SIZE, TILE_COLORS, TILE_CAVE, COLOR_MONSTER_HURT
from src.map_data import MapLoader
from src.entity import Player, NPC, Monster
from src.dialogue import DialogueScene
from src.inventory import Inventory,InventoryBox


def main():
    pygame.init()
    #加载两张地图
    village_map = MapLoader("assets/maps/village_map.txt")
    cave_map = MapLoader("assets/maps/cave_map.txt")
    player = Player(14, 5)

    #村庄NPC和怪物
    village_npcs = [
        NPC(5, 5, "Village Chief", "assets/dialogues/elder_dialogue.json"),
        NPC(25, 15, "Kid", "assets/dialogues/younger_dialogue.json"),
    ]
    village_monsters = [
        Monster(25, 12, "Goblin", 40, 8)
    ]
    #山洞怪物（没有NPC）
    cave_npcs = []
    cave_monsters = [
        Monster(14, 5, "Bat", 15, 4),
        Monster(5, 15, "Skeleton", 50, 10),
        Monster(25, 13, "Dark Slime", 30, 7)
    ]

    #当前场景
    current_map = village_map
    current_npcs = village_npcs
    current_monsters = village_monsters
    current_map_name = "village"

    dialogue_scene = None
    inventory=Inventory()
    inventory_box = InventoryBox()
    inventory.add("sword")
    inventory.add("giant_sword")
    inventory.add("potion", 3)
    show_inventory=False
    selected_item=0
    screen = pygame.display.set_mode((960, 640))
    pygame.display.set_caption("Mini RPG")
    clock = pygame.time.Clock()
    running = True
    game_over = False
    victory = False
    move_delay=10
    move_timer=0
    while running:
        events = pygame.event.get()

        #退出游戏检测
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if game_over or victory:
                if event.type == pygame.KEYDOWN:
                    pygame.quit()
                    sys.exit()

        #游戏结束后不再处理
        if not game_over and not victory:

            #判定是否对话
            if dialogue_scene is None:

                #一般类型事件，目前管理进入对话以及背包操作等
                for event in events:
                    if event.type == pygame.KEYDOWN:

                        #开关背包
                        if event.key == pygame.K_i:
                            show_inventory = not show_inventory
                            selected_item = 0

                        #背包使用
                        elif show_inventory:
                            items = inventory.get_list()
                            if event.key == pygame.K_UP and len(items)>0:
                                selected_item = (selected_item-1)%len(items)
                            elif event.key == pygame.K_DOWN and len(items)>0:
                                selected_item = (selected_item+1)%len(items)
                            elif event.key == pygame.K_z and len(items)>0:
                                item_name = items[selected_item][0]
                                inventory.use(item_name, player)

                        #对话，打开背包时不能进行
                        elif event.key == pygame.K_z:
                            for npc in current_npcs:
                                dist = abs(player.tile_x - npc.tile_x) + abs(player.tile_y - npc.tile_y)
                                if dist == 1:
                                    npc.reset()
                                    dialogue_scene = DialogueScene(screen, npc)
                                    break

                        #攻击键
                        elif event.key == pygame.K_SPACE:
                            for monster in current_monsters:
                                if not monster.alive:
                                    continue
                                dist=abs(player.tile_x - monster.tile_x)+abs(player.tile_y - monster.tile_y)
                                if dist == 1:
                                    monster.hp-=player.attack
                                    monster.interrupt_attack()
                                    monster.trigger_flash(COLOR_MONSTER_HURT)
                                    if monster.hp <= 0:
                                        monster.alive = False
                                    break

                #移动检测，做了按住不动就可以持续移动的功能，打开背包时不能移动
                if not show_inventory:
                    keys = pygame.key.get_pressed()
                    move_timer -= 1
                    if move_timer <=0 and (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]) :
                        move_timer = move_delay
                        if keys[pygame.K_UP]:
                            player.move(0, -1, current_map, current_npcs, current_monsters)
                        elif keys[pygame.K_DOWN]:
                            player.move(0, 1, current_map, current_npcs, current_monsters)
                        elif keys[pygame.K_LEFT]:
                            player.move(-1, 0, current_map, current_npcs, current_monsters)
                        elif keys[pygame.K_RIGHT]:
                            player.move(1, 0, current_map, current_npcs, current_monsters)

                    #场景切换，踩到洞穴砖块就切换
                    if current_map.get_tile(player.tile_x, player.tile_y) == TILE_CAVE:
                        if current_map_name == "village":
                            current_map = cave_map
                            current_npcs = cave_npcs
                            current_monsters = cave_monsters
                            player.tile_x, player.tile_y = 2, 9
                            current_map_name = "cave"
                        else:
                            current_map = village_map
                            current_npcs = village_npcs
                            current_monsters = village_monsters
                            player.tile_x, player.tile_y = 28, 9
                            current_map_name = "village"
            else:
                dialogue_scene.handle_events(events)

            #怪物AI更新，结束后不再更新
            for monster in current_monsters:
                monster.update(player, current_map, current_npcs, current_monsters)

        #游戏结束检测
        if not game_over and player.hp <= 0:
            game_over = True

        #胜利检测
        if not victory and current_map_name == "cave":
            if all(not m.alive for m in current_monsters):
                victory = True

        #地图与人物渲染
        for row in range(current_map.height):
            for col in range(current_map.width):
                tile_id = current_map.grid[row][col]
                color = TILE_COLORS[tile_id]
                x, y = col * TILE_SIZE, row * TILE_SIZE
                pygame.draw.rect(screen, color, (x, y, TILE_SIZE, TILE_SIZE))
        for npc in current_npcs:
            npc.render(screen)
        player.render(screen)
        for monster in current_monsters:
            if monster.alive: monster.render(screen)

        #背包渲染
        if show_inventory:
            inventory_box.render(screen, inventory, player, selected_item)

        #对话框渲染
        if dialogue_scene is not None:
            dialogue_scene.render(screen)
            if dialogue_scene.done:
                dialogue_scene = None

        #结束文字
        if game_over:
            font = pygame.font.Font(None, 64)
            text = font.render("GAME OVER", True, (255, 0, 0))
            rect = text.get_rect(center=(480, 320))
            screen.blit(text, rect)
        elif victory:
            font = pygame.font.Font(None, 48)
            text = font.render("VICTORY! All monsters defeated.", True, (255, 255, 0))
            rect = text.get_rect(center=(480, 320))
            screen.blit(text, rect)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
