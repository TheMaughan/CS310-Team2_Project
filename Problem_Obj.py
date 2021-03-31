import random

"""This creates a math problem based off of some randomly generated integers that will be either multiplied, divied, added, or subtracted form each other."""

class Problems():

    def __init__(self):
        self.MATH_LIST = ["*","/","+","-"]
        self.operator = random.randrange(4)
        self.first_val = random.randrange(9)
        self.second_val = random.randrange(9)
        #These are extra values that are not necessary, but may be helpful for generating multiple choice answers.
        self.third_val = random.randrange(8)
        self.fourth_val = random.randrange(7)
        self.question = ""
        self.answer = 0
        self.question = "{} {} {}".format(self.first_val, self.MATH_LIST[self.operator], self.second_val)
        #After the initial declaration of variables this will generate the numerical value for the answer.
        if self.operator == 0:
            self.answer = self.first_val * self.second_val
        elif self.operator == 1:
            while self.second_val == 0: # Cannot divide by 0, generate a new random number.
                self.second_val = random.randrange(9)
            self.answer = self.first_val / self.second_val
        elif self.operator == 2:
            self.answer = self.first_val + self.second_val
        elif self.operator == 3:
            self.answer = self.first_val - self.second_val
        self.answer = round(self.answer, 3)

    # Getters for another class to be able to use what was made in here.
    def get_question(self):
        return self.question

    def get_answer(self):
        return self.answer

    def get_first(self):
        return self.first_val

    def get_second(self):
        return self.second_val

    def get_third(self):
        return self.third_val

    def get_fourth(self):
        return self.fourth_val
