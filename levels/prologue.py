import pygame


class Prologue:
    def __init__(self, screen_width, screen_height):
        self.completed = False
        self.number = 1
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.Font('assets/fonts/Persimmona.ttf', int(self.screen_height * 0.035))
        #self.font = pygame.font.SysFont("Arial", int(self.screen_height * 0.035), bold=False)
        self.text_animation_speed = 15
        self.last_char_time = 0
        self.current_text = ""
        self.full_text = ""
        self.scenes = {
            "intro": self.main_scene,
            "question": self.main_scene,
            "outro": self.main_scene,
        }
        self.current_scene = "intro"
        self.char_index = 0
        self.text_lines = []
        self.presenter_text = (
            "Добрый вечер, уважаемые дамы и господа!",
            "Вы смотрите шоу о самых известных жителях нашей страны.",
            "Сегодня у нас в гостях самый известный детектив — Персиммона!",
        )
        self.presenter_question = ("Персиммона, скажите, как же вы обрели такую известность?",)
        self.persimmona_text = (
            "О, да, я точно помню день, когда это произошло,",
            "это было одно из самых интересных расследований в моей жизни!",
            "Вообщем, дело было так..."
        )
        self.start_text_animation(self.presenter_text)
        self.text_area_height = 150
        self.persimmona_image = pygame.image.load("assets/images/persimmona.png").convert_alpha()
        self.presenter_image = pygame.image.load("assets/images/presenter.png").convert_alpha()
        self.background_image = pygame.image.load("assets/images/interview_background.jpg").convert_alpha()
        reference_width, reference_height = 1920, 1080
        target_persimmona_width, target_persimmona_height = 316, 606
        target_presenter_width, target_presenter_height = 516, 516
        #target_background_width, target_background_height = self.screen_width, self.screen_height
        width_scale = self.screen_width / reference_width
        height_scale = self.screen_height / reference_height
        scale_factor = min(width_scale, height_scale)
        new_persimmona_width = max(int(target_persimmona_width * scale_factor), 50)
        new_persimmona_height = max(int(target_persimmona_height * scale_factor), 96)
        new_presenter_width = max(int(target_presenter_width * scale_factor), 50)
        new_presenter_height = max(int(target_presenter_height * scale_factor), 96)
        new_background_width = self.screen_width
        new_background_height = self.screen_height - 200 # Костыль
        self.persimmona_image = pygame.transform.scale(self.persimmona_image, (new_persimmona_width, new_persimmona_height))
        self.presenter_image = pygame.transform.scale(self.presenter_image, (new_presenter_width, new_presenter_height))
        self.background_image = pygame.transform.scale(self.background_image, (new_background_width, new_background_height))       
        self.background_rect = pygame.Rect(0, 0, self.screen_width, self.screen_height)
        self.persimmona_rect = pygame.Rect(self.screen_width - new_persimmona_width, self.screen_height - new_persimmona_height, new_persimmona_width, new_persimmona_height) # Работает только с максимальным разрешением
        self.presenter_rect = pygame.Rect(self.screen_width - new_presenter_width + 120, self.screen_height - new_presenter_height + 100, new_presenter_width, new_presenter_height) # Работает только с максимальным разрешением
        self.persimmona_text_max_width = self.screen_width - new_persimmona_width - 60 # Работает только с максимальным разрешением
        self.presenter_text_max_width = self.screen_width - new_presenter_width - 60 # Работает только с максимальным разрешением



    def start_text_animation(self, text):
        self.text_lines = text if isinstance(text, (list, tuple)) else [text]
        self.full_text = " ".join(self.text_lines)
        self.current_text = ""
        self.char_index = 0
        self.last_char_time = pygame.time.get_ticks()


    def update_text_animation(self, current_time):
        if current_time - self.last_char_time >= self.text_animation_speed and self.char_index < len(self.full_text):
            self.current_text = self.full_text[:self.char_index + 1]
            self.char_index += 1
            self.last_char_time = current_time


    def run(self, screen):
        current_time = pygame.time.get_ticks()
        self.update_text_animation(current_time)
        screen.fill((20, 20, 20))
        self.scenes[self.current_scene](screen)
        if self.current_scene not in ("intro", "question"):
            screen.blit(self.persimmona_image, self.persimmona_rect)
        else:
            screen.blit(self.presenter_image, self.presenter_rect)
        

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.current_text == self.full_text:
            if self.current_scene == "intro":
                self.start_text_animation(self.presenter_question)
                self.current_scene = "question"
            elif self.current_scene == "question":
                self.start_text_animation(self.persimmona_text)
                self.current_scene = "outro"
            elif self.current_scene == "outro":
                self.completed = True
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.completed = True


    def is_completed(self):
        return self.completed


    def render_text(self, screen, text, y_pos, center=False):
        lines = self.wrap_text(text, self.presenter_text_max_width - 75) # Костыль
        for i, line in enumerate(lines):
            text_surface = self.font.render(line, True, (255, 255, 255))
            if center:
                text_rect = text_surface.get_rect(center=(self.screen_width // 2, y_pos + i * 40))
            else:
                text_rect = text_surface.get_rect(topleft=(50, y_pos + i * 40))
            screen.blit(text_surface, text_rect)


    def wrap_text(self, text, max_width):
        words = text.split(" ")
        lines = []
        current_line = ""
        for word in words:
            test_line = current_line + word + " "
            if self.font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line.strip())
                current_line = word + " "
        if current_line:
            lines.append(current_line.strip())
        return lines


    def main_scene(self, screen):
        screen.blit(self.background_image, self.background_rect)
        self.render_text(screen, self.current_text, self.screen_height - self.text_area_height + 20, center=True)
