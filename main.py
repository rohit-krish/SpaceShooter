# coordinates in opencv and pygame are the same [which starts from the top left corner]
import pygame
import os

# initialise the pygame font lib
pygame.font.init()
# initialise the pygame sound lib
pygame.mixer.init()

pygame.display.set_caption('Space Shooter')
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

WHITE = (255, 255, 255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
FPS = 60
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
VEL = 2
BULLET_VEL = 7
MAX_BULLETS = 3

BORDER = pygame.Rect(WIDTH/2 - 11.5, 0, 10, HEIGHT)

YELLOW_INIT_X, YELLOW_INIT_Y = (
    WIDTH/4) - SPACESHIP_WIDTH/2, (HEIGHT/2) - SPACESHIP_HEIGHT/2

RED_INIT_X, RED_INIT_Y = (WIDTH*(3/4)) - SPACESHIP_WIDTH / \
    2, (HEIGHT/2) - SPACESHIP_HEIGHT/2

# CREATING A NEW EVENT , adding additional number is because to make sure the event id is unique
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

HEALTH_FONT = pygame.font.SysFont('comicsans',40)
WINNER_FONT = pygame.font.SysFont('comicsans',100)

BACKGROUND_SOUND = pygame.mixer.Sound(os.path.join('PYGAME','Space Shooter','Assets','background.mp3'))
BACKGROUND_SOUND.play()

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('PYGAME','Space Shooter','Assets','Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('PYGAME','Space Shooter','Assets','Gun+Silencer.mp3'))
WON_SOUND = pygame.mixer.Sound(os.path.join('PYGAME','Space Shooter','Assets','won.mp3'))

# importing the images
# using os is not manditory
YELLOW_SPACESHIP_IMGAE = pygame.image.load(
    os.path.join('PYGAME', 'Space Shooter', 'Assets', 'spaceship_yellow.png'))
RED_SPACESHIP_IMGAE = pygame.image.load(
    os.path.join('PYGAME', 'Space Shooter', 'Assets', 'spaceship_red.png'))

# rotating and scaling the image {rotating takespalce anticlock wise}
YELLOW_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(
        YELLOW_SPACESHIP_IMGAE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(
        RED_SPACESHIP_IMGAE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

SPACE = pygame.transform.scale(
    pygame.image.load(os.path.join('PYGAME', 'Space Shooter', 'Assets', 'space.png')), (WIDTH, HEIGHT))



def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):

    # WIN.fill(WHITE)
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render('Health: '+str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render(
        'Health: '+str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width()-10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))


    for bullet in red_bullets:
        pygame.draw.rect(WIN,RED,bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN,YELLOW,bullet)

    # we have to update the display inorder to work the changed that we do the display
    pygame.display.update()


def handle_movement(key_pressed, yellow, red):

    # YELLOW
    if key_pressed[pygame.K_s] and yellow.x > 7:  # LEFT
        yellow.x -= VEL
    if key_pressed[pygame.K_f] and yellow.x < WIDTH/2-SPACESHIP_WIDTH:  # RIGHT
        yellow.x += VEL
    if key_pressed[pygame.K_d] and yellow.y < HEIGHT - (SPACESHIP_HEIGHT+23):  # BOTTOM
        yellow.y += VEL
    if key_pressed[pygame.K_e] and yellow.y - 5> 0:  # TOP
        yellow.y -= VEL

    # RED
    if key_pressed[pygame.K_l] and red.x+VEL < WIDTH-(SPACESHIP_WIDTH - 10):  # RIGHT
        red.x += VEL
    if key_pressed[pygame.K_j] and red.x > WIDTH/2 + 1:  # LEFT
        red.x -= VEL
    if key_pressed[pygame.K_k] and red.y < HEIGHT - (SPACESHIP_HEIGHT+23):  # BOTTOM
        red.y += VEL
    if key_pressed[pygame.K_i] and red.y - 4> 1:  # TOP
        red.y -= VEL

def handle_bullets(yellow_bullets:list,red_bullets:list,yellow:pygame.Rect,red:pygame.Rect):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet): # did yellow's bullet collide with red rect
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH and len(yellow_bullets) > 0:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet): # did red's bullet collide with yellow rect
            pygame.event.post(pygame.event.Event(RED_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0 and len(red_bullets) > 0:
            red_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text,1,WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
             2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    BACKGROUND_SOUND.stop()
    WON_SOUND.play()
    pygame.time.delay(5000)

def main():

    # creating 2 rect to control the space ship
    red = pygame.Rect(RED_INIT_X, RED_INIT_Y,
                      SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(YELLOW_INIT_X, YELLOW_INIT_Y,
                         SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    clock = pygame.time.Clock()
    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    while True:
        # setting the framerate
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width, yellow.y+yellow.height/2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_SEMICOLON and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        red.x, red.y+red.height/2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ''
        if red_health <= 0:
            # the following line is because if we get 0 health then the function won't call unless i call here
            draw_window(red, yellow,red_bullets,yellow_bullets,red_health,yellow_health)
            winner_text = 'YELLOW WINS!'

        if yellow_health <= 0:
            # the following line is because if we get 0 health then the function won't call unless i call here
            draw_window(red, yellow,red_bullets,yellow_bullets,red_health,yellow_health)
            winner_text = 'RED WINS!'

        if winner_text != '':
            draw_winner(winner_text)
            break

        key_pressed = pygame.key.get_pressed()
        handle_movement(key_pressed, yellow, red)
        handle_bullets(yellow_bullets,red_bullets,yellow,red)
        draw_window(red, yellow,red_bullets,yellow_bullets,red_health,yellow_health)

    # pygame.quit()
    # instead of quiting the game call the main again to continue playing the game
    WON_SOUND.stop()
    BACKGROUND_SOUND.play()
    main()


if __name__ == '__main__':
    main()
