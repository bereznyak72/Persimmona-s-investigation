import pygame

class Level1:
    def __init__(self):
        self.completed = False

    def run(self, screen):
        screen.fill((0, 0, 255))
        font = pygame.font.Font(None, 74)
        text = font.render("Level 1", True, (255, 255, 255))
        screen.blit(text, (250, 250))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.completed = True

    def is_completed(self):
        return self.completed