import pygame
from config import w, h, COLOR_BACKGROUND, COLOR_TEXT


def main_menu(screen, clock):
    while True:
        clock.tick(30)
        screen.fill(COLOR_BACKGROUND)

        font_big = pygame.font.SysFont("arial", 60, bold=True)
        screen.blit(font_big.render("GAME", True, COLOR_TEXT), (w // 2 - 200, 40))

        font = pygame.font.SysFont("arial", 24)

        pygame.draw.rect(screen, (100,100,100), (150, 150, 300, 50))
        pygame.draw.rect(screen, COLOR_TEXT, (150, 150, 300, 50), 2)
        screen.blit(font.render("Играть", True, COLOR_TEXT), (260, 163))

        pygame.draw.rect(screen, (100,100,100), (150, 220, 300, 50))
        pygame.draw.rect(screen, COLOR_TEXT, (150, 220, 300, 50), 2)
        screen.blit(font.render("Лидерборд", True, COLOR_TEXT), (230, 233))

        pygame.draw.rect(screen, (100,100,100), (150, 290, 300, 50))
        pygame.draw.rect(screen, COLOR_TEXT, (150, 290, 300, 50), 2)
        screen.blit(font.render("Настройки", True, COLOR_TEXT), (230, 303))

        pygame.draw.rect(screen, (100,100,100), (150, 360, 300, 50))
        pygame.draw.rect(screen, COLOR_TEXT, (150, 360, 300, 50), 2)
        screen.blit(font.render("Выход", True, COLOR_TEXT), (265, 373))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if 150 < mx < 450 and 150 < my < 200:
                    return "play"
                if 150 < mx < 450 and 220 < my < 270:
                    return "leaderboard"
                if 150 < mx < 450 and 290 < my < 340:
                    return "settings"
                if 150 < mx < 450 and 360 < my < 410:
                    return "quit"


def username_input(screen, clock):
    username = ""

    while True:
        clock.tick(30)
        screen.fill(COLOR_BACKGROUND)

        font_big = pygame.font.SysFont("arial", 48, bold=True)
        screen.blit(font_big.render("Введите имя", True, COLOR_TEXT), (w // 2 - 150, 80))

        pygame.draw.rect(screen, (100,100,100), (100, 180, 400, 50))
        pygame.draw.rect(screen, COLOR_TEXT, (100, 180, 400, 50), 3)
        font = pygame.font.SysFont("arial", 32)
        screen.blit(font.render(username, True, COLOR_TEXT), (110, 190))

        btn_x, btn_y = w // 2 - 75, 280
        pygame.draw.rect(screen, (100,100,100), (btn_x, btn_y, 150, 50))
        pygame.draw.rect(screen, COLOR_TEXT, (btn_x, btn_y, 150, 50), 2)
        screen.blit(font.render("Начать", True, COLOR_TEXT), (btn_x + 20, btn_y + 10))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                elif event.key == pygame.K_RETURN:
                    if len(username) > 0:
                        return username
                else:
                    if len(username) < 20:
                        username += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if btn_x < mx < btn_x+150 and btn_y < my < btn_y+50:
                    if len(username) > 0:
                        return username


def leaderboard_screen(screen, clock, top_10):
    while True:
        clock.tick(30)
        screen.fill(COLOR_BACKGROUND)

        font_title = pygame.font.SysFont("arial", 48, bold=True)
        screen.blit(font_title.render("ЛИДЕРБОРД ТОП-10", True, COLOR_TEXT), (w // 2 - 250, 20))

        font = pygame.font.SysFont("arial", 20)
        y = 90

        if len(top_10) == 0:
            screen.blit(font.render("Нет данных", True, COLOR_TEXT), (w // 2 - 60, 150))
        else:
            screen.blit(font.render("Место | Имя | Счет | Уровень", True, (255,255,0)), (30, y))
            y += 35
            for i, (name, score, level, date) in enumerate(top_10, 1):
                line = f"{i}. {name} | {score} | Уровень {level}"
                screen.blit(font.render(line, True, COLOR_TEXT), (30, y))
                y += 25

        btn_x, btn_y = w // 2 - 75, h - 80
        pygame.draw.rect(screen, (100,100,100), (btn_x, btn_y, 150, 50))
        pygame.draw.rect(screen, COLOR_TEXT, (btn_x, btn_y, 150, 50), 2)
        font2 = pygame.font.SysFont("arial", 24)
        screen.blit(font2.render("Назад", True, COLOR_TEXT), (btn_x + 40, btn_y + 12))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if btn_x < mx < btn_x+150 and btn_y < my < btn_y+50:
                    return True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True


def settings_screen(screen, clock, settings):
    while True:
        clock.tick(30)
        screen.fill(COLOR_BACKGROUND)

        font_title = pygame.font.SysFont("arial", 48, bold=True)
        screen.blit(font_title.render("НАСТРОЙКИ", True, COLOR_TEXT), (w // 2 - 150, 40))

        font = pygame.font.SysFont("arial", 24)

        sound_text = "ЗВУК: ВКЛ" if settings["sound_enabled"] else "ЗВУК: ВЫКЛ"
        pygame.draw.rect(screen, (100,100,100), (100, 150, 400, 50))
        pygame.draw.rect(screen, COLOR_TEXT, (100, 150, 400, 50), 2)
        screen.blit(font.render(sound_text, True, COLOR_TEXT), (240, 163))

        btn_x, btn_y = w // 2 - 75, 230
        pygame.draw.rect(screen, (100,100,100), (btn_x, btn_y, 150, 50))
        pygame.draw.rect(screen, COLOR_TEXT, (btn_x, btn_y, 150, 50), 2)
        screen.blit(font.render("Сохранить", True, COLOR_TEXT), (btn_x + 10, btn_y + 12))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if 100 < mx < 500 and 150 < my < 200:
                    settings["sound_enabled"] = not settings["sound_enabled"]
                if btn_x < mx < btn_x+150 and btn_y < my < btn_y+50:
                    return True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True


def game_over_screen(screen, clock, score, level, personal_best):
    while True:
        clock.tick(30)
        screen.fill(COLOR_BACKGROUND)

        font_title = pygame.font.SysFont("arial", 60, bold=True)
        screen.blit(font_title.render("КОНЕЦ ИГРЫ", True, (255,0,0)), (w // 2 - 180, 40))

        font = pygame.font.SysFont("arial", 32)
        screen.blit(font.render(f"Счет:{score}", True, COLOR_TEXT), (w // 2 - 150, 130))
        screen.blit(font.render(f"Уровень:{level}", True, COLOR_TEXT), (w // 2 - 150, 180))
        screen.blit(font.render(f"Рекорд:{personal_best}", True, (255,255,0)), (w // 2 - 150, 230))

        font2 = pygame.font.SysFont("arial", 24)

        pygame.draw.rect(screen, (100,100,100), (50, 320, 200, 50))
        pygame.draw.rect(screen, COLOR_TEXT, (50, 320, 200, 50), 2)
        screen.blit(font2.render("Заново", True, COLOR_TEXT), (120, 333))

        pygame.draw.rect(screen, (100,100,100), (350, 320, 200, 50))
        pygame.draw.rect(screen, COLOR_TEXT, (350, 320, 200, 50), 2)
        screen.blit(font2.render("меню", True, COLOR_TEXT), (420, 333))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if 50 < mx < 250 and 320 < my < 370:
                    return "retry"
                if 350 < mx < 550 and 320 < my < 370:
                    return "menu"