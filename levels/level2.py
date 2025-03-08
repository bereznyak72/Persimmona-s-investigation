import pygame

class Level2:
    def __init__(self):
        self.completed = False

    def run(self, screen):
        screen.fill((0, 255, 0))
        font = pygame.font.Font(None, 74)
        text = font.render("Level 2", True, (255, 255, 255))
        screen.blit(text, (250, 250))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.completed = True

    def is_completed(self):
        return self.completed