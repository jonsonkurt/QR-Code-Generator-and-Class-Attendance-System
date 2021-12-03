from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.properties import NumericProperty

from libs.baseclass import login, register, forgot, generate, navigation_layout, classes, viewclass, scan, about, help
# this class serves as the main class that runs the system
class MyApp(MDApp):
    title="QR Code-Based Attendance System"

    current_index = NumericProperty()

    def show_screen(self, name):

        self.root.current = 'nav_screen'
        self.root.get_screen('nav_screen').ids.manage.current = name
        return True

    def build(self):

        self.theme_cls.primary_palette = "Teal"
        screen = Builder.load_file("main.kv")
        return screen

if __name__ == '__main__':
    MyApp().run()