from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from kivy.properties import ObjectProperty

from gui.root import StartScreen, GameScreen


Builder.load_file("gui/root.kv")


class SimonApp(App):
    """Base class for all activity of the program"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        interface = ObjectProperty(None)

        self.StartScreen = StartScreen()
        self.GameScreen = GameScreen()

        self.screenmanager = ScreenManager()
        self.screenmanager.add_widget(self.StartScreen)
        self.screenmanager.add_widget(self.GameScreen)

    def build(self):
        return self.screenmanager


if __name__ == "__main__":
    SimonApp().run()
