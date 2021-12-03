from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivymd.toast.kivytoast import toast
from kivy.uix.screenmanager import Screen
from libs.baseclass import user_key, class_key
import sqlite3
from kivy.clock import Clock
from openpyxl import *
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.utils import asynckivy
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty, StringProperty

Builder.load_file('./libs/kv/classes.kv')

class AddClass(BoxLayout):

    def count_char(self, word):
        
        return [char for char in word]

    # This function lets user to add new class
    def save_class(self, subject, section):

        user = user_key.user_key[-1]
        subject_name = subject
        course_section = section

        count_subject_name = self.count_char(subject_name)
        count_course_section = self.count_char(course_section)

        if subject_name == "" and course_section == "":
            return toast('Please complete the form.')
        elif len(count_subject_name) >= 24:
            return toast('Subject name too long.')
        elif len(count_course_section) >= 35:
            return toast('Course and Section too long.')
        elif subject_name == "":
            return toast('Enter subject name.')
        elif course_section == "":
            return toast('Enter course and section.')
        else:
            conn = sqlite3.connect("mybase.db")
            cur = conn.cursor()

            cur.execute("CREATE TABLE IF NOT EXISTS classes(class_id integer PRIMARY KEY, subject_name, section_name, id_user)")
            cur.execute("INSERT INTO classes(subject_name, section_name, id_user) VALUES(?,?,?)", (subject_name, course_section, user))

            conn.commit()
            conn.close()

            self.ids['subject_name'].text = ""
            self.ids['section_name'].text = ""

            return toast('Class has been saved.')

# this class displays the information of the classes on screen
class Card1(MDCard):
    
    dialog1 = None

    title = StringProperty('')
    body = StringProperty('')
    index = NumericProperty()

    def save_key(self, key):

        class_key.class_key.append(key)


class ClassScreen(Screen):
    
    dialog1 = None
    dialog2 = None

    index = NumericProperty()
    # this function clears all widget as user leaves the class screen
    def on_leave(self):
    
        self.ids.class_list.clear_widgets()
    # this function allows the class screen to refresh
    # to display newly added class
    def refresh_callback(self, *args):
    
            def refresh_callback(interval):
                
                self.ids.class_list.clear_widgets()
                
                if self.x == 0:
                    self.x, self.y = 1, 1
                else:
                    self.x, self.y = 0, 0
                self.on_enter()
                self.ids.refresh_layout.refresh_done()

            Clock.schedule_once(refresh_callback, 1)

    # this function displays created classes
    def on_enter(self, *args):  

        if len(user_key.user_key) >= 1:
            id_u = user_key.user_key[-1]
            conn = sqlite3.connect("mybase.db")
            cur = conn.cursor()

            async def on_enter():
                
                cur.execute("CREATE TABLE IF NOT EXISTS classes(class_id integer PRIMARY KEY, subject_name, section_name, id_user)")
                find = ("SELECT * FROM classes WHERE id_user=?")
                cur.execute(find, [(id_u)])
                results = cur.fetchall()

                if len(results) >= 1:
                    for i in results:
                        await asynckivy.sleep(0)
                        subject = i[1]
                        section = 'Attendance record for ' + i[2]

                        classes = Card1(index=i[0], title=f'{subject}', body=f'{section}')
                        self.ids.class_list.add_widget(classes)
                else:
                    print('')
            asynckivy.start(on_enter())
        else:
            print('')
    # this function displays required input fields in adding new class
    def add_class_dialog(self):
    
        if not self.dialog1:
            self.dialog1 = MDDialog(
                title="Add a Class:",
                type="custom",
                content_cls=AddClass(),
            )
        self.dialog1.open() 
