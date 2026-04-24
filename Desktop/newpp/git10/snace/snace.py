import pygame
import random

pygame.init()

w = 600
h = 400
cell = 20

screen = pygame.display.set_mode((w, h))

clock = pygame.time.Clock()

snake = [(5, 5), (4, 5), (3, 5)]

dx = 1
dy = 0

food = (10, 10)

score = 0

running = True

while running:

    clock.tick(10)

    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                dx = -1
                dy = 0
            if event.key == pygame.K_RIGHT:
                dx = 1
                dy = 0
            if event.key == pygame.K_UP:
                dx = 0
                dy = -1
            if event.key == pygame.K_DOWN:
                dx = 0
                dy = 1

    head_x = snake[0][0]
    head_y = snake[0][1]

    new_head = (head_x + dx, head_y + dy)

    if new_head[0] < 0 or new_head[0] >= w//cell or new_head[1] < 0 or new_head[1] >= h//cell:
        running = False

    if new_head in snake:
        running = False

    snake.insert(0, new_head)

    if new_head == food:
        food = (random.randint(0, w//cell - 1), random.randint(0, h//cell - 1))
        score += 1
    else:
        snake.pop()

    pygame.draw.rect(screen, (255, 0, 0),
                     (food[0]*cell, food[1]*cell, cell, cell))

    for i in snake:
        pygame.draw.rect(screen, (0, 255, 0),
                         (i[0]*cell, i[1]*cell, cell, cell))

    font = pygame.font.SysFont("Arial", 20)
    text = font.render("score: " + str(score), True, (255, 255, 255))
    screen.blit(text, (10, 10))

    pygame.display.update()

pygame.quit()