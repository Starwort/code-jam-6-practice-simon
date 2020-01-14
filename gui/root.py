"""Python file to contain declaration of root screens"""

from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivy.properties import ListProperty, NumericProperty
from kivy.animation import Animation


class StartScreen(Screen):
    """Class for the Start Screen"""

    pass


class GameScreen(Screen):
    """Class for the game screen"""

    pass


class SimonButton(Widget):
    """A custom curved shape button for the game"""

    background_color = ListProperty()
    start_angle = NumericProperty(0)
    end_angle = NumericProperty(360)
    radius = NumericProperty()

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            anim = Animation(
                background_color=[*self.background_color[:-1], 0.4], d=0.2
            ) + Animation(background_color=self.background_color, d=0.2)
            anim.start(self)

    def on_size(self, _, value):
        self.radius = min(self.parent.size) / 2.5

    #   Essentially a property but just a setter
    def __setattr__(self, name, value):
        if name == "angle":
            self.start_angle, self.end_angle = value
        super().__setattr__(name, value)
