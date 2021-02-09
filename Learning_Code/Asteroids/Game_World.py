"""
File: asteroids.py
Original Author: Br. Burton
Co-Author: Bryce Maughan

This program implements a version of the asteroids game.
"""
import arcade
import Asteroid_Obj
import Ship_Obj
import Projectile_Obj

# These are Global constants to use throughout the game
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800

BULLET_RADIUS = 30
BULLET_SPEED = 10
BULLET_LIFE = 60

SHIP_TURN_AMOUNT = 3
SHIP_THRUST_AMOUNT = 0.25
SHIP_RADIUS = 30

INITIAL_ROCK_COUNT = 5

BIG_ROCK_SPIN = 1
BIG_ROCK_SPEED = 1.5
BIG_ROCK_RADIUS = 15

MEDIUM_ROCK_SPIN = -2
MEDIUM_ROCK_RADIUS = 5

SMALL_ROCK_SPIN = 5
SMALL_ROCK_RADIUS = 2

 
#import Object_Foundation
#from Object_Foundation import *
#from Asteroid_Obj import Rock_Lrg

#import Ship_Obj
#import Projectile_Obj


class Game(arcade.Window):
    """
    This class handles all the game callbacks and interaction

    This class will then call the appropriate functions of
    each of the above classes.

    You are welcome to modify anything in this class.
    """

    def __init__(self, width, height):
        """
        Sets up the initial conditions of the game
        :param width: Screen width
        :param height: Screen height
        """
        super().__init__(width, height)
        arcade.set_background_color(arcade.color.SMOKY_BLACK)
        
        self.held_keys = set()
        
        self.bullets = []
        self.ship = [Ship_Obj.Ship()]
        self.rocks = []
        #self.create_rocks()
        for i in range(5):
            self.create_rocks()
        
        # TODO: declare anything here you need the game class to track

    def on_draw(self):
        """
        Called automatically by the arcade framework.
        Handles the responsibility of drawing all elements.
        """
        
        # clear the screen to begin drawing
        arcade.start_render()

        for rock in self.rocks:
            rock.draw()
        
        for bullet in self.bullets:
            bullet.draw()

        for ship in self.ship:
            ship.draw()

        # TODO: draw each object

    def update(self, delta_time):
        """
        Update each object in the game.
        :param delta_time: tells us how much time has actually elapsed
        """

        self.check_keys()
        self.cleanup_zombies()
        self.check_collisions()

        for rock in self.rocks:
            rock.advance()
            rock.rotate()

        for bullet in self.bullets:
            bullet.advance()
            bullet.set_life()

        for ship in self.ship:
            ship.advance()


        # TODO: Tell everything to advance or move forward one step in time

        # TODO: Check for collisions

    def create_rocks(self):
        lrg = Asteroid_Obj.Rock_Lrg()
        #med = Asteroid_Obj.Rock_Med()
        #sml = Asteroid_Obj.Rock_Sml()

        lrg.create()
        #med.create()
        #sml.create()

        self.rocks.append(lrg)
        #self.rocks.append(med)
        #self.rocks.append(sml)

    def check_collisions(self):
        """
        Checks to see if bullets have hit rocks.
        Updates scores and removes dead items.
        :return:
        """
        new_rock = []
        for bullet in self.bullets:
            for rock in self.rocks:

                # Make sure they are both alive before checking for a collision
                if bullet.alive and rock.alive:
                    too_close = bullet.radius + rock.radius

                    if (abs(bullet.center.x - rock.center.x) < too_close and
                                abs(bullet.center.y - rock.center.y) < too_close):
                        # its a hit!
                        bullet.alive = False
                        new_rock += rock.hit()
                        for rock in new_rock:
                            rock.create()
                            #rock.rotate()
                        # We will wait to remove the dead objects until after we
                        # finish going through the list
        for ship in self.ship:
            for rock in self.rocks:
                # Make sure they are both alive before checking for a collision
                if ship.alive and rock.alive:
                    too_close = ship.radius + rock.radius

                    if (abs(ship.center.x - rock.center.x) < too_close and
                                abs(ship.center.y - rock.center.y) < too_close):
                        # Crash!
                        ship.death_event()
                        # Put new rocks into a list
                        new_rock += rock.hit()
                        
                        
        # Add new rock list into the main rock list
        self.rocks += new_rock

        # Now, check for anything that is dead, and remove it
        self.cleanup_zombies()

    def cleanup_zombies(self):
        for bullet in self.bullets:
            if not bullet.alive:
                self.bullets.remove(bullet)

        for rock in self.rocks:
            if not rock.alive:
                self.rocks.remove(rock)
        for ship in self.ship:
            if not ship.alive:
                self.ship.remove(ship)

    def check_keys(self):
        """
        This function checks for keys that are being held down.
        You will need to put your own method calls in here.
        """
        player = []

        for ship in self.ship:
            if arcade.key.LEFT in self.held_keys:
                ship.rotate_left()
            
            if arcade.key.RIGHT in self.held_keys:
                ship.rotate_right()
            
            if arcade.key.UP in self.held_keys:
                ship.move_forward()
            
            if arcade.key.DOWN in self.held_keys:
                ship.move_backwards()

            if arcade.key.ENTER in self.held_keys:
                ship.alive = True
                player += ship.respawn()
                for play in player:
                    play.create()
                    play.draw()
            self.ship += player
        # Machine gun mode...
        #if arcade.key.SPACE in self.held_keys:
        #    pass


    def on_key_press(self, key: int, modifiers: int):
        """
        Puts the current key in the set of keys that are being held.
        You will need to add things here to handle firing the bullet.
        """
        for ship in self.ship:
            if ship:
                self.held_keys.add(key)
                #self.ship.move()
            
                if key == arcade.key.SPACE:
                    bullet = Projectile_Obj.Bullet()
                    bullet.fire(ship.center.x, ship.center.y, ship.angle)
                    self.bullets.append(bullet)
                    # TODO: Fire the bullet here!
                

    def on_key_release(self, key: int, modifiers: int):
        """
        Removes the current key from the set of held keys.
        """
        if key in self.held_keys:
            self.held_keys.remove(key)


# Creates the game and starts it going
window = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
arcade.run()