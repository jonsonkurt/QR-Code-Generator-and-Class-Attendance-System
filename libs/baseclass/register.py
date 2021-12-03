import sqlite3
import re
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen
from kivymd.toast.kivytoast import toast

Builder.load_file('./libs/kv/register.kv')

class RegisterScreen(Screen):
    # this function creates user accounts by getting first name,
    # second name, email, andd password
    def do_register(self, firsttext, lasttext, emailtext, passwordtext, copasstext):
    
        fname = firsttext
        lname = lasttext
        email = emailtext
        password = passwordtext
        conpass = copasstext
        conn = sqlite3.connect("mybase.db")
        cur = conn.cursor()

        cur.execute("CREATE TABLE IF NOT EXISTS accounts(id_num integer PRIMARY KEY, name VARCHAR(30),lastname VARCHAR(30),emid VARCHAR(40),passwd VARCHAR(30),cpasswd VARCHAR(30))")
        find = ("SELECT * FROM accounts WHERE emid=?")
        cur.execute(find,[(email)])

        if(len(fname) > 0 and len(lname) > 0 and len(email) > 0 and len(password) > 0 and len(conpass) > 0):
            if cur.fetchall():
                self.manager.transition.direction = "right"
                self.manager.transition.duration = 0.5
                self.manager.current = "login"
                return toast('User is already registered. Please login')
            else:
                cur.fetchall()

                if fname == "":
                    return toast('Enter your first name.')
                elif lname == "":
                    return toast('Enter your last name.')
                elif not re.match("^[A-Za-z0-9]+@[A-Za-z0-9]+.[A-Za-z0-9]", email):
                        return toast('Enter an email address.')
                elif not re.match("^[A-Za-z0-9]*$", password):
                        return toast('Enter a password.')
                elif not re.match("^[A-Za-z0-9]*$", password):
                        return toast('Please confirm your password.')
                elif (password==conpass):
                        cur.execute("INSERT INTO accounts(name,lastname,emid,passwd,cpasswd) VALUES(?,?,?,?,?)",(fname,lname,email,password,conpass))
                        cur.execute("SELECT * FROM accounts")
                        conn.commit()
                        self.manager.transition.direction = "right"
                        self.manager.transition.duration = 0.5
                        self.manager.current = "login"
                        toast('Registration complete. Please login.')
                else:
                    return toast('Please enter the same password.')
        else:
            return toast('Please enter your details.')

        conn.close()

        self.ids['fname'].text = ""
        self.ids['lname'].text = ""
        self.ids['emailid'].text = ""
        self.ids['passwd'].text = ""
        self.ids['cpass'].text = ""