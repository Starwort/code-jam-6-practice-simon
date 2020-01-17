from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager

from gui.root import GameScreen, StartScreen, ScoreScreen

Builder.load_file("gui/root.kv")


class SimonApp(App):
    """Base class for all activity of the program"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.StartScreen = StartScreen()
        self.GameScreen = GameScreen()
        self.ScoreScreen = ScoreScreen()

        self.screenmanager = ScreenManager()
        self.screenmanager.add_widget(self.StartScreen)
        self.screenmanager.add_widget(self.GameScreen)
        self.screenmanager.add_widget(self.ScoreScreen)

    def build(self):
        return self.screenmanager


if __name__ == "__main__":
    SimonApp().run()
