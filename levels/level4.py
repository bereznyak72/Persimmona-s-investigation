import pygame
from levels import memory_game


class Level4:
    def __init__(self):
        self.completed = False

    def run(self, screen):
        screen.fill((75, 75, 75))
        font = pygame.font.Font(None, 36)
        text = font.render("Level 4", True, (255, 255, 255))
        screen.blit(text, (200, 250))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.completed = True

    def is_completed(self):
        return self.completed

    # memory_game.main()
