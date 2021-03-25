import arcade


# --- Constants ---
SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_COIN = .25
COIN_COUNT = 50

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Implement Views Example"


class GameOverView(arcade.View):
    """ View to show when game is over """

    def __init__(self):
        """ This is run once when we switch to this view """
        super().__init__()
        #self.texture = arcade.load_texture("ship.png")
        self.level = 1

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        """ Draw this view """
        arcade.start_render()
        #self.texture.draw_sized(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                                #SCREEN_WIDTH, SCREEN_HEIGHT)
        
        #arcade.draw_text("You lost...", SCREEN_HEIGHT//2, arcade.color.RED)
        #arcade.draw_text("Press Enter to respawn", SCREEN_HEIGHT//2-80, arcade.color.WHITE)

        arcade.draw_text("You lost...", SCREEN_WIDTH / 2, SCREEN_HEIGHT//2,
                         arcade.color.RED, font_size=78, anchor_x="center")
        arcade.draw_text("Click to advance", SCREEN_WIDTH / 2, SCREEN_HEIGHT//2-80,
                         arcade.color.WHITE, font_size=62, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ If the user presses the mouse button, re-start the game. """
        from Game import MyGame
        game_view = MyGame()
        game_view.setup(self.level)
        self.window.show_view(game_view)