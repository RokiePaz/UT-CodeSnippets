import pygame
import sys
from game.settings import WIDTH, HEIGHT, FPS, TITLE
from game.core.state_manager import StateManager
from game.overworld.world import OverworldScene
from game.combat.battle import BattleScene


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.state = StateManager(
            self.screen,
            scene_factories={
                "overworld": lambda: OverworldScene(self.screen),
                "battle": lambda: BattleScene(self.screen),
            },
            start_scene_name="overworld",
        )

    def run(self):
        while True:
            dt = self.clock.tick(FPS) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                self.state.handle_event(event)
            self.state.update(dt)
            self.state.draw()
            pygame.display.flip()


if __name__ == "__main__":
    Game().run()