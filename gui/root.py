"""Python file to contain declaration of root screens"""

from functools import partial
from operator import itemgetter
import json

from kivy.animation import Animation
from kivy.clock import Clock
from kivy.app import App
from kivy.properties import ListProperty, NumericProperty
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup

from api.backend import Simon


class StartScreen(Screen):
    """Class for the Start Screen"""

    pass


class ScoreScreen(Screen):
    """Class for the high scores screen"""

    scores = ListProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        try:
            with open("assets/scores.json") as json_file:
                self.scores = json.load(json_file)
        except FileNotFoundError:
            self.scores = [{"name": "name", "score": "0"}] * 10

    def add_score(self, score, user="user"):
        """Add a score into the highscores"""
        if score > int(min(self.scores, key=itemgetter("score"))["score"]):
            self.scores.pop(-1)
            self.scores.append({"name": "User", "score": str(score)})
            self.save_scores()

    def save_scores(self):
        """Sort and save the scores"""
        self.scores = sorted(self.scores, key=itemgetter("score"), reverse=True)
        with open("assets/scores.json", "w") as json_file:
            json.dump(self.scores, json_file)


class GameScreen(Screen):
    """Class for the game screen"""

    buttons_list = ListProperty()
    score = NumericProperty()
    move_index = NumericProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.recv_input = True
        self.api = Simon()

        self.bind(on_enter=lambda _: self.show_sequence())

    def reset(self):
        self.move_index = self.score = 0
        self.api.moves = []
        Clock.schedule_once(lambda _: self.show_sequence(), 0.5)

    def check_sequence(self, pressed):
        if self.api.validate(pressed, self.move_index):
            self.move_index += 1
            self.score += 10
            if self.move_index >= len(self.api.moves):
                Clock.schedule_once(lambda _: self.show_sequence(), 0.5)
        else:
            self.api.play_sound("wrong")
            if self.score:
                App.get_running_app().ScoreScreen.add_score(self.score)
                LosePopup().open()
            else:
                self.reset()

    def button_press(self, number):
        if self.recv_input:
            self.check_sequence(number)

    def flash_button(self, button, i):
        self.api.play_sound("beep" + str(button.index))
        button.flash()

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
    index = NumericProperty()
    background_color = ListProperty()

    def flash(self):
        anim = Animation(opacity=0.5, d=0.1) + Animation(opacity=1, d=0.1)
        anim.start(self)

    def on_press(self):
        """Block the press if game_screen is not recieving input"""
        game_screen = self.parent.parent.parent

        if not game_screen.recv_input:
            self.state = "normal"
        else:
            self.flash()
            game_screen.button_press(self.index)


class LosePopup(Popup):
    """Popup to display when player loses"""

    pass
