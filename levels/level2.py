import pygame
from utils.constants import *
from utils.helpers import *

class Level2:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.SysFont("Arial", int(self.screen_height * 0.035), bold=False)
        self.completed = False
        self.current_scene = "intro"
        self.scenes = {
            "intro": self.intro_scene,
            "blueberry_room": self.blueberry_room_scene,
            "basement_search": self.basement_search_scene,
            "electrical_room": self.electrical_room_scene,
            "pineapple_room": self.pineapple_room_scene,
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
            "Мой золотой ананас украли прошлой ночью!",
            "Это семейная реликвия, я не могу его потерять!",
            "Прошу, помогите мне вернуть его!",
            "Я слышала, вы лучший детектив в городе.",
            "Я даже не знаю, кто мог это сделать... У меня нет врагов…",
        ]
        self.outro_text = [
            "Не волнуйтесь, мы найдём ваш ананас.",
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
            "Я проверю подвал, вдруг там что-то спрятано!",
            "Я останусь тут, осмотрю окна ещё раз… Вдруг что пропустили.",
            "Хорошо, Кукуруза, будь осторожен там внизу.",
            "Эй, ребята! Тут в подвале дверь, и она заперта на магниты!",
            "Магниты? Это необычно… Надо найти способ открыть её.",
            "Где-то должны быть рубильники.",
            "Я нашёл их!"
        ]
        self.current_line_index = 0
        start_text_animation(self, self.intro_text[self.current_line_index])
        self.text_area_height = TEXT_AREA_HEIGHT

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
                "rect": pygame.Rect(self.screen_width - new_width, self.screen_height - new_height, new_width, new_height)
            }

        max_char_width = max(CHARACTER_SIZES[char][0] * scale_factor for char in CHARACTER_SIZES)
        self.text_max_width = self.screen_width - int(max_char_width) - 60

        self.blueberry_items = {
            "footprints": {"rect": pygame.Rect(200, 100, 100, 50), "clicked": False},
            "notebook": {"rect": pygame.Rect(320, 100, 50, 50), "clicked": False}
        }
        self.blueberry_dialogue = "На полу следы грязи… Надо зарисовать их в блокнот."
        self.blueberry_dialogue_state = "start"

        switch_size = (100, 200)
        spacing = 20
        total_width = (switch_size[0] * 5) + (spacing * 4)
        start_x = (self.screen_width - total_width) // 2
        switch_y = (self.screen_height - self.text_area_height - switch_size[1]) // 2

        self.correct_combination = [False, False, True, False, True]
        self.electrical_items = {
            "switch1": {"rect": pygame.Rect(start_x, switch_y, switch_size[0], switch_size[1]), "state": False, "animating": False, "anim_progress": 0},
            "switch2": {"rect": pygame.Rect(start_x + (switch_size[0] + spacing), switch_y, switch_size[0], switch_size[1]), "state": False, "animating": False, "anim_progress": 0},
            "switch3": {"rect": pygame.Rect(start_x + (switch_size[0] + spacing) * 2, switch_y, switch_size[0], switch_size[1]), "state": False, "animating": False, "anim_progress": 0},
            "switch4": {"rect": pygame.Rect(start_x + (switch_size[0] + spacing) * 3, switch_y, switch_size[0], switch_size[1]), "state": False, "animating": False, "anim_progress": 0},
            "switch5": {"rect": pygame.Rect(start_x + (switch_size[0] + spacing) * 4, switch_y, switch_size[0], switch_size[1]), "state": False, "animating": False, "anim_progress": 0}
        }
        self.open_button = {"rect": pygame.Rect(self.screen_width // 2 - 100, switch_y + switch_size[1] + 20, 200, 40), "shaking": False, "shake_time": 0}
        self.electrical_dialogue = "Нужно подобрать правильную комбинацию рубильников!"
        self.electrical_dialogue_state = "start"
        self.lights_off = False
        self.door_unlocked = False
        self.animation_speed = 10
        self.shake_duration = 500

        self.pineapple_items = {
            "glass_shards": {"rect": pygame.Rect(200, 150, 100, 50), "clicked": False},
            "sniffer": {"rect": pygame.Rect(320, 150, 50, 50), "clicked": False}
        }
        self.pineapple_dialogue = "Осколки стекла у подоконника… Надо проверить запах."
        self.pineapple_dialogue_state = "start"

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
                    if self.current_line_index == 0 or self.current_line_index == 3 or self.current_line_index == 5:
                        self.current_character = "persimmona"
                    elif self.current_line_index == 1 or self.current_line_index == 4 or self.current_line_index == 7:
                        self.current_character = "corn"
                    elif self.current_line_index == 2 or self.current_line_index == 6:
                        self.current_character = "blueberry"
                else:
                    self.current_scene = "electrical_room"
                    self.current_character = "corn"
                    start_text_animation(self, self.electrical_dialogue)
            elif self.scene_finished:
                if self.current_scene == "blueberry_room":
                    self.current_scene = "basement_search"
                    self.scene_finished = False
                    self.current_character = "persimmona"
                    self.current_line_index = 0
                    start_text_animation(self, self.basement_search_text[self.current_line_index])
                elif self.current_scene == "electrical_room" and self.door_unlocked:
                    self.current_scene = "pineapple_room"
                    self.scene_finished = False
                    self.current_character = "persimmona"
                    start_text_animation(self, self.pineapple_dialogue)
                elif self.current_scene == "pineapple_room":
                    self.current_scene = "outro"
                    self.scene_finished = False
                    self.current_character = "persimmona"
                    self.current_line_index = 0
                    start_text_animation(self, self.outro_text[self.current_line_index])
            elif self.current_scene == "blueberry_room":
                for item, data in self.blueberry_items.items():
                    if data["rect"].collidepoint(pos) and not data["clicked"]:
                        data["clicked"] = True
                        self.current_character = "persimmona"
                        self.update_blueberry_dialogue(item)
                        break
            elif self.current_scene == "electrical_room":
                for item, data in self.electrical_items.items():
                    if data["rect"].collidepoint(pos) and not data["animating"]:
                        data["state"] = not data["state"]
                        data["animating"] = True
                        data["anim_progress"] = 0
                        break
                if self.open_button["rect"].collidepoint(pos):
                    self.update_electrical_dialogue()
            elif self.current_scene == "pineapple_room":
                for item, data in self.pineapple_items.items():
                    if data["rect"].collidepoint(pos) and not data["clicked"]:
                        data["clicked"] = True
                        self.current_character = "persimmona"
                        self.update_pineapple_dialogue(item)
                        break
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.completed = True

    def run(self, screen):
        current_time = pygame.time.get_ticks()
        update_text_animation(self, current_time)
        screen.fill(COLORS["BLACK"])
        self.scenes[self.current_scene](screen)
        
        if self.current_scene == "intro":
            if self.current_line_index >= 2:
                self.current_character = "blueberry"
                screen.blit(self.characters[self.current_character]["image"], self.characters[self.current_character]["rect"])
        elif self.current_scene == "outro":
            if self.current_line_index == 0:
                self.current_character = "persimmona"
            elif self.current_line_index == 1:
                self.current_character = "corn"
            elif self.current_line_index == 2:
                self.current_character = "persimmona"
            elif self.current_line_index == 3:
                self.current_character = "persimmona"
            elif self.current_line_index == 4:
                self.current_character = "blueberry"
            elif self.current_line_index == 5:
                self.current_character = "blueberry"
            elif self.current_line_index == 6:
                self.current_character = "blueberry"
            elif self.current_line_index == 7:
                self.current_character = "blueberry"
            screen.blit(self.characters[self.current_character]["image"], self.characters[self.current_character]["rect"])
        else:
            screen.blit(self.characters[self.current_character]["image"], self.characters[self.current_character]["rect"])

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
                    self.open_button["rect"].x = (self.screen_width // 2 - 100) + (5 if (current_time // 50) % 2 == 0 else -5)

    def is_completed(self):
        return self.completed

    def intro_scene(self, screen):
        pygame.draw.rect(screen, COLORS["INTRO_L2_BG"], (0, 0, self.screen_width, self.screen_height - self.text_area_height))
        pygame.draw.rect(screen, COLORS["BLACK"], (0, self.screen_height - self.text_area_height, self.screen_width, self.text_area_height))
        render_text(screen, self.current_text, self.font, self.screen_height - self.text_area_height + 50, self.text_max_width, COLORS["WHITE"], center=True)

    def outro_scene(self, screen):
        pygame.draw.rect(screen, COLORS["OUTRO_L2_BG"], (0, 0, self.screen_width, self.screen_height - self.text_area_height))
        pygame.draw.rect(screen, COLORS["BLACK"], (0, self.screen_height - self.text_area_height, self.screen_width, self.text_area_height))
        render_text(screen, self.current_text, self.font, self.screen_height - self.text_area_height + 50, self.text_max_width, COLORS["WHITE"], center=True)

    def basement_search_scene(self, screen):
        pygame.draw.rect(screen, COLORS["BASEMENT_BG"], (0, 0, self.screen_width, self.screen_height - self.text_area_height))
        pygame.draw.rect(screen, COLORS["BLACK"], (0, self.screen_height - self.text_area_height, self.screen_width, self.text_area_height))
        render_text(screen, self.current_text, self.font, self.screen_height - self.text_area_height + 50, self.text_max_width, COLORS["WHITE"])

    def update_blueberry_dialogue(self, item):
        if item == "footprints":
            if self.blueberry_dialogue_state == "start":
                self.blueberry_dialogue = "Следы грязи… Интересная форма. Откуда они?"
                self.blueberry_dialogue_state = "footprints"
            elif self.blueberry_dialogue_state == "footprints":
                self.blueberry_dialogue = "Это не похоже на обычную обувь."
        elif item == "notebook" and self.blueberry_items["footprints"]["clicked"]:
            if self.blueberry_dialogue_state in ("start", "footprints"):
                self.blueberry_dialogue = "Зарисовала след. Надо проверить остальной дом."
                self.blueberry_dialogue_state = "done"
                self.scene_finished = True
            elif self.blueberry_dialogue_state == "wrong":
                self.blueberry_dialogue = "Теперь можно зарисовать след."
                self.blueberry_dialogue_state = "done"
                self.scene_finished = True
        else:
            self.blueberry_dialogue = "Сначала нужно осмотреть следы."
            self.blueberry_dialogue_state = "wrong"
        start_text_animation(self, self.blueberry_dialogue)

    def update_electrical_dialogue(self):
        current_combination = [self.electrical_items[f"switch{i+1}"]["state"] for i in range(5)]
        if current_combination == self.correct_combination:
            self.electrical_dialogue = "Точно! Дверь открыта, свет горит!"
            self.electrical_dialogue_state = "done"
            self.door_unlocked = True
            self.scene_finished = True
            self.lights_off = False
        else:
            self.electrical_dialogue = "Нет, это не та комбинация… Попробуй ещё раз."
            self.electrical_dialogue_state = "wrong"
            self.lights_off = True
            self.open_button["shaking"] = True
            self.open_button["shake_time"] = pygame.time.get_ticks()
        start_text_animation(self, self.electrical_dialogue)

    def update_pineapple_dialogue(self, item):
        if item == "glass_shards":
            if self.pineapple_dialogue_state == "start":
                self.pineapple_dialogue = "Осколки стекла… Вор разбил окно?"
                self.pineapple_dialogue_state = "shards"
            elif self.pineapple_dialogue_state == "shards":
                self.pineapple_dialogue = "Похоже, кто-то лез снаружи."
        elif item == "sniffer" and self.pineapple_items["glass_shards"]["clicked"]:
            if self.pineapple_dialogue_state in ("start", "shards"):
                self.pineapple_dialogue = "Нюхач уловил свежий запах… Вор был здесь недавно!"
                self.pineapple_dialogue_state = "done"
                self.scene_finished = True
            elif self.pineapple_dialogue_state == "wrong":
                self.pineapple_dialogue = "Запах свежий, кто-то был тут недавно."
                self.pineapple_dialogue_state = "done"
                self.scene_finished = True
        else:
            self.pineapple_dialogue = "Сначала надо осмотреть осколки."
            self.pineapple_dialogue_state = "wrong"
        start_text_animation(self, self.pineapple_dialogue)

    def blueberry_room_scene(self, screen):
        pygame.draw.rect(screen, COLORS["BLUEBERRY_BG"], (0, 0, self.screen_width, self.screen_height - self.text_area_height))
        pygame.draw.rect(screen, COLORS["BLACK"], (0, self.screen_height - self.text_area_height, self.screen_width, self.text_area_height))
        if not self.scene_finished:
            for item, data in self.blueberry_items.items():
                pygame.draw.rect(screen, COLORS["GREEN"] if not data["clicked"] else COLORS["GRAY"], data["rect"])
        render_text(screen, self.current_text, self.font, self.screen_height - self.text_area_height + 50, self.text_max_width, COLORS["WHITE"])

    def electrical_room_scene(self, screen):
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

        if not self.scene_finished:
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
            pygame.draw.rect(screen, COLORS["GREEN"], button_rect)
            pygame.draw.rect(screen, COLORS["BLACK"], button_rect, 2)
            button_text = self.font.render("Открыть", True, COLORS["WHITE"])
            screen.blit(button_text, button_text.get_rect(center=button_rect.center))

        pygame.draw.rect(screen, COLORS["BLACK"], (0, self.screen_height - self.text_area_height, self.screen_width, self.text_area_height))
        render_text(screen, self.current_text, self.font, self.screen_height - self.text_area_height + 50, self.text_max_width, COLORS["WHITE"])

    def pineapple_room_scene(self, screen):
        pygame.draw.rect(screen, COLORS["PINEAPPLE_BG"], (0, 0, self.screen_width, self.screen_height - self.text_area_height))
        pygame.draw.rect(screen, COLORS["BLACK"], (0, self.screen_height - self.text_area_height, self.screen_width, self.text_area_height))
        if not self.scene_finished:
            for item, data in self.pineapple_items.items():
                pygame.draw.rect(screen, COLORS["GREEN"] if not data["clicked"] else COLORS["GRAY"], data["rect"])
        render_text(screen, self.current_text, self.font, self.screen_height - self.text_area_height + 50, self.text_max_width, COLORS["WHITE"])