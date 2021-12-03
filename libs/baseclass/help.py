from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen
from kivymd.uix.card import MDCard
from kivy.properties import StringProperty

Builder.load_file('./libs/kv/help.kv')

class FAQCard(MDCard):
    
    question = StringProperty('')
    answer = StringProperty('')

class HelpScreen(Screen):
    # this function displays frequently asked questions and
    # its corresponding answers
    def on_enter(self):

        faq_cards = [("How to reset my password?",
                "Select 'Forgot password' from the login screen. You'll be prompted for your previous email address, after which you'll be able to create a new password."),
                ("How to add class?",
                "Click the add button in classes, and you'll be prompted for the subject name, course, and section."),
                ("How to add students?","Click the add button in the upper right corner of the screen from the desired class. You will be asked for the name of the student."),
                ("How to add a list containing student names?",
                "Insert names separated by a forward slash '/' to add a list of students."),
                ("How to scan on-time student?",
                "To begin scanning on-time students, click the green On-Time button from the desired class. After scanning, the names of on-time students will appear in green."),
                ("How to scan late students?",
                "To begin scanning late students, click the red Late button from the desired class. After scanning, the names of late students will appear in red"),
                ("How to record absent students?",
                "For absent students, there is no scan button. Students whose names appear in white, on the other hand, will be declared absent."),
                ("How to delete student name?",
                "Click the student's name from the list in the desired class, a prompt will appear to confirm the action, then select 'Delete'"),
                ("How to delete class?",
                "Click the Delete Class button on the desired class."),
                ("Where can I generate QR Code for students?",
                "The QR Code button may be found at the bottom of the login screen. After entering the student's name, click 'Generate QR Code' to save the QR code.")]

        for card in faq_cards:
            faqs = FAQCard(question=card[0], answer=card[1])
            self.ids.faq.add_widget(faqs)

    # this function clears FAQ widgets
    def on_leave(self):

        self.ids.faq.clear_widgets()