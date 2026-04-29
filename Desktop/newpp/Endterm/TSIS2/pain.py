import pygame
import math
import datetime
import os
from collections import deque

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
UI_HEIGHT = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Advanced Pygame Painter")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# State Variables
current_color = BLACK
current_tool = 'pencil'
brush_size = 2
drawing = False
start_pos = (0, 0)
last_pos = (0, 0)

# Text Tool State
typing = False
text_buffer = ""
text_pos = (0, 0)

# Canvas
canvas = pygame.Surface((WIDTH, HEIGHT - UI_HEIGHT))
canvas.fill(WHITE)

font = pygame.font.SysFont("Arial", 22)
small_font = pygame.font.SysFont("Arial", 15)


def canvas_pos(pos):
    """Перевод координат экрана в координаты канваса"""
    return (pos[0], pos[1] - UI_HEIGHT)


def screen_pos(pos):
    """Перевод координат канваса в координаты экрана"""
    return (pos[0], pos[1] + UI_HEIGHT)


def get_shape_data(start, end, tool):
    x1, y1 = start
    x2, y2 = end
    dx, dy = x2 - x1, y2 - y1

    if tool == 'square':
        side = max(abs(dx), abs(dy))
        s_x = x1 if x2 > x1 else x1 - side
        s_y = y1 if y2 > y1 else y1 - side
        return (s_x, s_y, side, side)
    elif tool == 'right_tri':
        return [(x1, y1), (x1, y2), (x2, y2)]
    elif tool == 'equi_tri':
        height = dx * (math.sqrt(3) / 2)
        return [(x1, y2), (x2, y2), (x1 + dx / 2, y2 - height)]
    elif tool == 'rhombus':
        return [(x1 + dx / 2, y1), (x2, y1 + dy / 2), (x1 + dx / 2, y2), (x1, y1 + dy / 2)]
    elif tool == "rect":
        return (min(x1, x2), min(y1, y2), abs(dx), abs(dy))
    return None


def flood_fill(surface, x, y, new_color):
    target_color = surface.get_at((x, y))
    if target_color == new_color:
        return
    queue = deque([(x, y)])
    w, h = surface.get_size()
    while queue:
        cx, cy = queue.popleft()
        if surface.get_at((cx, cy)) != target_color:
            continue
        surface.set_at((cx, cy), new_color)
        for ddx, ddy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = cx + ddx, cy + ddy
            if 0 <= nx < w and 0 <= ny < h:
                if surface.get_at((nx, ny)) == target_color:
                    queue.append((nx, ny))


def save_canvas(surface):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    filename = os.path.join(desktop, f"drawing_{timestamp}.png")
    pygame.image.save(surface, filename)
    print(f"Сохранено: {filename}")


def draw_ui():
    # Фон панели
    pygame.draw.rect(screen, (235, 235, 235), (0, 0, WIDTH, UI_HEIGHT))
    pygame.draw.line(screen, (170, 170, 170), (0, UI_HEIGHT), (WIDTH, UI_HEIGHT), 1)

    # Инфо
    txt_info = font.render(f"Инструмент: {current_tool}   Размер: {brush_size}", True, (30, 30, 30))
    txt_ctrl = small_font.render(
        "1-0/T: инструмент   [ ]: размер   R/G/B/W: цвет   Cmd+S: сохранить",
        True, (100, 100, 100)
    )
    screen.blit(txt_info, (10, 8))
    screen.blit(txt_ctrl, (10, 38))

    # Квадратик текущего цвета
    pygame.draw.rect(screen, current_color, (WIDTH - 45, 12, 32, 32))
    pygame.draw.rect(screen, (120, 120, 120), (WIDTH - 45, 12, 32, 32), 1)


running = True
while running:
    screen.fill(WHITE)
    screen.blit(canvas, (0, UI_HEIGHT))
    mouse_pos = pygame.mouse.get_pos()
    c_mouse = canvas_pos(mouse_pos)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Режим ввода текста
        if typing:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    txt_surf = font.render(text_buffer, True, current_color)
                    canvas.blit(txt_surf, canvas_pos(text_pos))
                    text_buffer = ""
                    typing = False
                elif event.key == pygame.K_ESCAPE:
                    text_buffer = ""
                    typing = False
                elif event.key == pygame.K_BACKSPACE:
                    text_buffer = text_buffer[:-1]
                else:
                    text_buffer += event.unicode
            continue

        if event.type == pygame.KEYDOWN:
            mods = pygame.key.get_mods()

            # Cmd+S — сохранение (KMOD_META на macOS)
            if event.key == pygame.K_s and (mods & pygame.KMOD_META):
                save_canvas(canvas)

            # Инструменты
            if event.key == pygame.K_1: current_tool = 'pencil'
            if event.key == pygame.K_2: current_tool = 'line'
            if event.key == pygame.K_3: current_tool = 'rect'
            if event.key == pygame.K_4: current_tool = 'circle'
            if event.key == pygame.K_5: current_tool = 'eraser'
            if event.key == pygame.K_6: current_tool = 'square'
            if event.key == pygame.K_7: current_tool = 'right_tri'
            if event.key == pygame.K_8: current_tool = 'equi_tri'
            if event.key == pygame.K_9: current_tool = 'rhombus'
            if event.key == pygame.K_0: current_tool = 'fill'
            if event.key == pygame.K_t: current_tool = 'text'

            # Размер кисти: [ и ] (F1/F2/F3 перехватываются системой на Mac)
            if event.key == pygame.K_LEFTBRACKET:
                brush_size = max(1, brush_size - 1)
            if event.key == pygame.K_RIGHTBRACKET:
                brush_size = min(50, brush_size + 1)

            # Цвета
            if event.key == pygame.K_r: current_color = RED
            if event.key == pygame.K_g: current_color = GREEN
            if event.key == pygame.K_b: current_color = BLUE
            if event.key == pygame.K_w: current_color = BLACK

        # Клик мышью — только если ниже UI панели
        if event.type == pygame.MOUSEBUTTONDOWN and mouse_pos[1] > UI_HEIGHT:
            if current_tool == 'fill':
                flood_fill(canvas, c_mouse[0], c_mouse[1], current_color)
            elif current_tool == 'text':
                typing = True
                text_pos = mouse_pos
                text_buffer = ""
            else:
                drawing = True
                start_pos = c_mouse
                last_pos = c_mouse

        if event.type == pygame.MOUSEBUTTONUP:
            if drawing:
                if current_tool == 'line':
                    pygame.draw.line(canvas, current_color, start_pos, c_mouse, brush_size)
                elif current_tool == 'rect':
                    data = get_shape_data(start_pos, c_mouse, 'rect')
                    pygame.draw.rect(canvas, current_color, data, brush_size)
                elif current_tool == 'circle':
                    radius = int(math.hypot(c_mouse[0] - start_pos[0], c_mouse[1] - start_pos[1]))
                    pygame.draw.circle(canvas, current_color, start_pos, radius, brush_size)
                elif current_tool == 'square':
                    data = get_shape_data(start_pos, c_mouse, 'square')
                    pygame.draw.rect(canvas, current_color, data, brush_size)
                elif current_tool in ['right_tri', 'equi_tri', 'rhombus']:
                    pts = get_shape_data(start_pos, c_mouse, current_tool)
                    pygame.draw.polygon(canvas, current_color, pts, brush_size)
                drawing = False

        if event.type == pygame.MOUSEMOTION and drawing:
            if current_tool == 'pencil':
                pygame.draw.line(canvas, current_color, last_pos, c_mouse, brush_size)
                last_pos = c_mouse
            elif current_tool == 'eraser':
                pygame.draw.circle(canvas, WHITE, c_mouse, brush_size * 3)

    # Превью фигуры во время рисования
    if drawing:
        s_start = screen_pos(start_pos)
        if current_tool == 'line':
            pygame.draw.line(screen, current_color, s_start, mouse_pos, brush_size)
        elif current_tool == 'rect':
            data = get_shape_data(s_start, mouse_pos, 'rect')
            pygame.draw.rect(screen, current_color, data, brush_size)
        elif current_tool == 'circle':
            radius = int(math.hypot(mouse_pos[0] - s_start[0], mouse_pos[1] - s_start[1]))
            pygame.draw.circle(screen, current_color, s_start, radius, brush_size)
        elif current_tool == 'square':
            data = get_shape_data(s_start, mouse_pos, 'square')
            pygame.draw.rect(screen, current_color, data, brush_size)
        elif current_tool in ['right_tri', 'equi_tri', 'rhombus']:
            pts = get_shape_data(s_start, mouse_pos, current_tool)
            pygame.draw.polygon(screen, current_color, pts, brush_size)

    # Превью текста
    if typing:
        preview_txt = font.render(text_buffer + "|", True, current_color)
        screen.blit(preview_txt, text_pos)

    draw_ui()
    pygame.display.flip()

pygame.quit()