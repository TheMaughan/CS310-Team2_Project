import random

"""This creates a math problem based off of some randomly generated integers that will be either multiplied, divied, added, or subtracted form each other."""

class Problems():

    def __init__(self):
        self.MATH_LIST = ["*","/","+","-"]
        self.operator = random.randrange(4)
        self.first_val = random.randrange(9)
        self.second_val = random.randrange(9)
        self.third_val = random.randrange(8)
        self.fourth_val = random.randrange(7)
        self.question = ""
        self.answer = 0
        self.question = "{} {} {}".format(self.first_val, self.MATH_LIST[self.operator], self.second_val)
        #I want to take out of init so that this gneral format could still be used but adapted for making levels harder.
        if self.operator == 0:
            self.answer = self.first_val * self.second_val
        elif self.operator == 1:
            while self.second_val == 0:
                self.second_val = random.randrange(9)
            self.answer = self.first_val / self.second_val
        elif self.operator == 2:
            self.answer = self.first_val + self.second_val
        elif self.operator == 3:
            self.answer = self.first_val - self.second_val
        round(self.answer, 2)
        #print("question is: " + str(self.question) + " answer is: " + str(self.answer))

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
