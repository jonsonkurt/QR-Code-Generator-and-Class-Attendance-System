import sqlite3
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen
from kivymd.toast.kivytoast import toast

Builder.load_file('./libs/kv/forgot.kv')

class ForgotScreen(Screen):
    #This function will use the text inputs of user to set a new password
    def do_reset(self,reemailtext,pastext,repastext):

        reemail=reemailtext
        paste=pastext
        
        conn=sqlite3.connect("mybase.db")
        cu=conn.cursor()

        find=("SELECT * FROM accounts WHERE emid=? ")
        cu.execute(find,[(reemail)])
        results=cu.fetchall()

        if(len(reemail)>0):
            if results:
                if paste == repastext:
                    if paste == "" and repastext == "":
                        return toast('Enter a new password.')
                    else:
                        cu.execute('UPDATE accounts SET passwd=? WHERE emid=?', (paste, reemail))
                        conn.commit()
                        for element in results:
                            self.manager.transition.direction = "right"
                            self.manager.transition.duration = 0.5
                            self.manager.current = "login"
                            return toast('Your password has been updated. Please login.')
                else:
                    return toast('Please confirm your new password correctly.')
            else:
                return toast('Please enter your registered email.')
        else:
            return toast('Please enter an email address.')

        conn.close()
        self.ids['reemail'].text = ""
        self.ids['pas'].text = ""
        self.ids['repas'].text = ""
