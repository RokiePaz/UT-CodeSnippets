import pygame
from dataclasses import dataclass


@dataclass
class Heart:
    x: float
    y: float
    speed: float = 160.0
    size: int = 8
    color: tuple = (220, 60, 60)

    def rect(self) -> pygame.Rect:
        return pygame.Rect(int(self.x - self.size // 2), int(self.y - self.size // 2), self.size, self.size)

    def update(self, dt: float, bounds: pygame.Rect):
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
        r = self.rect()
        # clamp to bounds
        if r.left < bounds.left:
            self.x = bounds.left + self.size // 2
        if r.right > bounds.right:
            self.x = bounds.right - self.size // 2
        if r.top < bounds.top:
            self.y = bounds.top + self.size // 2
        if r.bottom > bounds.bottom:
            self.y = bounds.bottom - self.size // 2

    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(surface, self.color, self.rect())