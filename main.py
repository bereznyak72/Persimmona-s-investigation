import pygame
import math
import random
from levels import Level1, Level2, Level3, Level4, Level5, Level6, Epilogue, Prologue

pygame.init()
FONT_SIZE_RATIO = {'title': 0.1, 'button': 0.05}
BUTTON_STYLE = {
    'padding': 0.025, 'radius': 0.02,
    'main_bg': (30, 30, 50, 180), 'main_hover': (0, 255, 100), 'main_normal': (200, 200, 255),
    'end_bg': (60, 40, 60, 180), 'end_hover': (255, 200, 100), 'end_normal': (255, 255, 200)
}
COLORS = {
    'main_bg': (20, 20, 40), 'main_wave': (0, 100, 150), 'main_title': (150, 200, 255),
    'end_bg': (20, 10, 30), 'end_star': (255, 200, 100), 'end_title': (255, 200, 100), 'end_shadow': (100, 50, 0)
}

class MenuBase:
    def __init__(self, width: int, height: int, title_text: str, is_main_menu: bool = True):
        self.width = width
        self.height = height
        self.is_main_menu = is_main_menu
        self.title_font = pygame.font.Font('assets/fonts/Persimmona.ttf', int(height * FONT_SIZE_RATIO['title']))
        self.button_font = pygame.font.Font('assets/fonts/Persimmona.ttf', int(height * FONT_SIZE_RATIO['button']))
        self.title = self.title_font.render(title_text, True, COLORS['main_title' if is_main_menu else 'end_title'])
        self.title_shadow = self.title_font.render(title_text, True, COLORS['end_shadow']) if not is_main_menu else None
        self.selected = -1
        self.options = []
        self.button_rects = []
        self.bg_rects = []
        self.wave_offset = 0
        self.stars = [(random.randint(0, width), random.randint(0, height), random.uniform(0.5, 1.5), random.random(),
                       random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5)) for _ in
                      range(100)] if not is_main_menu else []

    def update_visuals(self):
        if self.is_main_menu:
            self.wave_offset = (self.wave_offset + 0.02) % (2 * math.pi)
        else:
            for i, (x, y, size, alpha, dx, dy) in enumerate(self.stars):
                x += dx
                y += dy
                alpha = max(0.0, min(1.0, alpha + random.uniform(-0.05, 0.05)))
                if not (0 <= x <= self.width and 0 <= y <= self.height):
                    x, y, dx, dy = random.randint(0, self.width), random.randint(0, self.height), random.uniform(-0.5,
                                                                                                                 0.5), random.uniform(
                        -0.5, 0.5)
                self.stars[i] = (x, y, size, alpha, dx, dy)

    def draw_background(self, screen):
        if self.is_main_menu:
            screen.fill(COLORS['main_bg'])
            for y in range(0, self.height, 4):
                for x in range(0, self.width, 4):
                    wave = math.sin(x / self.width * 4 * math.pi + self.wave_offset + y / self.height * math.pi)
                    intensity = (wave + 1) / 2
                    color = tuple(int(c * intensity) for c in COLORS['main_wave'])
                    pygame.draw.rect(screen, color, (x, y, 4, 4))
        else:
            screen.fill(COLORS['end_bg'])
            for x, y, size, alpha, _, _ in self.stars:
                pygame.draw.circle(screen, (*COLORS['end_star'][:3], int(255 * alpha)), (x, y), size)

    def draw_button(self, screen, text: str, y_pos: float, index: int):
        style_prefix = 'main' if self.is_main_menu else 'end'
        color = BUTTON_STYLE[f'{style_prefix}_hover'] if self.selected == index else BUTTON_STYLE[
            f'{style_prefix}_normal']
        surface = self.button_font.render(text, True, color)
        if self.selected == index:
            surface = pygame.transform.smoothscale(surface,
                                                   (int(surface.get_width() * 1.1), int(surface.get_height() * 1.1)))
        rect = surface.get_rect(center=(self.width / 2, y_pos))
        self.button_rects.append(rect)
        padding = int(self.height * BUTTON_STYLE['padding'])
        bg_rect = rect.inflate(padding * 2, padding)
        self.bg_rects.append(bg_rect)
        pygame.draw.rect(screen, BUTTON_STYLE[f'{style_prefix}_bg'], bg_rect,
                         border_radius=int(self.height * BUTTON_STYLE['radius']))
        if self.selected == index:
            pygame.draw.rect(screen, BUTTON_STYLE[f'{style_prefix}_hover'], bg_rect, 2,
                             border_radius=int(self.height * BUTTON_STYLE['radius']))
        screen.blit(surface, surface.get_rect(center=bg_rect.center))

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_DOWN):
                self.selected = (self.selected + (1 if event.key == pygame.K_DOWN else -1)) % len(self.options)
            elif event.key == pygame.K_RETURN and self.selected >= 0:
                return self.options[self.selected][1]
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i, rect in enumerate(self.bg_rects):
                if rect.collidepoint(event.pos):
                    self.selected = i
                    return self.options[i][1]
        elif event.type == pygame.MOUSEMOTION:
            self.selected = next((i for i, rect in enumerate(self.bg_rects) if rect.collidepoint(event.pos)), -1)
        return None

class MainMenu(MenuBase):
    def __init__(self, width: int, height: int):
        super().__init__(width, height, "Persimmona's Investigation", True)
        self.options = [("Start Game", "start"), ("Exit", "quit")]

    def run(self, screen):
        clock = pygame.time.Clock()
        while True:
            self.update_visuals()
            self.draw_background(screen)
            self.button_rects.clear()
            self.bg_rects.clear()
            screen.blit(self.title, self.title.get_rect(center=(self.width / 2, self.height * 0.25)))
            for i, (text, _) in enumerate(self.options):
                self.draw_button(screen, text, self.height * (0.5 + i * 0.15), i)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if result := self.handle_input(event):
                    return result
            pygame.display.flip()
            clock.tick(60)

class EndScreen(MenuBase):
    def __init__(self, width: int, height: int):
        super().__init__(width, height, "Game Completed!", False)
        self.options = [("Main Menu", "menu"), ("Exit", "quit")]

    def run(self, screen):
        clock = pygame.time.Clock()
        while True:
            self.update_visuals()
            self.draw_background(screen)
            self.button_rects.clear()
            self.bg_rects.clear()
            title_rect = self.title.get_rect(center=(self.width / 2, self.height * 0.25))
            screen.blit(self.title_shadow, (title_rect.x + 5, title_rect.y + 5))
            screen.blit(self.title, title_rect)
            for i, (text, _) in enumerate(self.options):
                self.draw_button(screen, text, self.height * (0.5 + i * 0.15), i)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if result := self.handle_input(event):
                    return result
            pygame.display.flip()
            clock.tick(60)

def main():
    info = pygame.display.Info()
    screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN)
    pygame.display.set_caption("Persimmona's Investigation")
    
    try:
        icon = pygame.image.load('assets/images/logo.png')
        pygame.display.set_icon(icon)
    except pygame.error as e:
        print(f"Warning: Could not load icon 'assets/images/logo.png': {e}")

    clock = pygame.time.Clock()
    while True:
        main_menu = MainMenu(*screen.get_size())
        result = main_menu.run(screen)
        if result == "quit":
            break
        elif result == "start":
            levels = [Prologue(*screen.get_size()), Level1(*screen.get_size()), Level2(*screen.get_size()),
                      Level3(*screen.get_size()), Level4(), Level5(*screen.get_size()), Level6(), Epilogue(*screen.get_size())]
            for level in levels:
                while not level.is_completed():
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            return
                        level.handle_event(event)
                    screen.fill(COLORS['end_bg'])
                    level.run(screen)
                    pygame.display.flip()
                    clock.tick(60)
            if EndScreen(*screen.get_size()).run(screen) == "quit":
                break
    pygame.quit()

if __name__ == "__main__":
    main()