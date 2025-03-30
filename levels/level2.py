import pygame
from utils import *
import random


class FootprintTask:
    def __init__(self, screen_width, screen_height, font, text_area_height, text_max_width):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = font
        self.text_area_height = text_area_height
        self.text_max_width = text_max_width
        self.completed = False
        self.task_active = False
        self.waiting_for_click = True
        self.stage = 1
        
        self.foot_template = [
            (screen_width // 2 - 180, screen_height // 2 + 120),
            (screen_width // 2 - 160, screen_height // 2 + 140),
            (screen_width // 2 - 130, screen_height // 2 + 160),
            (screen_width // 2 - 100, screen_height // 2 + 170),
            (screen_width // 2 - 70, screen_height // 2 + 175),
            (screen_width // 2 - 40, screen_height // 2 + 170),
            (screen_width // 2 - 10, screen_height // 2 + 160),
            (screen_width // 2 + 20, screen_height // 2 + 150),
            (screen_width // 2 + 50, screen_height // 2 + 140),
            (screen_width // 2 + 80, screen_height // 2 + 130),
            (screen_width // 2 + 110, screen_height // 2 + 120),
            (screen_width // 2 + 140, screen_height // 2 + 90),
            (screen_width // 2 + 150, screen_height // 2 + 60),
            (screen_width // 2 + 155, screen_height // 2 + 30),
            (screen_width // 2 + 165, screen_height // 2),
            (screen_width // 2 + 170, screen_height // 2 - 30),
            (screen_width // 2 + 165, screen_height // 2 - 60),
            (screen_width // 2 + 150, screen_height // 2 - 90),
            (screen_width // 2 + 130, screen_height // 2 - 110),
            (screen_width // 2 + 100, screen_height // 2 - 120),
            (screen_width // 2 + 70, screen_height // 2 - 130),
            (screen_width // 2 + 40, screen_height // 2 - 140),
            (screen_width // 2 + 10, screen_height // 2 - 145),
            (screen_width // 2 - 20, screen_height // 2 - 140),
            (screen_width // 2 - 50, screen_height // 2 - 135),
            (screen_width // 2 - 80, screen_height // 2 - 130),
            (screen_width // 2 - 110, screen_height // 2 - 125),
            (screen_width // 2 - 140, screen_height // 2 - 120),
            (screen_width // 2 - 170, screen_height // 2 - 115),
            (screen_width // 2 - 200, screen_height // 2 - 100),
            (screen_width // 2 - 220, screen_height // 2 - 85),
            (screen_width // 2 - 230, screen_height // 2 - 50),
            (screen_width // 2 - 225, screen_height // 2 - 20),
            (screen_width // 2 - 210, screen_height // 2 + 20),
            (screen_width // 2 - 195, screen_height // 2 + 60),
            (screen_width // 2 - 180, screen_height // 2 + 100)
        ]

        self.hand_template = [
            (screen_width // 2 - 160, screen_height // 2 + 100),
            (screen_width // 2 - 140, screen_height // 2 + 120),
            (screen_width // 2 - 110, screen_height // 2 + 135),
            (screen_width // 2 - 80, screen_height // 2 + 145),
            (screen_width // 2 - 50, screen_height // 2 + 150),
            (screen_width // 2 - 20, screen_height // 2 + 155),
            (screen_width // 2 + 10, screen_height // 2 + 155),
            (screen_width // 2 + 40, screen_height // 2 + 150),
            (screen_width // 2 + 70, screen_height // 2 + 140),
            (screen_width // 2 + 100, screen_height // 2 + 130),
            (screen_width // 2 + 130, screen_height // 2 + 110),
            (screen_width // 2 + 160, screen_height // 2 + 80),
            (screen_width // 2 + 180, screen_height // 2 + 50),
            (screen_width // 2 + 200, screen_height // 2 + 20),
            (screen_width // 2 + 210, screen_height // 2 - 10),
            (screen_width // 2 + 205, screen_height // 2 - 40),
            (screen_width // 2 + 190, screen_height // 2 - 70),
            (screen_width // 2 + 170, screen_height // 2 - 100),
            (screen_width // 2 + 140, screen_height // 2 - 120),
            (screen_width // 2 + 110, screen_height // 2 - 130),
            (screen_width // 2 + 80, screen_height // 2 - 140),
            (screen_width // 2 + 50, screen_height // 2 - 150),
            (screen_width // 2 + 20, screen_height // 2 - 160),
            (screen_width // 2 - 10, screen_height // 2 - 170),
            (screen_width // 2 - 40, screen_height // 2 - 180),
            (screen_width // 2 - 70, screen_height // 2 - 170),
            (screen_width // 2 - 100, screen_height // 2 - 160),
            (screen_width // 2 - 130, screen_height // 2 - 150),
            (screen_width // 2 - 160, screen_height // 2 - 140),
            (screen_width // 2 - 180, screen_height // 2 - 110),
            (screen_width // 2 - 190, screen_height // 2 - 80),
            (screen_width // 2 - 195, screen_height // 2 - 50),
            (screen_width // 2 - 190, screen_height // 2 - 20),
            (screen_width // 2 - 180, screen_height // 2 + 20),
            (screen_width // 2 - 170, screen_height // 2 + 60)
        ]

        self.current_template = self.foot_template
        self.player_path = []
        self.drawing = False
        self.covered_points = []
        self.current_point_index = 0

        self.max_deviation = 5
        self.min_points = 50
        self.required_coverage = 0.8
        self.max_gap = 2

        self.instruction_text = "Обведи след по порядку, начиная с красной точки!"
        self.hint_font = pygame.font.Font('assets/fonts/Persimmona.ttf', int(self.screen_height * 0.035))
        self.result_text = ""
        self.current_text = ""
        self.full_text = ""
        self.char_index = 0
        self.text_animation_speed = 25
        self.last_char_time = 0
        self.success_animation = False
        self.success_timer = 0
        self.success_duration = 500

        self.background_color = (139, 69, 19)
        self.shadow_surface = pygame.Surface((screen_width, screen_height - text_area_height), pygame.SRCALPHA)
        self.shadow_surface.fill((0, 0, 0, 50))

    def start_task(self):
        self.task_active = True
        self.waiting_for_click = False
        self.player_path = []
        self.drawing = False
        self.covered_points = []
        self.current_point_index = 0
        self.result_text = ""
        self.success_animation = False
        self.start_text_animation(self.instruction_text)

    def handle_event(self, event):
        if self.waiting_for_click:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.start_task()
                return True
            return False

        if not self.task_active or self.completed:
            return False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            if self.is_near_point(pos, self.current_template[0]):
                self.drawing = True
                self.player_path = [pos]
                self.update_covered_points(pos)
            return True

        elif event.type == pygame.MOUSEMOTION and self.drawing:
            last_point = self.player_path[-1]
            new_point = event.pos
            distance = ((new_point[0] - last_point[0]) ** 2 + (new_point[1] - last_point[1]) ** 2) ** 0.5
            if distance <= self.max_gap:
                self.player_path.append(new_point)
                self.update_covered_points(new_point)
            return True

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.drawing:
            self.drawing = False
            self.check_accuracy()
            return True

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            self.player_path = []
            self.covered_points = []
            self.current_point_index = 0
            return True

        return False

    def is_near_point(self, pos, template_point):
        distance = ((pos[0] - template_point[0]) ** 2 + (pos[1] - template_point[1]) ** 2) ** 0.5
        return distance <= self.max_deviation

    def update_covered_points(self, pos):
        """Проверка точек по порядку"""
        if self.current_point_index >= len(self.current_template):
            return

        next_point = self.current_template[self.current_point_index]
        if self.is_near_point(pos, next_point):
            if self.current_point_index not in self.covered_points:
                self.covered_points.append(self.current_point_index)
            self.current_point_index += 1

    def check_accuracy(self):
        if len(self.player_path) < self.min_points:
            self.result_text = "Слишком мало точек! Попробуй ещё раз."
            self.player_path = []
            self.covered_points = []
            self.current_point_index = 0
            self.start_text_animation(self.result_text)
            return

        coverage_ratio = len(self.covered_points) / len(self.current_template)
        accuracy = coverage_ratio * 100

        if coverage_ratio >= self.required_coverage and self.current_point_index >= len(self.current_template):
            if self.stage == 1:
                self.result_text = "Первый след зарисован! Теперь обведи второй след."
                self.stage = 2
                self.current_template = self.hand_template
                self.player_path = []
                self.covered_points = []
                self.current_point_index = 0
            else:
                self.result_text = f"Отлично! Точность: {accuracy:.1f}%. Второй след зарисован!"
                self.completed = True
                self.success_animation = True
                self.success_timer = pygame.time.get_ticks()
        else:
            self.result_text = f"Пройдено: {accuracy:.1f}%. Пройди все точки по порядку!"
            self.player_path = []
            self.covered_points = []
            self.current_point_index = 0

        self.start_text_animation(self.result_text)

    def start_text_animation(self, text):
        self.full_text = text
        self.current_text = ""
        self.char_index = 0
        self.last_char_time = pygame.time.get_ticks()

    def update_text_animation(self, current_time):
        if self.char_index < len(self.full_text) and current_time - self.last_char_time >= self.text_animation_speed:
            self.current_text += self.full_text[self.char_index]
            self.char_index += 1
            self.last_char_time = current_time

    def run(self, screen):
        if self.waiting_for_click or not self.task_active:
            return

        current_time = pygame.time.get_ticks()
        self.update_text_animation(current_time)

        pygame.draw.rect(screen, self.background_color,
                         (0, 0, self.screen_width, self.screen_height - self.text_area_height))

        for x in range(0, self.screen_width, 20):
            pygame.draw.line(screen, (160, 82, 45), (x, 0), (x, self.screen_height - self.text_area_height), 1)
        for y in range(0, self.screen_height - self.text_area_height, 50):
            pygame.draw.line(screen, (160, 82, 45), (0, y), (self.screen_width, y), 1)

        shadow_points = [(x + 5, y + 5) for x, y in self.current_template]
        pygame.draw.lines(screen, (0, 0, 0, 100), True, shadow_points, 5)
        screen.blit(self.shadow_surface, (0, 0))

        pygame.draw.lines(screen, (255, 215, 0), True, self.current_template, 6)
        for i, point in enumerate(self.current_template):
            if i == self.current_point_index and i not in self.covered_points:
                pygame.draw.circle(screen, COLORS["RED"], point, 6)
            else:
                color = (0, 255, 0, 200) if i in self.covered_points else (255, 255, 255, 150)
                pygame.draw.circle(screen, color, point, 6)
                pygame.draw.circle(screen, COLORS["WHITE"], point, 6, 1)

        if len(self.player_path) > 1:
            pygame.draw.lines(screen, (0, 0, 255, 200), False, self.player_path, 5)
            for i in range(1, len(self.player_path)):
                pygame.draw.circle(screen, (0, 0, 255, 100), self.player_path[i], 3)

        progress = len(self.covered_points) / len(self.current_template)
        bar_width = 300
        bar_height = 40
        bar_x = (self.screen_width - bar_width) // 2
        bar_y = self.screen_height - self.text_area_height - 50
        pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height), border_radius=5)
        pygame.draw.rect(screen, (0, 255, 0, 200), (bar_x, bar_y, bar_width * progress, bar_height), border_radius=5)
        pygame.draw.rect(screen, (255, 255, 255, 150), (bar_x, bar_y, bar_width, bar_height), 2, border_radius=5)
        progress_text = self.font.render(f"{int(progress * 100)}%", True, COLORS["WHITE"])
        screen.blit(progress_text, progress_text.get_rect(center=(bar_x + bar_width // 2, bar_y + bar_height // 2)))

        if self.success_animation:
            if current_time - self.success_timer < self.success_duration:
                alpha = int(255 * (1 - (current_time - self.success_timer) / self.success_duration))
                overlay = pygame.Surface((self.screen_width, self.screen_height - self.text_area_height),
                                         pygame.SRCALPHA)
                overlay.fill((0, 255, 0, alpha))
                screen.blit(overlay, (0, 0))
            else:
                self.success_animation = False

        render_text(screen, self.current_text, self.font, self.screen_height - self.text_area_height + 50,
                    self.text_max_width, COLORS["WHITE"])

    def is_completed(self):
        return self.completed


class Level2:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.Font('assets/fonts/Persimmona.ttf', int(self.screen_height * 0.035))
        self.hint_font = pygame.font.Font('assets/fonts/Persimmona.ttf', int(self.screen_height * 0.03))
        self.completed = False
        self.current_scene = "intro"
        self.scenes = {
            "intro": self.intro_scene,
            "blueberry_room": self.blueberry_room_scene,
            "basement_search": self.basement_search_scene,
            "electrical_room": self.electrical_room_scene,
            "outro": self.outro_scene
        }
        self.scene_finished = False
        self.text_animation_speed = TEXT_ANIMATION_SPEED
        self.last_char_time = 0
        self.current_text = ""
        self.full_text = ""
        self.char_index = 0
        self.text_lines = []
        self.intro_text = [
            "Персиммона входит в свою контору.",
            "Там её встречает весёлый помощник, и дама в синем платье, вся на нервах.",
            "Меня обокрали прошлой ночью!",
            "У меня дома много ценного",
            "Прошу, помогите мне вернуть украденное!",
            "Я слышала, вы лучший детектив в городе.",
            "Я даже не знаю, кто мог это сделать...",
        ]
        self.outro_text = [
            "Не волнуйтесь, мы найдём вора.",
            "Кстати, ночью ограбили Булочную и Мясную неподалёку!",
            "Интересно… Пора проверить улики дальше.",
            "Это может быть связано, надо выяснить.",
            "Спасибо вам, я так надеюсь на вас!",
            "Этот ананас — всё, что осталось от моего деда…",
            "Я верю, что вы раскроете это дело.",
            "Буду ждать хороших новостей!",
        ]
        self.basement_search_text = [
            "Надо обследовать всю квартиру, каждый уголок.",
            "Я проверю второй этаж, вдруг там что-то найду!",
            "Я останусь тут, осмотрю окна ещё раз… Вдруг что пропустили.",
            "Хорошо, Кукуруза, зови если что.",
            "Эй, ребята! Тут дверь, и она заперта на магниты!",
            "Магниты? Это необычно… Надо найти способ открыть её.",
            "Где-то должны быть рубильники.",
            "Я нашёл их!"
        ]
        self.after_electrical_text = [
            "Мы открыли дверь! Теперь можно проверить комнату.",
            "Постойте… Где золотой ананас? Он был здесь!",
            "Грабитель явно побывал здесь! Он, должно быть, унёс ананас через окно.",
        ]
        self.current_line_index = 0
        start_text_animation(self, self.intro_text[self.current_line_index])
        self.text_area_height = TEXT_AREA_HEIGHT

        # Загрузка фоновых изображений
        self.backgrounds = {
            "intro": pygame.image.load('assets/images/intro_bg.jpg').convert(),
            "basement_search": pygame.image.load('assets/images/basement_bg.jpg').convert(),
            "basement_door": pygame.image.load('assets/images/basement_door_bg.jpg').convert(),
            "electrical_after": pygame.image.load('assets/images/electrical_bg.jpg').convert(),
            "outro": pygame.image.load('assets/images/basement_bg.jpg').convert(), # outro_bg
            "blueberry_footprints": pygame.image.load('assets/images/blueberry_footprints_bg.jpg').convert()
        }
        # Масштабирование изображений под размер экрана
        for key, bg in self.backgrounds.items():
            self.backgrounds[key] = pygame.transform.scale(bg, (self.screen_width, self.screen_height - self.text_area_height))

        self.characters = {
            "persimmona": pygame.image.load(ASSETS["PERSIMMONA"]).convert_alpha(),
            "corn": pygame.image.load(ASSETS["CORN"]).convert_alpha(),
            "blueberry": pygame.image.load(ASSETS["BLUEBERRY"]).convert_alpha()
        }
        self.current_character = "persimmona"

        width_scale = self.screen_width / REFERENCE_WIDTH
        height_scale = self.screen_height / REFERENCE_HEIGHT
        scale_factor = min(width_scale, height_scale)

        for char, image in self.characters.items():
            target_width, target_height = CHARACTER_SIZES[char]
            new_width = max(int(target_width * scale_factor), MIN_CHAR_WIDTH)
            new_height = max(int(target_height * scale_factor), MIN_CHAR_HEIGHT)
            self.characters[char] = pygame.transform.scale(image, (new_width, new_height))
            self.characters[char] = {
                "image": self.characters[char],
                "rect": pygame.Rect(self.screen_width - new_width, self.screen_height - new_height, new_width,
                                    new_height)
            }

        max_char_width = max(CHARACTER_SIZES[char][0] * scale_factor for char in CHARACTER_SIZES)
        self.text_max_width = self.screen_width - int(max_char_width) - 60

        self.blueberry_dialogue = "На полу следы грязи… Надо зарисовать их в блокнот."
        self.blueberry_dialogue_state = "start"

        self.footprint_task = FootprintTask(self.screen_width, self.screen_height, self.font, self.text_area_height,
                                            self.text_max_width)
        switch_size = (100, 200)
        spacing = 20
        total_width = (switch_size[0] * 5) + (spacing * 4)
        start_x = (self.screen_width - total_width) // 2
        switch_y = (self.screen_height - self.text_area_height - switch_size[1]) // 2

        self.correct_combination = [random.choice([True, False]) for _ in range(5)]
        self.electrical_items = {
            "switch1": {"rect": pygame.Rect(start_x, switch_y, switch_size[0], switch_size[1]), "state": False,
                        "animating": False, "anim_progress": 0},
            "switch2": {
                "rect": pygame.Rect(start_x + (switch_size[0] + spacing), switch_y, switch_size[0], switch_size[1]),
                "state": False, "animating": False, "anim_progress": 0},
            "switch3": {
                "rect": pygame.Rect(start_x + (switch_size[0] + spacing) * 2, switch_y, switch_size[0], switch_size[1]),
                "state": False, "animating": False, "anim_progress": 0},
            "switch4": {
                "rect": pygame.Rect(start_x + (switch_size[0] + spacing) * 3, switch_y, switch_size[0], switch_size[1]),
                "state": False, "animating": False, "anim_progress": 0},
            "switch5": {
                "rect": pygame.Rect(start_x + (switch_size[0] + spacing) * 4, switch_y, switch_size[0], switch_size[1]),
                "state": False, "animating": False, "anim_progress": 0}
        }
        self.open_button = {"rect": pygame.Rect(self.screen_width // 2 - 100, switch_y + switch_size[1] + 20, 200, 40),
                            "shaking": False, "shake_time": 0}
        self.electrical_dialogue = "Нужно подобрать правильную комбинацию рубильников!"
        self.electrical_dialogue_state = "start"
        self.lights_off = False
        self.door_unlocked = False
        self.animation_speed = 10
        self.shake_duration = 500
        self.attempts_left = 5
        self.after_electrical_dialogue_index = 0

    def reset_combination(self):
        self.correct_combination = [random.choice([True, False]) for _ in range(5)]
        self.attempts_left = 5
        for item in self.electrical_items.values():
            item["state"] = False
            item["animating"] = False
            item["anim_progress"] = 0
        self.electrical_dialogue = "Комбинация сброшена! У тебя снова 5 попыток."
        start_text_animation(self, self.electrical_dialogue)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.current_text == self.full_text:
            pos = event.pos
            if self.current_scene == "intro":
                self.current_line_index += 1
                if self.current_line_index < len(self.intro_text):
                    start_text_animation(self, self.intro_text[self.current_line_index])
                else:
                    self.current_scene = "blueberry_room"
                    self.current_character = "persimmona"
                    start_text_animation(self, self.blueberry_dialogue)
            elif self.current_scene == "outro":
                self.current_line_index += 1
                if self.current_line_index < len(self.outro_text):
                    start_text_animation(self, self.outro_text[self.current_line_index])
                else:
                    self.completed = True
            elif self.current_scene == "basement_search":
                self.current_line_index += 1
                if self.current_line_index < len(self.basement_search_text):
                    start_text_animation(self, self.basement_search_text[self.current_line_index])
                    if self.current_line_index in (0, 3, 5):
                        self.current_character = "persimmona"
                    elif self.current_line_index in (1, 4, 7):
                        self.current_character = "corn"
                    elif self.current_line_index in (2, 6):
                        self.current_character = "blueberry"
                else:
                    self.current_scene = "electrical_room"
                    self.current_character = "corn"
                    start_text_animation(self, self.electrical_dialogue)
            elif self.current_scene == "electrical_room" and self.door_unlocked and not self.scene_finished:
                self.after_electrical_dialogue_index += 1
                if self.after_electrical_dialogue_index < len(self.after_electrical_text):
                    start_text_animation(self, self.after_electrical_text[self.after_electrical_dialogue_index])
                    if self.after_electrical_dialogue_index == 1:
                        self.current_character = "blueberry"
                    elif self.after_electrical_dialogue_index == 2:
                        self.current_character = "persimmona"
                    else:
                        self.current_character = "corn"
                else:
                    self.scene_finished = True
            elif self.scene_finished:
                if self.current_scene == "blueberry_room":
                    self.current_scene = "basement_search"
                    self.scene_finished = False
                    self.current_character = "persimmona"
                    self.current_line_index = 0
                    start_text_animation(self, self.basement_search_text[self.current_line_index])
                elif self.current_scene == "electrical_room" and self.door_unlocked:
                    self.current_scene = "outro"
                    self.scene_finished = False
                    self.current_character = "persimmona"
                    self.current_line_index = 0
                    start_text_animation(self, self.outro_text[self.current_line_index])
            elif self.current_scene == "blueberry_room":
                if self.footprint_task.handle_event(event):
                    return
                if self.footprint_task.is_completed():
                    self.update_blueberry_dialogue()
            elif self.current_scene == "electrical_room" and not self.door_unlocked:
                for item, data in self.electrical_items.items():
                    if data["rect"].collidepoint(pos) and not data["animating"]:
                        data["state"] = not data["state"]
                        data["animating"] = True
                        data["anim_progress"] = 0
                        break
                if self.open_button["rect"].collidepoint(pos):
                    self.update_electrical_dialogue()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.completed = True
        elif self.current_scene == "blueberry_room":
            self.footprint_task.handle_event(event)

    def run(self, screen):
        current_time = pygame.time.get_ticks()
        update_text_animation(self, current_time)
        screen.fill(COLORS["BLACK"])
        self.scenes[self.current_scene](screen)

        if self.current_scene == "intro":
            if self.current_line_index >= 2:
                self.current_character = "blueberry"
                screen.blit(self.characters[self.current_character]["image"],
                            self.characters[self.current_character]["rect"])
        elif self.current_scene == "outro":
            if self.current_line_index == 0:
                self.current_character = "persimmona"
            elif self.current_line_index == 1:
                self.current_character = "corn"
            elif self.current_line_index in (2, 3):
                self.current_character = "persimmona"
            elif self.current_line_index >= 4:
                self.current_character = "blueberry"
            screen.blit(self.characters[self.current_character]["image"],
                        self.characters[self.current_character]["rect"])
        else:
            screen.blit(self.characters[self.current_character]["image"],
                        self.characters[self.current_character]["rect"])

        if self.current_scene == "electrical_room":
            for item, data in self.electrical_items.items():
                if data["animating"]:
                    data["anim_progress"] += self.animation_speed
                    if data["anim_progress"] >= 100:
                        data["animating"] = False
                        data["anim_progress"] = 100 if data["state"] else 0
            if self.open_button["shaking"]:
                if current_time - self.open_button["shake_time"] > self.shake_duration:
                    self.open_button["shaking"] = False
                    self.open_button["rect"].x = self.screen_width // 2 - 100
                else:
                    self.open_button["rect"].x = (self.screen_width // 2 - 100) + (
                        5 if (current_time // 50) % 2 == 0 else -5)

    def is_completed(self):
        return self.completed

    def intro_scene(self, screen):
        screen.blit(self.backgrounds["intro"], (0, 0))
        pygame.draw.rect(screen, COLORS["BLACK"],
                         (0, self.screen_height - self.text_area_height, self.screen_width, self.text_area_height))
        render_text(screen, self.current_text, self.font, self.screen_height - self.text_area_height + 50,
                    self.text_max_width, COLORS["WHITE"], center=True)

    def outro_scene(self, screen):
        screen.blit(self.backgrounds["outro"], (0, 0))
        pygame.draw.rect(screen, COLORS["BLACK"],
                         (0, self.screen_height - self.text_area_height, self.screen_width, self.text_area_height))
        render_text(screen, self.current_text, self.font, self.screen_height - self.text_area_height + 50,
                    self.text_max_width, COLORS["WHITE"], center=True)

    def basement_search_scene(self, screen):
        if self.current_line_index in (4, 5, 6, 7):
            screen.blit(self.backgrounds["basement_door"], (0, 0))
        else:
            screen.blit(self.backgrounds["basement_search"], (0, 0))
        pygame.draw.rect(screen, COLORS["BLACK"],
                         (0, self.screen_height - self.text_area_height, self.screen_width, self.text_area_height))
        render_text(screen, self.current_text, self.font, self.screen_height - self.text_area_height + 50,
                    self.text_max_width, COLORS["WHITE"])

    def update_blueberry_dialogue(self):
        if self.footprint_task.is_completed():
            self.blueberry_dialogue = "Зарисовала оба следа. Надо проверить остальной дом."
            self.blueberry_dialogue_state = "done"
            self.scene_finished = True
        else:
            self.blueberry_dialogue = "Сначала нужно зарисовать оба следа."
            self.blueberry_dialogue_state = "wrong"
        start_text_animation(self, self.blueberry_dialogue)

    def update_electrical_dialogue(self):
        current_combination = [self.electrical_items[f"switch{i + 1}"]["state"] for i in range(5)]
        self.attempts_left -= 1

        if current_combination == self.correct_combination:
            self.electrical_dialogue = "Точно! Дверь открыта, свет горит!"
            self.electrical_dialogue_state = "done"
            self.door_unlocked = True
            self.lights_off = False
            self.after_electrical_dialogue_index = 0
            start_text_animation(self, self.after_electrical_text[self.after_electrical_dialogue_index])
            self.current_character = "corn"
        else:
            correct_count = sum(1 for i in range(5) if current_combination[i] == self.correct_combination[i])
            if self.attempts_left > 0:
                self.electrical_dialogue = f"Нет, это не та комбинация. Правильных: {correct_count}/5. Осталось попыток: {self.attempts_left}."
            else:
                self.electrical_dialogue = "Попытки закончились! Генерирую новую комбинацию..."
                self.reset_combination()
            self.electrical_dialogue_state = "wrong"
            self.lights_off = True
            self.open_button["shaking"] = True
            self.open_button["shake_time"] = pygame.time.get_ticks()

            start_text_animation(self, self.electrical_dialogue)

    def blueberry_room_scene(self, screen):
        if self.current_text == "На полу следы грязи… Надо зарисовать их в блокнот." and self.footprint_task.waiting_for_click:
            screen.blit(self.backgrounds["blueberry_footprints"], (0, 0))
        else:
            pygame.draw.rect(screen, COLORS["BLUEBERRY_BG"],
                             (0, 0, self.screen_width, self.screen_height - self.text_area_height))

        pygame.draw.rect(screen, COLORS["BLACK"],
                         (0, self.screen_height - self.text_area_height, self.screen_width, self.text_area_height))

        if self.footprint_task.waiting_for_click:
            render_text(screen, self.current_text, self.font, self.screen_height - self.text_area_height + 50,
                        self.text_max_width, COLORS["WHITE"])
        else:
            self.footprint_task.run(screen)
            if self.footprint_task.is_completed() and not self.scene_finished:
                self.update_blueberry_dialogue()

    def electrical_room_scene(self, screen):
        if self.door_unlocked and self.after_electrical_dialogue_index < len(self.after_electrical_text):
            screen.blit(self.backgrounds["electrical_after"], (0, 0))
        else:
            screen.fill(COLORS["GRAY"])
            brick_width = 100
            brick_height = 40
            for y in range(0, self.screen_height - self.text_area_height, brick_height):
                for x in range(0, self.screen_width, brick_width):
                    offset = brick_width // 2 if (y // brick_height) % 2 else 0
                    pygame.draw.rect(screen, COLORS["DARK_GRAY"], (x + offset, y, brick_width, brick_height))
                    pygame.draw.rect(screen, COLORS["BLACK"], (x + offset, y, brick_width, brick_height), 2)

            overlay = pygame.Surface((self.screen_width, self.screen_height - self.text_area_height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150 if self.lights_off else 0))
            screen.blit(overlay, (0, 0))

            if not self.door_unlocked:
                for item, data in self.electrical_items.items():
                    rect = data["rect"]
                    pygame.draw.rect(screen, COLORS["DARK_GRAY"], rect)
                    pygame.draw.rect(screen, COLORS["BLACK"], rect, 3)

                    handle_width = rect.width // 2
                    handle_height = rect.height // 3
                    handle_x = rect.x + (rect.width - handle_width) // 2
                    top_pos = rect.y + 10
                    bottom_pos = rect.y + rect.height - handle_height - 10

                    if data["animating"]:
                        progress = data["anim_progress"] / 100
                        if data["state"]:
                            handle_y = bottom_pos - (bottom_pos - top_pos) * progress
                        else:
                            handle_y = top_pos + (bottom_pos - top_pos) * progress
                    else:
                        handle_y = top_pos if data["state"] else bottom_pos

                    handle_color = COLORS["GREEN"] if data["state"] else COLORS["RED"]
                    pygame.draw.rect(screen, handle_color, (handle_x, handle_y, handle_width, handle_height))
                    pygame.draw.rect(screen, COLORS["BLACK"], (handle_x, handle_y, handle_width, handle_height), 2)

                button_rect = self.open_button["rect"]
                pygame.draw.rect(screen, COLORS["BLUE"], button_rect)
                pygame.draw.rect(screen, COLORS["BLACK"], button_rect, 2)
                button_text = self.font.render("Открыть", True, COLORS["WHITE"])
                screen.blit(button_text, button_text.get_rect(center=button_rect.center))

        pygame.draw.rect(screen, COLORS["BLACK"],
                         (0, self.screen_height - self.text_area_height, self.screen_width, self.text_area_height))
        render_text(screen, self.current_text, self.font, self.screen_height - self.text_area_height + 50,
                    self.text_max_width, COLORS["WHITE"])

        if not self.door_unlocked:
            attempts_text = f"Попытки: {self.attempts_left}/5"
            attempts_surface = self.hint_font.render(attempts_text, True, COLORS["WHITE"])
            attempts_rect = attempts_surface.get_rect(topright=(self.screen_width - 20, 20))
            pygame.draw.rect(screen, COLORS["BLUEBERRY_BG"], attempts_rect.inflate(20, 10), border_radius=8)
            pygame.draw.rect(screen, COLORS["WHITE"], attempts_rect.inflate(20, 10), 2, border_radius=8)
            screen.blit(attempts_surface, attempts_rect)