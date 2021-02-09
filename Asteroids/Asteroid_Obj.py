import arcade, math, random
from abc import abstractmethod
from abc import ABC
import Object_Foundation
 
# These are Global constants to use throughout the game
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800

STARTING_ASTEROID_COUNT = 5

BIG_ROCK_SPIN = 1
BIG_ROCK_SPEED = 1.5
BIG_ROCK_RADIUS = 15

MEDIUM_ROCK_SPIN = -2
MEDIUM_ROCK_RADIUS = 5

SMALL_ROCK_SPIN = 5
SMALL_ROCK_RADIUS = 2

#from Object_Foundation import Point, Velocity, Object #- Main Parent Modules

class A_Foundation(Object_Foundation.Object, ABC): #- Sets the design for the Asteroid template
    def __init__(self): #- Set perameters
        super().__init__()
        self.angle = 0.0
        self.change_angle = 0.0

    def rotate(self): #- Rotate
        self.angle += self.change_angle
        

    @abstractmethod
    def hit(self): #- Kill or React at event:
        pass

    @abstractmethod
    def create(self): #- Create at location based on random generator perameters:
        pass


class Rock_Lrg(A_Foundation):
    def __init__(self):
        super().__init__()

    #- Set dementions for the target to draw:

    #- Kill target on collision event:
    def hit(self):
        self.alive = False
        return [Rock_Med(self.center.x, self.center.y), Rock_Med(self.center.x, self.center.y), Rock_Sml(self.center.x, self.center.y)]

        
    #- Set dementions for the target to draw at a location:
    def create(self):
        # This will load the graphics file into an arcade texture object
        self.sprite = arcade.load_texture("big.png")
        self.size = (self.sprite.width // 2) + (self.sprite.height // 2)
        self.angle = math.degrees(random.randrange(360))
        self.change_angle = random.randint(-1, 1)
        self.rotate()
        self.alive = True
        self.center.x = random.randint(0, 1)
        self.center.y = random.randint(0, SCREEN_HEIGHT)
        self.velocity.dx = math.cos(math.radians(self.angle)) * 1.5
        self.velocity.dy = math.sin(math.radians(self.angle)) * 1.5
        self.radius = BIG_ROCK_RADIUS
        
        



class Rock_Med(A_Foundation):
    def __init__(self, x, y):
        super().__init__()
        self.center.x = x
        self.center.y = y

    #- Set dementions for the target to draw:

    #- Kills target on collision event:
    def hit(self):
        self.alive = False
        return [Rock_Sml(self.center.x, self.center.y), Rock_Sml(self.center.x, self.center.y)]
    
    #- Set dementions for the target to draw at a location.
    def create(self):
        # This will load the graphics file into an arcade texture object
        self.sprite = arcade.load_texture("medium.png")
        self.size = (self.sprite.width // 2) + (self.sprite.height // 2)
        self.angle = math.degrees(random.randrange(360))
        self.change_angle = random.randint(-2, 2)
        self.rotate()
        self.alive = True
        self.velocity.dx = math.cos(math.radians(self.angle)) * 2
        self.velocity.dy = math.sin(math.radians(self.angle)) * 2
        self.radius = MEDIUM_ROCK_RADIUS


class Rock_Sml(A_Foundation):
    def __init__(self, x, y):
        super().__init__()
        self.angle = 0
        self.center.x = x
        self.center.y = y
    #- Set dementions for the Safe_Target to draw:


    #- Kill the target on collision event.
    def hit(self):
        self.alive = False
        return []
        
    
    #- Set dementions for the target to draw at a location.
    def create(self):
        # This will load the graphics file into an arcade texture object
        self.sprite = arcade.load_texture("small.png")
        self.size = (self.sprite.width // 2) + (self.sprite.height // 2)
        self.angle = math.degrees(random.randrange(360))
        self.change_angle = random.randint(-5, 5)
        self.rotate()
        self.alive = True
        self.velocity.dx = math.cos(math.radians(self.angle)) * 2.5
        self.velocity.dy = math.sin(math.radians(self.angle)) * 2.5
        self.radius = SMALL_ROCK_RADIUS
