import json
import pygame
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT


#场景基类，负责事件分发和渲染（不知道有什么用？AI建议的）
class Scene:
    def handle_events(self, events):
        pass

    def update(self):
        pass

    def render(self, screen):
        pass


#N叉树节点，每个节点是一句对话，children是分支
class DialogueNode:
    def __init__(self, text):
        self.text = text
        self.children = []
        self.responses = []

    def add_child(self, child_node, response_text):
        self.children.append(child_node)
        self.responses.append(response_text)

    def is_leaf(self):
        return len(self.children) == 0

#对话树本体
class DialogueTree:
    def __init__(self, json_path):
        self.root = None
        self.current = None
        self._load(json_path)

    def _load(self, json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.root = self._build_from_dict(data)
        self.current = self.root

    def _build_from_dict(self, data):
        node = DialogueNode(data['text'])
        node.responses = data['responses']
        for child_data in data['children']:
            child_node = self._build_from_dict(child_data)
            node.children.append(child_node)
        return node

    def get_current_text(self):
        return self.current.text

    def get_responses(self):
        return self.current.responses

    def advance(self, choice_index):
        if choice_index < len(self.current.children):
            self.current = self.current.children[choice_index]

    def is_finished(self):
        return self.current.is_leaf()


#对话管理器，负责对话树的遍历和状态控制
class DialogueManager:
    def __init__(self, dialogue_tree):
        self.tree = dialogue_tree
        self.tree.current = self.tree.root

    def get_current_text(self):
        return self.tree.get_current_text()

    def get_current_responses(self):
        return self.tree.get_responses()

    def has_choices(self):
        return len(self.get_current_responses()) > 1

    def advance(self):
        if len(self.tree.current.children) == 1:
            self.tree.advance(0)

    def select_choice(self, index):
        self.tree.advance(index)

    def is_finished(self):
        return self.tree.is_finished()


#对话框绘制，负责文字渲染和选项显示
class DialogBox:
    def __init__(self):
        self.font = pygame.font.Font(None, 24)
        self.rect = pygame.Rect(10, SCREEN_HEIGHT - 160, SCREEN_WIDTH - 20, 150)

    def render(self, screen, text, choices=None, selected_index=0):
        #画半透明黑底
        bg = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        bg.fill((0, 0, 0, 200))
        screen.blit(bg, (self.rect.x, self.rect.y))
        #画白框
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)
        #渲染对话文字，自动换行
        lines = self._wrap_text(text, 40)
        y_offset = self.rect.y + 15
        for line in lines:
            line_surface = self.font.render(line, True, (255, 255, 255))
            screen.blit(line_surface, (self.rect.x + 15, y_offset))
            y_offset += 30
        #渲染选项
        if choices:
            y_offset += 10
            for i, choice in enumerate(choices):
                prefix = "> " if i == selected_index else "  "
                color = (255, 255, 0) if i == selected_index else (200, 200, 200)
                choice_surface = self.font.render(prefix + choice, True, color)
                screen.blit(choice_surface, (self.rect.x + 25, y_offset))
                y_offset += 30
        else:
            hint = self.font.render("Press Z to continue", True, (150, 150, 150))
            screen.blit(hint, (self.rect.x + self.rect.width - 155,
                                self.rect.y + self.rect.height - 30))

    def _wrap_text(self, text, max_chars):
        return [text[i:i + max_chars] for i in range(0, len(text), max_chars)]


#对话场景，管理一次完整的对话流程，外部直接调用这个类
class DialogueScene(Scene):
    def __init__(self, screen, npc):
        self.npc = npc
        self.manager = DialogueManager(npc.dialogue_tree)
        self.dialog_box = DialogBox()
        self.selected_choice = 0
        self.done = False

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                choices = self.manager.get_current_responses()

                if event.key == pygame.K_UP:
                    if len(choices) > 0:
                        self.selected_choice = (self.selected_choice - 1) % len(choices)

                elif event.key == pygame.K_DOWN:
                    if len(choices) > 0:
                        self.selected_choice = (self.selected_choice + 1) % len(choices)

                elif event.key in (pygame.K_z, pygame.K_SPACE, pygame.K_RETURN):
                    if self.manager.is_finished():
                        self.done = True
                    elif self.manager.has_choices():
                        self.manager.select_choice(self.selected_choice)
                        self.selected_choice = 0
                    else:
                        self.manager.advance()

    def render(self, screen):
        self.dialog_box.render(
            screen,
            self.manager.get_current_text(),
            self.manager.get_current_responses(),
            self.selected_choice
        )
