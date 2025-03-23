import pygame

class Level1:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.SysFont("Arial", int(self.screen_height * 0.035), bold=False)
        self.list_font = pygame.font.SysFont("Arial", int(self.screen_height * 0.03), bold=True)
        self.completed = False
        self.current_scene = "intro"
        self.scenes = {
            "intro": self.intro_scene,
            "bathroom": self.bathroom_scene,
            "kitchen": self.kitchen_scene,
            "bedroom": self.bedroom_scene,
            "outro": self.outro_scene
        }
        self.scene_finished = False
        self.text_animation_speed = 15
        self.last_char_time = 0
        self.current_text = ""
        self.full_text = ""
        self.char_index = 0
        self.text_lines = []
        self.intro_text = (
            "Персиммона просыпается в своей уютной квартире.",
            "Утренний свет льётся через маленькое окно,",
            "создавая мягкую атмосферу."
        )
        self.outro_text = (
            "Персиммона, полностью экипированная,",
            "в плаще, шляпе и с сумкой, покидает дом.",
            "Персимонна отправляется в контору"
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
        self.bathroom_items = {
            "toothbrush": {"rect": pygame.Rect(200, 50, 50, 50), "clicked": False, "order": 1},
            "toothpaste": {"rect": pygame.Rect(260, 50, 50, 50), "clicked": False, "order": 2},
            "faucet": {"rect": pygame.Rect(320, 50, 50, 50), "clicked": False, "order": 3},
            "towel": {"rect": pygame.Rect(380, 50, 50, 50), "clicked": False, "order": 4},
            "comb": {"rect": pygame.Rect(440, 50, 50, 50), "clicked": False, "order": 5}
        }
        self.bathroom_order = 1
        self.bathroom_dialogue = "Утро начинается как обычно… Сначала нужно взять зубную щётку…"
        self.kitchen_items = {
            "flour": {"rect": pygame.Rect(200, 50, 50, 50), "clicked": False, "order": 1, "strike_progress": 0},
            "eggs": {"rect": pygame.Rect(260, 50, 50, 50), "clicked": False, "order": 2, "strike_progress": 0},
            "milk": {"rect": pygame.Rect(320, 50, 50, 50), "clicked": False, "order": 3, "strike_progress": 0},
            "salt": {"rect": pygame.Rect(380, 50, 50, 50), "clicked": False, "order": 4, "strike_progress": 0},
            "sugar": {"rect": pygame.Rect(440, 50, 50, 50), "clicked": False, "order": 5, "strike_progress": 0},
            "bacon": {"rect": pygame.Rect(500, 50, 50, 50), "clicked": False, "order": 6, "strike_progress": 0}
        }
        self.kitchen_order = 1
        self.kitchen_dialogue = "Сначала нужна мука…"
        self.kitchen_ingredients_list = ["Мука", "Яйца", "Молоко", "Соль", "Сахар", "Бекон"]
        self.strike_animation_speed = 5
        self.bedroom_items = {
            "coat": {"rect": pygame.Rect(200, 50, 50, 50), "clicked": False},
            "hat": {"rect": pygame.Rect(260, 50, 50, 50), "clicked": False},
            "sniffer": {"rect": pygame.Rect(320, 50, 50, 50), "clicked": False},
            "notebook": {"rect": pygame.Rect(380, 50, 50, 50), "clicked": False},
            "magnifier": {"rect": pygame.Rect(440, 50, 50, 50), "clicked": False},
            "wallet": {"rect": pygame.Rect(500, 50, 50, 50), "clicked": False},
            "safe": {"rect": pygame.Rect(560, 50, 50, 50), "clicked": False}
        }
        self.bedroom_dialogue = "Возьми плащ детектива… без него никуда."
        self.safe_puzzle_solved = False

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

    def update_strike_animation(self):
        for item, data in self.kitchen_items.items():
            if data["clicked"] and data["strike_progress"] < 100:
                data["strike_progress"] += self.strike_animation_speed
                if data["strike_progress"] > 100:
                    data["strike_progress"] = 100

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.current_text == self.full_text:
            pos = event.pos
            if self.current_scene == "intro":
                self.current_scene = "bathroom"
                self.start_text_animation(self.bathroom_dialogue)
            elif self.current_scene == "outro":
                self.completed = True
            elif self.scene_finished:
                if self.current_scene == "bathroom":
                    self.current_scene = "kitchen"
                    self.scene_finished = False
                    self.start_text_animation(self.kitchen_dialogue)
                elif self.current_scene == "kitchen":
                    self.current_scene = "bedroom"
                    self.scene_finished = False
                    self.start_text_animation(self.bedroom_dialogue)
                elif self.current_scene == "bedroom":
                    self.current_scene = "outro"
                    self.scene_finished = False
                    self.start_text_animation(self.outro_text)
            elif self.current_scene == "bathroom":
                for item, data in self.bathroom_items.items():
                    if data["rect"].collidepoint(pos) and not data["clicked"]:
                        if data["order"] == self.bathroom_order:
                            data["clicked"] = True
                            self.bathroom_order += 1
                            self.update_bathroom_dialogue()
                        else:
                            self.bathroom_dialogue = "Нет, не сейчас…"
                            self.start_text_animation(self.bathroom_dialogue)
                        break
            elif self.current_scene == "kitchen":
                for item, data in self.kitchen_items.items():
                    if data["rect"].collidepoint(pos) and not data["clicked"]:
                        if data["order"] == self.kitchen_order:
                            data["clicked"] = True
                            self.kitchen_order += 1
                            self.update_kitchen_dialogue()
                        else:
                            self.kitchen_dialogue = "Нет, не сейчас…"
                            self.start_text_animation(self.kitchen_dialogue)
                        break
            elif self.current_scene == "bedroom":
                for item, data in self.bedroom_items.items():
                    if data["rect"].collidepoint(pos) and not data["clicked"]:
                        data["clicked"] = True
                        self.update_bedroom_dialogue(item)
                        break
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.completed = True

    def run(self, screen):
        current_time = pygame.time.get_ticks()
        self.update_text_animation(current_time)
        self.update_strike_animation()
        screen.fill((20, 20, 20))
        self.scenes[self.current_scene](screen)
        if self.current_scene not in ("intro", "outro"):
            screen.blit(self.character_image, self.character_rect)

    def is_completed(self):
        return self.completed

    def render_text(self, screen, text, y_pos, center=False):
        lines = self.wrap_text(text, self.text_max_width)
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

    def intro_scene(self, screen):
        pygame.draw.rect(screen, (255, 245, 200), (0, 0, self.screen_width, self.screen_height - self.text_area_height))
        self.render_text(screen, self.current_text, self.screen_height - self.text_area_height + 20, center=True)

    def outro_scene(self, screen):
        pygame.draw.rect(screen, (100, 100, 150), (0, 0, self.screen_width, self.screen_height - self.text_area_height))
        self.render_text(screen, self.current_text, self.screen_height - self.text_area_height + 20, center=True)

    def update_bathroom_dialogue(self):
        dialogues = {
            1: "Утро начинается как обычно… Сначала нужно взять зубную щётку…",
            2: "…теперь нужна зубная паста…",
            3: "…и, конечно, надо почистить зубы…",
            4: "Теперь надо умыться холодная вода бодрит!",
            5: "Надо вытереть лицо полотенцем…",
        }
        self.bathroom_dialogue = dialogues.get(self.bathroom_order, "Теперь можно и позавтракать!")
        self.start_text_animation(self.bathroom_dialogue)
        if self.bathroom_order > 5:
            self.scene_finished = True

    def update_kitchen_dialogue(self):
        dialogues = {
            1: "Сначала нужна мука…",
            2: "…потом яйца…",
            3: "…и молоко…",
            4: "…немного соли…",
            5: "…и сахара для вкуса…",
            6: "…и, конечно же, бекон!",
        }
        self.kitchen_dialogue = dialogues.get(self.kitchen_order, "Завтрак готов!")
        self.start_text_animation(self.kitchen_dialogue)
        if self.kitchen_order > 6:
            self.scene_finished = True

    def update_bedroom_dialogue(self, item):
        dialogues = {
            "coat": "Нужен плащ детектива… без него никуда.",
            "hat": "Возьму шляпу… классика.",
            "sniff": "Возьму нюхач… пригодится для улик.",
            "notebook": "Возьму блокнот и ручку… каждая деталь важна.",
            "magnifier": "Возьму увеличительное стекло… чтобы ничего не упустить.",
            "wallet": "Возьму кошелёк и ключи… и телефон, конечно.",
        }
        self.bedroom_dialogue = dialogues.get(item, "Всё готово. Пора в контору.")
        self.start_text_animation(self.bedroom_dialogue)
        if item == "safe" and all(data["clicked"] for data in self.bedroom_items.values()):
            self.scene_finished = True
        if item == "safe":
            self.safe_puzzle_solved = True

    def bathroom_scene(self, screen):
        pygame.draw.rect(screen, (200, 200, 255), (0, 0, self.screen_width, self.screen_height - self.text_area_height))
        if not self.scene_finished:
            for item, data in self.bathroom_items.items():
                pygame.draw.rect(screen, (0, 255, 0) if not data["clicked"] else (100, 100, 100), data["rect"])
        self.render_text(screen, self.current_text, self.screen_height - self.text_area_height + 20)

    def kitchen_scene(self, screen):
        pygame.draw.rect(screen, (255, 255, 200), (0, 0, self.screen_width, self.screen_height - self.text_area_height))
        if not self.scene_finished:
            for item, data in self.kitchen_items.items():
                pygame.draw.rect(screen, (0, 255, 0) if not data["clicked"] else (100, 100, 100), data["rect"])

            list_x = self.screen_width - 220
            list_y = 10
            list_width = 200
            list_height = len(self.kitchen_ingredients_list) * 40 + 20
            pygame.draw.rect(screen, (255, 255, 255), (list_x, list_y, list_width, list_height))

            for i, ingredient in enumerate(self.kitchen_ingredients_list):
                text_surface = self.list_font.render(ingredient, True, (0, 0, 0))
                text_rect = text_surface.get_rect(topleft=(list_x + 10, list_y + 10 + i * 40))
                screen.blit(text_surface, text_rect)

                item_key = list(self.kitchen_items.keys())[i]
                if self.kitchen_items[item_key]["clicked"]:
                    strike_progress = self.kitchen_items[item_key]["strike_progress"]
                    start_pos = (list_x + 10, list_y + 10 + i * 40 + text_surface.get_height() // 2)
                    end_pos_max = (list_x + 10 + text_surface.get_width(), list_y + 10 + i * 40 + text_surface.get_height() // 2)
                    end_pos = (
                        start_pos[0] + (end_pos_max[0] - start_pos[0]) * strike_progress / 100,
                        end_pos_max[1]
                    )
                    pygame.draw.line(screen, (255, 0, 0), start_pos, end_pos, 3)

        self.render_text(screen, self.current_text, self.screen_height - self.text_area_height + 20)

    def bedroom_scene(self, screen):
        pygame.draw.rect(screen, (200, 255, 200), (0, 0, self.screen_width, self.screen_height - self.text_area_height))
        if not self.scene_finished:
            for item, data in self.bedroom_items.items():
                pygame.draw.rect(screen, (0, 255, 0) if not data["clicked"] else (100, 100, 100), data["rect"])
        self.render_text(screen, self.current_text, self.screen_height - self.text_area_height + 20)