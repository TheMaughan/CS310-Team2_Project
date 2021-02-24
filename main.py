import arcade #py -m venv venv
import random
import os
import math
import time 

MUSIC_VOLUME = 0.5
SPRITE_SCALING = 0.2
TILE_SCALING = 0.9

SCREEN_WIDTH = 750
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Platformer"


MOVEMENT_SPEED = 3
GRAVITY = .0001 #change this to enable jumping
ANGLE_SPEED = 3

VIEWPORT_MARGIN = 250

class Player(arcade.Sprite):
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

        # Check for out-of-bounds  -- doesn't currently work with scrolling
        if self.left < 0:
            self.left = 0
            print("hello")
        elif self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH - 1

        if self.bottom < 0:
            self.bottom = 0

        elif self.top > SCREEN_HEIGHT - 1:
            self.top = SCREEN_HEIGHT - 1

        #angle_rad = math.radians(self.angle)

        #self.angle += self.change_angle

        #self.center_x += -self.speed * math.sin(angle_rad)
        #self.center_y += -self.speed * math.cos(angle_rad)		#change


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

        
        self.physics_engine = None

        # Variables that will hold sprite lists
        self.player_list = None
        self.platform_list =None
        self.enemy_list = None
        # Set up the player info
        self.player_sprite = None
        self.platform_sprite = None
        self.enemy_sprite = None

        self.total_time = 90.0

        # Set the background color
        arcade.set_background_color(arcade.color.LIGHT_BLUE) #change

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        #Sound
        self.music_list = []
        self.current_song_index = 0
        self.music = None
        self.hit_sound = arcade.load_sound("Sprites/gameover4.wav")

    def play_song(self):
        """What's currently in here, I think we could use as menu music, if we choose to add one."""
        # Stop what is currently playing.
        if self.music:
            self.music.stop()

        # Play the selected song. We could have the different areas set the current_song_index 
        # to a different value and then call this function to change the song
        """From https://www.fesliyanstudios.com/royalty-free-music/downloads-c/8-bit-music/6
        Another Website: https://freemusicarchive.org/genre/Chiptune"""
        self.music = arcade.Sound(self.music_list[self.current_song_index], streaming=True) 
        self.current_player = self.music.play(MUSIC_VOLUME)
        # This is a quick delay. If we don't do this, our elapsed time is 0.0
        # and on_update will think the music is over and advance us to the next
        # song before starting this one.
        time.sleep(0.03)


    def setup(self): #change this section 
        """ Set up the game and initialize the variables. """
        
        # Create the Sprite lists
        self.player_list = arcade.SpriteList()
        self.platform_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()

        # Set up the player Change this
        self.player_sprite = Player("Sprites\player.png", SPRITE_SCALING)
        self.player_sprite.center_x = 100
        self.player_sprite.center_y = 150
        self.player_list.append(self.player_sprite)

        self.enemy_sprite = arcade.Sprite("Sprites\\flipped_creeper.png", SPRITE_SCALING *.2)
        self.enemy_sprite.center_x = 250
        self.enemy_sprite.center_y = 210
        self.enemy_list.append(self.enemy_sprite)
            # --- Load in a map from the tiled editor ---

	 

        platform = arcade.Sprite("Sprites\platform.png", TILE_SCALING)
        platform.center_x = 120
        platform.center_y = 150
        self.platform_list.append(platform)
        

        platform = arcade.Sprite("Sprites\platform.png", TILE_SCALING)
        platform.center_x = 250
        platform.center_y = 150
        self.platform_list.append(platform)

        platform = arcade.Sprite("Sprites\platform.png", TILE_SCALING)
        platform.center_x = 400
        platform.center_y = 150
        self.platform_list.append(platform)

        self.music_list = ["Sprites\Old_Game_David_Fesliyan.mp3", "Sprites\sawsquarenoise-Final_Boss.mp3"]
        self.play_song() # Get the music going!

        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite,
                                                             self.platform_list,
                                                            GRAVITY)
        
        

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



    def on_draw(self):
        """
        Render the screen.
        """

         #timer set up

        minutes = int(self.total_time) // 60

        seconds = int(self.total_time) % 60

        output = f"Time:  {minutes: 02d}:{seconds:02d}"

        #output2 = f"Total coins: {self.total_coins} "

        #won_text = "You got all the coins!"

        #game_over = "Game Over"

        #total_score = f" Score: {self.total_coins}"


        

        # This command has to happen before we start drawing
        arcade.start_render()

        # Draw all the sprites. Make sure you place background frist
        self.player_list.draw()
        self.platform_list.draw()
        self.enemy_sprite.draw()

	
	#take this part out. Draws text on screen
        arcade.draw_text(output, 625, 750, arcade.color.BLACK, 18)
        #arcade.draw_text(output2, 610, 725, arcade.color.BLACK, 18)

        #if self.total_time < 0 :
        #    arcade.draw_text(game_over, 75, 600, arcade.color.RED, 80) 
        #    arcade.draw_text(total_score, 75, 520, arcade.color.RED, 80) 
        #if self.total_coins == 19:
        #        arcade.draw_text(won_text, 75, 520, arcade.color.RED, 40)
        #        arcade.draw_text(won_text, 75, 520, arcade.color.GLITTER, 41)




        

    def on_update(self, delta_time):
        """ Movement and game logic """

        self.physics_engine.update()
        self.enemy_list.update()

        #coin_hit_list = arcade.check_for_collision_with_list(self.player_sprite,self.coin_list
        self.total_time -= delta_time                                       
        """
        if self.total_time < 0:
            arcade.set_background_color(arcade.color.BLACK) 
        else:
            self.total_time -= delta_time
        if self.total_coins == 19:
            arcade.set_background_color(arcade.color.BLACK)
        else:
            
	    """

        """
        Keep track of if we changed the boundary. We don't want to call the
        set_viewport command if we didn't change the view port.
        """
        changed = False
        # Scroll left
        left_boundary = self.view_left + VIEWPORT_MARGIN
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left
            changed = True
        # Scroll right
        right_boundary = self.view_left + SCREEN_WIDTH - VIEWPORT_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary
            changed = True
        # Scroll up
        """
        top_boundary = self.view_bottom + SCREEN_HEIGHT - VIEWPORT_MARGIN
        if self.player_sprite.top > top_boundary:
            self.view_bottom += self.player_sprite.top - top_boundary
            changed = True
        # Scroll down
        bottom_boundary = self.view_bottom + VIEWPORT_MARGIN
        if self.player_sprite.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player_sprite.bottom
            changed = True
        """
        """
        I think we might have some difficulty with making this to fit to a certain sized platform area. 
        In the example I added a box around the maze area to limit where the player can go.
        """

        if changed:
            # Only scroll to integers. Otherwise we end up with pixels that
            # don't line up on the screen
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            # Do the scrolling
            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        # Currenlty if you move really fast, it doesn't add to the enemy_hit_list and therefore doesn't play the sound.
        enemy_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.enemy_list)
        if len(enemy_hit_list) > 0:
            arcade.play_sound(self.hit_sound)
        
        #for enemy in enemy_hit_list:
            #enemy.remove_from_sprite_lists()

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
        #if key == arcade.key.UP or key == arcade.key.DOWN:
        #    self.player_sprite.change_y = 0
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0


def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
