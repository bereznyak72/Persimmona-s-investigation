import pygame


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
    """
    def __init__(self, screen_width, screen_height):
        self.completed = False
        self.number = 1
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.SysFont("Arial", int(self.screen_height * 0.035), bold=False)
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


    def run(self, screen):
        screen.fill((50, 50, 50))
        font = pygame.font.Font(None, 36)
        text = font.render("Level 4", True, (255, 255, 255))
        screen.blit(text, (200, 250))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.completed = True

    def is_completed(self):
        return self.completed
"""
