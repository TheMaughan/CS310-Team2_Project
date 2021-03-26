import arcade
import os
import arcade.gui
from arcade.gui import UIManager

class MyFlatButton(arcade.gui.UIFlatButton):
    """
    To capture a button click, subclass the button and override on_click.
    """
    def on_click(self):
        """ Called when user lets off button """
        print("Click flat button. ")

#For Pause
WIDTH = 750
HEIGHT = 800

class PauseView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view
        self.operator = 0
        self.first_val = 0
        self.second_val = 0
        self.question = ""
        self.answer = 0
        self.ui_manager = UIManager()


    def on_show(self):
        #self.setup()
        arcade.set_background_color(arcade.color.LIGHT_BLUE)

    def on_draw(self):
        arcade.start_render()

        # Draw player, for effect, on pause screen.
        # The previous View (GameView) was passed in
        # and saved in self.game_view.
        player_sprite = self.game_view.player_sprite
        player_sprite.draw()

        # draw an orange filter over him
        arcade.draw_lrtb_rectangle_filled(left=player_sprite.left,
                                          right=player_sprite.right,
                                          top=player_sprite.top,
                                          bottom=player_sprite.bottom,
                                          color=arcade.color.LIGHT_BLUE + (200,))
        #changed the x and y so the question always was above the player
        arcade.draw_text(self.set_question, player_sprite.left-25, player_sprite.bottom + 300,
                         arcade.color.BLACK, font_size=50, anchor_x="center")

        # Show tip to return or reset
        arcade.draw_text("70",
                         player_sprite.left-50,
                         player_sprite.bottom+ 200,
                         arcade.color.BLACK,
                         font_size=20,
                         anchor_x="center")
        arcade.draw_text("67",
                         player_sprite.left+50,
                         player_sprite.bottom+ 200,
                         arcade.color.BLACK,
                         font_size=20,
                         anchor_x="center")
        player_sprite = self.game_view.player_sprite
        button = MyFlatButton(
            'FlatButton',
            player_sprite.left+100,
            player_sprite.bottom+ 100,
            width=250
        )
        self.ui_manager.add_ui_element(button)
        button = MyFlatButton(
            'FlatButton',
            player_sprite.left-200,
            player_sprite.bottom+ 100,
            width=250
        )
        self.ui_manager.add_ui_element(button)

        
    #def setup(self):

    def on_key_press(self, key, _modifiers):
        self.ui_manager.unregister_handlers()
        if key == arcade.key.ESCAPE:   # resume game
            self.window.show_view(self.game_view)
        elif key == arcade.key.ENTER:  # reset game
            game = GameView()
            self.window.show_view(game)
    
    def set_question(self):
        return self.question

    def set_answer(self):
        return self.answer

    def set_first(self):
        return self.first_val

    def set_second(self):
        return self.second_val
