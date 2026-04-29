import pygame

def draw_settings(screen, event, settings):

    slider_x = 300
    slider_y = 300
    slider_w = 200
    slider_h = 10

    volume = settings["volume"]

    # фон экрана
    pygame.draw.rect(screen, (40, 40, 40), (150, 150, 500, 400))

    # текст
    font = pygame.font.Font(None, 40)
    text = font.render("valume", True, (255,255,255))
    screen.blit(text, (350, 250))

    # линия слайдера
    pygame.draw.rect(screen, (120,120,120), (slider_x, slider_y, slider_w, slider_h))

    # обработка клика / drag
    if event.type == pygame.MOUSEBUTTONDOWN:
        mx, my = event.pos

        if slider_x <= mx <= slider_x + slider_w:
            volume = (mx - slider_x) / slider_w
            settings["volume"] = volume

    # заполнение
    fill = int(slider_w * volume)
    pygame.draw.rect(screen, (255,0,0), (slider_x, slider_y, fill, slider_h))

    # кнопка back
    back_btn = pygame.Rect(180, 480, 120, 40)
    pygame.draw.rect(screen, (200, 0, 0), back_btn)

    back_text = font.render("BACK", True, (255,255,255))
    screen.blit(back_text, (200, 490))

    if event.type == pygame.MOUSEBUTTONDOWN:
        if back_btn.collidepoint(event.pos):
            return "back", settings

    return None, settings