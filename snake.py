
import pygame, time, random, sys

pygame.init()

# settings
height = 400
width = 600
display = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake")

black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(240, 10, 10)
green = pygame.Color(0, 255, 0)
background = pygame.Color(36, 158, 93)
s = pygame.Color(185, 225, 95)
button = pygame.Color(1, 175, 170)
button2 = pygame.Color(1, 160, 180)
clock = pygame.time.Clock()
speed = 20

highscore = 0
delta = 20
score = 0
snakePos = [80, 240]
snakeBody = [[80, 240], [60, 240], [40, 240]]
foodPos = [random.randrange(1, width // delta) * delta, random.randrange(1, height // delta) * delta]
foodSpawn = True
direction = ''
changeto = ''

# when the user quits the game
def quit():
    pygame.event.post(pygame.event.Event(pygame.QUIT))
    sys.exit()

# when the snake is out of bounds or hits self
def gameOver():
    global score, highscore
    if score > highscore:
        highscore = score
    menu()
    
# start game
def start():
    global score, snakePos, snakeBody, foodPos, foodSpawn, direction, changeto
    score = 0
    snakePos = [80, 240]
    snakeBody = [[80, 240], [60, 240], [40, 240]]
    foodPos = [random.randrange(1, width // delta) * delta, random.randrange(1, height // delta) * delta]
    foodSpawn = True
    direction = 'r'
    changeto = ''

# shows the score
def showScore():
    font = pygame.font.SysFont(None, 40)
    scoreMenu = font.render(str(score), True, white) 
    highMenu = font.render(str(highscore), True, white) 
    scoreLoc = scoreMenu.get_rect()
    highLoc = highMenu.get_rect()
    highLoc.midtop = (370, 12)
    display.blit(pygame.image.load('images/apple.png'), (220, 10))
    display.blit(pygame.image.load('images/crown.png'), (310, 12))
    display.blit(scoreMenu, (265, 12))
    display.blit(highMenu, highLoc)
    
# visuals 
def draw():
    display.fill(black)
    for pos in snakeBody:
        pygame.draw.rect(display, green, pygame.Rect(pos[0], pos[1], delta, delta))
    pygame.draw.rect(display, red, pygame.Rect(foodPos[0], foodPos[1], delta, delta))
    showScore()


# check for out of bounds and self hits
def check():
    if 0 > snakePos[0] or snakePos[0] >= width or 0 > snakePos[1] or snakePos[1] >= height:
        gameOver()

    for block in snakeBody[1:]:
        if snakePos == block:
            gameOver()
    
# pause (spacebar)
def pause():
    pause = True
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit()
                if event.key == pygame.K_SPACE:
                    pause = False
        draw()
        display.blit(pygame.image.load('images/paused.png'), (225, 125))
        pygame.display.update()
        
# pause (spacebar)
def menu():
    menu = True
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit()
                if event.key == pygame.K_SPACE:
                    start()
                    menu = False
        display.fill(background)
        display.blit(pygame.image.load('images/snake.png'), (60, -40)) 
        showScore()
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if 235+120 > mouse[0] > 235 and 315+40 > mouse[1] > 315:
            pygame.draw.rect(display, button2, pygame.Rect(235, 315, 120, 40))
            if click[0] == 1:
                start()
                menu = False
        else:
            pygame.draw.rect(display, button, pygame.Rect(235, 315, 120, 40))
        font = pygame.font.SysFont('Times new roman', 32)
        butText = font.render('Play', True, black) 
        display.blit(butText, (270, 317))
        pygame.display.update()

# main game loop
menu()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            # validation of the snake movement (arrow keys or WASD)
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                changeto = 'r'
            if event.key == pygame.K_LEFT or event.key == pygame.K_a and direction != 'r':
                changeto =  'l'
            if event.key == pygame.K_UP or event.key == pygame.K_w and direction != 'd':
                changeto = 'u'
            if event.key == pygame.K_DOWN or event.key == pygame.K_s and direction != 'u':
                changeto = 'd'
            if event.key == pygame.K_ESCAPE:
                quit()
            if event.key == pygame.K_SPACE:
                pause()

    if changeto == 'r' and direction != 'l':
        direction = 'r'
    if changeto == 'l' and direction != 'r':
        direction = 'l'
    if changeto == 'u' and direction != 'd':
        direction = 'u'
    if changeto == 'd' and direction != 'u':
        direction = 'd'

    # updating position of snake
    if direction == 'r':
        snakePos[0] += delta
    if direction == 'l':
        snakePos[0] -= delta
    if direction == 'd':
        snakePos[1] += delta
    if direction == 'u':
        snakePos[1] -= delta

    # snake spawning
    snakeBody.insert(0, list(snakePos))
    if snakePos == foodPos:
        foodSpawn = False
        score += 1
        for i in range(5):
            snakeBody.append((snakeBody[-1][0],snakeBody[-1][1]))
    else:
        snakeBody.pop()

    # food spawning
    if foodSpawn == False:
        while foodSpawn is False:
            x = False
            foodPos = [random.randrange(1, width // delta) * delta, random.randrange(1, height // delta) * delta]
            for block in snakeBody[1:]:
                if foodPos == block:
                    x = True
            if x == False:
                foodSpawn = True
       
    check()
    draw()
    pygame.display.update()
    clock.tick(speed)