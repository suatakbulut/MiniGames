# sizes of the display area 
width  = 400
length = 400


block_size = 10 

white = (255, 255, 255)
black = (0, 0, 0)
red   = (255, 0, 0)

# initial speed of the snake
speed = 10

import random 
import pygame 


def pick_location():
    '''
    randomly selects an (x,y) coordinate in the display area

    Returns
    -------
    xpos : integer
        Horizontal Coordinate.
    ypos : integer
        Vertical Coordinate.

    '''
    xpos = random.choice(range(0, width, block_size))
    ypos = random.choice(range(0, length, block_size))

    return xpos, ypos

class Food:
    '''
    A food object is characterized as a random (x,y) coordinate on the display area
    
    Attributes:
        x (integer): horizontal position of a food
        y (integer): vertical position of a food
    '''
    def __init__(self):
        xpos, ypos = pick_location()
        self.x = xpos
        self.y = ypos 
        
    def pos(self): 
        '''
        The coordinates of a food as an (x,y) tuple

        '''

        return (self.x, self.y)

class Snake:
    '''
    
    Attributes:
        x (integer): the horizontal coordinate of the head of the snake
        y (integer): the vertical coordinate of the head of the snake
        total (integer): length of the snake 
        tail (array): the coordinates of the tail of the snake as an array of tuples
    
    '''
    
    def __init__(self):
        self.x = 0
        self.y = 0
        self.total = 0
        self.tail = []
    
    def move(self, x_change, y_change): 
        '''
        Given a direction to move, moves the snake's head in that direction

        Parameters
        ----------
        x_change : INTEGER
            how many pixel to move in the horizontal axis
        y_change : INTEGER
            how many pixel to move in the vertical axis

        Returns
        -------
        None.

        '''
        self.x += x_change 
        self.x = self.x % width
        
        self.y += y_change 
        self.y = self.y % length 
            
    def pos(self):
        '''
        The coordinates of the head of the snake as an (x,y) tuple

        '''
        return (self.x, self.y)
    
    def eat(self, food): 
        '''
        Determines if the snake eats the food        

        Parameters
        ----------
        food : FOOD class
            a food object in the display area.

        Returns
        -------
        BOOLEAN
            whether the snake eats the food or not

        '''
        return self.pos() == food.pos() 
    
    def is_dead(self): 
        '''
        Determines if the snake is dead. Remember that the snake dies only if 
        it tries to eat (or hit) itself

        Returns
        -------
        BOOLEAN
            whether the snake is dead or alive.

        '''
        return self.pos() in self.tail[:-1]
        
    def update(self, food, x_change, y_change):
        '''
        Given a food and a direction to move, finds and updates
            if the snake eats the food
            if the snake is dead 
            its head's new position 
            its total length 
            its tail

        Parameters
        ----------
        food : FOOD
            A Food object.
        x_change : INTEGER
            how many pixel to move in the horizontal axis
        y_change : INTEGER
            how many pixel to move in the vertical axis

        Returns
        -------
        Updates the snake's attributes, x, y, total, and tail.

        '''
        self.move(x_change, y_change) 
        self.tail.append(self.pos())
        
        if self.eat(food):
            self.total += 1 

        else:
            self.tail = self.tail[1:]
            
pygame.init() 

display = pygame.display.set_mode((width, length))
pygame.display.set_caption('Hello Snake Game')
clock = pygame.time.Clock()

score_font = pygame.font.SysFont("comicsansms", 35) 
end_font = pygame.font.SysFont("comicsansms", 30) 


def game_screen():
    game_over = False
    
    # Initialize a Snake and a food in the display area
    snake = Snake()
    food = Food() 
    
    x_change, y_change = 0, 0
    new_x_change, new_y_change = 0, 0
    
    
    while not game_over: 
        # Get the user's input through the arrow keys 
        # to determne the movement direction
        for event in pygame.event.get():             
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_LEFT: 
                    new_x_change = -block_size
                    new_y_change  = 0
                    
                elif event.key == pygame.K_RIGHT: 
                    new_x_change = block_size
                    new_y_change  = 0
                    
                elif event.key == pygame.K_UP:
                    new_x_change = 0
                    new_y_change  = -block_size
                
                
                elif event.key == pygame.K_DOWN:
                    new_x_change = 0
                    new_y_change  = +block_size
            
            # Do not allow the snake make a U turn and keep moving in the same 
            # direction if the user does not specify otherwise
            if x_change*new_x_change + y_change*new_y_change == 0:
                x_change = new_x_change
                y_change = new_y_change
        
        
        snake.update(food, x_change, y_change) 
        while food.pos() in snake.tail:
            food = Food()
        
        game_over = snake.is_dead()
        
        # the speed increases slowly but prabolicly 
        speed = 10 + 0.0004*snake.total**2
        
        # display the canvas, snake, and the food
        display.fill(black)
        pygame.draw.rect(display, white, [food.x, food.y, block_size, block_size])
               
        pygame.draw.rect(display, white, [snake.x, snake.y, block_size, block_size]) 
        
        for tail in snake.tail:
            pygame.draw.rect(display, white, [tail[0], tail[1], block_size, block_size]) 
        
        pygame.display.update() 
        clock.tick(speed)
        
    result = snake.total
    # return the total length of the snake to be used as score in the end_screen
    return result
     
def end_screen(result):
    '''
    Displays a screen showing the score of the user and 
    whether they want to quit or restart the game at the end of the game

    Parameters
    ----------
    result : INTEGER
        The total length of the snake in the previous game

    Returns
    -------
    None.

    '''
    while True:
        
              
        display.fill(black)
        
        end1 = end_font.render("Game Over.", True, red)
        display.blit(end1, [width/4, length/6])
        
        score = score_font.render("Your Score: {}".format(result), True, white)
        display.blit(score, [0, length*2/6])
        
        end2 = end_font.render("Press Q to quit", True, red)
        display.blit(end2, [0, length*3/6])     
        
        end2 = end_font.render("Any button to restart", True, red)
        display.blit(end2, [0, length*4/6])  
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q: 
                    pygame.quit()
                else:
                    game_screen()


result = game_screen()
    
end_screen(result)
