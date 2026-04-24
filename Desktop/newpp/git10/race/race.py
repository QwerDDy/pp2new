import pygame
import random



#display
pygame.init()
screen = pygame.display.set_mode((800,800))
fps = 60
running = True
clock = pygame.time.Clock()


#objects
car = pygame.image.load("git10/race/image/Viper.png").convert_alpha()
image = pygame.transform.scale(car, (125, 150))

car1 = pygame.image.load("git10/race/image/370z.png").convert_alpha()
car1 = pygame.transform.scale(car1, (125, 150))
car1_pos = 300
car2 = pygame.image.load("git10/race/image/500x.png").convert_alpha()
car2 = pygame.transform.scale(car2, (125, 150))
car3 = pygame.image.load("git10/race/image/Actros.png").convert_alpha()
car3 = pygame.transform.scale(car3, (125, 150))
car4 = pygame.image.load("git10/race/image/DB9.png").convert_alpha()
car4 = pygame.transform.scale(car4, (125, 150))
car5 = pygame.image.load("git10/race/image/Giulia.png").convert_alpha()
car5 = pygame.transform.scale(car5, (125, 150))
car6 = pygame.image.load("git10/race/image/Tipo.png").convert_alpha()
car6 = pygame.transform.scale(car6, (125, 150))
car7 = pygame.image.load("git10/race/image/VNL300.png").convert_alpha()
car7 = pygame.transform.scale(car7, (125, 150))
coint = pygame.image.load("git10/race/image/dollar.png").convert_alpha()
coint = pygame.transform.scale(coint, (30, 30))

enemy = [car1,car2,car3,car4,car5,car6,car7]
endict = {
        'x': random.randint(150,450),
        'y': -100,
        'speed': random.randint(3,13),
        'img': random.choice(enemy)
        }

espeed = 5

codict = {
    'x': random.randint(150,480),
    'y': -100,
}




enemies = []
enemies.append(enemy)

#spawn
spown_time = 0
dt = 0
spown_time_coin = 0



#fonts
myfont = pygame.font.Font("git10/race/fonty/bitcc.ttf",40)




#possition
xpos = 400
ypos = 600
speed = 0
line = 0

ex = 0
ey = 0

#bool
isdown = False
isup = False
isright = False
isleft = False
iscar = False
count = 0
cou = str(count)
isover = False




while running:
    screen.fill((0,120,0))
    pygame.draw.rect(screen,(50,50,50),(150,0,500,800))
    
    #font
    if not(isover):
        text = myfont.render(cou,True,'Red')
        screen.blit(text,(20,25))
    else:
        text = myfont.render("YOU LOSE!",True,'Red')
        screen.blit(text,(20,25))
    
    #road
    speed = max(0,min(speed,15))
    line += speed
    if line > 50:
        line = 0

    for i in range(-1, 15):
        pygame.draw.rect(
            screen,
            (255, 255, 255),
            (400, i * 60 + line, 10, 40)
    )
        
    screen.blit(image,(xpos,ypos))
    

    player = pygame.Rect(xpos+30, ypos,65,150)
    eplayer = pygame.Rect(endict['x']+30,endict['y'],65,150)
   





    #spawn
    spown_time += dt
    spown_time_coin += dt
    #coin
    if spown_time_coin >= 10000:
        print("spp")
        spown_time_coin = 0
        codict = {
        'x': random.randint(150,480),
        'y': -100,
        }
   
    screen.blit(coint,(codict['x'],codict['y']))
    coi = pygame.Rect(codict['x'], codict['y'],30,30)

   

        


    #enemys
    if spown_time >= 1000 and not(iscar):
        spown_time = 0
        iscar = True
        endict = {
        'x': random.randint(150,450),
        'y': -100,
        'speed': random.randint(3,13),
        'img': random.choice(enemy)
        }
        ex = endict['x']
        ey = endict['y']
        
    screen.blit(endict['img'],(endict['x'],endict['y']))

    espeed = endict['speed']
    endict['y'] += speed - espeed
    
    if endict['y'] > 800:
        espeed = 0
        iscar = False
    
    if player.colliderect(eplayer):
        print("GAME OVER")
        speed = 0
        isover = True
    
    if player.colliderect(coi):
        count+=1
        cou = str(count)
        codict['y'] = 900
        
    



    codict['y'] += speed

      
    

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and not(isover):
        xpos-=10
        isleft = True
        isright = isdown = isup = False
    elif keys[pygame.K_RIGHT] and not(isover):
        xpos+=10
        isright = True
        isleft = isdown = isup = False
    elif keys[pygame.K_UP] and not(isover):
        speed +=0.2
        isup = True
        isright = isdown = isleft = False
        
    elif keys[pygame.K_DOWN] and not(isover):
        speed -=0.2
        isdown = True
        isright = isleft = isup = False
    else:
        isright = isleft = isdown = isup = False
        speed -=0.04

    
    
    pygame.display.update()
    pygame.display.flip()
    


    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    

    dt = clock.tick(fps)
