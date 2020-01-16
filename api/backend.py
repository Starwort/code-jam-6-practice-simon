from random import randint
from kivy.core.audio import SoundLoader


class Simon:
    def __init__(self, *args, **kwargs):
        self.moves = []
        self.sounds = {
            'beep1': SoundLoader.load("assets/sound/beep1.wav"),
            'beep2': SoundLoader.load("assets/sound/beep2.wav"),
            'beep3': SoundLoader.load("assets/sound/beep3.wav"),
            'beep4': SoundLoader.load("assets/sound/beep4.wav"),
            'wrong': SoundLoader.load("assets/sound/wrong.wav")
        }

    def validate(self, _input: list, index: int):
        if _input == self.moves[index]:
            self.play_sound('beep' + str(_input))
            return True
        return False

    def add_press(self):
        self.moves.append(randint(1, 4))

    def play_sound(self, sound_name):
        self.sounds[sound_name].play()
