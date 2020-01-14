"""Python file to contain declaration of root screens"""

from kivy.uix.screenmanager import Screen
from api.backend import SimonSays


class StartScreen(Screen):
    """Class for the Start Screen"""
    pass


class GameScreen(Screen):
    """Class for the game screen"""

    move_index = 0
    sequence_len = 0

    def __init__(self, **kwargs):
        self.recv_input = True
        self.api = SimonSays()
        self.show_sequence()
        super(Screen,self).__init__(**kwargs)

    def reset(self):
        self.move_index = 0
        self.sequence_len = 0
        self.api = SimonSays()
        self.show_sequence()

    def check_sequence(self, input):
        if self.api.validate(input, self.move_index):
            self.move_index += 1
            if self.move_index >= self.sequence_len:
                self.show_sequence()
        else:
            print("Wrong!")
            self.reset()
            

    def yellow_press(self):
        if self.recv_input:
            self.check_sequence(1)

    def blue_press(self):
        if self.recv_input:
            self.check_sequence(2)

    def red_press(self):
        if self.recv_input:
            self.check_sequence(3)


    def green_press(self):
        if self.recv_input:
            self.check_sequence(4)


    def show_sequence(self):
        self.recv_input = False
        self.api.add_press()
        self.sequence_len += 1

        # my shitty temporary solution
        print(self.api.moves)

        # ADD THE BUTTON PROMPTS HERE
        # the buttons should flash to indicate that they should be pressed,
        # like in real Simon Says

        self.recv_input = True
        self.move_index = 0