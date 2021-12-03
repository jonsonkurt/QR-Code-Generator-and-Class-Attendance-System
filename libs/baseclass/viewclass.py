from kivy.lang.builder import Builder
from kivymd.toast.kivytoast import toast
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp

#These line of code will import a class from another python file
from libs.baseclass import user_key, class_key, student_key, scan_state

#These lines of code will import the module for database, camera, QR code reader, excel file generator and time
import sqlite3
from kivymd.uix.button import MDFillRoundFlatButton
from kivy.clock import Clock
from datetime import date
from openpyxl import *
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.utils import asynckivy
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty, StringProperty

from xlsxwriter.workbook import Workbook
from datetime import date

Builder.load_file('./libs/kv/viewclass.kv')

class AddStudent(BoxLayout):
    # this function adds student name
    # adding batch of student names needs to be
    # separated by "/"
    def save_student(self, student_list):
    
        user_id = user_key.user_key[-1]
        class_id = class_key.class_key[-1]
        stud_list = student_list
        final_stud_list = list(stud_list.split("/"))

        if stud_list == "":
            return toast('Please enter a list or name of student(s).')
        else:
            conn = sqlite3.connect("mybase.db")
            cur = conn.cursor()

            find = ("SELECT * FROM classes WHERE class_id=? AND id_user=?")
            cur.execute(find, [(class_id), (user_id)])
            results=cur.fetchall()

            for i in results:
                subject = i[1]
                section_course = i[2]

                cur.execute("CREATE TABLE IF NOT EXISTS students(student_id integer PRIMARY KEY, student_name, section, subject_name, class_id, id_user, status_attendance)")

                for stud in final_stud_list:
                    if len(stud) < 76:
                        find = ("SELECT * FROM students WHERE student_name=? AND class_id=?")
                        cur.execute(find, [(stud), (class_id)])
                        results=cur.fetchall()

                        if len(results) >= 1:
                            toast('Duplicate Name.')
                        else:
                            cur.execute("INSERT INTO students(student_name, section, subject_name, class_id, id_user, status_attendance) VALUES(?,?,?,?,?,?)", (stud, section_course, subject, class_id, user_id, 'Absent'))
                            toast('Student list/name has been saved.')
                    else:
                        toast('Name too long and can\'t be added.')
                conn.commit()
            conn.close()

            self.ids['stud_list'].text = ""


class DeleteStudent(BoxLayout):
    # this function deletes student name
    def delete_student_name(self):

        student_id = student_key.student_key[-1]

        conn = sqlite3.connect("mybase.db")
        cur = conn.cursor()        

        delete = "DELETE FROM students WHERE student_id=?"
        cur.execute(delete, [(student_id)])
        conn.commit()
        conn.close()

        toast('Student deleted.')

class Card2(MDCard):
    
    dialog2 = None
    name = StringProperty('')
    color_index = NumericProperty()
    index = NumericProperty()
    # this function displays delete student dialogue box
    def modify_student(self, key):

        if not self.dialog2:
            self.dialog2 = MDDialog(
                title="Delete this Student?",
                type="custom",
                content_cls=DeleteStudent(),
            )
        self.dialog2.open()
    # this function get student key of student to be deleted
    def add_student_key(self, key):

        student_key.student_key.append(key)

class ViewClassScreen(Screen):

    dialog1 = None
    dialog3 = None
    index = NumericProperty()
    # this function set the attendance status to "Present"
    def ontime_scan(self):

        scan_state.scan_state.append('Present')
    # this function set the attendance status to "Late"
    def late_scan(self):
    
        scan_state.scan_state.append('Late')
    # this function clear the student name widget
    def on_leave(self):
        
        self.ids.student_list.clear_widgets()

    # this function refresh the student names
    def refresh_callback(self, *args):
    
            def refresh_callback(interval):
                
                self.ids.student_list.clear_widgets()
                
                if self.x == 0:
                    self.x, self.y = 1, 1
                else:
                    self.x, self.y = 0, 0
                self.on_enter()
                self.ids.refresh_layout.refresh_done()

            Clock.schedule_once(refresh_callback, 1)

    # this function displays the students' names
    def on_enter(self, *args):

        self.ids.student_list.clear_widgets()

        id_u = user_key.user_key[-1]

        if len(class_key.class_key) >= 1:
            class_id = class_key.class_key[-1]
            conn = sqlite3.connect("mybase.db")
            cur = conn.cursor()

            find = ("SELECT * FROM classes WHERE id_user=? AND class_id=?")
            cur.execute(find, [(id_u), (class_id)])
            data = cur.fetchall()

            self.ids.class_name.text = data[0][1]
            self.ids.section_name.text = data[0][2]

            async def on_enter():

                cur.execute("CREATE TABLE IF NOT EXISTS students(student_id integer PRIMARY KEY, student_name, section, subject_name, class_id, id_user, status_attendance)")
                find = ("SELECT * FROM students WHERE class_id=? AND id_user=? ORDER BY student_name ASC")
                cur.execute(find, [(class_id), (id_u)])
                results = cur.fetchall()

                if len(results) >= 1:
                    for i in results:
                        await asynckivy.sleep(0)
                        stud_name = i[1]

                        if i[6] == 'Absent':
                            color = 1
                        elif i[6] == 'Present':
                            color = 2
                        elif i[6] == 'Late':
                            color = 3

                        studs = Card2(index=i[0], name=f'{stud_name}', color_index=f'{color}')
                        self.ids.student_list.add_widget(studs)
                else:
                    studs = Card2(name='  No available student names as of this moment.', color_index=1)
                    self.ids.student_list.add_widget(studs)

            asynckivy.start(on_enter())

    # this function displays dialog box for adding student
    def add_student_dialog(self):
        
        if not self.dialog1:
            self.dialog1 = MDDialog(
                title="Add Student:",
                type="custom",
                content_cls=AddStudent(),
            )
        self.dialog1.open()

    # this function display dialog box for deleting class
    def delete_class_dialog(self):

        if not self.dialog3:
            self.dialog3 = MDDialog(
                title="Delete this Class?",
                text="This will delete the class and the student names connected to it.",
                buttons=[
                    MDFillRoundFlatButton(
                        text="Delete", theme_text_color='Custom', \
                            md_bg_color='#39aea8', text_color='#FFFFFF', \
                            on_release=lambda x: self.delete_class()
                    ),
                ],
            )
        self.dialog3.open()
    # this function deletes class
    def delete_class(self):
    
        section = class_key.class_key[-1]

        conn = sqlite3.connect("mybase.db")
        cur = conn.cursor()        

        delete1 = "DELETE FROM students WHERE class_id=?"
        delete2 = "DELETE FROM classes WHERE class_id=?"
        cur.execute(delete1, [(section)])
        cur.execute(delete2, [(section)])
        conn.commit()
        conn.close()
        self.dialog_close()
        self.manager.current = 'classes'
        toast('Class deleted.')
    # this function closes the dialog box
    def dialog_close(self, *args):

        self.dialog3.dismiss(force=True)
    # this function exports attendance to excel file
    def export_excel(self):

        conn = sqlite3.connect("mybase.db")
        curr = conn.cursor()
        
        id_u = user_key.user_key[-1]
        section = class_key.class_key[-1]
        curr.execute("SELECT * FROM classes WHERE id_user=? AND class_id=?", (id_u, section))
        
        result = curr.fetchall()
        
        for i in result:

            title = i[1] + ' - ' + i[2] + ' - ' + str(date.today()) + ".xlsx"
            workbook = Workbook(title)
            worksheet = workbook.add_worksheet()

            mysel = curr.execute("""SELECT 
                                student_name, 
                                section,
                                status_attendance 
                                FROM students 
                                WHERE class_id=? AND id_user=? AND subject_name=? ORDER BY student_name ASC""", 
                                (section, id_u, i[1]))

            result2 = curr.fetchall()
            
            worksheet.write('A1', 'Student Name')
            worksheet.write('B1', 'Section')
            worksheet.write('C1', 'Status')
            
            for i, row in enumerate(result2, 1):
                for j, value in enumerate(row):
                    worksheet.write(i, j, value)
            
            workbook.close()

            curr.execute('UPDATE students SET status_attendance=? WHERE class_id=?', ('Absent', section))
            conn.commit()

            toast('Attendance Record Exported.')