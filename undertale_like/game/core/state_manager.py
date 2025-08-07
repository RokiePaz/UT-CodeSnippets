from typing import Dict, Callable
import pygame


class StateManager:
    def __init__(self, screen: pygame.Surface, scene_factories: Dict[str, Callable[[], object]], start_scene_name: str):
        self.screen = screen
        self.scene_factories = scene_factories
        self.current_scene_name = start_scene_name
        self.current_scene = self.scene_factories[self.current_scene_name]()

    def switch(self, next_name: str):
        if next_name not in self.scene_factories:
            raise ValueError(f"Unknown scene: {next_name}")
        self.current_scene_name = next_name
        self.current_scene = self.scene_factories[self.current_scene_name]()

    def handle_event(self, event: pygame.event.Event):
        self.current_scene.handle_event(event)

    def update(self, dt: float):
        self.current_scene.update(dt)
        if getattr(self.current_scene, "is_done", False) and getattr(self.current_scene, "next_scene_name", None):
            self.switch(self.current_scene.next_scene_name)

    def draw(self):
        self.current_scene.draw()