import pygame


class Level1:
    def __init__(self, screen_width, screen_height):
        self.completed = False
        self.current_level = 1  # 1 - Ванная, 2 - Кухня, 3 - Спальня
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.Font(None, int(screen_height * 0.05))  # Адаптивный шрифт
        self.clock = pygame.time.Clock()

        # Предварительное кэширование текстов заданий
        self.bathroom_tasks = [
            "Take toothbrush", "Apply toothpaste", "Brush teeth",
            "Wash face", "Dry face with towel", "Comb hair"
        ]
        self.kitchen_tasks = [
            "Get flour", "Get eggs", "Get milk", "Get salt", "Get sugar",
            "Get bacon", "Mix ingredients", "Fry pancakes", "Fry bacon",
            "Serve pancakes with bacon"
        ]
        self.bedroom_tasks = [
            "Grab detective coat", "Take hat", "Take sniffer",
            "Get notebook and pen", "Take magnifying glass",
            "Take wallet and keys", "Take ID from safe"
        ]

        # Кэширование текстов заданий
        self.bathroom_task_surfaces = [self.font.render(f"Task: {task}", True, (255, 255, 255)) for task in
                                       self.bathroom_tasks]
        self.kitchen_task_surfaces = [self.font.render(f"Task: {task}", True, (255, 255, 255)) for task in
                                      self.kitchen_tasks]
        self.bedroom_task_surfaces = [self.font.render(f"Task: {task}", True, (255, 255, 255)) for task in
                                      self.bedroom_tasks]

        self.init_bathroom()
        self.init_kitchen()
        self.init_bedroom()

    def init_bathroom(self):
        """Инициализация уровня 1: Ванная с адаптивными размерами."""
        self.current_task_index = 0
        obj_size = int(self.screen_height * 0.08)  # Размер объектов пропорционален экрану
        spacing = int(self.screen_width * 0.05)  # Адаптивный отступ

        self.toothbrush_rect = pygame.Rect(spacing, self.screen_height * 0.7, obj_size, obj_size)
        self.toothpaste_rect = pygame.Rect(spacing * 2 + obj_size, self.screen_height * 0.7, obj_size, obj_size)
        self.towel_rect = pygame.Rect(spacing * 3 + obj_size * 2, self.screen_height * 0.7, obj_size, obj_size)
        self.comb_rect = pygame.Rect(spacing * 4 + obj_size * 3, self.screen_height * 0.7, obj_size, obj_size)

        self.toothbrush_taken = False
        self.toothpaste_applied = False
        self.teeth_brushed = False
        self.face_washed = False
        self.face_dried = False
        self.hair_combed = False

    def init_kitchen(self):
        """Инициализация уровня 2: Кухня с адаптивными размерами."""
        self.current_kitchen_task_index = 0
        obj_size = int(self.screen_height * 0.08)
        spacing = int(self.screen_width * 0.05)

        self.flour_rect = pygame.Rect(spacing, self.screen_height * 0.7, obj_size, obj_size)
        self.eggs_rect = pygame.Rect(spacing * 2 + obj_size, self.screen_height * 0.7, obj_size, obj_size)
        self.milk_rect = pygame.Rect(spacing * 3 + obj_size * 2, self.screen_height * 0.7, obj_size, obj_size)
        self.salt_rect = pygame.Rect(spacing * 4 + obj_size * 3, self.screen_height * 0.7, obj_size, obj_size)
        self.sugar_rect = pygame.Rect(spacing * 5 + obj_size * 4, self.screen_height * 0.7, obj_size, obj_size)
        self.bacon_rect = pygame.Rect(spacing * 6 + obj_size * 5, self.screen_height * 0.7, obj_size, obj_size)

        self.flour_taken = False
        self.eggs_taken = False
        self.milk_taken = False
        self.salt_taken = False
        self.sugar_taken = False
        self.bacon_taken = False
        self.ingredients_mixed = False
        self.pancakes_fried = False
        self.bacon_fried = False
        self.meal_served = False

    def init_bedroom(self):
        """Инициализация уровня 3: Спальня с адаптивными размерами."""
        self.current_bedroom_task_index = 0
        obj_size = int(self.screen_height * 0.08)
        spacing = int(self.screen_width * 0.05)

        self.coat_rect = pygame.Rect(spacing, self.screen_height * 0.7, obj_size, obj_size)
        self.hat_rect = pygame.Rect(spacing * 2 + obj_size, self.screen_height * 0.7, obj_size, obj_size)
        self.sniffer_rect = pygame.Rect(spacing * 3 + obj_size * 2, self.screen_height * 0.7, obj_size, obj_size)
        self.notebook_rect = pygame.Rect(spacing * 4 + obj_size * 3, self.screen_height * 0.7, obj_size, obj_size)
        self.magnifying_glass_rect = pygame.Rect(spacing * 5 + obj_size * 4, self.screen_height * 0.7, obj_size,
                                                 obj_size)
        self.wallet_rect = pygame.Rect(spacing * 6 + obj_size * 5, self.screen_height * 0.7, obj_size, obj_size)
        self.safe_rect = pygame.Rect(spacing * 7 + obj_size * 6, self.screen_height * 0.7, obj_size, obj_size)

        self.coat_taken = False
        self.hat_taken = False
        self.sniffer_taken = False
        self.notebook_taken = False
        self.magnifying_glass_taken = False
        self.wallet_taken = False
        self.id_taken = False

    def handle_event(self, event):
        """Обработка событий, вызываемая из main.py."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.handle_click(event.pos)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.completed = True

    def run(self, screen):
        """Основной цикл уровня, адаптированный под main.py."""
        screen.fill((0, 0, 0))

        if self.current_level == 1:
            self.run_bathroom(screen)
        elif self.current_level == 2:
            self.run_kitchen(screen)
        elif self.current_level == 3:
            self.run_bedroom(screen)

    def run_bathroom(self, screen):
        """Отрисовка уровня 1: Ванная."""
        if self.current_task_index < len(self.bathroom_tasks):
            screen.blit(self.bathroom_task_surfaces[self.current_task_index], (20, 20))
            if not self.toothbrush_taken:
                pygame.draw.rect(screen, (0, 255, 0), self.toothbrush_rect)
            if not self.toothpaste_applied:
                pygame.draw.rect(screen, (255, 255, 0), self.toothpaste_rect)
            if not self.face_dried:
                pygame.draw.rect(screen, (0, 0, 255), self.towel_rect)
            if not self.hair_combed:
                pygame.draw.rect(screen, (255, 0, 0), self.comb_rect)
        else:
            self.current_level = 2
            self.current_task_index = 0

    def run_kitchen(self, screen):
        """Отрисовка уровня 2: Кухня."""
        if self.current_kitchen_task_index < len(self.kitchen_tasks):
            screen.blit(self.kitchen_task_surfaces[self.current_kitchen_task_index], (20, 20))
            if not self.flour_taken:
                pygame.draw.rect(screen, (255, 200, 150), self.flour_rect)
            if not self.eggs_taken:
                pygame.draw.rect(screen, (255, 255, 0), self.eggs_rect)
            if not self.milk_taken:
                pygame.draw.rect(screen, (255, 255, 255), self.milk_rect)
            if not self.salt_taken:
                pygame.draw.rect(screen, (200, 200, 200), self.salt_rect)
            if not self.sugar_taken:
                pygame.draw.rect(screen, (255, 255, 200), self.sugar_rect)
            if not self.bacon_taken:
                pygame.draw.rect(screen, (150, 75, 0), self.bacon_rect)
        else:
            self.current_level = 3
            self.current_kitchen_task_index = 0

    def run_bedroom(self, screen):
        """Отрисовка уровня 3: Спальня."""
        if self.current_bedroom_task_index < len(self.bedroom_tasks):
            screen.blit(self.bedroom_task_surfaces[self.current_bedroom_task_index], (20, 20))
            if not self.coat_taken:
                pygame.draw.rect(screen, (0, 0, 255), self.coat_rect)
            if not self.hat_taken:
                pygame.draw.rect(screen, (100, 100, 100), self.hat_rect)
            if not self.sniffer_taken:
                pygame.draw.rect(screen, (255, 0, 0), self.sniffer_rect)
            if not self.notebook_taken:
                pygame.draw.rect(screen, (255, 255, 0), self.notebook_rect)
            if not self.magnifying_glass_taken:
                pygame.draw.rect(screen, (0, 255, 255), self.magnifying_glass_rect)
            if not self.wallet_taken:
                pygame.draw.rect(screen, (150, 75, 0), self.wallet_rect)
            if not self.id_taken:
                pygame.draw.rect(screen, (255, 255, 255), self.safe_rect)
        else:
            self.completed = True

    def handle_click(self, mouse_pos):
        """Обработка кликов для всех уровней."""
        if self.current_level == 1:
            self.handle_bathroom_click(mouse_pos)
        elif self.current_level == 2:
            self.handle_kitchen_click(mouse_pos)
        elif self.current_level == 3:
            self.handle_bedroom_click(mouse_pos)

    def handle_bathroom_click(self, mouse_pos):
        if self.current_task_index < len(self.bathroom_tasks):
            task = self.bathroom_tasks[self.current_task_index]
            if task == "Take toothbrush" and self.toothbrush_rect.collidepoint(mouse_pos):
                self.toothbrush_taken = True
                self.current_task_index += 1
            elif task == "Apply toothpaste" and self.toothpaste_rect.collidepoint(mouse_pos):
                self.toothpaste_applied = True
                self.current_task_index += 1
            elif task == "Brush teeth" and self.toothbrush_taken and self.toothpaste_applied:
                self.teeth_brushed = True
                self.current_task_index += 1
            elif task == "Wash face":
                self.face_washed = True
                self.current_task_index += 1
            elif task == "Dry face with towel" and self.towel_rect.collidepoint(mouse_pos):
                self.face_dried = True
                self.current_task_index += 1
            elif task == "Comb hair" and self.comb_rect.collidepoint(mouse_pos):
                self.hair_combed = True
                self.current_task_index += 1

    def handle_kitchen_click(self, mouse_pos):
        if self.current_kitchen_task_index < len(self.kitchen_tasks):
            task = self.kitchen_tasks[self.current_kitchen_task_index]
            if task == "Get flour" and self.flour_rect.collidepoint(mouse_pos):
                self.flour_taken = True
                self.current_kitchen_task_index += 1
            elif task == "Get eggs" and self.eggs_rect.collidepoint(mouse_pos):
                self.eggs_taken = True
                self.current_kitchen_task_index += 1
            elif task == "Get milk" and self.milk_rect.collidepoint(mouse_pos):
                self.milk_taken = True
                self.current_kitchen_task_index += 1
            elif task == "Get salt" and self.salt_rect.collidepoint(mouse_pos):
                self.salt_taken = True
                self.current_kitchen_task_index += 1
            elif task == "Get sugar" and self.sugar_rect.collidepoint(mouse_pos):
                self.sugar_taken = True
                self.current_kitchen_task_index += 1
            elif task == "Get bacon" and self.bacon_rect.collidepoint(mouse_pos):
                self.bacon_taken = True
                self.current_kitchen_task_index += 1
            elif task == "Mix ingredients" and all(
                    [self.flour_taken, self.eggs_taken, self.milk_taken, self.salt_taken, self.sugar_taken]):
                self.ingredients_mixed = True
                self.current_kitchen_task_index += 1
            elif task == "Fry pancakes":
                self.pancakes_fried = True
                self.current_kitchen_task_index += 1
            elif task == "Fry bacon":
                self.bacon_fried = True
                self.current_kitchen_task_index += 1
            elif task == "Serve pancakes with bacon":
                self.meal_served = True
                self.current_kitchen_task_index += 1

    def handle_bedroom_click(self, mouse_pos):
        if self.current_bedroom_task_index < len(self.bedroom_tasks):
            task = self.bedroom_tasks[self.current_bedroom_task_index]
            if task == "Grab detective coat" and self.coat_rect.collidepoint(mouse_pos):
                self.coat_taken = True
                self.current_bedroom_task_index += 1
            elif task == "Take hat" and self.hat_rect.collidepoint(mouse_pos):
                self.hat_taken = True
                self.current_bedroom_task_index += 1
            elif task == "Take sniffer" and self.sniffer_rect.collidepoint(mouse_pos):
                self.sniffer_taken = True
                self.current_bedroom_task_index += 1
            elif task == "Get notebook and pen" and self.notebook_rect.collidepoint(mouse_pos):
                self.notebook_taken = True
                self.current_bedroom_task_index += 1
            elif task == "Take magnifying glass" and self.magnifying_glass_rect.collidepoint(mouse_pos):
                self.magnifying_glass_taken = True
                self.current_bedroom_task_index += 1
            elif task == "Take wallet and keys" and self.wallet_rect.collidepoint(mouse_pos):
                self.wallet_taken = True
                self.current_bedroom_task_index += 1
            elif task == "Take ID from safe" and self.safe_rect.collidepoint(mouse_pos):
                self.id_taken = True
                self.current_bedroom_task_index += 1

    def is_completed(self):
        return self.completed
