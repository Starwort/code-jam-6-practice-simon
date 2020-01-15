"""Python file to contain declaration of root screens"""

from functools import partial

from kivy.animation import Animation
from kivy.clock import Clock
from kivy.properties import ListProperty
from kivy.uix.screenmanager import Screen

from api.backend import Simon


class StartScreen(Screen):
    """Class for the Start Screen"""

    pass


class GameScreen(Screen):
    """Class for the game screen"""

    buttons_list = ListProperty()
    move_index = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.recv_input = True
        self.api = Simon()

        self.bind(on_enter=lambda _: self.show_sequence())

    def reset(self):
        self.move_index = 0
        self.api.moves = []
        Clock.schedule_once(lambda _: self.show_sequence(), 0.5)

    def check_sequence(self, input):
        if self.api.validate(input, self.move_index):
            self.move_index += 1
            if self.move_index >= len(self.api.moves):
                Clock.schedule_once(lambda _: self.show_sequence(), 0.5)
        else:
            print("Wrong!")
            self.reset()

    def button_press(self, number):
        if self.recv_input:
            self.check_sequence(number)

    def flash_button(self, button, *args):
        print(self.buttons_list.index(button) + 1, self.api.moves)
        anim = Animation(opacity=0.5, d=0.1) + Animation(opacity=1, d=0.1)
        anim.start(button)

    def flash_buttons(self):
        for i, move in enumerate(self.api.moves):
            Clock.schedule_once(
                partial(self.flash_button, self.buttons_list[move - 1]), i
            )

    def show_sequence(self):
        self.recv_input = False
        self.api.add_press()

        self.flash_buttons()

        self.recv_input = True
        self.move_index = 0
