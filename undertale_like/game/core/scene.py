from abc import ABC, abstractmethod
import pygame


class Scene(ABC):
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.is_done = False
        self.next_scene_name = None

    @abstractmethod
    def handle_event(self, event: pygame.event.Event):
        pass

    @abstractmethod
    def update(self, dt: float):
        pass

    @abstractmethod
    def draw(self):
        pass