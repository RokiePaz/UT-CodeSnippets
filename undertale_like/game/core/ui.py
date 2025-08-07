import pygame
from typing import Tuple


def get_font(name: str | None, size: int) -> pygame.font.Font:
    return pygame.font.Font(name, size)


def draw_text(surface: pygame.Surface, text: str, pos: Tuple[int, int], color=(255, 255, 255), font: pygame.font.Font | None = None):
    if font is None:
        font = get_font(None, 18)
    rendered = font.render(text, True, color)
    surface.blit(rendered, pos)


def draw_bordered_rect(surface: pygame.Surface, rect: pygame.Rect, fill_color, border_color, border_width: int = 2):
    pygame.draw.rect(surface, fill_color, rect)
    pygame.draw.rect(surface, border_color, rect, border_width)