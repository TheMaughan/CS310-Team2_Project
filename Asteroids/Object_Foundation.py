from abc import abstractmethod
from abc import ABC
import arcade
import Point_Velocity

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800

class Object(ABC): #- All travling objects share these same atrabutes:
    def __init__(self):
        self.center = Point_Velocity.Point()
        self.velocity = Point_Velocity.Velocity()
        self.max = self.velocity.max
        self.create()
        self.radius = 0

    @abstractmethod
    def create(self):
        pass
   

    def draw(self): #- Establish the physical properties:      
        arcade.draw_texture_rectangle(self.center.x, self.center.y, self.sprite.width / 2, self.sprite.height / 2, self.sprite, self.angle)
        self.wrap()

    def advance(self): #- Progress/move in a straight line:
        self.center.x += self.velocity.dx
        self.center.y += self.velocity.dy
    
    def wrap(self):
        #- Wrap around the screen
        if self.center.y < self.radius * -2:
            self.center.y = (SCREEN_HEIGHT + (self.radius * 2))

        if self.center.y > SCREEN_HEIGHT + (self.radius * 2):
            self.center.y = self.radius * -2

        if self.center.x < self.radius * -2:
            self.center.x = SCREEN_WIDTH + (self.radius * 2)

        if self.center.x > SCREEN_WIDTH + (self.radius * 2):
            self.center.x = self.radius * -2