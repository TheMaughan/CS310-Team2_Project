import arcade
import os

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


    def on_show(self):
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

    def on_key_press(self, key, _modifiers):
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
