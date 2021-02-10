import arcade
import random
import os
import math
import time 


SPRITE_SCALING = 0.2
TILE_SCALING = 0.4

SCREEN_WIDTH = 750
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Platformer"


MOVEMENT_SPEED = 3
GRAVITY = 0 #change this to enable jumping
ANGLE_SPEED = 3

class Car(arcade.Sprite):
    """ Player Class """

    def __init__(self, image, scale):

        super().__init__(image, scale)
        # Create a variable to hold our speed. 'angle' is created by the parent
        self.speed = 0

    def update(self):
        """ Move the player """
        # Move player.
        # Remove these lines if physics engine is moving player.
        #self.center_x += self.change_x
        #self.center_y += self.change_y

        # Check for out-of-bounds
        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH - 1

        if self.bottom < 0:
            self.bottom = 0

        elif self.top > SCREEN_HEIGHT - 1:
            self.top = SCREEN_HEIGHT - 1

        angle_rad = math.radians(self.angle)

        self.angle += self.change_angle

        self.center_x += -self.speed * math.sin(angle_rad)
        self.center_y += -self.speed * math.cos(angle_rad)		#change


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height, title):
        """
        Initializer
        """

        # Call the parent class initializer
        super().__init__(width, height, title)

        self.player_list = None

        self.physics_engine = None

        # Variables that will hold sprite lists
        self.player_list = None

        # Set up the player info
        self.player_sprite = None

        self.total_time = 90.0

        # Set the background color
        arcade.set_background_color(arcade.color.LIGHT_BLUE) #change

        #Sound



    def setup(self): #change this section 
        """ Set up the game and initialize the variables. """


        
        # Create the Sprite lists
        self.player_list = arcade.SpriteList()
	    self.platform = arcade.SpriteList()

        # Set up the player Change this
        self.player_sprite = Car("car1.png", SPRITE_SCALING)
        self.player_sprite.center_x = 100
        self.player_sprite.center_y = 150
        self.player_list.append(self.player_sprite)

            # --- Load in a map from the tiled editor ---
	"""
        # Name of map file to load
        map_name = "background.tmx"
        # Name of the layer in the file that has our platforms/walls
        tree_name = 'Tree_plat'
        # Name of the layer that has items for pick-up
        coins_layer_name = 'Coins_plat'

        road_layer_name = 'Road_plat'

        house_layer_name = 'House_plat'

        # Read in the tiled map
        my_map = arcade.tilemap.read_tmx(map_name)

        # -- Platforms
        self.tree_list = arcade.tilemap.process_layer(my_map,
                                                      layer_name=tree_name,
                                                      scaling=TILE_SCALING,
                                                      use_spatial_hash=True)


        # --- Other stuff
        self.road_list = arcade.tilemap.process_layer(my_map,road_layer_name, TILE_SCALING )

        self.house_list = arcade.tilemap.process_layer(my_map,house_layer_name, TILE_SCALING )


        # Set the background color
        if my_map.background_color:
            arcade.set_background_color(my_map.background_color)
	"""
        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite,
                                                             self.platform,
                                                             GRAVITY)
        
        





    def on_draw(self):
        """
        Render the screen.
        """

         #timer set up

        minutes = int(self.total_time) // 60

        seconds = int(self.total_time) % 60

        output = f"Time:  {minutes: 02d}:{seconds:02d}"

        output2 = f"Total coins: {self.total_coins} "

        won_text = "You got all the coins!"

        game_over = "Game Over"

        total_score = f" Score: {self.total_coins}"


        

        # This command has to happen before we start drawing
        arcade.start_render()

        # Draw all the sprites. Make sure you place background frist
        self.player_list.draw()

	
	#take this part ot. Draws text on screen
        arcade.draw_text(output, 625, 750, arcade.color.BLACK, 18)
        arcade.draw_text(output2, 610, 725, arcade.color.BLACK, 18)

        if self.total_time < 0 :
            arcade.draw_text(game_over, 75, 600, arcade.color.RED, 80) 
            arcade.draw_text(total_score, 75, 520, arcade.color.RED, 80) 
        if self.total_coins == 19:
                arcade.draw_text(won_text, 75, 520, arcade.color.RED, 40)
                arcade.draw_text(won_text, 75, 520, arcade.color.GLITTER, 41)



                
            
            


        

    def on_update(self, delta_time):
        """ Movement and game logic """

        self.physics_engine.update()

        self.player_list.update()
        #coin_hit_list = arcade.check_for_collision_with_list(self.player_sprite,self.coin_list
                                                             
	"""
        if self.total_time < 0:
            arcade.set_background_color(arcade.color.BLACK) 
        else:
            self.total_time -= delta_time

        if self.total_coins == 19:
            arcade.set_background_color(arcade.color.BLACK)
        else:
            self.total_time -= delta_time
	"""

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        # If the player presses a key, update the speed
        if key == arcade.key.UP:
            self.player_sprite.change_y  = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player_sprite.change_y = -MOVEMENT_SPEED

        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        # If a player releases a key, zero out the speed.
        # This doesn't work well if multiple keys are pressed.
        # Use 'better move by keyboard' example if you need to
        # handle this.
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0


def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
