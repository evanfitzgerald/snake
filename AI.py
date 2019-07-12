
import pygame, time, random, sys

# settings
pygame.init()
height = 400
width = 600
display = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake")

# change this to True to visualize the bad pathways
visualize = False

black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(240, 10, 10)
green = pygame.Color(0, 255, 0)
yellow = pygame.Color(255, 255, 0)
background = pygame.Color(36, 158, 93)
button = pygame.Color(1, 175, 170)
button2 = pygame.Color(1, 160, 180)
clock = pygame.time.Clock()
listy = spaces = caution = []
highscore = score = 0
delta = speed = 40
snakePos = [80, 240]
snakeBody = [[80, 240], [40, 240], [0, 240]]
foodPos = [random.randrange(1, width // delta) * delta, random.randrange(1, height // delta) * delta]
foodSpawn = True
direction = 'r'
changeto = ''

# when the user quits the game
def quit():
    pygame.display.quit()
    pygame.quit()
    exit()

# when the snake is out of bounds or hits self
def gameOver():
    global score, highscore
    if score > highscore:
        highscore = score
    menu()
    
# start game
def start():
    global score, snakePos, snakeBody, foodPos, foodSpawn, direction, changeto, listy, spaces
    score = 0
    listy = spaces = caution = []
    snakePos = [80, 240]
    snakeBody = [[80, 240], [40, 240], [0, 240]]
    foodPos = [random.randrange(1, width // delta) * delta, random.randrange(1, height // delta) * delta]
    foodSpawn = True
    direction = 'r'
    changeto = ''
    board()
    create() 

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
    #display.fill(black)
    for pos in snakeBody:
        pygame.draw.rect(display, green, pygame.Rect(pos[0], pos[1], delta, delta))
    pygame.draw.rect(display, red, pygame.Rect(foodPos[0], foodPos[1], delta, delta))
    showScore()

# check for out of bounds and self hits
def check():
    global snakeBody
    if 0 > snakePos[0] or snakePos[0] >= width or 0 > snakePos[1] or snakePos[1] >= height:
        gameOver()

    for block in snakeBody[1:]:
        if snakePos == block:
            gameOver()

# list of all possible spaces on board
def board():
    global spaces
    for i in range(-1, 16):
        for j in range(-1, 11):
            spaces.append([i*delta,j*delta])
    
# creates list of dangerous spaces
def create():
    global snakeBody, foodPos, spaces, listy, visualize
    listy = []
    for x in spaces:
        check1 = check2 = check3 = check4 = check5 = check6 = check7 = check8 = False
        for block in snakeBody:
            if x[0] > block[0] and x[1] == block[1]: 
                check1 = True
            if x[0] < block[0] and x[1] == block[1]: 
                check2 = True
            if x[0] == block[0] and x[1] < block[1]:
                check3 = True
            if x[0] == block[0] and x[1] > block[1]: 
                check4 = True
            if x[0] < 0:
                check5 = True
            if x[0] > 560:
                check6 = True
            if x[1] < 0:
                check7 = True
            if x[1] > 360:
                check8 = True

        if check1 == check2 == check3 == check4 == True and x != (snakeBody or foodPos):
            listy.append([x[0],x[1]])

        # outside the board
        if 0 > x[0] or x[0] > 560 or 0 > x[1] or x[1] > 360:
            listy.append([x[0],x[1]])

    # displays dangerous spaces on board
    display.fill(black)

    if visualize == True:
        for x in listy:
            if x != snakeBody or snakePos or foodPos:
                pygame.draw.rect(display, yellow, pygame.Rect(x[0], x[1], delta, delta))
    
# make list containing any cautioned areas
def warning():
    global caution
    caution = []
    caution.extend(listy)
    caution.extend(snakeBody)

def moving_validation():
    global direction, changeto, snakePos, foodPos, foodSpawn, score
    # checking snake is not moving in opposite direction
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
    else:
        snakeBody.pop()

    # food spawning
    if foodSpawn == False:
        while foodSpawn is False:
            x = False
            foodPos = [random.randrange(1, width // delta) * delta, random.randrange(1, height // delta) * delta]
            for block in snakeBody:
                if foodPos == block:
                    x = True
            if x == False:
                foodSpawn = True
              
    check()
    draw()
    pygame.display.update()
    clock.tick(speed)

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
        create()
        draw()
        display.blit(pygame.image.load('images/paused.png'), (225, 125))
        pygame.display.update()
        
# menu pane
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
        # start button
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


# how it decides to move
def move():
    create()
    global changeto, direction, listy
    #if snake is to the right of the food
    if snakePos[0] > foodPos[0]:
        changeto = 'l'
        if direction == 'r':
            #up or down
            if snakePos[1] < foodPos[1]:
                changeto = 'd'
            else: 
                changeto = 'u'
    
    #if snake is to the left of the food
    if snakePos[0] < foodPos[0]:
        changeto = 'r'
        if direction == 'l':
            #up or down
            if snakePos[1] < foodPos[1]:
                changeto = 'd'
            else: 
                changeto = 'u'
            
    #if snake is to the below of the food
    if snakePos[1] > foodPos[1]:
        changeto = 'u'
        if direction == 'd':
            #left or right
            if snakePos[0] < foodPos[0]:
                changeto = 'l'
            else: 
                changeto = 'r'

    #if snake is to the above of the food
    if snakePos[1] < foodPos[1]:
        changeto = 'd'
        if direction == 'u':
            #left or right
            if snakePos[0] < foodPos[0]:
                changeto = 'r'
            else: 
                changeto = 'l'

    # snake is below and to the right
    if snakePos[0] > foodPos[0] and snakePos[1] > foodPos[1]:
        # if the snake is closer by the right then the below
        if snakePos[0] - foodPos[0] > snakePos[1] - foodPos[1]:
            changeto = 'l'
            if direction == 'r':
                changeto = 'u'
        elif snakePos[0] - foodPos[0] < snakePos[1] - foodPos[1]:
            changeto = 'u'
            if direction == 'd':
                changeto = 'l'

    # snake is above and to the right
    if snakePos[0] > foodPos[0] and snakePos[1] < foodPos[1]:
        # if the snake is closer by the right then the above
        if snakePos[0] - foodPos[0] > foodPos[1] - snakePos[1]:
            changeto = 'l'
            if direction == 'r':
                changeto = 'd'
        elif snakePos[0] - foodPos[0] < foodPos[1] - snakePos[1]:
            changeto = 'd'
            if direction == 'u':
                changeto = 'l'

    # snake is below and to the left
    if snakePos[0] < foodPos[0] and snakePos[1] > foodPos[1]:
        # if the snake is closer by the right then the below
        if foodPos[0] - snakePos[0] > snakePos[1] - foodPos[1]:
            changeto = 'r'
            if direction == 'l':
                changeto = 'u'
        elif foodPos[0] - snakePos[0] < snakePos[1] - foodPos[1]:
            changeto = 'u'
            if direction == 'd':
                changeto = 'r'

    # snake is above and to the left
    if snakePos[0] < foodPos[0] and snakePos[1] < foodPos[1]:
        # if the snake is closer by the right then the above
        if foodPos[0] - snakePos[0] > foodPos[1] - snakePos[1]:
            changeto = 'r'
            if direction == 'l':
                changeto = 'd'
        elif foodPos[0] - snakePos[0] < foodPos[1] - snakePos[1]:
            changeto = 'd'
            if direction == 'u':
                changeto = 'r'

    warning()
    for block in caution:
        # wants to go left but body is there
        if changeto == 'l' and snakePos[0] - delta == block[0] and snakePos[1] == block[1]:
            create()
            if direction == 'l':
                # up or down
                changeto = 'u'
                for block in caution:
                    if snakePos[1] - delta == block[1] and snakePos[0] == block[0]:
                        changeto = 'd'
                
            if direction == 'u':
                # up or right
                changeto = 'u'
                for block in caution:
                    if snakePos[1] - delta == block[1] and snakePos[0] == block[0]:
                        changeto = 'r'

            if direction == 'd':
                # down or right
                changeto = 'd'
                for block in caution:
                    if snakePos[1] + delta == block[1] and snakePos[0] == block[0]:
                        changeto = 'r'

        # wants to go right but body is there           
        if changeto == 'r' and snakePos[0] + delta == block[0] and snakePos[1] == block[1]:
            create()
            if direction == 'r':
                # up or down 
                changeto = 'u'
                for block in caution:
                    if snakePos[1] - delta == block[1] and snakePos[0] == block[0]:
                        changeto = 'd'

            if direction == 'u':
                # up or left
                changeto = 'u'
                for block in caution:
                    if snakePos[1] - delta == block[1] and snakePos[0] == block[0]:
                        changeto = 'l'
                
            if direction == 'd':
                # down or left
                changeto = 'd'
                for block in caution:
                    if snakePos[1] + delta == block[1] and snakePos[0] == block[0]:
                        changeto = 'l'

        # wants to go up but body is there
        if changeto == 'u' and snakePos[1] - delta == block[1] and snakePos[0] == block[0]:
            create()
            if direction == 'u':
                # left or right 
                changeto = 'r' 
                for block in caution:
                    if snakePos[0] + delta == block[0] and snakePos[1] == block[1]:
                        changeto = 'l'

            if direction == 'l':
                # left or down
                changeto = 'l'
                for block in caution:
                    if snakePos[0] - delta == block[0] and snakePos[1] == block[1]:
                        changeto = 'd'

            if direction == 'r':
                # right or down
                changeto = 'r'
                for block in caution:
                    if snakePos[0] + delta == block[0] and snakePos[1] == block[1]:
                        changeto = 'd'

        # wants to go down but body is there
        if changeto == 'd' and snakePos[1] + delta == block[1] and snakePos[0] == block[0]:
            create()
            if direction == 'd':
                # left or right
                changeto = 'r'
                for block in caution:
                    if snakePos[0] + delta == block[0] and snakePos[1] == block[1]:
                        changeto = 'l'

            if direction == 'l':
                # left or up 
                changeto = 'l'
                for block in caution:
                    if snakePos[1] - delta == block[1] and snakePos[0] == block[0]:
                        changeto = 'u'

            if direction == 'r':
                # right or up 
                changeto = 'r'
                for block in caution:
                    if snakePos[0] + delta == block[0] and snakePos[1] == block[1]:
                        changeto = 'u' 
    
    if snakePos[0] == 0 and changeto == 'l':
        if direction == 'l':
            # up or down
            changeto = 'u'
            for block in caution:
                if snakePos[1] - delta == block[1] and snakePos[0] == block[0]:
                    changeto = 'd'
            
        if direction == 'u':
            # up or right
            changeto = 'u'
            for block in caution:
                if snakePos[1] - delta == block[1] and snakePos[0] == block[0]:
                    changeto = 'r'

        if direction == 'd':
            # down or right
            changeto = 'd'
            for block in caution:
                if snakePos[1] + delta == block[1] and snakePos[0] == block[0]:
                    changeto = 'r'

    if snakePos[0] == 560 and changeto == 'r':
        if direction == 'r':
            # up or down 
            changeto = 'u'
            for block in caution:
                if snakePos[1] - delta == block[1] and snakePos[0] == block[0]:
                    changeto = 'd'

        if direction == 'u':
            # up or left
            changeto = 'u'
            for block in caution:
                if snakePos[1] - delta == block[1] and snakePos[0] == block[0]:
                    changeto = 'l'
            
        if direction == 'd':
            # down or left
            changeto = 'd'
            for block in caution:
                if snakePos[1] + delta == block[1] and snakePos[0] == block[0]:
                    changeto = 'l'

    if snakePos[1] == 0 and changeto == 'u':
        if direction == 'u':
            # left or right 
            changeto = 'r' 
            for block in caution:
                if snakePos[0] + delta == block[0] and snakePos[1] == block[1]:
                    changeto = 'l'

        if direction == 'l':
            # left or down
            changeto = 'l'
            for block in caution:
                if snakePos[0] - delta == block[0] and snakePos[1] == block[1]:
                    changeto = 'd'

        if direction == 'r':
            # right or down
            changeto = 'r'
            for block in caution:
                if snakePos[0] + delta == block[0] and snakePos[1] == block[1]:
                    changeto = 'd'

    if snakePos[1] == 360 and changeto == 'd':
        if direction == 'd':
            # left or right
            changeto = 'r'
            for block in caution:
                if snakePos[0] + delta == block[0] and snakePos[1] == block[1]:
                    changeto = 'l'

        if direction == 'l':
            # left or up 
            changeto = 'l'
            for block in caution:
                if snakePos[1] - delta == block[1] and snakePos[0] == block[0]:
                    changeto = 'u'

        if direction == 'r':
            # right or up 
            changeto = 'r'
            for block in caution:
                if snakePos[0] + delta == block[0] and snakePos[1] == block[1]:
                    changeto = 'u'

menu()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quit()
            if event.key == pygame.K_SPACE:
                pause()

    move()
    moving_validation()