from Code.settings import *
from Code.edit_permission import Permission

from Code.slider import Numbers
from Code.sound import Music, Sound
from Code.window import MenuWindow, SettingsWindow, GameWindow


class Controller:
    def __init__(self) -> None:
        self.volume = Numbers(0, 1, 0.01, round(1 / 16, 3))
        self.volume_sound = {
            'crashes': Numbers(0, 1, 0.01, round(1 / 16, 3)),
            'moves': Numbers(0, 1, 0.01, round(1 / 16, 3)),
            'charge': Numbers(0, 1, 0.01, round(1 / 16, 3))}
        self.music = Music(path=ALL_BACKGROUND_MUSIC, volume=self.volume.value)
        self.sound = Sound(self.volume_sound)
        self.permission = Permission(active=DISPLAY_SIZE)
        #
        self.game = GameWindow(self, DISPLAY_SIZE, MENU_TITLE)
        self.menu = MenuWindow(self, DISPLAY_SIZE, MENU_TITLE)
        self.settings = SettingsWindow(self, DISPLAY_SIZE, MENU_TITLE)
        #
        self.windows = {'menu': self.menu, 'settings': self.settings, 'game': self.game}

    def init(self) -> None:
        del self.menu
        del self.settings
        del self.game
        del self.windows
        self.menu = MenuWindow(self, self.permission.active, MENU_TITLE)
        self.settings = SettingsWindow(self, self.permission.active, MENU_TITLE)
        self.game = GameWindow(self, self.permission.active, MENU_TITLE)
        #
        self.windows = {'menu': self.menu, 'settings': self.settings, 'game': self.game}

    def action_window(self, window_act: str) -> None:
        for window in self.windows.keys():
            if self.windows[window].is_run:
                self.windows[window].join()
                self.windows[window_act].run(last=window)

    def all_off(self) -> None:
        for window in self.windows.keys():
            self.windows[window].join()


if __name__ == '__main__':
    pg.mixer.pre_init(44100, -16, 1, 512)
    pg.init()
    controller = Controller()
    controller.menu.run()
