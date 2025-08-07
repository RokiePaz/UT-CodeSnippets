import os
import pygame
from game.core.scene import Scene
from game.overworld.player import Player
from game.overworld.npc import NPC
from game.overworld.dialogue import DialogueBox, load_dialogue_lines
from game.settings import WIDTH, HEIGHT, GRAY, LIGHT_GRAY


class OverworldScene(Scene):
    def __init__(self, screen: pygame.Surface):
        super().__init__(screen)
        self.player = Player(x=WIDTH // 2 - 8, y=HEIGHT // 2 - 8)
        self.npc = NPC(x=WIDTH // 2 + 60, y=HEIGHT // 2 - 8)
        self.dialogue: DialogueBox | None = None
        self.data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
        self.data_dir = os.path.abspath(self.data_dir)

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                if self.dialogue is None:
                    if self.player.rect().colliderect(self.npc.rect().inflate(24, 24)):
                        lines = load_dialogue_lines(self.data_dir, "intro")
                        self.dialogue = DialogueBox(lines)
                else:
                    self.dialogue.advance()
            if event.key in (pygame.K_x, pygame.K_ESCAPE):
                if self.dialogue is not None and self.dialogue.done:
                    self.dialogue = None
            if event.key == pygame.K_RETURN:
                if self.player.rect().colliderect(self.npc.rect().inflate(24, 24)):
                    self.is_done = True
                    self.next_scene_name = "battle"

    def update(self, dt: float):
        self.player.handle_input(dt)
        if self.dialogue:
            self.dialogue.update(dt)

    def draw(self):
        self.screen.fill(GRAY)
        # simple room border
        pygame.draw.rect(self.screen, LIGHT_GRAY, pygame.Rect(8, 8, WIDTH - 16, HEIGHT - 16), 2)
        self.npc.draw(self.screen)
        self.player.draw(self.screen)
        if self.dialogue:
            self.dialogue.draw(self.screen)