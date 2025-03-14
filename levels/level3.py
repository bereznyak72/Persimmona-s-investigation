import pygame


class Level3:
    def __init__(self):
        self.completed = False

    def run(self, screen):
        screen.fill((200, 200, 200))
        font = pygame.font.Font(None, 36)
        text = font.render("Level 3", True, (0, 0, 0))
        screen.blit(text, (200, 250))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.completed = True

    def is_completed(self):
        return self.completed
