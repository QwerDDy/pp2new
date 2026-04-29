import pygame
import json
import random
from persistence import save_leaderboard
import os
def create_game(settings):
    car1 = pygame.image.load("Endterm/TSIS3/assets/370z.png").convert_alpha()
    car1 = pygame.transform.scale(car1, (125, 150))

    car2 = pygame.image.load("Endterm/TSIS3/assets/500x.png").convert_alpha()
    car2 = pygame.transform.scale(car2, (125, 150))
    car3 = pygame.image.load("Endterm/TSIS3/assets/Actros.png").convert_alpha()
    car3 = pygame.transform.scale(car3, (125, 150))
    car4 = pygame.image.load("Endterm/TSIS3/assets/DB9.png").convert_alpha()
    car4 = pygame.transform.scale(car4, (125, 150))
    car5 = pygame.image.load("Endterm/TSIS3/assets/Giulia.png").convert_alpha()
    car5 = pygame.transform.scale(car5, (125, 150))
    car6 = pygame.image.load("Endterm/TSIS3/assets/Tipo.png").convert_alpha()
    car6 = pygame.transform.scale(car6, (125, 150))
    car7 = pygame.image.load("Endterm/TSIS3/assets/VNL300.png").convert_alpha()
    car7 = pygame.transform.scale(car7, (125, 150))
    coint = pygame.image.load("Endterm/TSIS3/assets/dollar.png").convert_alpha()
    coint = pygame.transform.scale(coint, (30, 30))
    xpos = 400
    ypos = 600
    return{
        'score' : 0,
        'speed' : 5,
        'distance' : 0,
        'isgameover' : False,
        'settings':settings,
        'enemies':[car1,car2,car3,car4,car5,car6,car7],
        'enlist':[],
        'spawntimer':0,
        'player': pygame.Rect(xpos+35,ypos,65,150),
        'car': pygame.image.load('Endterm/TSIS3/assets/Viper.png').convert_alpha(),
        'xpos':xpos,
        'ypos':ypos,
        #boost
        'boost_active': False,
        'boost_timer': 0,
        'shield_active': False,
        'shield_timer': 0,
        'base_speed': 5,
        #line
        'line':0,
        #name
        'username': '',
        'coins': [],
        'cointimer': 0,
        'coint': coint,
        'traps': [],
        'traptimer': 0,
        'coincount': 0,
    }

def moves(game,event):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        game['xpos'] -= 10

    elif keys[pygame.K_RIGHT]:
        game['xpos'] +=10

    game['xpos'] = max(150, min(580, game['xpos']))   

    game['player'].x = game['xpos']
    game['player'].y = game['ypos']

    if keys[pygame.K_SPACE] and not game['boost_active']:
        game['boost_active'] = True
        game['boost_timer'] = 180  # 3 секунды
        game['speed'] = game['base_speed'] + 5
    if keys[pygame.K_s] and not game['shield_active']:
        game['shield_active'] = True
        game['shield_timer'] = 300  # 5 секунд

    
    

def update(game):
    if game['isgameover']:
        return

    # таймер буста
    if game['boost_active']:
        game['boost_timer'] -= 1
        game['score'] += 2  # двойной счёт во время буста
        if game['boost_timer'] <= 0:
            game['boost_active'] = False
            game['speed'] = game['base_speed']

# таймер щита
    if game['shield_active']:
        game['shield_timer'] -= 1
        if game['shield_timer'] <= 0:
            game['shield_active'] = False

    # спавн врагов
    game['spawntimer'] += 1
    if game['spawntimer'] > 300:
        enemy_img = random.choice(game['enemies'])
        x = random.randint(170, 500)
        rect = pygame.Rect(x, -100, 60, 150)  # меньше размер
        game['enlist'].append({
            'img': enemy_img,
            'rect': rect,
            'dx': random.choice([-1, 0, 0, 0, 1])  # чаще прямо
        })
        game['spawntimer'] = 0
    elif game['spawntimer'] == 250:
        game['distance'] +=1
    # движение врагов
    for enemy in game['enlist']:
        enemy['rect'].y += game['speed']
        enemy['rect'].x += enemy['dx']
        # не выезжают за дорогу
        enemy['rect'].x = max(155, min(580, enemy['rect'].x))

    # удаление вышедших за экран
    game['enlist'] = [e for e in game['enlist'] if e['rect'].y < 800]

    # обновляем игрока
    game['player'].x = game['xpos']
    game['player'].y = game['ypos']

    # столкновения
    for enemy in game['enlist'][:]:  # копия списка
        if game['player'].colliderect(enemy['rect']):
            if game['shield_active']:
                game['enlist'].remove(enemy)
                game['score'] += 50
            else:
                game['isgameover'] = True
                print("saving:", game['username'], game['score'], game['distance'])
                save_leaderboard(game['username'], game['score'], game['distance'])

                return

    # счёт и ускорение каждые 200 очков
    game['score'] += 1
    if game['score'] % 1000 == 0:
        game['speed'] += 1
        game['base_speed'] += 1
    game['cointimer'] += 1
    if game['cointimer'] > 180:
        x = random.randint(170, 550)
        game['coins'].append(pygame.Rect(x, -30, 30, 30))
        game['cointimer'] = 0

# движение монет
    for coin in game['coins']:
        coin.y += game['speed']
    game['coins'] = [c for c in game['coins'] if c.y < 800]

# сбор монет
    for coin in game['coins'][:]:
        if game['player'].colliderect(coin):
            game['coins'].remove(coin)
            game['score'] += 10
            game['coincount'] += 1

# спавн ловушек (масляное пятно)
    game['traptimer'] += 1
    if game['traptimer'] > 400:
        x = random.randint(170, 550)
        game['traps'].append(pygame.Rect(x, -40, 50, 30))
        game['traptimer'] = 0

# движение ловушек
    for trap in game['traps']:
        trap.y += game['speed']
    game['traps'] = [t for t in game['traps'] if t.y < 800]

# столкновение с ловушкой — замедляет
    for trap in game['traps'][:]:
        if game['player'].colliderect(trap):
            game['traps'].remove(trap)
            game['speed'] = max(2, game['speed'] - 2)

    


def draw(game,screen):
    game['line'] = (game['line'] + game['speed']) % 60
    screen.fill((0,120,0))

    pygame.draw.rect(screen,(50,50,50),(150,0,500,800))
    if not(game['isgameover']):
        for i in range(-1, 15):
            pygame.draw.rect(
                screen,
                (255, 255, 255),
                (400, i * 60 + game['line'], 10, 40)
    )
    #pygame.draw.rect(screen,(255,0,0),game['player'])
    pcar = pygame.transform.scale(game['car'], (125, 150))
    screen.blit(pcar,(game['xpos']-29,game['ypos']))

    for enemy in game['enlist']:
        screen.blit(enemy['img'], (enemy['rect'].x-32,enemy['rect'].y))
        #pygame.draw.rect(screen, (255, 0, 0), enemy['rect'], 2)

    font = pygame.font.Font(None,40)
    text = font.render(f'score:{game["score"]}',True,(255,0,0))
    screen.blit(text,(20,20))

    speedtext = font.render(f'speed:{game["speed"]}',True,(255,0,0))
    screen.blit(speedtext,(20,60))

    distext = font.render(f"distance:{game['distance']}",True,(255,0,0))
    screen.blit(distext,(20,100))

    if game['boost_active']:
        btxt = font.render(f'BOOST: {game["boost_timer"]//60+1}s', True, (255, 200, 0))
        screen.blit(btxt, (20, 140))

    if game['shield_active']:
        # синий круг вокруг машины
        cx = game['xpos'] + 30
        cy = game['ypos'] + 75
        pygame.draw.circle(screen, (0, 150, 255), (cx, cy), 70, 3)
        stxt = font.render(f'SHIELD: {game["shield_timer"]//60+1}s', True, (0, 150, 255))
        screen.blit(stxt, (20, 180))
    
    # монеты
    for coin in game['coins']:
        screen.blit(game['coint'], (coin.x, coin.y))

    # ловушки — красный квадрат
    for trap in game['traps']:
        pygame.draw.rect(screen, (220, 30, 30), trap)
        pygame.draw.rect(screen, (150, 0, 0), trap, 3)

    # счётчик монет
    cointxt = font.render(f'coins:{game["coincount"]}', True, (255, 200, 0))
    screen.blit(cointxt, (20, 220))
    
    