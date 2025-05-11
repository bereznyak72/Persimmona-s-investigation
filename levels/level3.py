import pygame
from utils import *
import random
import math


class SnifferTask:
    def __init__(self, screen_width, screen_height, font, text_area_height, text_max_width):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.Font('assets/fonts/Persimmona.ttf', int(screen_height * 0.035))
        self.pulse_font = pygame.font.Font('assets/fonts/Persimmona.ttf', int(screen_height * 0.035 * 1.05))
        self.text_area_height = text_area_height
        self.text_max_width = text_max_width
        self.completed = False
        self.task_active = False
        self.waiting_for_click = True

        self.target_pos = (random.randint(100, screen_width - 100), random.randint(100, screen_height - text_area_height - 100))
        self.decoy_positions = [(random.randint(100, screen_width - 100), random.randint(100, screen_height - text_area_height - 100)) for _ in range(3)]
        self.player_pos = [screen_width // 2, screen_height // 2]
        self.max_distance = math.sqrt(screen_width ** 2 + (screen_height - text_area_height) ** 2)
        self.signal_strength = 0
        self.max_signal = 100
        self.min_signal_distance = 50
        self.hint_text = "Используй нюхач, чтобы найти место, где лежали заготовки!"
        self.dynamic_hint = "Начни искать!"
        self.last_hint = self.dynamic_hint
        self.result_text = ""
        
        self.background_color = (150, 100, 50)
        self.sniffer_radius = 20
        self.signal_cooldown = 500
        self.last_signal_time = 0
        
        self.current_text = ""
        self.full_text = ""
        self.char_index = 0
        self.text_animation_speed = 25
        self.last_char_time = 0
        self.success_animation = False
        self.success_timer = 0
        self.success_duration = 2000
        self.pulse_timer = 0
        self.pulse_duration = 500
        self.particles = []

    def start_task(self):
        self.task_active = True
        self.waiting_for_click = False
        self.result_text = ""
        self.success_animation = False
        self.start_text_animation(f"{self.hint_text} {self.dynamic_hint}")

    def handle_event(self, event):
        if self.waiting_for_click:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.start_task()
                return True
            return False

        if not self.task_active or self.completed:
            return False

        if event.type == pygame.MOUSEMOTION:
            self.player_pos = list(event.pos)
            if random.random() < 0.2:
                self.particles.append({
                    "pos": self.player_pos.copy(),
                    "alpha": 255,
                    "scale": random.uniform(0.5, 1.5)
                })
            return True

        return False

    def update_signal(self):
        if self.completed:
            return

        distance = math.sqrt((self.player_pos[0] - self.target_pos[0]) ** 2 + 
                            (self.player_pos[1] - self.target_pos[1]) ** 2)
        self.signal_strength = max(0, min(self.max_signal, 
                                        (1 - distance / self.max_distance) * self.max_signal))
        
        for decoy_pos in self.decoy_positions:
            decoy_distance = math.sqrt((self.player_pos[0] - decoy_pos[0]) ** 2 + 
                                      (self.player_pos[1] - decoy_pos[1]) ** 2)
            if decoy_distance < distance:
                self.signal_strength = max(0, min(self.max_signal * 0.3, 
                                                (1 - decoy_distance / self.max_distance) * self.max_signal * 0.3))

        new_hint = self.dynamic_hint
        if self.signal_strength > 80:
            new_hint = "Ты очень близко!"
        elif self.signal_strength > 50:
            new_hint = "Ты на верном пути!"
        elif self.signal_strength > 20:
            new_hint = "Слабый сигнал, ищи дальше."
        else:
            new_hint = "Никакого запаха, попробуй другое место."

        if new_hint != self.last_hint:
            self.dynamic_hint = new_hint
            self.last_hint = new_hint
            self.start_text_animation(f"{self.hint_text} {self.dynamic_hint}")

        if distance < self.min_signal_distance:
            self.result_text = "Нашёл! Здесь лежали заготовки для выпечки!"
            self.completed = True
            self.success_animation = True
            self.success_timer = pygame.time.get_ticks()
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

        if current_time - self.last_signal_time >= self.signal_cooldown and not self.completed:
            self.update_signal()
            self.last_signal_time = current_time

        pygame.draw.rect(screen, self.background_color, 
                        (0, 0, self.screen_width, self.screen_height - self.text_area_height))
        for x in range(0, self.screen_width, 120):
            for y in range(0, self.screen_height - self.text_area_height, 60):
                pygame.draw.rect(screen, (139, 69, 19), (x, y, 100, 40), 2)
                pygame.draw.ellipse(screen, (200, 200, 150), (x + 20, y + 10, 60, 20))
                pygame.draw.ellipse(screen, COLORS["BLACK"], (x + 20, y + 10, 60, 20), 1)

        if not self.completed:
            if random.random() < 0.1:
                self.particles.append({
                    "pos": [self.target_pos[0] + random.uniform(-20, 20), self.target_pos[1] + random.uniform(-20, 20)],
                    "alpha": 200,
                    "scale": random.uniform(0.5, 1.0)
                })

        for decoy_pos in self.decoy_positions:
            if random.random() < 0.05:
                self.particles.append({
                    "pos": [decoy_pos[0] + random.uniform(-15, 15), decoy_pos[1] + random.uniform(-15, 15)],
                    "alpha": 150,
                    "scale": random.uniform(0.3, 0.8)
                })

        for particle in self.particles[:]:
            particle["alpha"] -= 5
            if particle["alpha"] <= 0:
                self.particles.remove(particle)
                continue
            pygame.draw.circle(screen, (255, 255, 255, int(particle["alpha"])), 
                              (int(particle["pos"][0]), int(particle["pos"][1])), int(3 * particle["scale"]))

        if self.completed:
            for decoy_pos in self.decoy_positions:
                pulse_scale = 1 + 0.2 * math.sin((current_time % self.pulse_duration) / self.pulse_duration * 2 * math.pi)
                pygame.draw.circle(screen, (255, 0, 0), decoy_pos, 20 * pulse_scale)
                pygame.draw.circle(screen, COLORS["WHITE"], decoy_pos, 20 * pulse_scale, 2)
            pulse_scale = 1 + 0.2 * math.sin((current_time % self.pulse_duration) / self.pulse_duration * 2 * math.pi)
            pygame.draw.circle(screen, COLORS["GREEN"], self.target_pos, 30 * pulse_scale)
            pygame.draw.circle(screen, COLORS["WHITE"], self.target_pos, 30 * pulse_scale, 2)

        pulse_scale = 1 + 0.1 * math.sin((current_time % self.pulse_duration) / self.pulse_duration * 2 * math.pi)
        pygame.draw.circle(screen, (0, 0, 255, 100), self.player_pos, self.sniffer_radius * pulse_scale * 1.5)
        pygame.draw.circle(screen, COLORS["BLUE"], self.player_pos, self.sniffer_radius * pulse_scale)
        pygame.draw.circle(screen, COLORS["WHITE"], self.player_pos, self.sniffer_radius * pulse_scale, 2)

        bar_width = 300
        bar_height = 40
        bar_x = (self.screen_width - bar_width) // 2
        bar_y = self.screen_height - self.text_area_height - 50
        pygame.draw.rect(screen, (20, 20, 20), (bar_x - 5, bar_y - 5, bar_width + 10, bar_height + 10), border_radius=10)
        pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height), border_radius=5)
        signal_color = (255, 165, 0) if self.signal_strength < 80 else (0, 255, 0)
        pygame.draw.rect(screen, signal_color, 
                        (bar_x, bar_y, bar_width * (self.signal_strength / self.max_signal), bar_height), 
                        border_radius=5)
        pygame.draw.rect(screen, COLORS["WHITE"], (bar_x, bar_y, bar_width, bar_height), 2, border_radius=5)
        signal_text = self.font.render(f"Сигнал: {int(self.signal_strength)}%", True, COLORS["WHITE"])
        screen.blit(signal_text, signal_text.get_rect(center=(bar_x + bar_width // 2, bar_y + bar_height // 2)))

        if self.success_animation and current_time - self.success_timer < self.success_duration:
            alpha = int(255 * (1 - (current_time - self.success_timer) / self.success_duration))
            overlay = pygame.Surface((self.screen_width, self.screen_height - self.text_area_height), pygame.SRCALPHA)
            overlay.fill((0, 255, 0, alpha))
            screen.blit(overlay, (0, 0))
        
        text_font = self.pulse_font if self.signal_strength >= 80 else self.font
        text_alpha = 255 if self.signal_strength < 80 else 255 * (0.8 + 0.2 * math.sin(current_time / 200))
        render_text(screen, self.current_text, text_font, self.screen_height - self.text_area_height + 50,
                    self.text_max_width, (*COLORS["WHITE"][:3], int(text_alpha)))

    def is_completed(self):
        return self.completed


class BreakInTask:
    def __init__(self, screen_width, screen_height, font, text_area_height, text_max_width):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = font
        self.text_area_height = text_area_height
        self.text_max_width = text_max_width
        self.completed = False
        self.task_active = False
        self.waiting_for_click = True

        self.traces = [
            {"pos": (screen_width // 5, 100), "type": "вентиляция", "color": (100, 100, 255), "detail": "grid", "fake": False},
            {"pos": (2 * screen_width // 5, 150), "type": "семечки", "color": (255, 200, 100), "detail": "stars", "fake": False},
            {"pos": (screen_width // 3, 200), "type": "пыль", "color": (200, 200, 200), "detail": "dots", "fake": False},
            {"pos": (screen_width // 2, 250), "type": "запах", "color": (255, 100, 255), "detail": "waves", "fake": False},
            {"pos": (3 * screen_width // 5, 300), "type": "царапины", "color": (255, 50, 50), "detail": "sparks", "fake": False},
            {"pos": (4 * screen_width // 5, 200), "type": "грязь", "color": (139, 69, 19), "detail": "splash", "fake": False},
            {"pos": (screen_width // 4, 300), "type": "обрывок ткани", "color": (150, 150, 255), "detail": "wave", "fake": False},
            {"pos": (screen_width // 6, 250), "type": "кофейное пятно", "color": (100, 50, 0), "detail": "stain", "fake": True},
            {"pos": (3 * screen_width // 4, 150), "type": "перо", "color": (255, 255, 255), "detail": "feather", "fake": True},
            {"pos": (2 * screen_width // 3, 100), "type": "след воды", "color": (50, 150, 255), "detail": "drop", "fake": True}
        ]
        self.correct_order = ["вентиляция", "семечки", "пыль", "запах", "царапины", "грязь", "обрывок ткани"]
        self.current_trace = self.traces[0]
        self.connections = []
        self.hint_text = "Начни с вентиляции и соедини следы в порядке действий вора."
        self.result_text = ""
        
        self.background_color = (139, 69, 19)
        self.current_text = ""
        self.full_text = ""
        self.char_index = 0
        self.text_animation_speed = 25
        self.last_char_time = 0
        self.success_animation = False
        self.success_timer = 0
        self.success_duration = 2000
        self.pulse_timer = 0
        self.pulse_duration = 500
        self.reset_button = pygame.Rect(screen_width - 50, 20, 30, 30)
        self.task_timer = 0
        self.time_limit = 60000

    def start_task(self):
        self.task_active = True
        self.waiting_for_click = False
        self.result_text = ""
        self.success_animation = False
        self.task_timer = pygame.time.get_ticks()
        self.start_text_animation(self.hint_text)

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
            if self.reset_button.collidepoint(pos):
                self.connections = []
                self.current_trace = self.traces[0]
                self.task_timer = pygame.time.get_ticks()
                self.start_text_animation(self.hint_text)
                return True
            for trace in self.traces:
                if math.hypot(pos[0] - trace["pos"][0], pos[1] - trace["pos"][1]) < 30 and trace != self.current_trace:
                    if trace["fake"]:
                        self.connections = []
                        self.current_trace = self.traces[0]
                        self.task_timer = pygame.time.get_ticks()
                        self.start_text_animation(f"Ошибка! {trace['type'].capitalize()} не связан с вором. Начни заново!")
                    else:
                        expected_type = self.correct_order[self.correct_order.index(self.current_trace["type"]) + 1]
                        if trace["type"] == expected_type:
                            self.connections.append((self.current_trace, trace))
                            self.current_trace = trace
                            if len(self.connections) == len(self.correct_order) - 1:
                                self.result_text = "Правильно! Вор проник через вентиляцию!"
                                self.completed = True
                                self.success_animation = True
                                self.success_timer = pygame.time.get_ticks()
                                self.start_text_animation(self.result_text)
                            else:
                                self.start_text_animation(f"Верно! Теперь соедини с {expected_type}.")
                        else:
                            self.start_text_animation(f"Ошибка! Попробуй соединить с {expected_type}.")
                    return True
        return False

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

        if not self.completed and current_time - self.task_timer > self.time_limit:
            self.connections = []
            self.current_trace = self.traces[0]
            self.task_timer = pygame.time.get_ticks()
            self.start_text_animation("Ты слишком медлишь! Начни заново.")

        for y in range(self.screen_height - self.text_area_height):
            color = (139 - y // 10, 69 - y // 20, 19 + y // 10)
            pygame.draw.line(screen, color, (0, y), (self.screen_width, y))

        overlay = pygame.Surface((self.screen_width, self.screen_height - self.text_area_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 100))
        pygame.draw.circle(overlay, (0, 0, 0, 0), self.current_trace["pos"], 100)
        screen.blit(overlay, (0, 0))

        for trace in self.traces:
            pulse_scale = 1 + 0.1 * math.sin((current_time % self.pulse_duration) / self.pulse_duration * 2 * math.pi)
            pygame.draw.circle(screen, (0, 0, 0, 50), (trace["pos"][0] + 5, trace["pos"][1] + 5), 35 * pulse_scale)
            pygame.draw.circle(screen, trace["color"], trace["pos"], 30 * pulse_scale)
            if trace == self.current_trace:
                pygame.draw.circle(screen, trace["color"], trace["pos"], 40 * pulse_scale, 3)
            pygame.draw.circle(screen, COLORS["WHITE"], trace["pos"], 30 * pulse_scale, 2)
            if trace["detail"] == "grid":
                for i in range(-2, 3):
                    alpha = 255 * (0.5 + 0.5 * math.sin(current_time / 500))
                    color = (*COLORS["WHITE"][:3], int(alpha))
                    pygame.draw.line(screen, color, (trace["pos"][0] + i * 10, trace["pos"][1] - 20), 
                                     (trace["pos"][0] + i * 10, trace["pos"][1] + 20), 1)
                    pygame.draw.line(screen, color, (trace["pos"][0] - 20, trace["pos"][1] + i * 10), 
                                     (trace["pos"][0] + 20, trace["pos"][1] + i * 10), 1)
            elif trace["detail"] == "stars":
                for i in range(4):
                    angle = i * math.pi / 2 + current_time / 1000
                    pygame.draw.line(screen, COLORS["WHITE"], 
                                     (trace["pos"][0] + math.cos(angle) * 10, trace["pos"][1] + math.sin(angle) * 10),
                                     (trace["pos"][0] + math.cos(angle) * 20, trace["pos"][1] + math.sin(angle) * 20), 2)
            elif trace["detail"] == "dots":
                for i in range(8):
                    angle = i * math.pi / 4 + math.sin(current_time / 1000)
                    pygame.draw.circle(screen, COLORS["WHITE"], 
                                      (int(trace["pos"][0] + math.cos(angle) * 15), int(trace["pos"][1] + math.sin(angle) * 15)), 3)
            elif trace["detail"] == "waves":
                for i in range(4):
                    angle = i * math.pi / 2
                    offset = 5 * math.sin(current_time / 500 + i)
                    pygame.draw.line(screen, COLORS["WHITE"], 
                                     (trace["pos"][0] + math.cos(angle) * 10 + offset, trace["pos"][1] + math.sin(angle) * 10),
                                     (trace["pos"][0] + math.cos(angle) * 20 + offset, trace["pos"][1] + math.sin(angle) * 20), 2)
            elif trace["detail"] == "sparks":
                for i in range(-2, 3):
                    offset = 5 * math.sin(current_time / 300 + i)
                    pygame.draw.line(screen, COLORS["WHITE"], 
                                     (trace["pos"][0] + i * 10 + offset, trace["pos"][1] - 20), 
                                     (trace["pos"][0] + i * 10 + offset + 10, trace["pos"][1] + 20), 2)
            elif trace["detail"] == "splash":
                for i in range(6):
                    angle = i * math.pi / 3 + math.sin(current_time / 800)
                    pygame.draw.circle(screen, COLORS["WHITE"], 
                                      (int(trace["pos"][0] + math.cos(angle) * 20), int(trace["pos"][1] + math.sin(angle) * 20)), 2)
            elif trace["detail"] == "wave":
                for i in range(-15, 16, 5):
                    offset = 5 * math.sin(current_time / 400 + i / 5)
                    pygame.draw.line(screen, COLORS["WHITE"], 
                                     (trace["pos"][0] + i, trace["pos"][1] - 15 + offset), 
                                     (trace["pos"][0] + i, trace["pos"][1] + 15 + offset), 1)
            elif trace["detail"] == "stain":
                for i in range(5):
                    pygame.draw.circle(screen, COLORS["WHITE"], 
                                      (int(trace["pos"][0] + random.uniform(-10, 10)), int(trace["pos"][1] + random.uniform(-10, 10))), 3)
            elif trace["detail"] == "feather":
                for i in range(-2, 3):
                    pygame.draw.line(screen, COLORS["WHITE"], 
                                     (trace["pos"][0] + i * 8, trace["pos"][1] - 15), 
                                     (trace["pos"][0] + i * 8 + 10, trace["pos"][1] + 15), 1)
            elif trace["detail"] == "drop":
                for i in range(3):
                    offset = 5 * math.sin(current_time / 600 + i)
                    pygame.draw.ellipse(screen, COLORS["WHITE"], 
                                       (trace["pos"][0] - 10 + i * 10 + offset, trace["pos"][1] - 10, 8, 15))

        for start_trace, end_trace in self.connections:
            line_width = 3 + int(2 * math.sin(current_time / 200))
            for i in range(line_width):
                alpha = 255 * (1 - i / line_width)
                color = (*start_trace["color"], int(alpha))
                pygame.draw.line(screen, color, start_trace["pos"], end_trace["pos"], line_width - i)

        pygame.draw.line(screen, COLORS["RED"], (self.reset_button.left, self.reset_button.top), 
                         (self.reset_button.right, self.reset_button.bottom), 3)
        pygame.draw.line(screen, COLORS["RED"], (self.reset_button.left, self.reset_button.bottom), 
                         (self.reset_button.right, self.reset_button.top), 3)

        bar_width = 300
        bar_height = 40
        bar_x = (self.screen_width - bar_width) // 2
        bar_y = self.screen_height - self.text_area_height - 50
        progress = len(self.connections) / (len(self.correct_order) - 1)
        pygame.draw.rect(screen, (20, 20, 20), (bar_x - 5, bar_y - 5, bar_width + 10, bar_height + 10), border_radius=10)
        pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height), border_radius=5)
        pygame.draw.rect(screen, (0, 255, 0, 200), (bar_x, bar_y, bar_width * progress, bar_height), border_radius=5)
        pygame.draw.rect(screen, COLORS["WHITE"], (bar_x, bar_y, bar_width, bar_height), 2, border_radius=5)
        progress_text = self.font.render(f"Соединения: {len(self.connections)}/{len(self.correct_order) - 1}", True, COLORS["WHITE"])
        screen.blit(progress_text, progress_text.get_rect(center=(bar_x + bar_width // 2, bar_y + bar_height // 2)))

        time_left = max(0, (self.time_limit - (current_time - self.task_timer)) // 1000)
        timer_text = self.font.render(f"Время: {time_left}с", True, COLORS["WHITE"])
        screen.blit(timer_text, (20, 20))

        if self.success_animation and current_time - self.success_timer < self.success_duration:
            alpha = int(255 * (1 - (current_time - self.success_timer) / self.success_duration))
            overlay = pygame.Surface((self.screen_width, self.screen_height - self.text_area_height), pygame.SRCALPHA)
            overlay.fill((0, 255, 0, alpha))
            screen.blit(overlay, (0, 0))

        render_text(screen, self.current_text, self.font, self.screen_height - self.text_area_height + 50,
                    self.text_max_width, COLORS["WHITE"])

    def is_completed(self):
        return self.completed


class Level3:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.Font('assets/fonts/Persimmona.ttf', int(self.screen_height * 0.035))
        self.hint_font = pygame.font.Font('assets/fonts/Persimmona.ttf', int(self.screen_height * 0.03))
        self.completed = False
        self.current_scene = "intro"
        self.scenes = {
            "intro": self.intro_scene,
            "bakery_room": self.bakery_room_scene,
            "break_in_room": self.break_in_room_scene,
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
            "Персиммона и Кукуруза входят в Булочную.",
            "Тут пусто, хотя обычно полно народу.",
            "Ночью нас обчистили! Ящики с заготовками пропали.",
            "Мы должны найти улики. Это может быть связано с делом Голубики.",
            "На полу следы, похожие на те, что были у Голубики!",
            "И тут семечко… Арбузное. Надо проверить всё."
        ]
        self.outro_text = [
            "Мы нашли путь вора! Это вентиляция.",
            "Арбузное семечко и следы — это не совпадение.",
            "Надо навестить Огурца. Он что-то знает.",
            "Пойдём, Кукуруза, время раскрывать тайны!"
        ]
        self.bakery_room_text = [
            "Надо найти место, где лежали заготовки.",
            "Используй нюхач, он уловит запах муки и дрожжей!",
            "Я осмотрю полки, вдруг что ещё найду."
        ]
        self.break_in_room_text = [
            "Теперь выясним, как вор проник в кладовку.",
            "Соедини следы, чтобы восстановить путь вора.",
            "Я помогу искать улики на полу."
        ]
        self.current_line_index = 0
        start_text_animation(self, self.intro_text[self.current_line_index])
        self.text_area_height = TEXT_AREA_HEIGHT

        self.backgrounds = {
            "intro": pygame.image.load('assets/images/intro_bg_3.jpg').convert(),
            "bakery_room": pygame.image.load('assets/images/bakery_room.jpg').convert(),
            "break_in_room": pygame.image.load('assets/images/bakery_room.jpg').convert(),
            "outro": pygame.image.load('assets/images/outro_bg_3.jpg').convert()
        }
        for key, bg in self.backgrounds.items():
            self.backgrounds[key] = pygame.transform.scale(bg, (self.screen_width, self.screen_height - self.text_area_height))

        self.characters = {
            "persimmona": pygame.image.load(ASSETS["PERSIMMONA"]).convert_alpha(),
            "corn": pygame.image.load(ASSETS["CORN"]).convert_alpha(),
            "eggplant": pygame.image.load(ASSETS["EGGPLANT"]).convert_alpha()
        }
        self.current_character = "persimmona"

        width_scale = self.screen_width / REFERENCE_WIDTH
        height_scale = self.screen_height / REFERENCE_HEIGHT
        scale_factor = min(width_scale, height_scale)

        for char, image in self.characters.items():
            target_width, target_height = CHARACTER_SIZES.get(char, (200, 300))
            new_width = max(int(target_width * scale_factor), MIN_CHAR_WIDTH)
            new_height = max(int(target_height * scale_factor), MIN_CHAR_HEIGHT)
            self.characters[char] = pygame.transform.scale(image, (new_width, new_height))
            self.characters[char] = {
                "image": self.characters[char],
                "rect": pygame.Rect(self.screen_width - new_width, self.screen_height - new_height, new_width, new_height)
            }

        max_char_width = max(CHARACTER_SIZES.get(char, (200, 300))[0] * scale_factor for char in self.characters)
        self.text_max_width = self.screen_width - int(max_char_width) - 60

        self.sniffer_task = SnifferTask(self.screen_width, self.screen_height, self.font, self.text_area_height,
                                       self.text_max_width)
        self.break_in_task = BreakInTask(self.screen_width, self.screen_height, self.font, self.text_area_height,
                                        self.text_max_width)
        self.task_index = 0
        self.tasks = [self.sniffer_task, self.break_in_task]

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            if self.current_text != self.full_text:
                self.current_text = self.full_text
                self.char_index = len(self.full_text)

            if self.scene_finished:
                if self.current_scene == "bakery_room" and self.sniffer_task.is_completed():
                    self.current_scene = "break_in_room"
                    self.scene_finished = False
                    self.sniffer_task.task_active = False
                    self.current_character = "persimmona"
                    self.current_line_index = 0
                    start_text_animation(self, self.break_in_room_text[self.current_line_index])
                    return True
                elif self.current_scene == "break_in_room" and self.break_in_task.is_completed():
                    self.current_scene = "outro"
                    self.scene_finished = False
                    self.break_in_task.task_active = False
                    self.current_character = "persimmona"
                    self.current_line_index = 0
                    start_text_animation(self, self.outro_text[self.current_line_index])
                    return True

            if self.current_scene == "intro":
                self.current_line_index += 1
                if self.current_line_index < len(self.intro_text):
                    start_text_animation(self, self.intro_text[self.current_line_index])
                    if self.current_line_index in (0, 3, 4, 5):
                        self.current_character = "persimmona"
                    elif self.current_line_index == 1:
                        self.current_character = "corn"
                    elif self.current_line_index == 2:
                        self.current_character = "eggplant"
                else:
                    self.current_scene = "bakery_room"
                    self.current_character = "persimmona"
                    self.current_line_index = 0
                    start_text_animation(self, self.bakery_room_text[self.current_line_index])
                return True

            elif self.current_scene == "outro":
                self.current_line_index += 1
                if self.current_line_index < len(self.outro_text):
                    start_text_animation(self, self.outro_text[self.current_line_index])
                    self.current_character = "persimmona" if self.current_line_index in (0, 2, 3) else "corn"
                else:
                    self.completed = True
                return True

            elif self.current_scene == "bakery_room" and not self.sniffer_task.task_active:
                self.current_line_index += 1
                if self.current_line_index < len(self.bakery_room_text):
                    start_text_animation(self, self.bakery_room_text[self.current_line_index])
                    self.current_character = "persimmona" if self.current_line_index in (0, 1) else "corn"
                else:
                    self.sniffer_task.start_task()
                return True

            elif self.current_scene == "break_in_room" and not self.break_in_task.task_active:
                self.current_line_index += 1
                if self.current_line_index < len(self.break_in_room_text):
                    start_text_animation(self, self.break_in_room_text[self.current_line_index])
                    self.current_character = "persimmona" if self.current_line_index in (0, 1) else "corn"
                else:
                    self.break_in_task.start_task()
                return True

        if self.current_scene == "bakery_room" and self.sniffer_task.task_active:
            if self.sniffer_task.handle_event(event):
                return True
            if self.sniffer_task.is_completed():
                self.scene_finished = True
                return True
        elif self.current_scene == "break_in_room" and self.break_in_task.task_active:
            if self.break_in_task.handle_event(event):
                return True
            if self.break_in_task.is_completed():
                self.scene_finished = True
                return True

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.completed = True
            return True

        return False

    def run(self, screen):
        current_time = pygame.time.get_ticks()
        update_text_animation(self, current_time)
        screen.fill(COLORS["BLACK"])
        self.scenes[self.current_scene](screen)

        screen.blit(self.characters[self.current_character]["image"],
                    self.characters[self.current_character]["rect"])

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

    def bakery_room_scene(self, screen):
        if self.sniffer_task.task_active:
            self.sniffer_task.run(screen)
        else:
            screen.blit(self.backgrounds["bakery_room"], (0, 0))
            pygame.draw.rect(screen, COLORS["BLACK"],
                            (0, self.screen_height - self.text_area_height, self.screen_width, self.text_area_height))
            render_text(screen, self.current_text, self.font, self.screen_height - self.text_area_height + 50,
                        self.text_max_width, COLORS["WHITE"])

    def break_in_room_scene(self, screen):
        if self.break_in_task.task_active:
            self.break_in_task.run(screen)
        else:
            screen.blit(self.backgrounds["break_in_room"], (0, 0))
            pygame.draw.rect(screen, COLORS["BLACK"],
                            (0, self.screen_height - self.text_area_height, self.screen_width, self.text_area_height))
            render_text(screen, self.current_text, self.font, self.screen_height - self.text_area_height + 50,
                        self.text_max_width, COLORS["WHITE"])