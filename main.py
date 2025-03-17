import pygame
from levels import Level1, Level2, Level3, Level4, Level5, Level6, Epilogue, Prologue

# Константы
pygame.init()
DEFAULT_RESOLUTION = pygame.display.Info()
FONT_LARGE_SIZE = 0.1
FONT_SMALL_SIZE = 0.06
BUTTON_PADDING = 0.015
BUTTON_RADIUS = 0.01


class MainMenu:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.Font(None, int(self.screen_height * FONT_LARGE_SIZE))
        self.small_font = pygame.font.Font(None, int(self.screen_height * FONT_SMALL_SIZE))
        self.selected = 0
        self.options = ["Начать игру", "Настройки", "Выход"]
        self.button_rects = []
        self.title_surface = self.font.render("Persimmona's Investigation", True, (255, 255, 255))
        self.title_shadow_surface = self.font.render("Persimmona's Investigation", True, (100, 100, 100))

    def run(self, screen):
        clock = pygame.time.Clock()
        running = True
        while running:
            screen.fill((20, 20, 20))
            self.button_rects.clear()

            title_rect = self.title_surface.get_rect(center=(self.screen_width / 2, self.screen_height * 0.25))
            screen.blit(self.title_shadow_surface, (title_rect.x + 3, title_rect.y + 3))
            screen.blit(self.title_surface, title_rect)

            for i, option in enumerate(self.options):
                color = (0, 255, 0) if self.selected == i else (255, 255, 255)
                text = self.small_font.render(option, True, color)
                text_rect = text.get_rect(center=(self.screen_width / 2, self.screen_height * (0.4 + i * 0.15)))
                self.button_rects.append(text_rect)
                padding = int(self.screen_height * BUTTON_PADDING)
                pygame.draw.rect(screen, (50, 50, 50), text_rect.inflate(padding * 2, padding),
                                 border_radius=int(self.screen_height * BUTTON_RADIUS))
                screen.blit(text, text_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected = (self.selected - 1) % len(self.options)
                    elif event.key == pygame.K_DOWN:
                        self.selected = (self.selected + 1) % len(self.options)
                    elif event.key == pygame.K_RETURN:
                        return ["start", "settings", "quit"][self.selected]
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for i, rect in enumerate(self.button_rects):
                        if rect.collidepoint(event.pos):
                            return ["start", "settings", "quit"][i]
                elif event.type == pygame.MOUSEMOTION:
                    for i, rect in enumerate(self.button_rects):
                        if rect.collidepoint(event.pos):
                            self.selected = i

            pygame.display.flip()
            clock.tick(60)


class SettingsMenu:
    def __init__(self, screen_width, screen_height, current_resolution):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.Font(None, int(self.screen_height * FONT_LARGE_SIZE))
        self.small_font = pygame.font.Font(None, int(self.screen_height * FONT_SMALL_SIZE))
        self.selected = 0
        self.resolutions = [(800, 600), (1024, 768), (1280, 720), (1920, 1080)]
        self.current_resolution = current_resolution
        self.button_rects = []
        self.title_surface = self.font.render("Настройки", True, (255, 255, 255))
        self.show_resolutions = False  # Флаг для выпадающего списка

    def run(self, screen):
        clock = pygame.time.Clock()
        running = True
        new_resolution = self.current_resolution  # Временное хранение выбранного разрешения

        while running:
            screen.fill((20, 20, 20))
            self.button_rects.clear()

            # Заголовок
            title_rect = self.title_surface.get_rect(center=(self.screen_width / 2, self.screen_height * 0.25))
            screen.blit(self.title_surface, title_rect)

            # Пункт "Выбрать разрешение"
            res_text = f"Выбрать разрешение: {new_resolution[0]}x{new_resolution[1]}"
            color = (0, 255, 0) if self.selected == 0 else (255, 255, 255)
            text = self.small_font.render(res_text, True, color)
            text_rect = text.get_rect(center=(self.screen_width / 2, self.screen_height * 0.4))
            self.button_rects.append(text_rect)
            padding = int(self.screen_height * BUTTON_PADDING)
            pygame.draw.rect(screen, (50, 50, 50), text_rect.inflate(padding * 2, padding),
                             border_radius=int(self.screen_height * BUTTON_RADIUS))
            screen.blit(text, text_rect)

            # Выпадающий список разрешений
            if self.show_resolutions:
                for i, resolution in enumerate(self.resolutions, start=1):
                    color = (0, 255, 0) if self.selected == i else (255, 255, 255)
                    text = self.small_font.render(f"{resolution[0]}x{resolution[1]}", True, color)
                    text_rect = text.get_rect(
                        center=(self.screen_width / 2, self.screen_height * (0.5 + (i - 1) * 0.1)))
                    self.button_rects.append(text_rect)
                    pygame.draw.rect(screen, (50, 50, 50), text_rect.inflate(padding * 2, padding),
                                     border_radius=int(self.screen_height * BUTTON_RADIUS))
                    screen.blit(text, text_rect)

            # Кнопка "Применить изменения"
            apply_text = "Применить изменения"
            color = (0, 255, 0) if self.selected == (1 + len(self.resolutions) if self.show_resolutions else 1) else (
            255, 255, 255)
            text = self.small_font.render(apply_text, True, color)
            apply_rect = text.get_rect(center=(self.screen_width / 2, self.screen_height * (
                0.7 if not self.show_resolutions else 0.5 + len(self.resolutions) * 0.1)))
            self.button_rects.append(apply_rect)
            pygame.draw.rect(screen, (50, 50, 50), apply_rect.inflate(padding * 2, padding),
                             border_radius=int(self.screen_height * BUTTON_RADIUS))
            screen.blit(text, apply_rect)

            # Кнопка "Назад"
            back_text = "Назад"
            color = (0, 255, 0) if self.selected == (2 + len(self.resolutions) if self.show_resolutions else 2) else (
            255, 255, 255)
            text = self.small_font.render(back_text, True, color)
            back_rect = text.get_rect(center=(self.screen_width / 2, self.screen_height * (
                0.8 if not self.show_resolutions else 0.6 + len(self.resolutions) * 0.1)))
            self.button_rects.append(back_rect)
            pygame.draw.rect(screen, (50, 50, 50), back_rect.inflate(padding * 2, padding),
                             border_radius=int(self.screen_height * BUTTON_RADIUS))
            screen.blit(text, back_rect)

            # Обработка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                elif event.type == pygame.KEYDOWN:
                    max_options = 2 + len(self.resolutions) if self.show_resolutions else 2
                    if event.key == pygame.K_UP:
                        self.selected = (self.selected - 1) % (max_options + 1)
                    elif event.key == pygame.K_DOWN:
                        self.selected = (self.selected + 1) % (max_options + 1)
                    elif event.key == pygame.K_RETURN:
                        if self.selected == 0:
                            self.show_resolutions = not self.show_resolutions
                        elif self.show_resolutions and 1 <= self.selected <= len(self.resolutions):
                            new_resolution = self.resolutions[self.selected - 1]
                            self.show_resolutions = False
                            self.selected = 0
                        elif self.selected == (1 + len(self.resolutions) if self.show_resolutions else 1):
                            return new_resolution  # Применить изменения
                        elif self.selected == (2 + len(self.resolutions) if self.show_resolutions else 2):
                            return "back"  # Назад в главное меню
                    elif event.key == pygame.K_ESCAPE:
                        return "back"
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    clicked_outside = True
                    for i, rect in enumerate(self.button_rects):
                        if rect.collidepoint(event.pos):
                            clicked_outside = False
                            self.selected = i
                            if i == 0:
                                self.show_resolutions = not self.show_resolutions
                            elif self.show_resolutions and 1 <= i <= len(self.resolutions):
                                new_resolution = self.resolutions[i - 1]
                                self.show_resolutions = False
                                self.selected = 0
                            elif i == (1 + len(self.resolutions) if self.show_resolutions else 1):
                                return new_resolution
                            elif i == (2 + len(self.resolutions) if self.show_resolutions else 2):
                                return "back"
                    if self.show_resolutions and clicked_outside:
                        self.show_resolutions = False
                        self.selected = 0
                elif event.type == pygame.MOUSEMOTION:
                    for i, rect in enumerate(self.button_rects):
                        if rect.collidepoint(event.pos):
                            self.selected = i

            pygame.display.flip()
            clock.tick(60)


class EndScreen:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.Font(None, int(self.screen_height * FONT_LARGE_SIZE))
        self.small_font = pygame.font.Font(None, int(self.screen_height * FONT_SMALL_SIZE))
        self.selected = 0
        self.options = ["Главное меню", "Выход"]
        self.button_rects = []
        self.title_surface = self.font.render("Игра завершена!", True, (255, 255, 255))

    def run(self, screen):
        clock = pygame.time.Clock()
        running = True
        while running:
            screen.fill((20, 20, 20))
            self.button_rects.clear()

            title_rect = self.title_surface.get_rect(center=(self.screen_width / 2, self.screen_height * 0.25))
            screen.blit(self.title_surface, title_rect)

            for i, option in enumerate(self.options):
                color = (0, 255, 0) if self.selected == i else (255, 255, 255)
                text = self.small_font.render(option, True, color)
                text_rect = text.get_rect(center=(self.screen_width / 2, self.screen_height * (0.4 + i * 0.15)))
                self.button_rects.append(text_rect)
                padding = int(self.screen_height * BUTTON_PADDING)
                pygame.draw.rect(screen, (50, 50, 50), text_rect.inflate(padding * 2, padding),
                                 border_radius=int(self.screen_height * BUTTON_RADIUS))
                screen.blit(text, text_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected = (self.selected - 1) % 2
                    elif event.key == pygame.K_DOWN:
                        self.selected = (self.selected + 1) % 2
                    elif event.key == pygame.K_RETURN:
                        return ["menu", "quit"][self.selected]
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for i, rect in enumerate(self.button_rects):
                        if rect.collidepoint(event.pos):
                            return ["menu", "quit"][i]
                elif event.type == pygame.MOUSEMOTION:
                    for i, rect in enumerate(self.button_rects):
                        if rect.collidepoint(event.pos):
                            self.selected = i

            pygame.display.flip()
            clock.tick(60)


def main():
    info = pygame.display.Info()
    current_resolution = [info.current_w, info.current_h]
    screen = pygame.display.set_mode(current_resolution, pygame.FULLSCREEN)
    pygame.display.set_caption("Persimmona's Investigation")
    clock = pygame.time.Clock()

    running = True
    while running:
        menu = MainMenu(current_resolution[0], current_resolution[1])
        menu_result = menu.run(screen)

        if menu_result == "quit":
            running = False
            break
        elif menu_result == "settings":
            while True:  # Цикл для возврата в настройки
                settings = SettingsMenu(current_resolution[0], current_resolution[1], current_resolution)
                settings_result = settings.run(screen)
                if settings_result == "quit":
                    running = False
                    break
                elif settings_result == "back":
                    break  # Возврат в главное меню
                elif settings_result:
                    current_resolution[0], current_resolution[1] = settings_result
                    screen = pygame.display.set_mode(current_resolution, pygame.FULLSCREEN)
                    break
            if not running:
                break
            continue

        levels = [Prologue(current_resolution[0], current_resolution[1]), Level1(current_resolution[0], current_resolution[1]),
                  Level2(), Level3(),
                  Level4(), Level5(),
                  Level6(), Epilogue()]
        current_level_index = 0

        while current_level_index < len(levels):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
                levels[current_level_index].handle_event(event)

            if not running:
                break

            levels[current_level_index].run(screen)
            if levels[current_level_index].is_completed():
                current_level_index += 1

            pygame.display.flip()
            clock.tick(60)

        if not running:
            break

        end_screen = EndScreen(current_resolution[0], current_resolution[1])
        end_result = end_screen.run(screen)

        if end_result == "quit":
            running = False

    pygame.quit()


if __name__ == "__main__":
    main()
