import pygame
import random
from config import w, h, cell_size, initial_speed, COLOR_SNAKE, COLOR_FOOD, COLOR_POISON, COLOR_BACKGROUND
from settings import load_settings

def create_game():
    game = {
        "snake": [(5, 5), (4, 5), (3, 5)],
        "dx": 1,
        "dy": 0,
        "food": (10, 10),
        "poison": None,
        "score": 0,
        "level": 1,
        "speed": initial_speed,
        "food_eaten": 0,
        "game_over": False,
        "obstacles": [],
        "settings": load_settings()
    }
    
    # Спавним еду и яд
    game["food"] = spawn_food(game)
    game["poison"] = spawn_poison(game)
    
    return game

def spawn_food(game):
    
    while True:
        #местоположения еды
        x = random.randint(0, w // cell_size - 1)
        y = random.randint(0, h // cell_size - 1)
        #проверка
        if (x, y) not in game["snake"] and (x, y) not in game["obstacles"]:
            return (x, y)

def spawn_poison(game):
    
    if random.random() < 0.3: # яд с щансом 30 проц
        while True:
            x = random.randint(0, w // cell_size - 1)
            y = random.randint(0, h // cell_size - 1)
            
            if (x, y) not in game["snake"] and (x, y) != game["food"] and (x, y) not in game["obstacles"]: # проверка
                return (x, y)
    return None

def add_obstacles(game):
    """Добавляет препятствия с уровня 3"""
    game["obstacles"] = []
    num_obstacles = 2 + game["level"]
    
    for i in range(num_obstacles):
        while True:
            x = random.randint(2, w // cell_size - 3)
            y = random.randint(2, h // cell_size - 3)
            
            if (x, y) not in game["snake"]:
                game["obstacles"].append((x, y)) # если нашли позицию след итеретион
                break

def update_game(game):

    if game["game_over"]:
        return
    
    #работа с головой змеии (5,5) dx = 1 dy =0 -> (5+1,5+0) = (6,5)
    head_x = game["snake"][0][0] + game["dx"]
    head_y = game["snake"][0][1] + game["dy"]
    new_head = (head_x, head_y)
    
    # Добавляем голову
    game["snake"].insert(0, new_head)
    
    # Проверяем столкновение со стеной
    if new_head[0] < 0 or new_head[0] >= w // cell_size or \
       new_head[1] < 0 or new_head[1] >= h // cell_size:
        game["game_over"] = True
        return
    
    # Проверяем столкновение с собой
    if new_head in game["snake"][1:]:
        game["game_over"] = True
        return
    
    # Проверяем столкновение с препятствием
    if new_head in game["obstacles"]:
        game["game_over"] = True
        return
    
    # Проверяем съеденную еду
    if new_head == game["food"]:
        game["score"] += 10
        game["food_eaten"] += 1
        game["food"] = spawn_food(game)
        
        # Новый уровень
        if game["food_eaten"] >= 5:
            game["level"] += 1
            game["speed"] += 2
            game["food_eaten"] = 0
            
            # Препятствия с уровня 3
            if game["level"] == 3:
                add_obstacles(game)
    else:
        # Убираем хвост если не съели еду
        game["snake"].pop()
    
    # Проверяем съеденный яд
    if new_head == game["poison"]:
        # Укорачиваем на 2
        game["snake"] = game["snake"][:-2]
        
        # проверяем размер змеии
        if len(game["snake"]) <= 1:
            game["game_over"] = True
            return
        
        game["poison"] = spawn_poison(game)

def draw_game(screen, game):
    screen.fill(COLOR_BACKGROUND)
    
    
    for x in range(0, w, cell_size):
        pygame.draw.line(screen, (50, 50, 50), (x, 0), (x, h))
    for y in range(0, h, cell_size):
        pygame.draw.line(screen, (50, 50, 50), (0, y), (w, y))
    

    pygame.draw.rect(screen, COLOR_FOOD,
                    (game["food"][0] * cell_size, game["food"][1] * cell_size, cell_size, cell_size))# позиция на экране еда
    
    # Яд pos on the screen
    if game["poison"]:
        pygame.draw.rect(screen, COLOR_POISON,
                        (game["poison"][0] * cell_size, game["poison"][1] * cell_size, cell_size, cell_size))
    
    # Препятствия pos on the screen
    for obs in game["obstacles"]:
        pygame.draw.rect(screen, (100, 100, 100),
                        (obs[0] * cell_size, obs[1] * cell_size, cell_size, cell_size))
    
    # Змейка
    snake_color = tuple(game["settings"]["snake_color"])
    for segment in game["snake"]:
        pygame.draw.rect(screen, snake_color,
                        (segment[0] * cell_size, segment[1] * cell_size, cell_size, cell_size))
    
    # Текст
    font = pygame.font.SysFont("arial", 20)
    text_score = font.render(f"Score: {game['score']}", True, (255, 255, 255))
    text_level = font.render(f"Level: {game['level']}", True, (255, 255, 255))
    text_speed = font.render(f"Speed: {game['speed']}", True, (255, 255, 255))
    
    screen.blit(text_score, (10, 10))
    screen.blit(text_level, (10, 35))
    screen.blit(text_speed, (10, 60))
    
    pygame.display.update()