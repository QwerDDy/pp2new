import pygame
from config import w, h, COLOR_BACKGROUND
from db import create_tables, get_player_id, save_result, get_top_10, get_best_score
from settings import load_settings, save_settings
from game import create_game, update_game, draw_game
from menu import main_menu, username_input, leaderboard_screen, settings_screen, game_over_screen

pygame.init()
screen = pygame.display.set_mode((w, h))
clock = pygame.time.Clock()

create_tables()
current_settings = load_settings()

running = True
while running:
    menu_choice = main_menu(screen, clock)

    if menu_choice == "quit":
        running = False

    elif menu_choice == "play":
        username = username_input(screen, clock)
        if username is None:
            continue

        player_id = get_player_id(username)
        personal_best = get_best_score(player_id)

        game_choice = "retry"
        while game_choice == "retry":
            game = create_game()
            game_running = True

            while game_running:
                clock.tick(game["speed"])

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        game_running = False
                        running = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT and game["dx"] == 0:
                            game["dx"] = -1
                            game["dy"] = 0
                        elif event.key == pygame.K_RIGHT and game["dx"] == 0:
                            game["dx"] = 1
                            game["dy"] = 0
                        elif event.key == pygame.K_UP and game["dy"] == 0:
                            game["dx"] = 0
                            game["dy"] = -1
                        elif event.key == pygame.K_DOWN and game["dy"] == 0:
                            game["dx"] = 0
                            game["dy"] = 1
                        elif event.key == pygame.K_ESCAPE:
                            game["game_over"] = True

                update_game(game)
                draw_game(screen, game)

                if game["game_over"]:
                    save_result(player_id, game["score"], game["level"])
                    game_choice = game_over_screen(screen, clock, game["score"], game["level"], personal_best)
                    game_running = False

            if game_choice == "quit":
                running = False

    elif menu_choice == "leaderboard":
        top_10 = get_top_10()
        leaderboard_screen(screen, clock, top_10)

    elif menu_choice == "settings":
        current_settings = load_settings()
        saved = settings_screen(screen, clock, current_settings)
        if saved:
            save_settings(current_settings)

pygame.quit()