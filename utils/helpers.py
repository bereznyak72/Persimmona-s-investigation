import pygame

def start_text_animation(obj, text):
    """Запускает анимацию текста для объекта."""
    if isinstance(text, (list, tuple)):
        obj.text_lines = text
        obj.full_text = " ".join(text)
    else:
        obj.text_lines = [text]
        obj.full_text = text
    obj.current_text = ""
    obj.char_index = 0
    obj.last_char_time = pygame.time.get_ticks()

def update_text_animation(obj, current_time):
    """Обновляет анимацию текста."""
    if current_time - obj.last_char_time >= obj.text_animation_speed and obj.char_index < len(obj.full_text):
        obj.current_text = obj.full_text[:obj.char_index + 1]
        obj.char_index += 1
        obj.last_char_time = current_time

def render_text(screen, text, font, y_pos, max_width, color, center=False):
    """Отрисовывает текст с учетом переносов."""
    lines = wrap_text(text, font, max_width)
    for i, line in enumerate(lines):
        text_surface = font.render(line, True, color)
        if center:
            text_rect = text_surface.get_rect(center=(screen.get_width() // 2, y_pos + i * 40))
        else:
            text_rect = text_surface.get_rect(topleft=(50, y_pos + i * 40))
        screen.blit(text_surface, text_rect)
    return lines  # Возвращаем строки для дальнейшей обработки, если нужно

def wrap_text(text, font, max_width):
    """Переносит текст по словам, если он превышает максимальную ширину."""
    words = text.split(" ")
    lines = []
    current_line = ""
    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line.strip())
            current_line = word + " "
    if current_line:
        lines.append(current_line.strip())
    return lines