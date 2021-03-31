import arcade
import time

# --- Constants ---
SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_COIN = .25
COIN_COUNT = 50

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Implement Views Example"

MUSIC_VOLUME = .1


class InstructionView(arcade.View):
    def __init__(self):
        super().__init__()
        self.level = 1
        # attributes of the buttons
        self.button_restart = {"text": "new game", "pos": (SCREEN_WIDTH/2, 180), "size": (140, 60)}
        self.button_continue = {"text": "continue", "pos": (SCREEN_WIDTH/2, 100), "size": (140, 60)}
        # state of the button (if the mouse is on -> True)
        self.button_states = {"new game": False, "continue": False}

        self.mouse_pos = (0,0)
        self.current_player = None
        self.music = None
    

    def play_song(self):
        # Stop what is currently playing. This is to avoid having mutliple songs playing at the same time.
        if self.music:
            # This will keep there from just being silence playing and delete the player to keep there from wasted memory usage.
            self.current_player.pause()
            self.current_player.delete()

        """From https://www.fesliyanstudios.com/royalty-free-music/downloads-c/8-bit-music/6
        Another Website: https://freemusicarchive.org/genre/Chiptune"""
        # Basically sets up the directory to the music.
        self.music = arcade.Sound("Sprites\Old_Game_David_Fesliyan.mp3", streaming=True) # Streaming will tell the program to stream instead of making a copy of the file.
        # Creates the music player, using the stored information from music. 
        self.current_player = self.music.play(MUSIC_VOLUME)
        # Gives a quick pause in the music. If we did not include this it would see the song as being done and skip through it.
        time.sleep(0.03)


    def on_show(self):
        arcade.set_background_color(arcade.csscolor.DARK_SLATE_BLUE)

        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)
        self.play_song()

    def on_draw(self):
        """ Draw this view """
        arcade.start_render()
        arcade.draw_text("Instructions Screen", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        #arcade.draw_text("Click to advance", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2-75,
        #                 arcade.color.WHITE, font_size=20, anchor_x="center")

        self.button(self.button_continue)
        self.button(self.button_restart)


    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_pos = (x, y)


    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ If the user presses the mouse button, start the game. """
        if self.button_states["new game"] == True:
            self.current_player.pause()
            self.current_player.delete()
            print("creation of the NEW game..")
            from Game import MyGame
            game_view = MyGame()
            game_view.setup(self.level)
            self.window.show_view(game_view)

        if self.button_states["continue"] == True:
            self.current_player.pause()
            self.current_player.delete()
            print("continue the game..")
            from Game import MyGame
            game_view = MyGame()
            game_view.setup(self.level, "continue")
            self.window.show_view(game_view)


    def button(self, attributes):
        self.button_states[attributes["text"]] = False
        color = arcade.color.AMAZON
        # check if the mouse is on the button
        if attributes["pos"][0]-attributes["size"][0]/2 < self.mouse_pos[0] < attributes["pos"][0] + attributes["size"][0]/2 :
            if attributes["pos"][1]-attributes["size"][1]/2 < self.mouse_pos[1] < attributes["pos"][1] + attributes["size"][1]/2 :
                self.button_states[attributes["text"]] = True
                # change the color of  the button
                color = arcade.color.ANDROID_GREEN

        # draw the rectangle
        arcade.draw_rectangle_filled(attributes["pos"][0], attributes["pos"][1],
                                    attributes["size"][0], attributes["size"][1], color)
        # draw the text
        arcade.draw_text(attributes["text"], attributes["pos"][0], attributes["pos"][1],
                         arcade.color.WHITE, font_size=24, anchor_x="center", anchor_y="center")


def main():
    """ Main method """
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = InstructionView()
    window.show_view(start_view)
    arcade.run()

if __name__ == "__main__":
    main()
