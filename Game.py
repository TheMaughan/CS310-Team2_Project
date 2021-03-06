from typing import Optional
import arcade #py -m venv venv
import random, os, math, time
from os import path
from Player_Obj import Player
from Enemy_Obj import Enemy
from Problem_Obj import Problems
from Math_Interaction_Obj import PauseView

MUSIC_VOLUME = 0.1

# Constants used to scale our sprites from their original size
CHARACTER_SCALING = 0.2
SPRITE_SCALING = 0.2
TILE_SCALING = 3
COIN_SCALING = 3
SPRITE_PIXEL_SIZE = 16
GRID_PIXEL_SIZE = (SPRITE_PIXEL_SIZE * TILE_SCALING)

# Sets up the screen dimensions and the window title.
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

VIEWPORT_MARGIN = 250 # Used to create the scrolling feature. If it is changed to a smaller value there will be more movement room before the screen scrolls.

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

        self.save_time = 3 # the game will be saved every X sec

        self.physics_engine: Optional[arcade.PymunkPhysicsEngine] = None

        # Track the current state of what key is pressed
        self.left_pressed: bool = False
        self.right_pressed: bool = False
        self.up_pressed: bool = False
        self.down_pressed: bool = False
        self.jump_needs_reset: bool = False

        # Variables that will hold sprite lists
        self.player_list: Optional[arcade.SpriteList] = None
        #self.player_sprite = Optional[Player]

        # Made in the Tiled Mapmaker:
        # I don't know exactly what 'Optional' does, I assume that it helps with processing the game and
            # helps with writing less code.
        self.wall_list: Optional[arcade.SpriteList] = None
        self.coin_list: Optional[arcade.SpriteList] = None
        self.ladder_list: Optional[arcade.SpriteList] = None
        self.foreground_list: Optional[arcade.SpriteList] = None
        self.background_list: Optional[arcade.SpriteList] = None
        self.dont_touch_list: Optional[arcade.SpriteList] = None

        # Set up sprites
        self.player_sprite: Optional[Player] = None
        self.enemy_hit_list = None
        self.enemy_sprite: Optional[Enemy] = None

        # Player Progression:
        self.score = 0
        self.high_score = 0
        self.total_time = 90.0
        self.interacion = []

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        # Map Stuff:
        self.end_of_map = 0
        self.level = 1

        # Music
        self.music_list = []
        self.current_song_index = 0
        self.current_player = None
        self.music = None

        # Load sounds:
        self.hit_sound = arcade.load_sound("Sprites/gameover4.wav")
        self.collect_coin_sound = arcade.load_sound("sounds/coin1.wav")
        self.jump_sound = arcade.load_sound("sounds/jump1.wav")
        self.game_over = arcade.load_sound("sounds/gameover1.wav")

    # ---- Background Music Functions: ---- #
    """Will iterate through the index of songs. If it reaches the end it will start over from the beginning again."""
    def advance_song(self):
        self.current_song_index += 1
        if self.current_song_index >= len(self.music_list):
            self.current_song_index = 0

    """Will match the song to be played with the current level.
    Note that the levels start at one, so there has to be another song in the index location of 0 for this to work"""
    def level_music(self):
        self.current_song_index = self.level

    """What actually gets the songs to play.
    It requires a player that will be used to access and adjust the songs."""
    def play_song(self):
        # Stop what is currently playing. This is to avoid having mutliple songs playing at the same time.
        if self.music:
            # This will keep there from just being silence playing and delete the player to keep there from wasted memory usage.
            self.current_player.pause()
            self.current_player.delete()

        """From https://www.fesliyanstudios.com/royalty-free-music/downloads-c/8-bit-music/6
        Another Website: https://freemusicarchive.org/genre/Chiptune"""
        # Basically sets up the directory to the music.
        self.music = arcade.Sound(self.music_list[self.current_song_index], streaming=True) # Streaming will tell the program to stream instead of making a copy of the file.
        # Creates the music player, using the stored information from music. 
        self.current_player = self.music.play(MUSIC_VOLUME)
        # Gives a quick pause in the music. If we did not include this it would see the song as being done and skip through it.
        time.sleep(0.03)

        # ^^^^ End of Background Music ^^^^ #


    # ---- Save Game Code: ---- #
    def read_previous_game(self):
        """ Read the text file and make a dico with that contain all the states (position,..) of the previous game"""

        d = {}
        with open("previous_game.txt") as f:
            for line in f:
                (key, val) = line.split("=")
                d[key] = val[:-1]
        return d


    def load_previous_game(self):

        states_dico = self.read_previous_game()

        # position of the player
        player_pos = states_dico["player_sprite.position"].split(",")
        self.player_sprite.position = [int(player_pos[0]), int(player_pos[1])]

        # view left
        #self.view_left = int(states_dico["view_left"])

        # time
        self.total_time = float(states_dico["total_time"])
        # score
        self.score = int(states_dico["score"])
        # high score
        self.high_score = int(states_dico["high_score"])
        # health of the player
        self.player_sprite.health = int(states_dico["lives"])
        # level
        self.level = int(states_dico["level"])
        self.setup(self.level) # Needed to actually start at level 2 from the saves.

        self.continue_first_lunch = True # make that the set_viewport is called

    """Used to read in only the high score"""
    def load_high_score(self):
         # Check for previous game
        if path.exists("previous_game.txt"):
            states_dico = self.read_previous_game()
            self.high_score = int(states_dico["high_score"])
        else:
            return


    def save_game(self, delta_time):

        f = open('previous_game.txt', 'w') # delete all the content of the file

        # position of the player
        f.write(f"player_sprite.position={int(self.player_sprite.position[0])},{int(self.player_sprite.position[1])}\n")
        # time
        f.write(f"total_time={int(self.total_time)}\n")

        f.write(f"score={self.score}\n")

        f.write(f"high_score={self.high_score}\n")

        f.write(f"lives={self.player_sprite.health}\n")

        f.write(f"level={self.level}\n")

        f.close() # close  the file

        print("-- game saved")

        # ^^^^ End of Save Game Code: ^^^^ #


    def reset(self):        #reset the game
        # Set the background color
        self.total_time = 90.0
        self.view_left = 0


    def setup(self, level, lunch_type="new game"): #change this section
        """ Set up the game and initialize the variables. """
        arcade.set_background_color(arcade.color.LIGHT_BLUE) #change
        # Create the map layer lists
        self.enemy_list = arcade.SpriteList()

        # Set up the player Change this
        self.player_sprite = Player()
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player_sprite)
        self.player_sprite.center_x = PLAYER_START_X
        self.player_sprite.center_y = PLAYER_START_Y
        #self.player = arcade.AnimatedWalkingSprite()

        # Set up for the Enemy Sprite.
        self.enemy_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.enemy_list)
        self.enemy_sprite = Enemy()
        self.enemy_sprite.center_x = 250
        self.enemy_sprite.center_y = 125
        self.enemy_list.append(self.enemy_sprite)

        #self.enemy_list = arcade.SpriteList()
        #self.enemy = arcade.AnimatedTimeSprite()

        # Set up for the music. Includes a list with each song title, sets to the current level, and then plays song.
        self.music_list = ["sounds\Old_Game_David_Fesliyan.mp3", "sounds\Super Mario Bros. Theme - 8-Bit Dance Remix.mp3", "sounds\sawsquarenoise-Final_Boss.mp3", "sounds\Jim Hall - Trapped In the Upside Down.mp3"]
        self.level_music()
        self.play_song() # Get the music going!

        #---------------------------- Map Code ----------------------------#
        # Name of the layer in the file that has our platforms/walls
        platforms_layer_name = 'Platforms'
        # Name of the layer containing moving platforms:
        moving_platforms_layer_name = 'Moving Platforms'
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
        map_name = f"Sprites/level_{level}.tmx"
        # Read in the tiled map
        my_map = arcade.tilemap.read_tmx(map_name)


        #- Read the Map & find the end of the map:
        self.end_of_map = my_map.map_size.width * GRID_PIXEL_SIZE

        # -- Map Layers -- #

        # Platforms & Boundry objects (player cannot move through)
        self.wall_list = arcade.tilemap.process_layer(my_map,
                                                      platforms_layer_name,
                                                      TILE_SCALING,
                                                      use_spatial_hash=True)
        # -- Moving Platforms -- #
        moving_platforms_list = arcade.tilemap.process_layer(my_map, moving_platforms_layer_name, TILE_SCALING)
        for sprite in moving_platforms_list:
            self.wall_list.append(sprite) #- All moving platforms are classified as 'walls' in our code.
            #- Using the same logic for moving platforms, we can also make simple enemies.

        # Background Layer:
        self.background_list = arcade.tilemap.process_layer(my_map,
                                                            background_layer_name,
                                                            TILE_SCALING)
        #self.ladder_list = arcade.tilemap.process_layer(my_map, "Ladders",
                                                        #TILE_SCALING,
                                                        #use_spatial_hash=True)

        # Foreground Layer:
        self.foreground_list = arcade.tilemap.process_layer(my_map,
                                                            foreground_layer_name,
                                                            TILE_SCALING)

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

        # --------- Physics Engine & Logic --------- #
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite,
                                                             self.wall_list,
                                                             GRAVITY)
        self.physics_engine_enemy = arcade.PhysicsEnginePlatformer(self.enemy_sprite,
                                                                    self.wall_list,
                                                                    GRAVITY)

        if lunch_type == "continue":
            if path.exists("previous_game.txt"): # Check for file to avoid errors - Will just create a new game if there is no save file
                self.load_previous_game()
        else:
            self.load_high_score() # Set high score
            self.continue_first_lunch = False

        # make that the game is saved every X sec
        arcade.schedule(self.save_game, self.save_time)


    def on_draw(self):
        """
        Render the screen.
        """
         #timer set up

        minutes = int(self.total_time) // 60

        seconds = int(self.total_time) % 60

        Time = f"Time:  {minutes: 02d}:{seconds:02d}"

        # This command has to happen before we start drawing
        arcade.start_render()

        # - Map Objects (IMPORTANT! The Order Objects are
        #       drawn matter, Objects drawn first will appear behind!):
        self.background_list.draw() # This draws first, and is behind all
        self.dont_touch_list.draw() # You touch, you die (lava, acid, and other enviromental hazards)
        self.wall_list.draw() # Player & Enemies cannot move through objects drawn in this layer (platforms, the ground, walls, etc.)
        self.coin_list.draw() # Money! Points! Touch this layer and add value to a counter!
        #self.ladder_list.draw() # I don't have any ladders yet, understanding the code for this will take time... maybe later...

        self.enemy_list.draw()
        self.enemy_sprite.draw() # The Enemy layer

        self.player_list.draw() # The Player Layer
        self.player_sprite.draw() # ^

        self.foreground_list.draw() # This draws last, and goes in front of all

        # --- Draw a Coin collection Counter, UI Element --- #
        score_text = f"Score: {self.score}"
        arcade.draw_text(score_text, 10 + self.view_left, 10 + self.view_bottom, arcade.csscolor.WHITE, 18)
        """
        # Display position:
        self.position = int(self.player_sprite.changed_x), int(self.player_sprite.changed_y)
        position_text = f"Position: {self.position}"
        arcade.draw_text(position_text, 50 + self.view_left, 50 + self.view_bottom, arcade.csscolor.WHITE, 18)
        """
        # --- Draw a High Score feature --- #
        score_text = f"High Score: {self.high_score}"
        arcade.draw_text(score_text, self.view_left + SCREEN_WIDTH - 140, 10 + self.view_bottom, arcade.csscolor.WHITE, 18)

        # ---- Enemy Interaction ---- #
        for enemy in self.enemy_hit_list:
            self.enemy_hit_list.pop()
            question = self.interacion[len(self.enemy_hit_list)-1].get_question()
            answer = self.interacion[len(self.enemy_hit_list)-1].get_answer()
            firstnum = self.interacion[len(self.enemy_hit_list)-1].get_first()
            secondnum = self.interacion[len(self.enemy_hit_list)-1].get_second()
            #call the pause menu
            pause = PauseView(self, self.player_sprite)
            pause.set_question = question
            pause.set_answer = answer
            pause.set_first = firstnum
            pause.set_second = secondnum
            self.window.show_view(pause)

        arcade.draw_text(Time, 20 + self.view_left, 750, arcade.color.YELLOW_ROSE, 26)
        arcade.draw_text("lives : "+str(self.player_sprite.health), 625 + self.view_left, 750, arcade.color.RED, 32)

        #####---- This calls the 'Game Over' Viewport ----#####
        if self.player_sprite.has_lost:
            #self.music.stop(self.current_player) Instead:
            self.current_player.pause()
            self.current_player.delete()
            from EndMenu import GameOverView
            end_view = GameOverView()
            self.window.show_view(end_view)


    def on_update(self, delta_time):
        """ Movement and game logic """

        self.physics_engine.update()
        self.physics_engine_enemy.update()

        self.player_sprite.update()
        #self.player_list.update()
        self.player_list.update_animation()

        #update map animations:
        self.coin_list.update_animation(delta_time)
        self.background_list.update_animation(delta_time)
        self.foreground_list.update_animation(delta_time)
        self.dont_touch_list.update_animation(delta_time)
        

        # ----- Moving Platform Logic ----- #
        #update moving platforms:
        self.wall_list.update()
        # See if the moving wall hit a boundary and needs to reverse direction.
        for wall in self.wall_list:

            if wall.boundary_right and wall.right > wall.boundary_right and wall.change_x > 0:
                wall.change_x *= -1
            if wall.boundary_left and wall.left < wall.boundary_left and wall.change_x < 0:
                wall.change_x *= -1
            if wall.boundary_top and wall.top > wall.boundary_top and wall.change_y > 0:
                wall.change_y *= -1
            if wall.boundary_bottom and wall.bottom < wall.boundary_bottom and wall.change_y < 0:
                wall.change_y *= -1


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

        # Loop through the music by checking if the music in the music player finished.
        if self.music.is_complete(self.current_player):
            self.play_song()
        #Currently code is of no effect, since the music is just cleared when we call EndMenu.
        if self.total_time <= 0:
            if self.music:
                # What the stop() function from arcade should be doing idk why but using stop() doesn't work.
                self.current_player.pause()
                self.current_player.delete()
            self.advance_song()
            self.play_song()
            
        #Gets how far into the song we are at.
        position = self.music.get_stream_position(self.current_player)
        # Reset the time on level 2. Will currently reset when you load a game saved on level 2.
        if self.level == 2 and self.player_sprite.health == 5 and position < 1.0:
            self.total_time = 100.0

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

        # Some enemy updates
        self.enemy_list.update()
        self.enemy_sprite.follow_sprite(self.player_sprite)

        # Calls function from the enemy class to have it follow the player sprite
        for enemy in self.enemy_list:
            enemy.follow_sprite(self.player_sprite)

        # If the enemy falls off of the screen then reset it back to it's original position.
        if self.enemy_sprite.top < 0:
            self.enemy_sprite.reset_pos()

        # Sets up the hit list for when there are enemies that are in the hitbox of the player sprite
        self.enemy_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.enemy_list)
        
        # A loop to go through and add Problem objects to be used to display a math problem.
        for enemy in self.enemy_hit_list:
            temp = Problems()
            self.interacion.append(temp)
            enemy.remove_from_sprite_lists()

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
        coin_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)

        for coin in coin_hit_list: #- Remove a coin, add a point, make a sound:
            coin.remove_from_sprite_lists()
            arcade.play_sound(self.collect_coin_sound)
            self.score += 1

        # Sets the high score
        if self.score > self.high_score:
            self.high_score = self.score


        # ------> Player Death Event <------ #
        changed_viewport = False # - Setting the View to the Game, for now...
        # - Did the Player Die?
        if (self.player_sprite.center_y < -100) or (arcade.check_for_collision_with_list(self.player_sprite,
                                                                                self.dont_touch_list)): #- Restart Position:
            # Reset Player
            self.player_sprite.center_x = 0
            self.player_sprite.center_y = 0
            self.player_sprite.center_x = PLAYER_START_X
            self.player_sprite.center_y = PLAYER_START_Y

            # Reset View
            self.view_left = 0
            self.view_bottom = 0
            changed_viewport = True
            arcade.play_sound(self.game_over)


        # ------> Player Win Event <------ #
        if self.player_sprite.center_x >= self.end_of_map:
            self.level += 1 # Advance a level
            self.setup(self.level) # Restart Game at new Level
            # Reset the Viewport
            self.view_left = 0
            self.view_bottom = 0
            changed_viewport = True
            
            #Load the player


    # For more smooth player movement:
    def process_keychange(self):
        """
        Called when we change a key up/down or we move on/off a ladder.
        """
        # Process up/down
        if self.up_pressed and not self.down_pressed:
            if self.physics_engine.is_on_ladder(): 
                #The ladder code doesn't work yet, there has to be more code in the Plaer() class
                self.player_sprite.change_y = MOVEMENT_SPEED
            elif self.physics_engine.can_jump(y_distance=10) and not self.jump_needs_reset:
                self.player_sprite.change_y = JUMP_SPEED
                self.jump_needs_reset = True
                arcade.play_sound(self.jump_sound)
        elif self.down_pressed and not self.up_pressed:
            if self.physics_engine.is_on_ladder():
                self.player_sprite.change_y = -MOVEMENT_SPEED

        # Process up/down when on a ladder and no movement
        if self.physics_engine.is_on_ladder():
            if not self.up_pressed and not self.down_pressed:
                self.player_sprite.change_y = 0
            elif self.up_pressed and self.down_pressed:
                self.player_sprite.change_y = 0

        # Process left/right
        if self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = MOVEMENT_SPEED
        elif self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        else:
            self.player_sprite.change_x = 0

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if len(self.enemy_hit_list) > 0: # Play a noise when an enemy is hit.
            arcade.play_sound(self.hit_sound)


        # Better movement is best when using pymunk physics:
        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = True
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = True
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True

        self.process_keychange()


    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """
        """
        # If a player releases a key, zero out the speed.
        # This doesn't work well if multiple keys are pressed.
        # Use 'better move by keyboard' example if you need to
        # handle this.
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0
        """
        # Better movement is best when using pymunk physics:
        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = False
            self.jump_needs_reset = False
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = False
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False

        self.process_keychange()

