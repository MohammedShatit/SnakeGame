#Mohammed Shatit
#Snake Game made for educational purposes
#1/6/2021


#importing labriries
import pygame
import random

class cube(): #cube class to build the snake class with and the food object
    rows = 50 #dividing the space into 50 rows (make less for bigger snake)
    width = 500
    def __init__(self, start, dirnx = 1, dirny = 0, color = (0,255,0)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color
    
    def move(self, dirnx, dirny): #a method to move the individual cubes
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, screen, eyes = False): #drawing each cube to the screen
        distance = self.width // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(screen, self.color, (i*distance, j*distance, distance, distance))

        if eyes: #checking for the head cube and drawing eyes to it
            centre = distance//2
            radius = 1
            circleMiddle = (i*distance + centre-radius, j*distance+5)
            circleMiddle2 = (i*distance + distance -radius*2, j*distance+5)
            pygame.draw.circle(screen, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(screen, (0,0,0), circleMiddle2, radius)   


class snake(): #snake class made of cube instances
    body  = [] #a list for the cubes
    turns = {} #a dictionary to hold the position of the turns
    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1

    def draw(self, screen): #drawing the cubes and checking for the head cube
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(screen, True)
            else:
                c.draw(screen)

    def move(self): #moving the snake
        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns: #checking for turns
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body)-1:
                    self.turns.pop(p)
            else: #keep moving in the same direction if no turns
                if c.dirnx == -1 and c.pos[0] <= 0: 
                    c.pos = (c.rows-1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows-1: 
                    c.pos = (0,c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows-1: 
                    c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0: 
                    c.pos = (c.pos[0],c.rows-1)
                else: 
                    c.move(c.dirnx,c.dirny)

    def reset(self, pos): #resetting the snake after colliding with itself
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def grow(self): #method to add cubes to the body of the snake
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0: #where to the add the cube at the tail?
            self.body.append(cube((tail.pos[0]-1,tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1,tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0],tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0],tail.pos[1]+1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy
        
def food(rows, item): #function for generating food for the snake
    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)

        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0: 
            #a check to not generate the food on the snake
            continue
        else:
            break
    return (x,y)

def draw(screen): #function to group all the drawing method calls
    global rows, width, snake1, apple
    screen.fill((20,20,20))
    snake1.draw(screen)
    apple.draw(screen)

    pygame.display.update()



def main(): #main function
    pygame.init()

    global width, height, rows, snake1, apple
    width = 500
    height = 500
    rows = 50
    screen = pygame.display.set_mode((width, height))  #making the window
    pygame.display.set_caption("Snake!") 

    snake1 = snake((50,195,74), (10, 10)) #a snake object
    apple = cube(food(rows, snake1), color=(195,50,50)) #food object

    clock = pygame.time.Clock()

    font = pygame.font.SysFont("Comicsans", 100)
    score = 0

    run = True
    while run: #main game loop
        pygame.time.delay(50)
        clock.tick(10)
        for event in pygame.event.get(): #checking for hitting the x button
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()

        for key in keys: #checking the user input to move the snake
            if keys[pygame.K_RIGHT]: #right
                snake1.dirnx = 1
                snake1.dirny = 0
                snake1.turns[snake1.head.pos[:]] = [snake1.dirnx, snake1.dirny] #keeping track of turns

            elif keys[pygame.K_LEFT]: #left
                snake1.dirnx = -1
                snake1.dirny = 0
                snake1.turns[snake1.head.pos[:]] = [snake1.dirnx, snake1.dirny]

            elif keys[pygame.K_UP]: #up
                snake1.dirnx = 0
                snake1.dirny = -1
                snake1.turns[snake1.head.pos[:]] = [snake1.dirnx, snake1.dirny]

            elif keys[pygame.K_DOWN]: #down
                snake1.dirnx = 0
                snake1.dirny = 1
                snake1.turns[snake1.head.pos[:]] = [snake1.dirnx, snake1.dirny]

        snake1.move() #calling the move method of the snake class

        if snake1.body[0].pos == apple.pos: #checking if the snake collides with the apple
            snake1.grow() #adding cubes to the body of the snake
            apple = cube(food(rows, snake1), color=(195,50,50))

        for x in range(len(snake1.body)):
            if snake1.body[x].pos in list(map(lambda z:z.pos, snake1.body[x+1:])): 
                #colliding with the body itself
                print('Score: ', len(snake1.body))
                text = font.render('You Lost', 1 , (0,0,0)) #adding a text when hitting the body
                screen.blit(text, (250 - text.get_width()/2, 200))
                pygame.display.update()
                i = 0 
                while i < 200: #delay loop
                    pygame.time.delay(10)
                    i += 1
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            i = 201
                            pygame.quit()

                snake1.reset((10,10)) #restting the snake after hitting itself
                break

        draw(screen)

    pygame.quit()

main()