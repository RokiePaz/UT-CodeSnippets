import json
import os
import pygame
from typing import List
from game.settings import WIDTH, HEIGHT, DIALOG_BOX_COLOR, DIALOG_BOX_BORDER, DIALOG_TEXT_COLOR, FONT_NAME, FONT_SIZE
from game.core.ui import draw_bordered_rect, get_font


class DialogueBox:
    def __init__(self, lines: List[str]):
        self.lines = lines
        self.current_index = 0
        self.char_progress = 0
        self.done = False
        self.font = get_font(FONT_NAME, FONT_SIZE)
        self.box_rect = pygame.Rect(16, HEIGHT - 140, WIDTH - 32, 124)
        self.chars_per_second = 90

    def advance(self):
        if self.done:
            return
        if self.char_progress < len(self.current_line()):
            self.char_progress = len(self.current_line())
        else:
            self.current_index += 1
            self.char_progress = 0
            if self.current_index >= len(self.lines):
                self.done = True

    def current_line(self) -> str:
        if self.current_index < len(self.lines):
            return self.lines[self.current_index]
        return ""

    def update(self, dt: float):
        if self.done:
            return
        self.char_progress = min(len(self.current_line()), self.char_progress + int(self.chars_per_second * dt))

    def draw(self, surface: pygame.Surface):
        draw_bordered_rect(surface, self.box_rect, DIALOG_BOX_COLOR, DIALOG_BOX_BORDER, 3)
        if self.done:
            return
        text_to_show = self.current_line()[: self.char_progress]
        y = self.box_rect.y + 16
        for line in wrap_text(text_to_show, self.font, self.box_rect.width - 24):
            surface.blit(self.font.render(line, True, DIALOG_TEXT_COLOR), (self.box_rect.x + 12, y))
            y += self.font.get_linesize()


def wrap_text(text: str, font: pygame.font.Font, max_width: int) -> List[str]:
    words = text.split(" ")
    lines: List[str] = []
    current = ""
    for word in words:
        test = word if current == "" else current + " " + word
        if font.size(test)[0] <= max_width:
            current = test
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def load_dialogue_lines(data_dir: str, name: str) -> List[str]:
    path = os.path.join(data_dir, "dialogues", f"{name}.json")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    # Expect { "lines": ["..."] }
    if not isinstance(data, dict) or "lines" not in data:
        return ["..."]
    return [str(x) for x in data["lines"]]