import random
import pygame
from typing import List
from game.core.scene import Scene
from game.settings import WIDTH, HEIGHT, BATTLE_BOX_COLOR, BATTLE_BOX_BORDER, WHITE
from game.combat.heart import Heart
from game.combat.bullet import Bullet
from game.combat.patterns import radial_burst, aimed_shot
from game.core.ui import draw_bordered_rect, get_font


class BattleScene(Scene):
    def __init__(self, screen: pygame.Surface):
        super().__init__(screen)
        margin = 120
        self.box = pygame.Rect(80, 80, WIDTH - 160, HEIGHT - margin)
        self.heart = Heart(self.box.centerx, self.box.centery)
        self.bullets: List[Bullet] = []
        self.spawn_timer = 0.0
        self.spawn_interval = 1.2
        self.hp = 20
        self.font = get_font(None, 18)

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_x, pygame.K_ESCAPE):
                self.is_done = True
                self.next_scene_name = "overworld"

    def update(self, dt: float):
        self.heart.update(dt, self.box)
        self.spawn_timer += dt
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = 0.0
            self.spawn_wave()
        # update bullets
        for b in self.bullets:
            b.update(dt)
        # cull
        self.bullets = [b for b in self.bullets if not b.is_offscreen(self.box)]
        # collisions
        heart_rect = self.heart.rect()
        for b in self.bullets:
            if b.collides_rect(heart_rect):
                self.hp = max(0, self.hp - 1)
        if self.hp <= 0:
            self.is_done = True
            self.next_scene_name = "overworld"

    def draw(self):
        self.screen.fill((0, 0, 0))
        draw_bordered_rect(self.screen, self.box, BATTLE_BOX_COLOR, BATTLE_BOX_BORDER, 2)
        self.heart.draw(self.screen)
        for b in self.bullets:
            b.draw(self.screen)
        # UI
        hp_text = self.font.render(f"HP: {self.hp}", True, WHITE)
        self.screen.blit(hp_text, (10, 10))
        tip = self.font.render("ESC/X: Flee", True, WHITE)
        self.screen.blit(tip, (WIDTH - tip.get_width() - 10, 10))

    def spawn_wave(self):
        cx, cy = self.box.center
        choice = random.choice(["radial", "aimed"])
        if choice == "radial":
            self.bullets.extend(radial_burst(cx, cy, speed=90.0, count=16))
        else:
            self.bullets.extend(aimed_shot(cx, cy, self.heart.x, self.heart.y, speed=120.0, n=5, spread_deg=25.0))