import pygame
import math

pygame.init()

# window
W, H = 800, 600
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Simple Paint")
clock = pygame.time.Clock()

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# start setup
canvas = pygame.Surface((W, H))
canvas.fill(WHITE)

tool = "brush"     # brush / rect / circle / eraser
color = BLACK
size = 6

drawing = False
start_pos = (0, 0)
last_pos = None

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # keyboard controls
        if event.type == pygame.KEYDOWN:
            # choose tool
            if event.key == pygame.K_1:
                tool = "brush"
            elif event.key == pygame.K_2:
                tool = "rect"
            elif event.key == pygame.K_3:
                tool = "circle"
            elif event.key == pygame.K_4:
                tool = "eraser"

            # choose color
            elif event.key == pygame.K_r:
                color = RED
            elif event.key == pygame.K_g:
                color = GREEN
            elif event.key == pygame.K_b:
                color = BLUE
            elif event.key == pygame.K_k:
                color = BLACK

            # brush size
            elif event.key == pygame.K_UP:
                size = min(50, size + 1)
            elif event.key == pygame.K_DOWN:
                size = max(1, size - 1)

            # clear all
            elif event.key == pygame.K_c:
                canvas.fill(WHITE)

        # mouse pressed
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            drawing = True
            start_pos = event.pos
            last_pos = event.pos

        # mouse released
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if drawing:
                end_pos = event.pos

                # draw final rectangle
                if tool == "rect":
                    x1, y1 = start_pos
                    x2, y2 = end_pos
                    rect = pygame.Rect(min(x1, x2), min(y1, y2),
                                       abs(x2 - x1), abs(y2 - y1))
                    pygame.draw.rect(canvas, color, rect, size)

                # draw final circle
                elif tool == "circle":
                    x1, y1 = start_pos
                    x2, y2 = end_pos
                    radius = int(math.hypot(x2 - x1, y2 - y1))
                    pygame.draw.circle(canvas, color, start_pos, radius, size)

            drawing = False
            last_pos = None

        # mouse move
        if event.type == pygame.MOUSEMOTION and drawing:
            mx, my = event.pos

            if tool == "brush":
                pygame.draw.line(canvas, color, last_pos, (mx, my), size)

            elif tool == "eraser":
                pygame.draw.line(canvas, WHITE, last_pos, (mx, my), size * 2)

            last_pos = (mx, my)

    # draw canvas
    screen.fill(WHITE)
    screen.blit(canvas, (0, 0))

    # preview shape while dragging
    if drawing and tool in ["rect", "circle"]:
        temp = canvas.copy()
        mx, my = pygame.mouse.get_pos()

        if tool == "rect":
            x1, y1 = start_pos
            rect = pygame.Rect(min(x1, mx), min(y1, my),
                               abs(mx - x1), abs(my - y1))
            pygame.draw.rect(temp, color, rect, size)

        elif tool == "circle":
            x1, y1 = start_pos
            radius = int(math.hypot(mx - x1, my - y1))
            pygame.draw.circle(temp, color, start_pos, radius, size)

        screen.blit(temp, (0, 0))

    # UI text
    font = pygame.font.SysFont(None, 24)
    info = f"Tool: {tool} | Size: {size} | Keys: 1-brush 2-rect 3-circle 4-eraser | R/G/B/K | C-clear"
    text = font.render(info, True, BLACK)
    screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()