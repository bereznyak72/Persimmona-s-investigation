import pygame
import random

# === Размеры и всякие приколы ===
GRID_SIZE = 7
LINE_WIDTH = 4
CIRCLE_RADIUS_RATIO = 3  # Отношение радиуса круга к размеру ячейки
CIRCLE_WIDTH = 4
CROSS_SIZE_RATIO = 3  # Отношение размера креста к размеру ячейки
CROSS_WIDTH = 4
BG_COLOR = (199, 252, 236)
LINE_COLOR = (0, 0, 0)
CIRCLE_COLOR = (0, 128, 255)
CROSS_COLOR = (255, 0, 0)
FONT_COLOR = (0, 0, 0)
RED_COLOR = (255, 0, 0)
WIN_LENGTH = 5
DIALOG_BG_COLOR = (255, 255, 255)

# === Размеры для nextpuzzle ===
PUZZLE_CELL_SIZE_RATIO = 5  # Отношение размера ячейки пятнашек к меньшей стороне экрана


class Level5:  # Крестики нолики
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Вычисляем размеры, исходя из размеров экрана
        self.cell_size = min(self.screen_width, self.screen_height) // GRID_SIZE
        self.circle_radius = self.cell_size // CIRCLE_RADIUS_RATIO
        self.cross_size = self.cell_size // CROSS_SIZE_RATIO
        self.puzzle_cell_size = min(self.screen_width, self.screen_height) // PUZZLE_CELL_SIZE_RATIO
        self.puzzle_x_offset = (self.screen_width - self.puzzle_cell_size * 4) // 2
        self.puzzle_y_offset = (self.screen_height - self.puzzle_cell_size * 4) // 2

        self.board = [['' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.current_player = 'X'
        self.game_over = False
        self.winner = None
        self.dialog_index = 0
        self.game_started = False
        self.post_win_dialog_index = 0
        self.show_puzzle = False  # Flag для показа nextpuzzle
        self.puzzle_solved = False  # Новый флаг!
        self.final_dialog_index = 0  # Индекс для финального диалога
        self.next_puzzle = NextPuzzle()  # Создаем экземпляр NextPuzzle здесь
        self.completed = False

        # Вычисляем смещения для центрирования
        self.board_width = self.cell_size * GRID_SIZE
        self.board_height = self.cell_size * GRID_SIZE
        self.x_offset = (self.screen_width - self.board_width) // 2
        self.y_offset = (self.screen_height - self.board_height) // 2
        self.persimmona_image = pygame.image.load("assets/images/persimmona.png").convert_alpha()
        reference_width, reference_height = 1920, 1080
        width_scale = self.screen_width / reference_width
        height_scale = self.screen_height / reference_height
        scale_factor = min(width_scale, height_scale)
        target_persimmona_width, target_persimmona_height = 316, 606
        new_persimmona_width = max(int(target_persimmona_width * scale_factor), 50)
        new_persimmona_height = max(int(target_persimmona_height * scale_factor), 96)
        self.persimmona_image = pygame.transform.scale(self.persimmona_image,
                                                       (new_persimmona_width, new_persimmona_height))
        self.persimmona_rect = pygame.Rect(self.screen_width - new_persimmona_width,
                                           self.screen_height - new_persimmona_height, new_persimmona_width,
                                           new_persimmona_height)
        self.persimmona_text_max_width = self.screen_width - new_persimmona_width - 60

    def run(self, screen):
        """Основная функция для отрисовки Level5."""
        screen.fill(BG_COLOR)  # Очищаем экран
        if not self.game_started and not self.show_puzzle and not self.puzzle_solved:
            self.display_next_sentence(screen)  # Показываем диалог
        elif self.game_over and self.winner == "Вы" and self.post_win_dialog_index < len(
                self.show_post_win_dialog()) and not self.show_puzzle:  # Рисует пока есть реплики
            self.draw_dialog(screen, self.show_post_win_dialog, "post_win_dialog_index")
        elif self.puzzle_solved and self.final_dialog_index < len(self.show_final_dialog()):
            self.draw_dialog(screen, self.show_final_dialog, "final_dialog_index")
        elif self.show_puzzle and not self.puzzle_solved:  # Рисуем nextpuzzle
            self.draw_puzzle(screen, self.next_puzzle)
        else:
            self.draw_board(screen)
            self.draw_lines(screen)

        pygame.display.flip()

    def handle_event(self, event):
        """Обрабатывает события Pygame."""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.completed = True
        if not self.game_started and not self.show_puzzle and not self.puzzle_solved:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.dialog_index < len(self.show_dialog()) - 1:
                    self.dialog_index += 1
                else:
                    self.game_started = True
                    self.reset_game()

        elif self.game_over and self.winner == "Вы" and not self.show_puzzle:  # Обработка диалога после победы
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.post_win_dialog_index < len(self.show_post_win_dialog()):
                    self.post_win_dialog_index += 1
            if self.post_win_dialog_index >= len(self.show_post_win_dialog()):
                self.show_puzzle = True  # Показываем nextpuzzle
                self.game_started = False  # Предотвращаем запуск крестиков-ноликов
                self.game_over = False  # Убираем флаг окончания игры
                # self.winner = None  # Убираем победителя
                self.next_puzzle = NextPuzzle()  # Инициализируем заново nextpuzzle
                print("nextpuzzle запущен")

        elif self.show_puzzle and not self.puzzle_solved:  # Обработка nextpuzzle
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                # Вычисляем координаты плитки, на которую кликнули
                col = (mx - self.puzzle_x_offset) // self.puzzle_cell_size
                row = (my - self.puzzle_y_offset) // self.puzzle_cell_size

                # Проверяем, что клик был в пределах доски
                if 0 <= row < self.next_puzzle.size and 0 <= col < self.next_puzzle.size:
                    # Пытаемся передвинуть плитку
                    if row == self.next_puzzle.empty_row and col == self.next_puzzle.empty_col + 1:
                        self.next_puzzle.move("left")  # Двигаем влево
                    elif row == self.next_puzzle.empty_row and col == self.next_puzzle.empty_col - 1:
                        self.next_puzzle.move("right")  # Двигаем вправо
                    elif col == self.next_puzzle.empty_col and row == self.next_puzzle.empty_row + 1:
                        self.next_puzzle.move("up")  # Двигаем вверх
                    elif col == self.next_puzzle.empty_col and row == self.next_puzzle.empty_row - 1:
                        self.next_puzzle.move("down")  # Двигаем вниз
            if self.next_puzzle.is_solved():
                self.puzzle_solved = True  # Игра решена!
                print("Пятнашки решены!")
                self.completed = True

        elif self.puzzle_solved:  # Обработка финального диалога
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.final_dialog_index < len(self.show_final_dialog()):
                    self.final_dialog_index += 1
                if self.final_dialog_index >= len(self.show_final_dialog()):
                    self.completed = True
                    print("Level 5 пройден")

        elif self.game_started and not self.game_over and self.current_player == 'O' and not self.show_puzzle:
            if not any("" in row for row in self.board) and not self.check_winner('X') and not self.check_winner('O'):
                self.game_over = True
                self.show_winner("Ничья!")
        elif self.game_started and not self.game_over and self.winner is None and not self.show_puzzle:
            if event.type == pygame.MOUSEBUTTONDOWN and self.current_player == 'X':
                mx, my = event.pos
                # === Учитываем смещение ===
                mx -= self.x_offset
                my -= self.y_offset

                col = mx // self.cell_size
                row = my // self.cell_size

                if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE and self.board[row][col] == '':
                    self.board[row][col] = self.current_player
                    if self.check_winner(self.current_player):
                        self.game_over = True
                        self.winner = "Вы"
                        self.post_win_dialog_index = 0  # Начинает диалог после победы
                        return  # Выходит из функции, чтобы не продолжать ходы
                    else:
                        self.current_player = 'O'

                        if self.bot_move():
                            if self.check_winner('O'):
                                self.game_over = True
                                self.winner = "Капуста"
                                self.show_winner("Капуста победила!")
                            elif not any("" in row for row in self.board):
                                self.game_over = True
                                self.show_winner("Ничья!")
                            else:
                                self.current_player = 'X'
                        else:
                            self.game_over = True
                            self.show_winner("Ничья!")

    def is_completed(self):
        return self.completed

    def draw_board(self, screen):
        """Рисует игровое поле на экране."""
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                x = self.x_offset + col * self.cell_size
                y = self.y_offset + row * self.cell_size
                if self.board[row][col] == 'X':
                    pygame.draw.line(screen, CROSS_COLOR, (
                        x + self.cell_size // 2 - self.cross_size, y + self.cell_size // 2 - self.cross_size),
                                     (x + self.cell_size // 2 + self.cross_size,
                                      y + self.cell_size // 2 + self.cross_size), CROSS_WIDTH)
                    pygame.draw.line(screen, CROSS_COLOR, (
                        x + self.cell_size // 2 + self.cross_size, y + self.cell_size // 2 - self.cross_size),
                                     (x + self.cell_size // 2 - self.cross_size,
                                      y + self.cell_size // 2 + self.cross_size), CROSS_WIDTH)
                elif self.board[row][col] == 'O':
                    pygame.draw.circle(screen, CIRCLE_COLOR, (x + self.cell_size // 2, y + self.cell_size // 2),
                                       self.circle_radius, CIRCLE_WIDTH)

    def draw_lines(self, screen):
        """Рисует линии сетки и внешние границы."""
        board_width = self.cell_size * GRID_SIZE
        board_height = self.cell_size * GRID_SIZE

        # Рисуем вертикальные линии сетки
        for i in range(1, GRID_SIZE):
            pygame.draw.line(screen, LINE_COLOR, (self.x_offset + i * self.cell_size, self.y_offset),
                             (self.x_offset + i * self.cell_size, self.y_offset + board_height), LINE_WIDTH)

        # Рисуем горизонтальные линии сетки
        for i in range(1, GRID_SIZE):
            pygame.draw.line(screen, LINE_COLOR, (self.x_offset, self.y_offset + i * self.cell_size),
                             (self.x_offset + board_width, self.y_offset + i * self.cell_size), LINE_WIDTH)

        # Рисуем внешние границы
        pygame.draw.line(screen, LINE_COLOR, (self.x_offset, self.y_offset),
                         (self.x_offset + board_width, self.y_offset), LINE_WIDTH)  # Верхняя граница
        pygame.draw.line(screen, LINE_COLOR, (self.x_offset, self.y_offset + board_height),
                         (self.x_offset + board_width, self.y_offset + board_height), LINE_WIDTH)  # Нижняя граница
        pygame.draw.line(screen, LINE_COLOR, (self.x_offset, self.y_offset),
                         (self.x_offset, self.y_offset + board_height), LINE_WIDTH)  # Левая граница
        pygame.draw.line(screen, LINE_COLOR, (self.x_offset + board_width, self.y_offset),
                         (self.x_offset + board_width, self.y_offset + board_height), LINE_WIDTH)  # Правая граница

    def show_winner(self, message):
        """Отображает сообщение о победителе и перезапускает игру при ничьей."""
        font = pygame.font.Font(None, 36)
        text = font.render(message, True, FONT_COLOR)
        text_rect = text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
        # screen.blit(text, text_rect) #Убрано чтобы не было ошибки
        pygame.display.flip()
        pygame.time.delay(2000)

        if self.winner == "Ничья":
            self.reset_game()
            self.game_started = True

        if self.winner == "Капуста":
            self.reset_game()
            self.game_started = True

    def check_sequence(self, board, row_start, col_start, row_step, col_step, player, win_length):
        """Проверяет, есть ли последовательность из win_length символов player в направлении (row_step, col_step)"""
        for i in range(win_length):
            row = row_start + i * row_step
            col = col_start + i * col_step
            if row < 0 or row >= len(board) or col < 0 or col >= len(board[0]) or board[row][col] != player:
                return False
        return True

    def check_winner(self, player):
        """Проверяет, есть ли победитель (WIN_LENGTH в ряд)."""
        board = self.board
        size = GRID_SIZE

        # Горизонталь
        for row in range(size):
            for col in range(size - WIN_LENGTH + 1):
                if self.check_sequence(board, row, col, 0, 1, player, WIN_LENGTH):
                    return True

        # Вертикаль
        for col in range(size):
            for row in range(size - WIN_LENGTH + 1):
                if self.check_sequence(board, row, col, 1, 0, player, WIN_LENGTH):
                    return True

        # Диагональ (слева направо, сверху вниз)
        for row in range(size - WIN_LENGTH + 1):
            for col in range(size - WIN_LENGTH + 1):
                if self.check_sequence(board, row, col, 1, 1, player, WIN_LENGTH):
                    return True

        # Диагональ (справа налево, сверху вниз)
        for row in range(size - WIN_LENGTH + 1):
            for col in range(WIN_LENGTH - 1, size):
                if self.check_sequence(board, row, col, 1, -1, player, WIN_LENGTH):
                    return True

        return False

    def show_dialog(self):
        return [
            "Капуста, привет! Слышала, что у тебя пропало мясо. (П)", "Можно я поищу какие-нибудь улики? (П)",
            "Привет, Персиммона, конечно! (К)", "Я заметила скомканную бумагу на столе, её раньше не было... (К)",
            "Погоди, на ней что-то написано. (П)", "\"Сыграйте в игры и так уж и быть получите своё мясо\"",
            "Скорее всего я была на работе, когда кто-то подложил записку... (К)",
            "Давай сыграем, если это поможет расследованию. (П)",
            "\n\nЗадача: Победить Капусту в мясных крестиках ноликах 7 на 7."
            "\nПримечание: Нужно составить линию из 5."
            "\nВы будете играть за крестики."
        ]

    def display_text(self, screen, text, color, font_path, font_size, position="center", y_offset=0):
        """Отображает текст на экране, поддерживая многострочность и различное выравнивание."""
        font = pygame.font.Font(font_path, font_size)
        lines = text.split('\n')
        total_height = sum(font.size(line)[1] for line in lines)  # Общая высота текста

        start_y = 0
        if position == "center":
            start_y = (self.screen_height - total_height) // 2
        else:
            start_y = y_offset  # Было position[1]
        current_y = start_y + y_offset
        for line in lines:
            text_surface = font.render(line, True, color)
            text_rect = text_surface.get_rect()
            if position == "center":
                text_rect.center = (self.screen_width // 2, current_y)
            else:
                text_rect.topleft = (0, current_y)  # Было position[0]
            screen.blit(text_surface, text_rect)
            current_y += text_surface.get_height()
        screen.blit(self.persimmona_image, self.persimmona_rect)

    def display_dialog_sentence(self, screen, sentence, y_position):
        """Отображает предложение диалога в заданной позиции."""
        self.display_text(screen, sentence, FONT_COLOR, 'assets/fonts/Persimmona.ttf', 24,
                          position="center", y_offset=y_position)

    def display_red_text_center(self, screen, sentence):
        """Отображает красный текст в центре экрана."""
        self.display_text(screen, sentence, RED_COLOR, 'assets/fonts/Persimmona.ttf', 24, position="center")

    def display_next_sentence(self, screen):
        """Отображает следующее предложение диалога, разделяя красный текст."""
        if self.dialog_index < len(self.show_dialog()):
            sentence = self.show_dialog()[self.dialog_index]
            lines = sentence.split('\n')
            # Определяем, есть ли красный текст (последние 3 строки)
            if len(lines) > 3:
                # Отображаем обычный диалог (все строки, кроме последних трех) внизу
                normal_dialog = '\n'.join(lines[:-3])
                self.display_dialog_sentence(screen, normal_dialog, self.screen_height - 600)

                # Отображаем красный текст (последние три строки) в центре
                red_text = '\n'.join(lines[-3:])
                self.display_red_text_center(screen, red_text)
            else:
                # Если нет красного текста, отображаем весь диалог внизу
                self.display_dialog_sentence(screen, sentence, self.screen_height - 600)
        pygame.display.flip()

    def reset_game(self):
        """Сбрасывает состояние игры."""
        self.board = [['' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.current_player = 'X'
        self.game_over = False
        self.winner = None
        self.post_win_dialog_index = 0
        self.show_puzzle = False  # Скрываем nextpuzzle
        self.puzzle_solved = False  # Сбрасываем флаг
        self.final_dialog_index = 0  # Сбрасываем индекс финального диалога

    def try_move(self, board, player):
        """Проверяет, может ли игрок выиграть, и делает ход, если да."""
        size = GRID_SIZE
        for row in range(size):
            for col in range(size):
                if board[row][col] == '':
                    board[row][col] = player  # Временно ставит символ игрока
                    self.board = board
                    if self.check_winner(player):
                        return row, col  # Игрок выигрывает!
                    board[row][col] = ''  # Отменяет ход
        return None, None

    def bot_move(self):
        """Улучшенный бот: блокировка, победа, центр, смежность."""
        board = self.board
        size = GRID_SIZE

        # 1. Проверка возможности победы
        row, col = self.try_move(board, 'O')
        if row is not None:
            board[row][col] = 'O'
            self.board = board
            return True  # Бот выигрывает!

        # 2. Проверка необходимости блокировки
        row, col = self.try_move(board, 'X')
        if row is not None:
            board[row][col] = 'O'
            self.board = board
            return True  # Блокирует игрока

        # 3. Предпочтение центральным позициям
        center_row = size // 2
        center_col = size // 2
        if board[center_row][center_col] == '':
            board[center_row][center_col] = 'O'
            # board[center_row][center_col] = 'O'  # Дубликат строки. Возможно, стоит убрать
            self.board = board
            return True

        # 4. Анализ смежных позиций
        for row in range(size):
            for col in range(size):
                if board[row][col] == 'O':  # Ищет свои символы
                    # Проверяет соседние позиции
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue  # Пропускает текущую позицию
                            new_row = row + dr
                            new_col = col + dc
                            if 0 <= new_row < size and 0 <= new_col < size and board[new_row][new_col] == '':
                                board[new_row][new_col] = 'O'  # Расширяет свои владения
                                self.board = board
                                return True

        # 5. Случайный ход (если ничего не подошло)
        empty_cells = [(r, c) for r in range(size) for c in range(size) if board[r][c] == '']
        if empty_cells:
            row, col = random.choice(empty_cells)
            board[row][col] = 'O'
            self.board = board
            return True

        return False  # Нет доступных ходов

    def show_post_win_dialog(self):
        """Возвращает диалог после победы игрока."""
        return [
            "Юху поздравляю! (К)",
            "Ну и что нам это дало? Эх... (П)",
            "*Персиммона от злости роняет кусок мяса на пол*",
            "*Она наклоняется, чтобы поднять его*",
            "Стой! Тут ещё одна записка! (П)",
            "Серьёзно? Где? (К)",
            "Она приклеена под столом. Ну-ка... (П)",
            '"Следующее испытание вас ждёт во улице"',
            "Ну-у-у, у нас не то чтобы был выбор с тобой...(П)",
            "Пойдём! (К)", "*спустя некоторое время* (типо губка боб мем, можно кста такое сделать если хотите)",
            "Я нашла коробку с задней частью для ключа! (К)", "Очень похоже на игру Пятнашки. (П)",
            "Судя по запискам нашего анонима, мы на правильном пути... (П)",
            "Приготовься!\n\nЗадача: Собрать все пятнашки.\nПередвигайте плитки, чтобы расположить их по порядку от 1 до 15.\nПустая клетка должна быть в правом нижнем углу."
        ]

    def draw_puzzle(self, screen, puzzle):
        """Рисует доску nextpuzzle."""
        font = pygame.font.Font(None, self.puzzle_cell_size // 2)
        for row in range(puzzle.size):
            for col in range(puzzle.size):
                tile = puzzle.board[row][col]
                x = self.puzzle_x_offset + col * self.puzzle_cell_size
                y = self.puzzle_y_offset + row * self.puzzle_cell_size  # исправил
                pygame.draw.rect(screen, (100, 100, 100), (x, y, self.puzzle_cell_size, self.puzzle_cell_size))
                if tile != 0:
                    text = font.render(str(tile), True, (255, 255, 255))
                    text_rect = text.get_rect(center=(x + self.puzzle_cell_size // 2, y + self.puzzle_cell_size // 2))
                    screen.blit(text, text_rect)
                pygame.draw.rect(screen, LINE_COLOR, (x, y, self.puzzle_cell_size, self.puzzle_cell_size), 1)  # Обводка

    def show_final_dialog(self):
        """Возвращает финальный диалог после решения NextPuzzle."""
        return [
            "Получилось! (К)",
            "Стой, что это был за звук? (П)",
            "Ключи от коробки упали, теперь мы наконец узнаём, что же в ней находится! (К)",
            "Момент истины... (П)",
            "*звук открывания*", "*в коробке лежало очень много мяса и рыбья чешуя",
            "Похоже, что наш вор не успел замести все свои следы до конца. (П)",
            "Чешуя - важная зацепка в нашем деле! (П)", "Что ж, пора отправляться в порт... (П)"
        ]

    def draw_dialog(self, screen, dialog_function, dialog_index_name):
        """Отображает диалоговое окно."""
        dialog = dialog_function()  # Получаем список предложений диалога
        dialog_index = getattr(self, dialog_index_name)  # Получаем текущий индекс диалога
        if dialog_index < len(dialog):
            sentence = dialog[dialog_index]
            lines = sentence.split('\n')

            # Определяем, есть ли красный текст (последние 3 строки)
            if len(lines) > 3:
                # Отображаем обычный диалог (все строки, кроме последних трех) внизу
                normal_dialog = '\n'.join(lines[:-3])
                self.display_dialog_sentence(screen, normal_dialog, self.screen_height - 600)

                # Отображаем красный текст (последние три строки) в центре
                red_text = '\n'.join(lines[-3:])
                self.display_red_text_center(screen, red_text)
            else:
                # Если нет красного текста, отображаем весь диалог внизу
                self.display_dialog_sentence(screen, sentence, self.screen_height - 600)
            pygame.display.flip()

class NextPuzzle:
    def __init__(self):
        self.size = 4  # Размер поля (4x4)
        self.board = list(range(1, self.size * self.size)) + [0]  # Инициализация доски
        random.shuffle(self.board)  # Перемешиваем плитки
        self.board = [self.board[i:i + self.size] for i in range(0, len(self.board), self.size)]  # Преобразуем в 2D
        self.empty_row, self.empty_col = self.find_empty()
        self.game_over = False

    def find_empty(self):
        """Находит позицию пустой клетки (0)."""
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] == 0:
                    return r, c

    def move(self, direction):
        """Перемещает плитку в указанном направлении."""
        if self.game_over:
            return

        row, col = self.empty_row, self.empty_col

        if direction == "up" and row < self.size - 1:
            new_row, new_col = row + 1, col
        elif direction == "down" and row > 0:
            new_row, new_col = row - 1, col
        elif direction == "left" and col < self.size - 1:
            new_row, new_col = row, col + 1
        elif direction == "right" and col > 0:
            new_row, new_col = row, col - 1
        else:
            return  # Недопустимый ход

        self.board[row][col], self.board[new_row][new_col] = self.board[new_row][new_col], self.board[row][col]
        self.empty_row, self.empty_col = new_row, new_col

        if self.is_solved():
            self.game_over = True

    def is_solved(self):
        """Проверяет, решена ли головоломка."""
        solution = list(range(1, self.size * self.size)) + [0]
        solved_board = [solution[i:i + self.size] for i in range(0, len(solution), self.size)]
        solved_board[-1][-1] = 0  # Учитываем, что 0 должен быть в конце
        return self.board == solved_board