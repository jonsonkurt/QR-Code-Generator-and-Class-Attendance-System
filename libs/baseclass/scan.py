from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
import sqlite3
from kivymd.toast.kivytoast import toast
from kivymd.app import MDApp

# these line of code will import a class from another python file
from libs.baseclass import user_key, class_key, scan_state

Builder.load_file('./libs/kv/scan.kv')

scanned_student_names = []

# scan screen of the system
class ScanScreen(Screen):

    qr_text = StringProperty()

    # this function prevent scanning duplicate student QR code
    def save_scanned(self):

        scanned = self.ids.scanned_name.text2

        if scanned in scanned_student_names:
            pass
        else:
            scanned_student_names.append(scanned)

    # this function scans students' QR codes then update
    # the attendance status
    def scan(self):
    
        section = class_key.class_key[-1]
        state = scan_state.scan_state[-1]

        conn = sqlite3.connect("mybase.db")
        cur = conn.cursor()
        
        names = scanned_student_names

        final_names = []

        for items in names:
            a = names.index(items)
            b = len(items)
            items = items[2:(b-1)]
            final_names.append(items)

        final_names.sort()

        final_names2 = []

        for i in final_names:
            cname = i
            find = ("SELECT * FROM students WHERE student_name=? AND class_id=?")
            cur.execute(find,(cname,section))
            results = cur.fetchall()
            if results:
                s = final_names.index(i)
                final_names2.append(final_names[s])
            else:
                continue

        for names in final_names2:
            cur.execute('UPDATE students SET status_attendance=? WHERE class_id=? AND student_name=?', (state, section, names))
            conn.commit()

        scanned_student_names.clear()

        return toast('Scanning complete!')