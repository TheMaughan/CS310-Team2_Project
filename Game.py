from typing import Optional
import arcade #py -m venv venv
import random, os, math, time
from Player_Obj import Player
from Enemy_Obj import Enemy

MUSIC_VOLUME = 0.0

# Constants used to scale our sprites from their original size
CHARACTER_SCALING = 1
SPRITE_SCALING = 0.5
TILE_SCALING = 0.5
COIN_SCALING = 0.5
SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = (SPRITE_PIXEL_SIZE * TILE_SCALING)
#TILE_SCALING = 0.9

SCREEN_WIDTH = 750
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Platformer"


MOVEMENT_SPEED = 3
GRAVITY = 1 #0.2 change this to enable jumping
JUMP_SPEED = 20 #11

#Friction:
PLAYER_FRICTION = 1.0
WALL_FRICTION = 0.7
DYNAMIC_ITEM_FRICTION = 0.6

# Mass (defaults to 1)
PLAYER_MASS = 2.0

# Limit Speed (setter & getter)
PLAYER_MAX_HORIZONAL_SPEED = 450
PLAYER_MAX_VERTICAL_SPEED = 1600

#Speed lost per second:
DEFAULT_DAMPING = 0.4
PLAYER_DAMPING = 1.0

"""
LEFT_VIEWPORT_MARGIN = 200
RIGHT_VIEWPORT_MARGIN = 200
BOTTOM_VIEWPORT_MARGIN = 150
TOP_VIEWPORT_MARGIN = 100
"""

VIEWPORT_MARGIN = 250

TEXTURE_LEFT = 0
TEXTURE_RIGHT = 1

PLAYER_START_X = 64
PLAYER_START_Y = 225


class MyGame(arcade.View):
    """
    Main application class.
    """

    def __init__(self):
        """
        Initializer
        """

        # Call the parent class initializer
        super().__init__()

        
        self.physics_engine: Optional[arcade.PymunkPhysicsEngine] = None

        # Variables that will hold sprite lists
        self.player_list: Optional[arcade.SpriteList] = None
        self.player = None
        
        # Made in the Tiled Mapmaker:
        self.wall_list = None
        self.coin_list = None
        self.foreground_list = None
        self.background_list = None
        self.dont_touch_list = None

        # Set up sprites
        self.player_sprite: Optional[Player] = None
        self.enemy_list = None
        
        # Player Prograssion:
        self.score = 0
        self.total_time = 90.0


        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        # Map Stuff:
        self.end_of_map = 0
        self.level = 1

        #Sound
        self.music_list = []
        self.current_song_index = 0
        self.music = None
        self.hit_sound = arcade.load_sound("Sprites/gameover4.wav")

        # Load sounds:
        self.collect_coin_sound = arcade.load_sound("sounds/coin1.wav")
        self.jump_sound = arcade.load_sound("sounds/jump1.wav")
        self.game_over = arcade.load_sound("sounds/gameover1.wav")

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

    def reset(self):        #reset the game
        # Set the background color
        self.total_time = 90.0
        self.view_left = 0
        
    def setup(self): #change this section 
        """ Set up the game and initialize the variables. """
        arcade.set_background_color(arcade.color.LIGHT_BLUE) #change
        # Create the map layer lists
        self.enemy_list = arcade.SpriteList()
        
        self.foreground_list = arcade.SpriteList()
        self.background_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()

        # Set up the player Change this
        #self.player_sprite = Player("Sprites\player.png", SPRITE_SCALING)
        self.player_sprite = Player()
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player_sprite)
        self.player_sprite.center_x = 75
        self.player_sprite.center_y = 150
        #self.player = arcade.AnimatedWalkingSprite()

        self.enemy_sprite = Enemy("Sprites\\flipped_creeper.png", SPRITE_SCALING *.2)
        self.enemy_sprite.center_x = 250
        self.enemy_sprite.center_y = 125
        #self.enemy_list.append(self.enemy_sprite)

        self.enemy_list = arcade.SpriteList()
        self.enemy = arcade.AnimatedTimeSprite()
        self.enemy.textures = []


        self.music_list = ["Sprites\Old_Game_David_Fesliyan.mp3", "Sprites\sawsquarenoise-Final_Boss.mp3"]
        self.play_song() # Get the music going!

        #---------------------------- Map Code ----------------------------#
        # Name of the layer in the file that has our platforms/walls
        platforms_layer_name = 'Platforms'
        # Name of the layer that has items for pick-up
        coins_layer_name = 'Coins'
        # Name of the layer that has items for foreground
        foreground_layer_name = 'Foreground'
        # Name of the layer that has items for background
        background_layer_name = 'Background'
        # Name of the layer that has items we shouldn't touch
        dont_touch_layer_name = "Don't Touch"
        # --- Load File --- #
        # Name of map file to load
        map_name = f"level_{level}.tmx"
        # Read in the tiled map
        my_map = arcade.tilemap.read_tmx(map_name)
        

        #- Read the Map:
        self.end_of_map = my_map.map_size.width * GRID_PIXEL_SIZE

        # -- Map Layers -- #
                                                      
        # Background Layer:
        self.background_list = arcade.tilemap.process_layer(my_map,
                                                            background_layer_name,
                                                            TILE_SCALING)

        # Foreground Layer:
        self.foreground_list = arcade.tilemap.process_layer(my_map,
                                                            foreground_layer_name,
                                                            TILE_SCALING)
        # Platforms & Boundry objects (player cannot move through)
        self.wall_list = arcade.tilemap.process_layer(map_object=my_map,
                                                      layer_name=platforms_layer_name,
                                                      scaling=TILE_SCALING,
                                                      use_spatial_hash=True)
        
        # -- Map Coins -- #
        # Name of the layer that has items for pick-up
        self.coin_list = arcade.tilemap.process_layer(my_map,
                                                      coins_layer_name,
                                                      TILE_SCALING,
                                                      use_spatial_hash=True)

        # Insta-death Layer Name (lava, fall off map, spikes, etc.):
        self.dont_touch_list = arcade.tilemap.process_layer(my_map,
                                                            dont_touch_layer_name,
                                                            TILE_SCALING,
                                                            use_spatial_hash=True)
        # --- Other Map Details -- #
        # Set the background color
        if my_map.background_color:
            arcade.set_background_color(my_map.background_color)
        # ^^^^^^^^^^^^^^^^^^^ End of Map Code ^^^^^^^^^^^^^^^^^^^ #


        
        

        # Name of map file to load
        map_name = "Sprites\map1.tmx"
         # Name of the layer in the file that has our platforms/walls
        main_layer = 'foreground'
        background_layer = 'background'
        #cloud_layer = 'cloud.png'
        #house_layer = 'house.png'
        #stone_layer = 'stone.png'
        #sun_layer = 'sun.png'
        my_map = arcade.tilemap.read_tmx(map_name)
        self.ground_list = arcade.tilemap.process_layer(my_map,main_layer, TILE_SCALING )
        self.brick_list = arcade.tilemap.process_layer(my_map,main_layer, TILE_SCALING )
        self.clear_list =  arcade.tilemap.process_layer(my_map,main_layer, TILE_SCALING )
        self.stone_list =  arcade.tilemap.process_layer(my_map,background_layer, TILE_SCALING ) 
        self.cloud_list =  arcade.tilemap.process_layer(my_map,background_layer, TILE_SCALING ) 
        self.sun_list =  arcade.tilemap.process_layer(my_map,background_layer, TILE_SCALING ) 
        self.house_list =  arcade.tilemap.process_layer(my_map,background_layer, TILE_SCALING ) 

        # --------- Physics Engine & Logic --------- #
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player,
                                                             self.wall_list,
                                                             GRAVITY)
        self.physics_engine_enemy = arcade.PhysicsEnginePlatformer(self.enemy_sprite,
                                                             self.ground_list,
                                                            GRAVITY)


    def on_draw(self):
        """
        Render the screen.
        """

         #timer set up

        minutes = int(self.total_time) // 60

        seconds = int(self.total_time) % 60

        Time = f"Time:  {minutes: 02d}:{seconds:02d}"

        #output2 = f"Total coins: {self.total_coins} "

        #won_text = "You got all the coins!"

        #game_over = "Game Over"

        #total_score = f" Score: {self.total_coins}"


        

        # This command has to happen before we start drawing
        arcade.start_render()

        # - Map Objects (IMPORTANT! The Order Objects are
        #       drawn matter, Objects drawn first will appear behind other objects!):
        self.background_list.draw()
        self.dont_touch_list.draw()
        self.wall_list.draw()
        self.coin_list.draw()
        self.enemy_sprite.draw()
        self.player_list.draw()
        self.player_sprite.draw()
        self.foreground_list.draw()
        
        score_text = f"Score: {self.score}"
        arcade.draw_text(score_text, 10 + self.view_left, 10 + self.view_bottom, arcade.csscolor.WHITE, 18)

	
	#take this part ot. Draws text on screen
        #arcade.draw_text(output, 625, 750, arcade.color.BLACK, 18) timer
        #arcade.draw_text(output2, 610, 725, arcade.color.BLACK, 18)

        #if self.total_time < 0 :
        #    arcade.draw_text(game_over, 75, 600, arcade.color.RED, 80) 
        #    arcade.draw_text(total_score, 75, 520, arcade.color.RED, 80) 
        #if self.total_coins == 19:
        #        arcade.draw_text(won_text, 75, 520, arcade.color.RED, 40)
        #        arcade.draw_text(won_text, 75, 520, arcade.color.GLITTER, 41)
        arcade.draw_text(Time, 20 + self.view_left, 750, arcade.color.BLACK, 26)
        arcade.draw_text("lives : "+str(self.player_sprite.health), 625 + self.view_left, 750, arcade.color.RED, 32)

        #####---- This call the 'Game Over' Viewport ----#####
        if self.player_sprite.has_lost:
            from EndMenu import GameOverView
            end_view = GameOverView()
            self.window.show_view(end_view)
        

    def on_update(self, delta_time):
        """ Movement and game logic """

        self.physics_engine.update()
        self.physics_engine_enemy.update()

        #self.player_sprite.update()
        self.player_list.update()
        self.player_list.update_animation()


        #coin_hit_list = arcade.check_for_collision_with_list(self.player_sprite,self.coin_list
        self.total_time -= delta_time

        if self.player_sprite.top < 0 or self.total_time < 0:
            if self.player_sprite.health > 1 and self.total_time > 0: # if the player falls off the screen
                self.view_left = 0
                self.player_sprite.reset_pos()
                self.player_sprite.health -= 1
            else: # if no more health or no more time
                self.player_sprite.has_lost = True
                self.player_sprite.health = 0                                 
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
        I think we might have some difficulty with making this to fit to a certain sized brick area. 
        In the example I added a box around the maze area to limit where the player can go.
        """

        self.enemy_list.update()
        for enemy in self.enemy_list:
            enemy.follow_sprite(self.player_sprite)
        if self.enemy_sprite.top < 0:
            self.enemy_sprite.reset_pos()

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

        # ----- Coin Logic: ----- #
        coin_hit_list = arcade.check_for_collision_with_list(self.player, self.coin_list)

        for coin in coin_hit_list: #- Remove a coin, add a point, make a sound:
            coin.remove_from_sprite_lists()
            arcade.play_sound(self.collect_coin_sound)
            self.score += 1

        # ------> Player Death Event <------ #
        changed_viewport = False # - Setting the View to the Game, for now...
        # - Did the Player Die?
        if (self.player.center_y < -100) or (arcade.check_for_collision_with_list(self.player,
                                                                                self.dont_touch_list)): #- Restart Position:
            # Reset Player
            self.player.center_x = 0
            self.player.center_y = 0
            self.player.center_x = PLAYER_START_X
            self.player.center_y = PLAYER_START_Y

            # Reset View
            self.view_left = 0
            self.view_bottom = 0
            changed_viewport = True
            arcade.play_sound(self.game_over)
        

        # ------> Player Win Event <------ #
        if self.player.center_x >= self.end_of_map:
            self.level += 1 # Advance a level
            self.setup(self.level) # Restart Game at new Level
            # Reset the Viewport
            self.view_left = 0
            self.view_bottom = 0
            changed_viewport = True

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        
        # Currenlty if you move really fast, it doesn't add to the enemy_hit_list and therefore doesn't play the sound.
        enemy_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.enemy_list)
        if len(enemy_hit_list) > 0:
            arcade.play_sound(self.hit_sound)


        #add here
        for enemy in enemy_hit_list:
            enemy.remove_from_sprite_lists()





        # If the player presses a key, update the speed
        if key == arcade.key.UP:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = JUMP_SPEED
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
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

"""
def main():
    "" Main method ""
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
"""
