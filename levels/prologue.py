import pygame


class Prologue:
    def __init__(self, screen_width, screen_height):
        self.completed = False
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.SysFont("Arial", int(self.screen_height * 0.035), bold=False)
        self.text_animation_speed = 15
        self.last_char_time = 0
        self.current_text = ""
        self.full_text = ""
        self.char_index = 0
        self.text_lines = []
        self.intro_text = (
            "Добрый вечер, уважаемые дамы и господа!",
            "Вы смотрите шоу о самых известных жителях нашей страны.",
            "Сегодня у нас в гостях самый известный детектив — Персиммона!"
        )
        self.outro_text = (
            "О, да, я точно помню день когда это произошло,",
            "это было одно из самых интересных расследований в моей жизни!",
            "Вообщем, дело было так..."
        )
        self.start_text_animation(self.intro_text)
        self.text_area_height = 150
        self.character_image = pygame.image.load("assets/images/persimmona.png").convert_alpha()
        reference_width, reference_height = 1920, 1080
        target_character_width, target_character_height = 316, 606
        width_scale = self.screen_width / reference_width
        height_scale = self.screen_height / reference_height
        scale_factor = min(width_scale, height_scale)
        new_width = int(target_character_width * scale_factor)
        new_height = int(target_character_height * scale_factor)
        new_width = max(new_width, 50)
        new_height = max(new_height, 96)
        self.character_image = pygame.transform.scale(self.character_image, (new_width, new_height))
        self.character_rect = pygame.Rect(self.screen_width - new_width, self.screen_height - new_height, new_width, new_height)
        self.text_max_width = self.screen_width - new_width - 60



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
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 36)
        text = font.render("Prologue", True, (255, 255, 255))
        screen.blit(self.character_image, self.character_rect) # text, (200, 250)

        current_time = pygame.time.get_ticks()
        self.update_text_animation(current_time)
        screen.fill((20, 20, 20))
        

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.current_text == self.full_text:
            pos = event.pos
            

            self.completed = True

    def is_completed(self):
        return self.completed
