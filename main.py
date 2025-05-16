from kivy.config import Config
Config.set('graphics', 'fullscreen', 'auto')   # or '1' on Windows/Linux

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

# pull the individual screen classes in from the package-level exports
from screens import (
    SplashScreen, FileSelectScreen, LiveInputScreen,
    ConvertedSelectScreen, ConvertedStaffScreen,
    StaffScreen, FisherPriceDisplayScreen,
)


class FisherPriceApp(App):
    def build(self):
        sm = ScreenManager()

        # add every screen instance once
        sm.add_widget(SplashScreen(name="splash"))
        sm.add_widget(FileSelectScreen(name="file_select"))
        sm.add_widget(LiveInputScreen(name="live"))
        sm.add_widget(ConvertedSelectScreen(name="converted"))
        sm.add_widget(ConvertedStaffScreen(name="converted_staff"))
        sm.add_widget(StaffScreen(name="staff"))
        sm.add_widget(FisherPriceDisplayScreen(name="fisher_roller"))

        sm.current = "splash"          # start on the splash screen
        return sm


if __name__ == "__main__":
    FisherPriceApp().run()
