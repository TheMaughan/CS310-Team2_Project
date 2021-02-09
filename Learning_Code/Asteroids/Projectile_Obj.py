import arcade, math, random
from abc import abstractmethod
from abc import ABC
import Object_Foundation #- Main Parent Module
import Ship_Obj

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800

BULLET_RADIUS = 30
BULLET_SPEED = 10
BULLET_LIFE = 60


class Bullet(Object_Foundation.Object):
    def __init__(self):
        super().__init__()
        #- Call the ceation of the bullet:
        self.create()

    #- Create the Bullet in the Rifle
    def create(self): #- Set the perameters for the bullet
        self.sprite = arcade.load_texture("laser.png")
        self.size = (self.sprite.width // 2) + (self.sprite.height // 2)
        self.ship = Ship_Obj.Ship()
        self.center.x = 0.0
        self.center.y = 0.0
        self.velocity.dx = 0.0
        self.velocity.dy = 0.0
        self.radius = BULLET_RADIUS
        self.life = 0.0
        self.alive = True

    #- Sets the angle of the bullet tragectory and initiates the creation of the bullet.
    def fire(self, x, y, angle):
        self.alive = True
        self.angle = angle + 90
        self.center.x = x
        self.center.y = y
        self.velocity.dx = (math.cos(math.radians(self.angle)) * BULLET_SPEED)
        self.velocity.dy = (math.sin(math.radians(self.angle)) * BULLET_SPEED)
        
        #self.angle = math.degrees(math.atan2(self.velocity.dy, self.velocity.dx))

    def set_life(self):
        self.life += 1

        if self.life > BULLET_LIFE:
            self.alive = False
        else:
            self.alive = True