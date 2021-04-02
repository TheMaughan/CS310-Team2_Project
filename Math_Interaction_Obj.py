import arcade
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
# <--- Handles Math question and displays the questions and answer --- >
class PauseView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view
        self.background = arcade.get_window().background_color
        self.operator = 0
        self.first_val = 0
        self.second_val = 0
        self.question = ""
        self.answer = 0
        self.q1= 0
        self.q2 = 0
        self.q3 = 0
        self.q4 = 0
        self.questionwithans = 0
        self.run = True
        self.operator = random.randrange(4)
        self.tries = 2

        self.button_question1 = {"text": "Q1", "pos": (SCREEN_WIDTH/3, 180), "size": (140, 60)}
        self.button_question2 = {"text": "Q2", "pos": (SCREEN_WIDTH/3, 90), "size": (140, 60)}
        self.button_question3 = {"text": "Q3", "pos": (600, 180), "size": (140, 60)}
        self.button_question4 = {"text": "Q4", "pos": (600, 90), "size": (140, 60)}
        # state of the button (if the mouse is on -> True)
        self.button_states = {"Q1": False, "Q2": False, "Q3": False ,"Q4": False }
        self.mouse_pos = (0,0)


    def on_show(self):
        #self.setup()
        arcade.set_background_color(arcade.color.LIGHT_BLUE)

        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)
    
    # <--- Sets a up the buttons with the question unless they have the answer --->
    def handlequestion(self, question):
            if question == 0:
                if self.questionwithans == 0:
                    return
                else:
                    self.q1 = self.set_first + self.second_val + 2
            if question == 1:
                if self.questionwithans == 1:
                    return
                else:
                    self.q2 = self.set_second - self.second_val + 1
            if question == 2:
                if self.questionwithans == 2:
                    return
                else:
                    self.q3 = self.set_first * self.set_second + 2

            if question == 3:
                if self.questionwithans == 3:
                    return
                else:
                    self.q4 = self.set_first - self.set_second + 9

    
    def on_draw(self):
        arcade.start_render()

        # Draw player, for effect, on pause screen.
        # The previous View (GameView) was passed in
        # and saved in self.game_view.
        player_sprite = self.game_view.player_sprite
        player_sprite.draw()
    
        #changed the x and y so the question always was above the player
        arcade.draw_text(self.set_question, SCREEN_WIDTH/2 + 30, SCREEN_HEIGHT/2,
                         arcade.color.BLACK, font_size=50, anchor_x="center")
        arcade.draw_text(f"You have {self.tries} trie(s) left", SCREEN_WIDTH/2 + 30, SCREEN_HEIGHT/2 - 65,
                         arcade.color.BLACK, font_size=30, anchor_x="center")

        # <--- Handles which button will hold the answer ---> 
        if self.run == True:
            
            x = random.randrange(4)
            if x == 0:
                self.q1 = self.set_answer
                self.questionwithans = 0
            if x == 1:
                self.q2 = self.set_answer
                self.questionwithans = 1
            if x == 2:
                self.q3 = self.set_answer
                self.questionwithans = 2
            if x == 3:
                self.q4 = self.set_answer 
                self.questionwithans = 3

            for i in range (4):
                self.handlequestion(i)
            self.run = False
        # makes the buttons
        self.button_question1 = {"text": str(self.q1), "pos": (SCREEN_WIDTH/3, 180), "size": (140, 60)}
        self.button_question2 = {"text": str(self.q2), "pos": (SCREEN_WIDTH/3, 90), "size": (140, 60)}
        self.button_question3 = {"text": str(self.q3), "pos": (600, 180), "size": (140, 60)}
        self.button_question4 = {"text": str(self.q4), "pos": (600, 90), "size": (140, 60)}

        # adds each button 
        self.button(self.button_question1)
        self.button(self.button_question2)
        self.button(self.button_question3)
        self.button(self.button_question4)



    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_pos = (x, y)
        
    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ If the user presses the mouse button, start the game. """
        # user has 2 tries to guess. Will exit the pause screen here
        if self.button_states[str(self.q1)] == True:
            if self.questionwithans == 0:
                arcade.set_background_color(self.background)
                self.window.show_view(self.game_view)
            else:
                self.tries -= 1
            if self.tries == 0:
                arcade.set_background_color(self.background)
                self.window.show_view(self.game_view)
        if self.button_states[str(self.q2)] == True:
            if self.questionwithans == 1: 
                arcade.set_background_color(self.background)
                self.window.show_view(self.game_view)
            else:
                self.tries -= 1
            if self.tries == 0:
                arcade.set_background_color(self.background)
                self.window.show_view(self.game_view)
        if self.button_states[str(self.q3)] == True:
            if self.questionwithans == 2: 
                arcade.set_background_color(self.background)
                self.window.show_view(self.game_view)
            else:
                self.tries -= 1
            if self.tries == 0:
                self.window.show_view(self.game_view)
        if self.button_states[str(self.q4)] == True:
            if self.questionwithans == 3: 
                arcade.set_background_color(self.background) 
                self.window.show_view(self.game_view)
            else:
                self.tries -= 1
            if self.tries == 0:
                arcade.set_background_color(self.background)
                self.window.show_view(self.game_view)

    # <-- adds style to the button --->
    def button(self, attributes):
        self.button_states[attributes["text"]] = False
        color = arcade.color.RED_BROWN
        # check if the mouse is on the button
        if attributes["pos"][0]-attributes["size"][0]/2 < self.mouse_pos[0] < attributes["pos"][0] + attributes["size"][0]/2 :
            if attributes["pos"][1]-attributes["size"][1]/2 < self.mouse_pos[1] < attributes["pos"][1] + attributes["size"][1]/2 :
                self.button_states[attributes["text"]] = True
                # change the color of  the button
                color = arcade.color.BLUE_GRAY

        # draw the rectangle
        arcade.draw_rectangle_filled(attributes["pos"][0], attributes["pos"][1],
                                    attributes["size"][0], attributes["size"][1], color)
        # draw the text
        arcade.draw_text(attributes["text"], attributes["pos"][0], attributes["pos"][1],
                         arcade.color.WHITE, font_size=24, anchor_x="center", anchor_y="center")

    def set_question(self):
        return self.question

    def set_answer(self):
        return self.answer

    def set_first(self):
        return self.first_val

    def set_second(self):
        return self.second_val
