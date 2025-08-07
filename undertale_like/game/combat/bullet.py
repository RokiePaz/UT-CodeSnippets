import pygame
from dataclasses import dataclass


@dataclass
class Bullet:
    x: float
    y: float
    vx: float
    vy: float
    radius: int = 3
    color: tuple = (240, 240, 240)

    def update(self, dt: float):
        self.x += self.vx * dt
        self.y += self.vy * dt

    def draw(self, surface: pygame.Surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

    def is_offscreen(self, rect: pygame.Rect) -> bool:
        return not rect.inflate(40, 40).collidepoint(self.x, self.y)

    def collides_rect(self, rect: pygame.Rect) -> bool:
        # approximate circle-rect collision with rect inflate
        return rect.inflate(-2, -2).collidepoint(self.x, self.y)