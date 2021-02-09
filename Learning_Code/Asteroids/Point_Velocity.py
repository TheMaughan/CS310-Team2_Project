
INPUT_DATA = 0.0
MAX_SPEED = 10

class Point: #- Object Location
    def __init__(self):
        self.x = 0.0
        self.y = 0.0

class Velocity: #- Object progression
    def __init__(self):
        self.max = 10
        self.min = self.max * -1
        self.dx = 0.0
        self.dy = 0.0
    
    #- This sets the accelaration of an object to 0.25 per iteration:
    @property
    def dy(self):
        return self._dy
    @dy.setter
    def dy(self, dy):
        if dy < 0.0:
            self._dy = 0.0
        if dy > self.max:
            self._dy = self.max
        if dy < self.min:
            self._dy = self.min
        else:
            self._dy = dy

    @property
    def dx(self):
        return self._dx
    @dx.setter
    def dx(self, dx):
        if dx < 0.0:
            self._dx = 0.0
        if dx > self.max:
            self._dx = self.max
        if dx < self.min:
            self._dx = self.min
        else:
            self._dx = dx
    


    """
    def display(self):
        print("Moved: {}".format(self.min))


def main():
    thrust = Velocity()
    thrust.dy = 1
    thrust.dy = 1
    thrust.display()
    thrust.dy = -1
    thrust.display()
    thrust.dy = -2
    thrust.display()
    thrust.dy = 39
    thrust.display()

if __name__ == "__main__":
    main()
"""