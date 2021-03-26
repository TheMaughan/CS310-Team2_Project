import arcade

# --- Constants ---
SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_COIN = .25
COIN_COUNT = 50

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Implement Views Example"


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


    def on_show(self):
        arcade.set_background_color(arcade.csscolor.DARK_SLATE_BLUE)

        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)

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
            print("creation of the NEW game..")
            from Game import MyGame
            game_view = MyGame()
            game_view.setup(self.level)
            self.window.show_view(game_view)

        if self.button_states["continue"] == True:
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
