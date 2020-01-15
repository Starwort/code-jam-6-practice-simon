"""Python file to contain declaration of root screens"""

from functools import partial

from kivy.animation import Animation
from kivy.clock import Clock
from kivy.properties import ListProperty, NumericProperty
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen

from api.backend import Simon


class StartScreen(Screen):
    """Class for the Start Screen"""

    pass


class GameScreen(Screen):
    """Class for the game screen"""

    buttons_list = ListProperty()
    score = NumericProperty()
    move_index = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.recv_input = True
        self.api = Simon()

        self.bind(on_enter=lambda _: self.show_sequence())

    def reset(self):
        self.move_index = 0
        self.score = 0
        self.api.moves = []
        Clock.schedule_once(lambda _: self.show_sequence(), 0.5)

    def check_sequence(self, pressed):
        if self.api.validate(pressed, self.move_index):
            self.move_index += 1
            self.score += 10
            if self.move_index >= len(self.api.moves):
                Clock.schedule_once(lambda _: self.show_sequence(), 0.5)
        else:
            print("Wrong!")
            self.reset()

    def button_press(self, number):
        if self.recv_input:
            self.check_sequence(number)

    def flash_button(self, button, i):
        print(self.buttons_list.index(button) + 1, self.api.moves)
        anim = Animation(opacity=0.5, d=0.1) + Animation(opacity=1, d=0.1)
        anim.start(button)

        # The time interval is the index of the move so this actually works
        if round(i) + 1 == len(self.api.moves):
            self.recv_input = True

    def flash_buttons(self):
        for i, move in enumerate(self.api.moves):
            Clock.schedule_once(
                partial(self.flash_button, self.buttons_list[move - 1]), i
            )

    def show_sequence(self):
        self.recv_input = False
        self.api.add_press()
        self.flash_buttons()
        self.move_index = 0


class SimonButton(Button):
    def on_press(self):
        """Block the press if game_screen is not recieving input"""
        game_screen = self.parent.parent.parent

        if not game_screen.recv_input:
            self.state = "normal"
