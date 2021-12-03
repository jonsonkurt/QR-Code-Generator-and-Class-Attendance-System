from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.lang.builder import Builder
from libs.baseclass import user_key, class_key

Builder.load_file('./libs/kv/navigation_layout.kv')

class NavLayoutScreen(Screen):
    # this function clears the user_key list and class_key list
    def on_leave(self):
        
        user_key.user_key.clear()
        class_key.class_key.clear()
