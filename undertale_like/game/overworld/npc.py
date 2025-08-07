import pygame
from dataclasses import dataclass


@dataclass
class NPC:
    x: int
    y: int
    size: int = 16
    color: tuple = (70, 180, 240)

    def rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.size, self.size)

    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(surface, self.color, self.rect())