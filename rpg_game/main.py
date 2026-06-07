import pygame
import sys

from src.constants import TILE_SIZE, TILE_COLORS
from src.map_data import MapLoader
from src.entity import Player, NPC
from src.dialogue import DialogueScene
from src.inventory import Inventory,InventoryBox


def main():
    pygame.init()
    game_map = MapLoader("assets/maps/village_map.txt")
    player = Player(15, 9)
    npc_list = [
        NPC(5, 5, "Village Chief", "assets/dialogues/elder_dialogue.json"),
        NPC(25, 15, "Kid", "assets/dialogues/younger_dialogue.json"),
    ]
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
    move_delay=10
    move_timer=0
    while running:
        events = pygame.event.get()

        #判定是否对话
        if dialogue_scene is None:

            #一般类型事件，目前管理进入对话以及退出游戏
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                    #开关背包
                    elif event.key == pygame.K_i:
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
                        for npc in npc_list:
                            dist = abs(player.tile_x - npc.tile_x) + abs(player.tile_y - npc.tile_y)
                            if dist == 1:
                                npc.reset()
                                dialogue_scene = DialogueScene(screen, npc)
                                break

            #移动检测，做了按住不动就可以持续移动的功能，打开背包时不能移动
            if not show_inventory:
                keys = pygame.key.get_pressed()
                move_timer -= 1
                if move_timer <=0 and (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]) :
                    move_timer = move_delay
                    if keys[pygame.K_UP]:
                        player.move(0, -1, game_map, npc_list)
                    elif keys[pygame.K_DOWN]:
                        player.move(0, 1, game_map, npc_list)
                    elif keys[pygame.K_LEFT]:
                        player.move(-1, 0, game_map, npc_list)
                    elif keys[pygame.K_RIGHT]:
                        player.move(1, 0, game_map, npc_list)
        else:
            dialogue_scene.handle_events(events)

        #地图与人物渲染
        for row in range(game_map.height):
            for col in range(game_map.width):
                tile_id = game_map.grid[row][col]
                color = TILE_COLORS[tile_id]
                x, y = col * TILE_SIZE, row * TILE_SIZE
                pygame.draw.rect(screen, color, (x, y, TILE_SIZE, TILE_SIZE))
        for npc in npc_list:
            npc.render(screen)
        player.render(screen)

        #背包渲染
        if show_inventory:
            inventory_box.render(screen, inventory, player, selected_item)

        #对话框渲染
        if dialogue_scene is not None:
            dialogue_scene.render(screen)
            if dialogue_scene.done:
                dialogue_scene = None

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
