import pygame
from dataclasses import dataclass


@dataclass
class Player:
    x: float
    y: float
    speed: float = 140.0
    size: int = 16

    def rect(self) -> pygame.Rect:
        return pygame.Rect(int(self.x), int(self.y), self.size, self.size)

    def handle_input(self, dt: float):
        keys = pygame.key.get_pressed()
        dx = dy = 0.0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy -= 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy += 1
        if dx != 0 and dy != 0:
            dx *= 0.7071
            dy *= 0.7071
        self.x += dx * self.speed * dt
        self.y += dy * self.speed * dt

    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(surface, (240, 240, 240), self.rect())