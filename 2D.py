import pygame
import sys


pygame.init()


WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("2d Platformer Game")


clock= pygame.time.Clock()


#colors
WHITE = (255,255,255)
BLACK= (0,0,0)
BLUE = (50,150,255)
GREEN = (50,200,50)




player = pygame.Rect(50,HEIGHT-70,50,50)
player_speed = 5
velocity_y = 0
gravity = .5
jump_strength = 12
on_ground = False


levels = [
     [  # Level 1 platforms
        pygame.Rect(0, HEIGHT - 20, WIDTH, 20),
        pygame.Rect(200, HEIGHT - 120, 150, 20),
        pygame.Rect(450, HEIGHT - 220, 150, 20),
        pygame.Rect(650, HEIGHT - 320, 100, 20),
    ],
    [  # Level 2 platforms
        pygame.Rect(0, HEIGHT - 20, WIDTH, 20),
        pygame.Rect(100, HEIGHT - 150, 120, 20),
        pygame.Rect(350, HEIGHT - 250, 180, 20),
        pygame.Rect(600, HEIGHT - 180, 120, 20),
        pygame.Rect(700, HEIGHT - 350, 50, 20),
    ]
]


current_level = 0
platforms = levels[current_level]


def move_player(keys):
    global velocity_y,on_ground,current_level,platforms


    dx = 0
    if keys[pygame.K_LEFT]or keys[pygame.K_a]:
        dx = -player_speed
    if keys[pygame.K_RIGHT]or keys[pygame.K_d]:
        dx = player_speed
    player.x += dx
    for platform in platforms:
        if player.colliderect(platform):
            if dx > 0:
                player.right=platform.left
            if dx<0:
                player.left = platform.right
   
    if player.left >WIDTH:
        if current_level < len(levels)-1:
            current_level +=1
            platforms = levels[current_level]
            player.left = 0
    elif player.right <0:
        if current_level>0:
            current_level -=1
            platforms = levels[current_level]
            player.right = WIDTH
   
    velocity_y += gravity
    player.y += velocity_y


    on_ground = False
    for platform in platforms:
        if player.colliderect(platform):
            if velocity_y>0:
                player.bottom=platform.top
                velocity_y = 0
                on_ground = True
            elif velocity_y <0:
                player.top = platform.bottom
                velocity_y = 0




def jump():
    global velocity_y,on_ground
    if on_ground:
        velocity_y = -jump_strength


def draw():
    screen.fill(WHITE)


    for platform in platforms:
        pygame.draw.rect(screen,GREEN, platform)
   
    pygame.draw.rect(screen, BLUE, player)


    pygame.display.flip()


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or  event.key == pygame.K_w:
                jump()
   
    keys =pygame.key.get_pressed()
    move_player(keys)
    draw()
    clock.tick(60)


pygame.quit()
sys.exit()
