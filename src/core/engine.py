from src.core.actors.player.player import Player
from src.core.render import render as render


class Engine:
    def __init__(self):
        self.renderer = render.CursesRenderer()
        self.player = Player(self)

    def start(self):
        try:
            self.main_loop()
        finally:
            self.renderer.tear_down()

    def main_loop(self):
        while True:
            self.step()

    def step(self):
        self.render()
        self.handle_io()

    def render(self):
        self.renderer.render()

    def handle_io(self):
        self.wait_keypress()

    def wait_keypress(self):
        self.renderer.wait_keypress()
