import pygame
import random
import json
from ui import draw_settings
from persistence import load_settings,save_settings
from racer import create_game,moves,update,draw
pygame.init()


# screen
w,h = 800,800
screen = pygame.display.set_mode((w,h))
fps = 60
clock = pygame.time.Clock() 

#varibles
running = True

state = 'menu'
menu = 'menu'
vgame = 'game'
vsetting = 'setting'
vleaders = 'leaders'
vquit = 'quit'

action = 'menu'


#functions

def get_menu(screen, event):
    begrawnd = pygame.draw.rect(screen,(50,50,50),(30,30,740,740))

    bgame = pygame.draw.rect(screen,(255,0,0),(350,200,100,50))
    bsetting = pygame.draw.rect(screen,(0,255,0),(350,300,100,50))
    bleaders = pygame.draw.rect(screen,(0,0,255),(350,400,100,50))
    bquit = pygame.draw.rect(screen,(255,120,0),(350,500,100,50))

    if event.type == pygame.MOUSEBUTTONDOWN:
        if bgame.collidepoint(event.pos):
            return vgame
        elif bsetting.collidepoint(event.pos):
            return vsetting
        elif bleaders.collidepoint(event.pos):
            return vleaders
        elif bquit.collidepoint(event.pos):
            return vquit
    return None


#setting func

settings = load_settings()
game = create_game(settings)

pygame.mixer.music.load("Endterm/TSIS3/assets/music.mp3")
pygame.mixer.music.set_volume(settings.get('volume', 0.5))
if settings.get('sound', True):
    pygame.mixer.music.play(-1)
#leaderboard

# username
def get_username(screen, clock):
    font = pygame.font.Font(None, 50)
    small = pygame.font.Font(None, 36)
    name = ''
    while True:
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (50, 50, 50), (200, 250, 400, 300))
        
        title = font.render('name:', True, (255, 0, 0))
        screen.blit(title, (300, 280))
        
        pygame.draw.rect(screen, (80, 80, 80), (250, 350, 300, 50))
        name_txt = font.render(name, True, (255, 200, 0))
        screen.blit(name_txt, (260, 360))
        
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name.strip():
                    return name.strip()
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif len(name) < 12:
                    name += event.unicode
        
        pygame.display.flip()
        clock.tick(fps)

while running:
    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif state == vsetting:
            action, settings = draw_settings(screen, event, settings)
            if action == "back":
                save_settings(settings)
                pygame.mixer.music.set_volume(settings.get('volume', 0.5))
                state = menu

    if state == menu:
        action = get_menu(screen, event)
        if action == vgame:
            username = get_username(screen, clock)
            game = create_game(settings)
            game['username'] = username
            state = vgame
        elif action == vsetting:
            state = vsetting
        elif action == vleaders:
            state = vleaders
        elif action == vquit:
            running = False

    elif state == vgame:
        moves(game, event)
        update(game)
        draw(game, screen)

    elif state == vsetting:
        draw_settings(screen, event, settings)

    elif state == vleaders:
        from persistence import load_leaderboard
        data = load_leaderboard()
        font = pygame.font.Font(None, 40)
        screen.fill((0, 0, 0))
        for i, entry in enumerate(data):
            txt = font.render(f"{i+1}. {entry['name']} — {entry['score']}", True, (255,255,255))
            screen.blit(txt, (250, 100 + i * 50))
        back = pygame.draw.rect(screen, (180, 30, 30), (330, 650, 140, 45))
        screen.blit(font.render("НАЗАД", True, (255,255,255)), (355, 660))
        if event.type == pygame.MOUSEBUTTONDOWN:
            if back.collidepoint(event.pos):
                state = menu

    pygame.display.flip()
    clock.tick(fps)

        

    
    
    

    

