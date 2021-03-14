import arcade #py -m venv venv
import random, os, math, time
from Player_Obj import Player
from Enemy_Obj import Enemy

MUSIC_VOLUME = 0.0
SPRITE_SCALING = 0.5
TILE_SCALING = 0.9

SCREEN_WIDTH = 750
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Platformer"


MOVEMENT_SPEED = 3
GRAVITY = .2 #change this to enable jumping
JUMP_SPEED = 11  

VIEWPORT_MARGIN = 250

TEXTURE_LEFT = 0
TEXTURE_RIGHT = 1


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

        
        self.physics_engine = None

        # Variables that will hold sprite lists
        self.player_list = None
        self.brick_list =None
        self.ground_list =None
        self.stone_list = None
        self.sun_list = None
        self.cloud_list = None
        self.house_list = None
        self.enemy_list = None
        # Set up sprites
        self.player_sprite = None
        self.brick_sprite = None
        self.ground_sprite = None
        self.stone_sprite = None
        self.sun_sprite = None
        self.cloud_sprite = None
        self.house_sprite = None
        self.enemy_sprite = None
        
        self.total_time = 90.0


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

    def reset(self):        #reset the game
        # Set the background color
        self.total_time = 90.0
        self.view_left = 0
        
    def setup(self): #change this section 
        """ Set up the game and initialize the variables. """
        arcade.set_background_color(arcade.color.LIGHT_BLUE) #change
        # Create the Sprite lists
        self.player_list = arcade.SpriteList()
        self.brick_list = arcade.SpriteList()
        self.ground_list = arcade.SpriteList()
        self.stone_list = arcade.SpriteList()
        self.sun_list = arcade.SpriteList()
        self.cloud_list = arcade.SpriteList()
        self.house_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        #self.player_sprite.reset_pos()

        # Set up the player Change this
        self.player_sprite = Player("Sprites\player.png", SPRITE_SCALING)
        self.player_sprite.center_x = 75
        self.player_sprite.center_y = 150
        self.player_list.append(self.player_sprite)

        self.enemy_sprite = Enemy("Sprites\\flipped_creeper.png", SPRITE_SCALING *.2)
        self.enemy_sprite.center_x = 250
        self.enemy_sprite.center_y = 125
        self.enemy_list.append(self.enemy_sprite)

        self.music_list = ["Sprites\Old_Game_David_Fesliyan.mp3", "Sprites\sawsquarenoise-Final_Boss.mp3"]
        self.play_song() # Get the music going!

            # --- Load in a map from the tiled editor ---
        self.brick_sprite = arcade.Sprite('Sprites\\brick.png', TILE_SCALING)
        self.brick_list.append(self.brick_sprite)

        self.ground_sprite = arcade.Sprite('Sprites\\ground.png', TILE_SCALING)
        self.ground_list.append(self.ground_sprite)

        self.stone_sprite = arcade.Sprite('Sprites\\stone.png', TILE_SCALING)
        self.stone_list.append(self.stone_sprite)

        self.sun_sprite = arcade.Sprite('Sprites\\sun.png', TILE_SCALING)
        self.sun_list.append(self.sun_sprite)

        self.cloud_sprite = arcade.Sprite('Sprites\\cloud.png', TILE_SCALING)
        self.cloud_list.append(self.cloud_sprite)

        self.house_sprite = arcade.Sprite('Sprites\\house.png', TILE_SCALING)
        self.house_list.append(self.house_sprite)


        
        

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
        self.stone_list =  arcade.tilemap.process_layer(my_map,background_layer, TILE_SCALING ) 
        self.cloud_list =  arcade.tilemap.process_layer(my_map,background_layer, TILE_SCALING ) 
        self.sun_list =  arcade.tilemap.process_layer(my_map,background_layer, TILE_SCALING ) 
        self.house_list =  arcade.tilemap.process_layer(my_map,background_layer, TILE_SCALING ) 

        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite,
                                                             self.ground_list,
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

        # Draw all the sprites. Make sure you place background frist
        self.ground_list.draw()
        self.brick_list.draw()
        self.stone_list.draw()
        self.cloud_list.draw()
        self.house_list.draw()
        self.enemy_sprite.draw()
        self.player_list.draw()
       

	
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

        if self.player_sprite.has_lost:
            from EndMenu import GameOverView
            end_view = GameOverView()
            self.window.show_view(end_view)
        

    def on_update(self, delta_time):
        """ Movement and game logic """

        self.physics_engine.update()
        self.physics_engine_enemy.update()


        #coin_hit_list = arcade.check_for_collision_with_list(self.player_sprite,self.coin_list
        self.total_time -= delta_time      

        if self.player_sprite.top < 0 or self.total_time < 0:
            if self.player_sprite.health > 1 and self.total_time > 0: # if the player fall of the screen
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