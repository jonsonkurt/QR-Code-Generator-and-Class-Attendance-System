#QR Code-Based Attendance System
#Developed by Gatdula, Jonson and Pacomio

#-------------------------------------------------
#Install Kivy, OpenCV, pyzbar, pandas, xlsxwriter
#-------------------------------------------------


#These line of codes will import the necessary modules for Kivy GUI
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.uix.vkeyboard import VKeyboard 

#These line of codes will import the module for database, set of strings, camera, QR code reader, excel file generator and time
import sqlite3
import re
import cv2
import pyzbar.pyzbar as pyzbar
import time
import smtplib
import matplotlib.pyplot as plt
import pandas as pd 
import xlsxwriter

#These line of codes will import the module for date, cvs reader and email
from datetime import date
from pandas import DataFrame, read_csv
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.utils import formatdate
from email import encoders

#These line of codes contain the Kivy Language for Box Layout, Grid Layout, Screen Manager, Buttons. It can be seperated into a new file with file extension .kv
Builder.load_string("""

#--------------------------------------------------------------------------------------------------------------
#This first screen is for starting page of the application wherein you can sign in, sign up or forgot password
#--------------------------------------------------------------------------------------------------------------

<ScreenTwo>:
    name: "start"
    canvas.before:
        Rectangle:
            pos: self.pos
            source:'login_bg.jpg'
            size: self.size
    GridLayout:
        rows:2
        BoxLayout:
            size_hint_y: None
            height:200
            spacing:5
            padding:5
            
            canvas:
                Color:
                    rgba:1,1,1,1
                Rectangle:
                    pos:self.pos
                    size:self.size
                    source:"nothing.png"
   
    BoxLayout:
        id:login_layout
        orientation:"vertical"
        size_hint:0.9,0.6
        padding:root.width*.02,root.height*.02
        spacing:min(root.width,root.height)*.02
        
        pos_hint:{"center_x":0.5,"center_y":0.5}
        canvas:
            
            Rectangle:
                size:self.size
                
                pos:self.pos
                
        Image:
            source:'Logo.png'
            pos_hint: {'left':1, 'top':1}
            size:self.size


        BoxLayout:
            orientation:"horizontal"
            pos_hint:{"center_x":0.5,"center_y":0.5}
            Button:
                text:"SIGN IN"
                background_color: (255,255,255,1)
                color: 0, 0, 0, 1
                halign: 'left'
                valign:'center'
               

            Button:
                text:"SIGN UP"
                background_color: (255,255,255,1)
                color: 0, 0, 0, 1
                
                on_press:
                    root.manager.transition.direction="left"
                    root.manager.transition.duration=0
                    root.manager.current="ScreenThree"
                        
        BoxLayout:
            orientation:"vertical"
            
                
            TextInput:
                pos_hint:{"center_x":0.5,"center_y":0.5}
                canvas.before:
    
                    Line:
                        points: self.x + 20, self.y, self.x + self.width - 20, self.y
                        width: 1
                hint_text:"Email"
                background_color: 0,0,0,0  
                
                size_hint:(0.7,0.3)
                
                id:username
                multiline:False

        BoxLayout:
            orientation:"vertical"
            pos_hint:{"center_x":0.5,"center_y":0.5}
            
                
            TextInput:
                pos_hint:{"center_x":0.5,"center_y":0.5}
                hint_text:"Password"
                canvas.before:
    
                    Line:
                        points: self.x + 20, self.y, self.x + self.width - 20, self.y
                        width: 1
                
                background_color: 0,0,0,0  
                
                size_hint:(0.7,0.3)
                id:password
                
                
                multiline:False
                password:True
                
                
        BoxLayout:
            orientation:"vertical"
            pos_hint:{"center_x":0.5,"center_y":0.5}
            padding:3,3
            Button:
                text:"LOGIN"
                pos_hint:{"center_x":0.5,"center_y":0.5}
                background_color: .33, 0, 0, 1
                padding:5,5
                size_hint:(0.2,0.4)
                on_press:root.do_login(username.text,password.text)
                
            
            Button:
                pos_hint:{"center_x":0.5,"center_y":0.5}
                text:"Forgot Password?"
                padding:5,5
                color:0,0,0,1
                background_color: (255,255,255,1)
                on_press:
                    root.manager.transition.direction="left"
                    root.manager.transition.duration=0
                    root.manager.current="ScreenOne"

#--------------------------------------------------------------------------------------------------------------
#This second screen is for forgot password where in you will input your email on sign up and set a new password
#--------------------------------------------------------------------------------------------------------------
                   
<ScreenOne>:
    canvas.before:
        Rectangle:
            pos: self.pos
            source:'forgot_bg.jpg'
            size: self.size

    GridLayout:
        rows:2
        
        BoxLayout:
            size_hint_y:None
            height:100
            spacing:20
            padding:10
            pos_hint:{"center_x":0.5,"center_y":0.5}
            canvas:
                Color:
                    rgba:1,1,1,1
                Rectangle:
                    pos:self.pos
                    size:self.size
                    source:"nothing.png"
            Button:
                
                background_color: 1,0,0,1
                size_hint_x:None
                
                width:150
                text:"[b] GO BACK [/b]"
                markup:True
                on_press:
                    root.manager.transition.direction="left"
                    root.manager.transition.duration=0
                    root.manager.current="ScreenTwo"
                    
    BoxLayout:
        id:login_layout
        orientation:"vertical"
        size_hint:0.9,0.6
        padding:root.width*.02,root.height*.02
        spacing:min(root.width,root.height)*.02
        
        pos_hint:{"center_x":0.5,"center_y":0.5}
        canvas:
            
            Rectangle:
                size:self.size
                
                pos:self.pos
                
        
        Label:
            text:"Reset your password using your email"
            pos_hint:{"center_x":0.5,"center_y":0.5}
            color:0,0,0,1
            size_hint:(0.3,0.2)
        
        TextInput:
            id:reemail
            hint_text:"Email Address"
            pos_hint:{"center_x":0.5,"center_y":0.5}
            canvas.before:
                Line:
                    points: self.x + 20, self.y, self.x + self.width - 20, self.y
                    width: 1
                
            background_color: 0,0,0,0  
            multiline:False
            size_hint:(0.6,0.15)
        TextInput:
            id:pas
            hint_text:"Password"
            pos_hint:{"center_x":0.5,"center_y":0.5}
            canvas.before:
                Line:
                    points: self.x + 20, self.y, self.x + self.width - 20, self.y
                    width: 1
            password:True    
            background_color: 0,0,0,0  
            multiline:False
            size_hint:(0.6,0.15)

        TextInput:
            id:repas
            hint_text:"Re-enter Password"
            pos_hint:{"center_x":0.5,"center_y":0.5}
            canvas.before:
                Line:
                    points: self.x + 20, self.y, self.x + self.width - 20, self.y
                    width: 1
            password:True     
            background_color: 0,0,0,0  
            multiline:False
            size_hint:(0.6,0.15)
        Button:
            text:"RESET PASSWORD"
            pos_hint:{"center_x":0.5,"center_y":0.5}
            background_color: .33, 0, 0, 1
            size_hint:(0.8,0.1)
            on_press:
                root.do_reset(reemail.text,pas.text,repas.text)
                
#--------------------------------------------------------------------------------------------------------------
#This third screen is for sign up page where you will enter your details to create an account for the app
#--------------------------------------------------------------------------------------------------------------

<ScreenThree>:
    canvas.before:
        Rectangle:
            pos: self.pos
            source:'signup_bg.jpg'
            size: self.size

    GridLayout:
        rows:2
        
        BoxLayout:
            size_hint_y:None
            height:100
            spacing:10
            padding:10
            pos_hint:{"center_x":0.5,"center_y":0.5}
            canvas:
                Color:
                    rgba:1,1,1,1
                Rectangle:
                    pos:self.pos
                    size:self.size
                    source:"nothing.png"
                    
            Button:
                
                background_color: 1,0,0,1
                size_hint_x:None
                width:150
                text:"[b] BACK [/b]"
                markup:True
                
                on_press:
                    root.manager.transition.direction="left"
                    root.manager.transition.duration=0
                    root.manager.current="ScreenTwo"
    BoxLayout:
        orientation:'vertical'
        padding:root.width*.02,root.height*.02
        
        
        
        size_hint:0.9,0.7
        pos_hint:{"center_x":0.5,"center_y":0.5}
        canvas:
            Rectangle:
                size:self.size
                pos:self.pos        
                
        Label:
            text:"[b][size=40]PROFESSOR'S INFORMATION[/size][/b]"
            size_hint:1,None
            color: (138,43,226)
            markup:'True'

        BoxLayout:
            orientation:"vertical"
            pos_hint:{"center_x":0.5,"center_y":0.5}
            
            TextInput:
                pos_hint:{"center_x":0.5,"center_y":0.5}
                hint_text:"First Name"
                color:0,0,0,1
                background_color: 0,0,0,0 
                canvas.before:
    
                    Line:
                        points: self.x + 20, self.y, self.x + self.width - 20, self.y
                        width: 1
                id:fname
                size_hint:(0.7,0.3)
                multiline:False
                
        BoxLayout:
            orientation:"vertical"
            pos_hint:{"center_x":0.5,"center_y":0.5}
            
            TextInput:
                hint_text:"Last Name"
                text_size:self.size
                id:lname
                canvas.before:
    
                    Line:
                        points: self.x + 20, self.y, self.x + self.width - 20, self.y
                        width: 1
                background_color: 0,0,0,0 
                pos_hint:{"center_x":0.5,"center_y":0.5}
                size_hint:(0.7,0.3)
                multiline:False
                
        BoxLayout:
            orientation:"vertical"
            pos_hint:{"center_x":0.5,"center_y":0.5}
            
            TextInput:
                hint_text:"sample.email@gmail.com"
                text_size:self.size
                id:emailid
                canvas.before:
    
                    Line:
                        points: self.x + 20, self.y, self.x + self.width - 20, self.y
                        width: 1
                background_color: 0,0,0,0 
                pos_hint:{"center_x":0.5,"center_y":0.5}
                size_hint:(0.7,0.3)
                multiline:False
        

        BoxLayout:
            orientation:"vertical"
            pos_hint:{"center_x":0.5,"center_y":0.5}
            
            TextInput:
                hint_text:"Password"
                text_size:self.size
                id:passwd
                canvas.before:
    
                    Line:
                        points: self.x + 20, self.y, self.x + self.width - 20, self.y
                        width: 1
                background_color: 0,0,0,0 
                pos_hint:{"center_x":0.5,"center_y":0.5}
                size_hint:(0.7,0.3)
                multiline:False
                password:True
                
        BoxLayout:
            orientation:"vertical"
            pos_hint:{"center_x":0.5,"center_y":0.5}
            
            TextInput:
                hint_text:"Confirm Password"
                background_color: 0,0,0,0 
                canvas.before:
    
                    Line:
                        points: self.x + 20, self.y, self.x + self.width - 20, self.y
                        width: 1
                password:True
                size_hint:(0.7,0.3)
                pos_hint:{"center_x":0.5,"center_y":0.5}
                
                id:cpass
                multiline:False
                
        BoxLayout:
            orientation:'horizontal'
            padding:5,5
            spacing:10,10
            size_hint:(0.7,0.3)
            pos_hint:{"center_x":0.5,"center_y":0.5}
            
            Button:
                id:btn
                icon:'face'
                text:"CONFIRM"
                pos_hint:{"center_x":0.5,"center_y":0.5}
                background_color: .33, 0, 0, 1
                padding:5,5
                size_hint:(0.7,1)
                on_press:
                    root.do_register(fname.text,lname.text,emailid.text,passwd.text,cpass.text)
                    
#--------------------------------------------------------------------------------------------------------------
#This fourth screen is the main screen of this application. It contains different classes handled by the instructor
#--------------------------------------------------------------------------------------------------------------
                    
<ScreenFour>:
    name: "start"
    canvas.before:
        Rectangle:
            pos: self.pos
            source:'add_bg.jpg'
            size: self.size
                
    GridLayout:
        rows:3
        BoxLayout:
            size_hint_y: None
            height:100
            spacing:5
            padding:5
            
            canvas:
                Color:
                    rgba:1,1,1,1
                Rectangle:
                    pos:self.pos
                    size:self.size
                    source:"nothing.png"
                    
            Button:
                
                background_color: 0,0.29,0.42,0
                size_hint_x:None
                width:50
                text:"[b] = [/b]"
                markup:True
                
                on_press:
                    root.manager.transition.direction="right"
                    root.manager.transition.duration=1
                    root.manager.current="ScreenFive"
                    
      

        GridLayout:
            rows: 5         

            BoxLayout:           
                Button:
                    id:btn
                    icon:'face'
                    text:"Class 1"
                    pos_hint:{"center_x":0.5,"center_y":0.5}
                    background_color: .33, 0, 0, 1
                    padding:5,5
                    size_hint:(0.5,0.8)
                    on_press:
                        root.manager.transition.direction="left"
                        root.manager.transition.duration=0
                        root.manager.current="Class1"                                

            BoxLayout:
                Button:
                    id:btn
                    icon:'face'
                    text:"Class 2"
                    pos_hint:{"center_x":0.5,"center_y":0.5}
                    background_color: .33, 0, 0, 1
                    padding:5,5
                    size_hint:(0.5,0.8)
                    on_press:
                        root.manager.transition.direction="left"
                        root.manager.transition.duration=0
                        root.manager.current="Class2"        

            BoxLayout:                    
                Button:
                    id:btn
                    icon:'face'
                    text:"Class 3"
                    pos_hint:{"center_x":0.5,"center_y":0.5}
                    background_color: .33, 0, 0, 1
                    padding:5,5
                    size_hint:(0.5,0.8)
                    on_press:
                        root.manager.transition.direction="left"
                        root.manager.transition.duration=0
                        root.manager.current="Class3"        

            BoxLayout:
                Button:
                    id:btn
                    icon:'face'
                    text:"Class 4"
                    pos_hint:{"center_x":0.5,"center_y":0.5}
                    background_color: .33, 0, 0, 1
                    padding:5,5
                    size_hint:(0.5,0.8)
                    on_press:
                        root.manager.transition.direction="left"
                        root.manager.transition.duration=0
                        root.manager.current="Class4"        

            BoxLayout: 
                Button:
                    id:btn
                    icon:'face'
                    text:"Class 5"
                    pos_hint:{"center_x":0.5,"center_y":0.5}
                    background_color: .33, 0, 0, 1
                    padding:5,5
                    size_hint:(0.5,0.8)
                    on_press:
                        root.manager.transition.direction="left"
                        root.manager.transition.duration=0
                        root.manager.current="Class5"        
                        
#--------------------------------------------------------------------------------------------------------------
#This fifth screen is for the Help and About the Developers section of the appllication
#--------------------------------------------------------------------------------------------------------------
                
<ScreenFive>:
    name: "start"
    canvas.before:
        Rectangle:
            pos: self.pos
            source:'background.jpg'
            size: self.size
    GridLayout:
        rows:3
        BoxLayout:
            size_hint_y: None
            height:100
            spacing:5
            padding:5
            
                    
            Button:
                pos_hint:{"center_x":0.10,"center_y":0.10}
                background_color: 1,0.94,0.83,0.6
                size_hint_x: 1
                width:10
                text:"[b] Back to Home [/b]"
                markup:True
                
                on_press:
                    root.manager.transition.direction="left"
                    root.manager.transition.duration=0
                    root.manager.current="ScreenFour"
                    
        BoxLayout:
            size_hint_y: None
            height:100
            spacing:5
            padding:5
            
                    
            Button:
                pos_hint:{"center_x":0.10,"center_y":0.10}
                background_color: 1,0.94,0.83,0.6
                size_hint_x: 1
                width:10
                text:"[b] Help [/b]"
                markup:True
                
                on_press:
                    root.manager.transition.direction="left"
                    root.manager.transition.duration=0
                    root.manager.current="Help"
                    
        BoxLayout:
            size_hint_y: None
            height:100
            spacing:5
            padding:5
            
                    
            Button:
                pos_hint:{"center_x":0.10,"center_y":0.10}
                background_color: 1,0.94,0.83,0.6
                size_hint_x: 1
                width:10
                text:"[b] About the Developers [/b]"
                markup:True
                
                on_press:
                    root.manager.transition.direction="left"
                    root.manager.transition.duration=0
                    root.manager.current="Developers"         
                    
#--------------------------------------------------------------------------------------------------------------
#This screen is the Help section that displays the instructions or guide on how to use this application
#--------------------------------------------------------------------------------------------------------------

<Help>:
    name: "start"
    canvas.before:
        Rectangle:
            pos: self.pos
            source:'help_bg.jpg'
            size: self.size
    
    GridLayout:
        rows:2
        BoxLayout:
            size_hint_y: None
            height:100
            spacing:5
            padding:5
            
            canvas:
                Color:
                    rgba:1,1,1,1
                Rectangle:
                    pos:self.pos
                    size:self.size
                    source:"nothing.png"
                    
            Button:
                
                background_color: 0,0.29,0.42,0
                size_hint_x:None
                width:50
                text:"[b] < [/b]"
                markup:True
                
                on_press:
                    root.manager.transition.direction="right"
                    root.manager.transition.duration=0
                    root.manager.current="ScreenFive"
                    
#--------------------------------------------------------------------------------------------------------------
#This section is the About the Developers section. It displays the developers information and pictures
#--------------------------------------------------------------------------------------------------------------

<Developers>:
    name: "start"
    canvas.before:
        Rectangle:
            pos: self.pos
            source:'developers.jpg'
            size: self.size
    GridLayout:
        rows:2
        BoxLayout:
            size_hint_y: None
            height:100
            spacing:5
            padding:5
            
            canvas:
                Color:
                    rgba:1,1,1,1
                Rectangle:
                    pos:self.pos
                    size:self.size
                    source:"nothing.png"
                    
            Button:
                
                background_color: 0,0.29,0.42,0
                size_hint_x:None
                width:50
                text:"[b] < [/b]"
                markup:True
                
                on_press:
                    root.manager.transition.direction="right"
                    root.manager.transition.duration=0
                    root.manager.current="ScreenFive"
                    

#--------------------------------------------------------------------------------------------------------------
#These are the line of codes for each class of the user/instructor
#Each of the class has its own text input for the section, class list, QR Code Scanner, excel generator and email
#--------------------------------------------------------------------------------------------------------------
   
<Class1>
    name: "start"
    canvas.before:
        Rectangle:
            pos: self.pos
            source:'background.jpg'
            size: self.size
    GridLayout:
        rows:2
        BoxLayout:
            size_hint_y: None
            height:100
            spacing:5
            padding:5
            
            canvas:
                Color:
                    rgba:1,1,1,1
                Rectangle:
                    pos:self.pos
                    size:self.size
                    source:"b.jpg"
                    
            Button:
                
                background_color: 0,0.29,0.42,0
                size_hint_x:None
                width:50
                text:"[b] < [/b]"
                markup:True
                
                on_press:
                    root.manager.transition.direction="right"
                    root.manager.transition.duration=0
                    root.manager.current="ScreenFour"
                    
            TextInput:
                pos_hint:{"center_x":0.5,"center_y":0.5}
                hint_text:"Input Class Section"
                hint_text_color:1,1,1,1
                background_color:0,0,0,0
                foreground_color: 1,1,1,1
                size_hint:(.3,None)
                height:55

                canvas.before:
    
                    Line:
                        points: self.x, self.y, self.x + self.width, self.y
                        width: 0.1
                id:class1
                multiline:False 
            
        GridLayout:
            rows: 8
            
            BoxLayout:
                orientation:"vertical"
                pos_hint:{"center_x":0.5,"center_y":0.5}
                padding:3,3
                
                Label:
                    text: ""          
            
            BoxLayout:
                orientation:"vertical"
                pos_hint:{"center_x":0.5,"center_y":0.5}
                padding:3,3
                
                TextInput:
                    pos_hint:{"center_x":0.5,"center_y":0.5}
                    hint_text:"Enter Student Names"
                    hint_text_color:0,0,0,1
                    background_color:1,1,1,1
                    foreground_color: 0,0,0,1
                    size_hint:(.5,.8)
                    height:50

                    id:names
                    multiline:True                    
                
                Button:
                    text:"IMPORT RECORD OF THE CLASS"
                    pos_hint:{"center_x":0.5,"center_y":0.5}
                    background_color: .33, 0, 0, 1
                    padding:5,5
                    size_hint:(0.7,1)
                    
                    on_press:
                        root.CreateClassList(names)

            BoxLayout:
                orientation:"vertical"
                pos_hint:{"center_x":0.5,"center_y":0.5}
                padding:3,3
                
                Label:
                    text: ""                      
                          
                

            
            BoxLayout:
                orientation:"horizontal"
                pos_hint:{"center_x":0.5,"center_y":0.5}
                padding:3,3
                    
                    
                Button:
                    text:"START SCANNING"
                    pos_hint:{"center_x":0.5,"center_y":0.5}
                    padding:5,5
                    size_hint:(0.2,0.8)
                    border: (0,0,0,0)    
                    
                    on_press:
                        root.VKeyboard()                        
                        root.QRScanner()


            BoxLayout:
                orientation:"vertical"
                pos_hint:{"center_x":0.5,"center_y":0.5}
                padding:3,3
                
                Label:
                    text: ""          
            
            BoxLayout:
                orientation:"vertical"
                pos_hint:{"center_x":0.5,"center_y":0.5}
                padding:3,3
                
                TextInput:
                    pos_hint:{"center_x":0.5,"center_y":0.5}
                    hint_text:"INPUT EMAIL BEFORE EXPORT"
                    hint_text_color:0,0,0,1
                    background_color:1,1,1,1
                    foreground_color: 0,0,0,1
                    size_hint:(.5,.8)
                    height:50

                    id:email
                    multiline:False                     
                
                Button:
                    text:"EXPORT ATTENDANCE TO EMAIL"
                    pos_hint:{"center_x":0.5,"center_y":0.5}
                    background_color: .33, 0, 0, 1
                    padding:5,5
                    size_hint:(0.7,1)
                    
                    on_press:
                        root.email_file(email)                   

            BoxLayout:
                orientation:"vertical"
                pos_hint:{"center_x":0.5,"center_y":0.5}
                padding:3,3
                
                Label:
                    text: ""      


<Class2>
    name: "start"
    canvas.before:
        Rectangle:
            pos: self.pos
            source:'background.jpg'
            size: self.size
    GridLayout:
        rows:2
        BoxLayout:
            size_hint_y: None
            height:100
            spacing:5
            padding:5
            
            canvas:
                Color:
                    rgba:1,1,1,1
                Rectangle:
                    pos:self.pos
                    size:self.size
                    source:"b.jpg"
                    
            Button:
                
                background_color: 0,0.29,0.42,0
                size_hint_x:None
                width:50
                text:"[b] < [/b]"
                markup:True
                
                on_press:
                    root.manager.transition.direction="right"
                    root.manager.transition.duration=0
                    root.manager.current="ScreenFour"
                    
            TextInput:
                pos_hint:{"center_x":0.5,"center_y":0.5}
                hint_text:"Input Class Section"
                hint_text_color:1,1,1,1
                background_color:0,0,0,0
                foreground_color: 1,1,1,1
                size_hint:(.3,None)
                height:55

                canvas.before:
    
                    Line:
                        points: self.x, self.y, self.x + self.width, self.y
                        width: 0.1
                id:class1
                multiline:False 
            
        GridLayout:
            rows: 8
            
            BoxLayout:
                orientation:"vertical"
                pos_hint:{"center_x":0.5,"center_y":0.5}
                padding:3,3
                
                Label:
                    text: ""          
            
            BoxLayout:
                orientation:"vertical"
                pos_hint:{"center_x":0.5,"center_y":0.5}
                padding:3,3
                
                TextInput:
                    pos_hint:{"center_x":0.5,"center_y":0.5}
                    hint_text:"Enter Student Names"
                    hint_text_color:0,0,0,1
                    background_color:1,1,1,1
                    foreground_color: 0,0,0,1
                    size_hint:(.5,.8)
                    height:50

                    id:names
                    multiline:True                    
                
                Button:
                    text:"IMPORT RECORD OF THE CLASS"
                    pos_hint:{"center_x":0.5,"center_y":0.5}
                    background_color: .33, 0, 0, 1
                    padding:5,5
                    size_hint:(0.7,1)
                    
                    on_press:
                        root.CreateClassList(names)

            BoxLayout:
                orientation:"vertical"
                pos_hint:{"center_x":0.5,"center_y":0.5}
                padding:3,3
                
                Label:
                    text: ""                      
                          
                

            
            BoxLayout:
                orientation:"horizontal"
                pos_hint:{"center_x":0.5,"center_y":0.5}
                padding:3,3
                    
                    
                Button:
                    text:"START SCANNING"
                    pos_hint:{"center_x":0.5,"center_y":0.5}
                    padding:5,5
                    size_hint:(0.2,0.8)
                    border: (0,0,0,0)    
                    
                    on_press:
                        root.VKeyboard()                        
                        root.QRScanner()


            BoxLayout:
                orientation:"vertical"
                pos_hint:{"center_x":0.5,"center_y":0.5}
                padding:3,3
                
                Label:
                    text: ""          
            
            BoxLayout:
                orientation:"vertical"
                pos_hint:{"center_x":0.5,"center_y":0.5}
                padding:3,3
                
                TextInput:
                    pos_hint:{"center_x":0.5,"center_y":0.5}
                    hint_text:"INPUT EMAIL BEFORE EXPORT"
                    hint_text_color:0,0,0,1
                    background_color:1,1,1,1
                    foreground_color: 0,0,0,1
                    size_hint:(.5,.8)
                    height:50

                    id:email
                    multiline:False                     
                
                Button:
                    text:"EXPORT ATTENDANCE TO EMAIL"
                    pos_hint:{"center_x":0.5,"center_y":0.5}
                    background_color: .33, 0, 0, 1
                    padding:5,5
                    size_hint:(0.7,1)
                    
                    on_press:
                        root.email_file(email)                   

            BoxLayout:
                orientation:"vertical"
                pos_hint:{"center_x":0.5,"center_y":0.5}
                padding:3,3
                
                Label:
                    text: ""   


<Class3>
    name: "start"
    canvas.before:
        Rectangle:
            pos: self.pos
            source:'background.jpg'
            size: self.size
    GridLayout:
        rows:2
        BoxLayout:
            size_hint_y: None
            height:100
            spacing:5
            padding:5
            
            canvas:
                Color:
                    rgba:1,1,1,1
                Rectangle:
                    pos:self.pos
                    size:self.size
                    source:"b.jpg"
                    
            Button:
                
                background_color: 0,0.29,0.42,0
                size_hint_x:None
                width:50
                text:"[b] < [/b]"
                markup:True
                
                on_press:
                    root.manager.transition.direction="right"
                    root.manager.transition.duration=0
                    root.manager.current="ScreenFour"
                    
            TextInput:
                pos_hint:{"center_x":0.5,"center_y":0.5}
                hint_text:"Input Class Section"
                hint_text_color:1,1,1,1
                background_color:0,0,0,0
                foreground_color: 1,1,1,1
                size_hint:(.3,None)
                height:55

                canvas.before:
    
                    Line:
                        points: self.x, self.y, self.x + self.width, self.y
                        width: 0.1
                id:class1
                multiline:False 
            
        GridLayout:
            rows: 8
            
            BoxLayout:
                orientation:"vertical"
                pos_hint:{"center_x":0.5,"center_y":0.5}
                padding:3,3
                
                Label:
                    text: ""          
            
            BoxLayout:
                orientation:"vertical"
                pos_hint:{"center_x":0.5,"center_y":0.5}
                padding:3,3
                
                TextInput:
                    pos_hint:{"center_x":0.5,"center_y":0.5}
                    hint_text:"Enter Student Names"
                    hint_text_color:0,0,0,1
                    background_color:1,1,1,1
                    foreground_color: 0,0,0,1
                    size_hint:(.5,.8)
                    height:50

                    id:names
                    multiline:True                    
                
                Button:
                    text:"IMPORT RECORD OF THE CLASS"
                    pos_hint:{"center_x":0.5,"center_y":0.5}
                    background_color: .33, 0, 0, 1
                    padding:5,5
                    size_hint:(0.7,1)
                    
                    on_press:
                        root.CreateClassList(names)

            BoxLayout:
                orientation:"vertical"
                pos_hint:{"center_x":0.5,"center_y":0.5}
                padding:3,3
                
                Label:
                    text: ""                      
                          
                

            
            BoxLayout:
                orientation:"horizontal"
                pos_hint:{"center_x":0.5,"center_y":0.5}
                padding:3,3
                    
                    
                Button:
                    text:"START SCANNING"
                    pos_hint:{"center_x":0.5,"center_y":0.5}
                    padding:5,5
                    size_hint:(0.2,0.8)
                    border: (0,0,0,0)    
                    
                    on_press:
                        root.VKeyboard()                        
                        root.QRScanner()


            BoxLayout:
                orientation:"vertical"
                pos_hint:{"center_x":0.5,"center_y":0.5}
                padding:3,3
                
                Label:
                    text: ""          
            
            BoxLayout:
                orientation:"vertical"
                pos_hint:{"center_x":0.5,"center_y":0.5}
                padding:3,3
                
                TextInput:
                    pos_hint:{"center_x":0.5,"center_y":0.5}
                    hint_text:"INPUT EMAIL BEFORE EXPORT"
                    hint_text_color:0,0,0,1
                    background_color:1,1,1,1
                    foreground_color: 0,0,0,1
                    size_hint:(.5,.8)
                    height:50

                    id:email
                    multiline:False                     
                
                Button:
                    text:"EXPORT ATTENDANCE TO EMAIL"
                    pos_hint:{"center_x":0.5,"center_y":0.5}
                    background_color: .33, 0, 0, 1
                    padding:5,5
                    size_hint:(0.7,1)
                    
                    on_press:
                        root.email_file(email)                   

            BoxLayout:
                orientation:"vertical"
                pos_hint:{"center_x":0.5,"center_y":0.5}
                padding:3,3
                
                Label:
                    text: ""   


<Class4>
    name: "start"
    canvas.before:
        Rectangle:
            pos: self.pos
            source:'background.jpg'
            size: self.size
    GridLayout:
        rows:2
        BoxLayout:
            size_hint_y: None
            height:100
            spacing:5
            padding:5
            
            canvas:
                Color:
                    rgba:1,1,1,1
                Rectangle:
                    pos:self.pos
                    size:self.size
                    source:"b.jpg"
                    
            Button:
                
                background_color: 0,0.29,0.42,0
                size_hint_x:None
                width:50
                text:"[b] < [/b]"
                markup:True
                
                on_press:
                    root.manager.transition.direction="right"
                    root.manager.transition.duration=0
                    root.manager.current="ScreenFour"
                    
            TextInput:
                pos_hint:{"center_x":0.5,"center_y":0.5}
                hint_text:"Input Class Section"
                hint_text_color:1,1,1,1
                background_color:0,0,0,0
                foreground_color: 1,1,1,1
                size_hint:(.3,None)
                height:55

                canvas.before:
    
                    Line:
                        points: self.x, self.y, self.x + self.width, self.y
                        width: 0.1
                id:class1
                multiline:False 
            
        GridLayout:
            rows: 8
            
            BoxLayout:
                orientation:"vertical"
                pos_hint:{"center_x":0.5,"center_y":0.5}
                padding:3,3
                
                Label:
                    text: ""          
            
            BoxLayout:
                orientation:"vertical"
                pos_hint:{"center_x":0.5,"center_y":0.5}
                padding:3,3
                
                TextInput:
                    pos_hint:{"center_x":0.5,"center_y":0.5}
                    hint_text:"Enter Student Names"
                    hint_text_color:0,0,0,1
                    background_color:1,1,1,1
                    foreground_color: 0,0,0,1
                    size_hint:(.5,.8)
                    height:50

                    id:names
                    multiline:True                    
                
                Button:
                    text:"IMPORT RECORD OF THE CLASS"
                    pos_hint:{"center_x":0.5,"center_y":0.5}
                    background_color: .33, 0, 0, 1
                    padding:5,5
                    size_hint:(0.7,1)
                    
                    on_press:
                        root.CreateClassList(names)

            BoxLayout:
                orientation:"vertical"
                pos_hint:{"center_x":0.5,"center_y":0.5}
                padding:3,3
                
                Label:
                    text: ""                      
                          
                

            
            BoxLayout:
                orientation:"horizontal"
                pos_hint:{"center_x":0.5,"center_y":0.5}
                padding:3,3
                    
                    
                Button:
                    text:"START SCANNING"
                    pos_hint:{"center_x":0.5,"center_y":0.5}
                    padding:5,5
                    size_hint:(0.2,0.8)
                    border: (0,0,0,0)    
                    
                    on_press:
                        root.VKeyboard()                        
                        root.QRScanner()


            BoxLayout:
                orientation:"vertical"
                pos_hint:{"center_x":0.5,"center_y":0.5}
                padding:3,3
                
                Label:
                    text: ""          
            
            BoxLayout:
                orientation:"vertical"
                pos_hint:{"center_x":0.5,"center_y":0.5}
                padding:3,3
                
                TextInput:
                    pos_hint:{"center_x":0.5,"center_y":0.5}
                    hint_text:"INPUT EMAIL BEFORE EXPORT"
                    hint_text_color:0,0,0,1
                    background_color:1,1,1,1
                    foreground_color: 0,0,0,1
                    size_hint:(.5,.8)
                    height:50

                    id:email
                    multiline:False                     
                
                Button:
                    text:"EXPORT ATTENDANCE TO EMAIL"
                    pos_hint:{"center_x":0.5,"center_y":0.5}
                    background_color: .33, 0, 0, 1
                    padding:5,5
                    size_hint:(0.7,1)
                    
                    on_press:
                        root.email_file(email)                   

            BoxLayout:
                orientation:"vertical"
                pos_hint:{"center_x":0.5,"center_y":0.5}
                padding:3,3
                
                Label:
                    text: ""   


<Class5>
    name: "start"
    canvas.before:
        Rectangle:
            pos: self.pos
            source:'background.jpg'
            size: self.size
    GridLayout:
        rows:2
        BoxLayout:
            size_hint_y: None
            height:100
            spacing:5
            padding:5
            
            canvas:
                Color:
                    rgba:1,1,1,1
                Rectangle:
                    pos:self.pos
                    size:self.size
                    source:"b.jpg"
                    
            Button:
                
                background_color: 0,0.29,0.42,0
                size_hint_x:None
                width:50
                text:"[b] < [/b]"
                markup:True
                
                on_press:
                    root.manager.transition.direction="right"
                    root.manager.transition.duration=0
                    root.manager.current="ScreenFour"
                    
            TextInput:
                pos_hint:{"center_x":0.5,"center_y":0.5}
                hint_text:"Input Class Section"
                hint_text_color:1,1,1,1
                background_color:0,0,0,0
                foreground_color: 1,1,1,1
                size_hint:(.3,None)
                height:55

                canvas.before:
    
                    Line:
                        points: self.x, self.y, self.x + self.width, self.y
                        width: 0.1
                id:class1
                multiline:False 
            
        GridLayout:
            rows: 8
            
            BoxLayout:
                orientation:"vertical"
                pos_hint:{"center_x":0.5,"center_y":0.5}
                padding:3,3
                
                Label:
                    text: ""          
            
            BoxLayout:
                orientation:"vertical"
                pos_hint:{"center_x":0.5,"center_y":0.5}
                padding:3,3
                
                TextInput:
                    pos_hint:{"center_x":0.5,"center_y":0.5}
                    hint_text:"Enter Student Names"
                    hint_text_color:0,0,0,1
                    background_color:1,1,1,1
                    foreground_color: 0,0,0,1
                    size_hint:(.5,.8)
                    height:50

                    id:names
                    multiline:True                    
                
                Button:
                    text:"IMPORT RECORD OF THE CLASS"
                    pos_hint:{"center_x":0.5,"center_y":0.5}
                    background_color: .33, 0, 0, 1
                    padding:5,5
                    size_hint:(0.7,1)
                    
                    on_press:
                        root.CreateClassList(names)

            BoxLayout:
                orientation:"vertical"
                pos_hint:{"center_x":0.5,"center_y":0.5}
                padding:3,3
                
                Label:
                    text: ""                      
                          
                

            
            BoxLayout:
                orientation:"horizontal"
                pos_hint:{"center_x":0.5,"center_y":0.5}
                padding:3,3
                    
                    
                Button:
                    text:"START SCANNING"
                    pos_hint:{"center_x":0.5,"center_y":0.5}
                    padding:5,5
                    size_hint:(0.2,0.8)
                    border: (0,0,0,0)    
                    
                    on_press:
                        root.VKeyboard()                        
                        root.QRScanner()


            BoxLayout:
                orientation:"vertical"
                pos_hint:{"center_x":0.5,"center_y":0.5}
                padding:3,3
                
                Label:
                    text: ""          
            
            BoxLayout:
                orientation:"vertical"
                pos_hint:{"center_x":0.5,"center_y":0.5}
                padding:3,3
                
                TextInput:
                    pos_hint:{"center_x":0.5,"center_y":0.5}
                    hint_text:"INPUT EMAIL BEFORE EXPORT"
                    hint_text_color:0,0,0,1
                    background_color:1,1,1,1
                    foreground_color: 0,0,0,1
                    size_hint:(.5,.8)
                    height:50

                    id:email
                    multiline:False                     
                
                Button:
                    text:"EXPORT ATTENDANCE TO EMAIL"
                    pos_hint:{"center_x":0.5,"center_y":0.5}
                    background_color: .33, 0, 0, 1
                    padding:5,5
                    size_hint:(0.7,1)
                    
                    on_press:
                        root.email_file(email)                   

            BoxLayout:
                orientation:"vertical"
                pos_hint:{"center_x":0.5,"center_y":0.5}
                padding:3,3
                
                Label:
                    text: ""   


            """)

#--------------------------------------------------------------------------------------------------------------
#This class inherits the Screen and Boxlayout from Kivy so that it can display innovative user interface
#--------------------------------------------------------------------------------------------------------------
    
class ScreenOne(Screen,BoxLayout):

    #This function will use the text inputs from ScreenOne in Kivy Language to set a new password
    def do_reset(self,reemailtext,pastext,repastext):
        reemail=reemailtext
        paste=pastext
        print(paste)
        conn=sqlite3.connect("mybase.db")
        cu=conn.cursor()
        
        find=("SELECT * FROM register WHERE emid=? ")
        print(find)
        cu.execute(find,[(reemail)])
        results=cu.fetchall()
        if (len(reemail)>0):
            
            
            if results:
                cu.execute('UPDATE register SET passwd=? WHERE emid = ?', (paste,reemail))
                conn.commit()
                for i in results:
                    
                    self.manager.transition.direction="left"
                    self.manager.transition.duration=0
                    self.manager.current="ScreenTwo"
            else:
                popup=Popup(title="QR CODE-BASED ATTENDANCE SYSTEM LOGIN",content=Label(text="Enter Registered Email Address"),size_hint=(0.8,0.3))
                popup.open()
        else:
            popup=Popup(title="QR CODE-BASED ATTENDANCE SYSTEM LOGIN",content=Label(text="Enter Email Address"),size_hint=(0.8,0.3))
            popup.open()
        conn.close()
        self.ids['reemail'].text = ""
        self.ids['pas'].text = ""
        self.ids['repas'].text = ""
     
#--------------------------------------------------------------------------------------------------------------
#This class inherits the Screen and Gridlayout from Kivy so that it can display innovative user interface
#--------------------------------------------------------------------------------------------------------------
        
class ScreenTwo(Screen,GridLayout):

    #This function will use the text inputs from ScreenTwo of the Kivy Language to know if the user will be signed in to the system or not
    def do_login(self,usernametext,passwordtext):
        useri=usernametext
        passwd=passwordtext
        conn=sqlite3.connect("mybase.db")
        cur=conn.cursor()
        
        cur.execute("CREATE TABLE  IF NOT EXISTS login(userid VARCHAR(40),passwrd VARCHAR(40))")
        cur.execute("INSERT INTO login(userid,passwrd) VALUES(?,?)",(useri,passwd))
        cur.execute("SELECT * FROM register")
        print(cur.fetchall())
        if(len(useri)>0 and len(passwd)>0):
            
            find=("SELECT * FROM register WHERE emid=? AND passwd=?")
            cur.execute(find,[(useri),(passwd)])
            results=cur.fetchall()
            if results:
                for i in results:
                    popup=Popup(title="Welcome to QR Code-Based Attendance System",content=Label(text="Start scanning, "+i[0]+"!"),size_hint=(0.6,0.3))
                    popup.open()
                    self.manager.transition.direction="left"
                    self.manager.transition.duration=0
                    self.manager.current="ScreenFour"

            else:
                popup=Popup(title="QR CODE-BASED ATTENDANCE SYSTEM LOGIN",content=Label(text="Enter Correct Email and Password"),size_hint=(0.8,0.3))
                popup.open()

        else:
            popup=Popup(title="QR CODE-BASED ATTENDANCE SYSTEM LOGIN",content=Label(text="Enter Email and Password"),size_hint=(0.8,0.3))
            popup.open()
            
            
                
            
        print("table created successfully")
        conn.close()
        
        self.ids['username'].text = ""
        self.ids['password'].text = ""

#--------------------------------------------------------------------------------------------------------------
#This class inherits the Screen and Boxlayout from Kivy so that it can display innovative user interface
#--------------------------------------------------------------------------------------------------------------
        
class ScreenThree(Screen,BoxLayout):
    
    #This function will use the text inputs from ScreenThree of the Kivy Language to store the information of the user to the database using sqlite3    
    def do_register(self,firsttext,lasttext,emailtext,passwordtext,copasstext):
        fname=firsttext
        lname=lasttext
        email=emailtext
        password=passwordtext
        conpass=copasstext
        conn=sqlite3.connect("mybase.db")
        cu=conn.cursor()
        
        cu.execute("CREATE TABLE IF NOT EXISTS register(name VARCHAR(30),lastname VARCHAR(30),emid VARCHAR(40),passwd VARCHAR(30),cpasswd VARCHAR(30))")
        find=("SELECT * FROM register WHERE emid=?")
        cu.execute(find,[(email)])
        
            
        if(len(fname)>0 and len(lname)>0 and len(email)>0 and len(password)>0 and len(conpass)>0):
            if cu.fetchall():
                popup=Popup(title="ERROR", content=Label(text="User is already registered. Please login"),size_hint=(0.6,0.3))
                popup.open()
                self.manager.transition.direction="right"
                self.manager.transition.duration=0
                self.manager.current="ScreenTwo"
            else:
            
            
                
                print(cu.fetchall())
                
                if not re.match("^[A-Za-z]*$", fname):
                    popup=Popup(title="SETUP", content=Label(text="Enter Your First Name"),size_hint=(0.6,0.3))
                    popup.open()
                elif not re.match("^[A-Za-z]*$", lname):
                        popup=Popup(title="SETUP", content=Label(text="Enter Your Last Name"),size_hint=(0.6,0.3))
                        popup.open()

                    
                elif not re.match("^[A-Za-z0-9]+@[A-Za-z0-9]+\.[A-Za-z0-9]", email):
                        popup=Popup(title="SETUP", content=Label(text="Enter an Email Address"),size_hint=(0.6,0.3))
                        popup.open()
                    
                    
                elif not re.match("^[A-Za-z0-9]*$", password):
                        popup=Popup(title="SETUP", content=Label(text="Enter a Password"),size_hint=(0.6,0.3))
                        popup.open()
                
                    
                    
                    
                elif not re.match("^[A-Za-z0-9]*$", password):
                        popup=Popup(title="SETUP", content=Label(text="Please Confirm  password"),size_hint=(0.6,0.3))
                        popup.open()
                    
                elif (password==conpass):
                        cu.execute("INSERT INTO register(name,lastname,emid,passwd,cpasswd) VALUES(?,?,?,?,?)",(fname,lname,email,password,conpass))
                        cu.execute("SELECT * FROM register")
                        conn.commit()
                        print("regis")
                        popup=Popup(title="SETUP", content=Label(text="Registration Complete\n Please Login"),size_hint=(0.6,0.3))
                        popup.open()
                        self.manager.transition.direction="right"
                        self.manager.transition.duration=0
                        self.manager.current="ScreenTwo"
                   
                else:
                    popup=Popup(title="ERROR", content=Label(text="Please Enter the same Password"),size_hint=(0.6,0.3))
                    popup.open()
      
        else:
            popup=Popup(title="ERROR", content=Label(text="Please Enter Your Details"),size_hint=(0.6,0.3))
            popup.open()
            print("fields")
        conn.close()
        self.ids['fname'].text = ""
        self.ids['lname'].text = ""
        self.ids['emailid'].text = ""
        self.ids['passwd'].text = ""
        self.ids['cpass'].text = ""

#--------------------------------------------------------------------------------------------------------------
#These classes inherits the Screen and Boxlayout from Kivy so that it can display innovative user interface
#--------------------------------------------------------------------------------------------------------------

class ScreenFour(Screen,GridLayout):
    pass #Putting pass will only project the layout set in the ScreenFour from Kivy Language

class ScreenFive(Screen,GridLayout):
    pass #Putting pass will only project the layout set in the ScreenFive from Kivy Language

class Help(Screen,GridLayout):
    pass #Putting pass will only project the layout set in the Help from Kivy Language

class Developers(Screen,GridLayout):
    pass #Putting pass will only project the layout set in the Developers from Kivy Language

#--------------------------------------------------------------------------------------------------------------
#These are the classes for each class of the instructor. All of them inherit Screen and GridLayout from Kivy
#--------------------------------------------------------------------------------------------------------------

class Class1(Screen,GridLayout):

    #This centers the text input from the Kivy Language
    def update_padding(self, text_input, *args):
        text_width = text_input._get_text_width(
            text_input.text,
            text_input.tab_width,
            text_input._label_cached
        )
        text_input.padding_x = (text_input.width - text_width)/2
   
    names = [] #Empty list

    #Function for keyboard
    def VKeyboard(VKeyboard): 
        pass

    #Function for QR Code scanner
    def QRScanner(self):
        cap = cv2.VideoCapture(0)
        
        global names
        
        names=[]
        def enterData(z):
            if z in names:
                pass
            else:
                names.append(z)
    
        print('Reading...')
    
        def checkData(data):
            data=str(data)    
            if data in names:
                print('Already Present')
            else:
                print(data)
                enterData(data)
      
        while True:
            _, frame = cap.read() 
            decodedObjects = pyzbar.decode(frame)
            for obj in decodedObjects:
                checkData(obj.data)
                time.sleep(1)
           
            cv2.imshow("Frame", frame)
    
            if cv2.waitKey(1)& 0xFF == ord('s'):
                cv2.destroyAllWindows()
                break
        
        names = names      
    
        final_names = []
        
        for items in names:
            a = names.index(items)
            b = len(items)
            items = items[2:(b-1)]
            final_names.append(items)
        
        today = date.today()
        date1 = today.strftime("%B %d, %Y")
        
        final_names.sort()
        
        a = open("Class1.txt", "r")
        students = a.read()
        
        for i in final_names:
            if i not in students:
                s = final_names.index(i)
                del final_names[s]
            else:
                continue
            
        present = [date1] + final_names
        
        print(present)
        
        f = open("Class1.txt", "r") 
        
        if f.mode == 'r':
            contents = f.read()
            
            for items in names:
                if items in contents:
                    v = contents.index(items)
                    x = len(items)
                    print(x)
                    z = contents[v:(v+x)]
                    present.append(z)

                
        workbook = xlsxwriter.Workbook('Attendance_Class1.xlsx')
        worksheet = workbook.add_worksheet('Data1')
        
        #Start from the first cell. Rows and columns are zero indexed.
        row = 0
        col = 0
        
        #Iterate over the data and write it out row by row.
        for item in (present):
            worksheet.write(row, col, item)
            row += 1
        
        
        workbook.close()    

    #Function for emailing the generated excel file to entered email address from the text input in the Kivy Language    
    def email_file(self,email):
        file = 'Attendance_Class1.xlsx'
        username='qrcodebased.attendance@gmail.com'
        password='2019bscpe1-2'
        send_from = 'qrcodebased.attendance@gmail.com'
        send_to = email.text
        msg = MIMEMultipart()
        msg['From'] = 'qrcodebased.attendance'
        msg['To'] = email.text
        msg['Cc'] = 'Attendance for Today!'
        msg['Date'] = formatdate(localtime = True)
        msg['Subject'] = ''
        server = smtplib.SMTP_SSL('smtp.gmail.com')
        port = '465'
        fp = open(file, 'rb')
        part = MIMEBase('application','vnd.ms-excel')
        part.set_payload(fp.read())
        fp.close()
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment', filename='Attendance_Class1.xlsx')
        msg.attach(part)
        smtp = smtplib.SMTP_SSL('smtp.gmail.com')
        smtp.ehlo()
        smtp.login(username,password)
        smtp.sendmail(send_from, send_to.split(',') + msg['Cc'].split(','), msg.as_string())
        smtp.quit()

    #Function for storing the class list in a text file    
    def CreateClassList(self,names):
        fd = open("Class1.txt","w")
        student_names = str(names.text)
        fd.write(student_names)
        fd.close()


#--------------------------------------------------------------------------------------------------------------
#Class 2, same class from the previous one with different class name
#--------------------------------------------------------------------------------------------------------------

class Class2(Screen,GridLayout):
    def update_padding(self, text_input, *args):
        text_width = text_input._get_text_width(
            text_input.text,
            text_input.tab_width,
            text_input._label_cached
        )
        text_input.padding_x = (text_input.width - text_width)/2
   
    names = []
    
    def VKeyboard(VKeyboard): 
        pass
    
    def QRScanner(self):
        cap = cv2.VideoCapture(0)
        
        global names
        
        names=[]
        def enterData(z):
            if z in names:
                pass
            else:
                names.append(z)
    
        print('Reading...')
    
        def checkData(data):
            data=str(data)    
            if data in names:
                print('Already Present')
            else:
                print(data)
                enterData(data)
      
        while True:
            _, frame = cap.read() 
            decodedObjects = pyzbar.decode(frame)
            for obj in decodedObjects:
                checkData(obj.data)
                time.sleep(1)
           
            cv2.imshow("Frame", frame)
    
            if cv2.waitKey(1)& 0xFF == ord('s'):
                cv2.destroyAllWindows()
                break
        
        names = names      
    
        final_names = []
        
        for items in names:
            a = names.index(items)
            b = len(items)
            items = items[2:(b-1)]
            final_names.append(items)
        
        today = date.today()
        date1 = today.strftime("%B %d, %Y")
        
        final_names.sort()
        
        a = open("Class2.txt", "r")
        students = a.read()
        
        for i in final_names:
            if i not in students:
                s = final_names.index(i)
                del final_names[s]
            else:
                continue
            
        present = [date1] + final_names
        
        print(present)
        
        f = open("Class2.txt", "r")
        
        if f.mode == 'r':
            contents = f.read()
            
            for items in names:
                if items in contents:
                    v = contents.index(items)
                    x = len(items)
                    print(x)
                    z = contents[v:(v+x)]
                    present.append(z)

                
        workbook = xlsxwriter.Workbook('Attendance_Class2.xlsx')
        worksheet = workbook.add_worksheet('Data1')
        
        # Start from the first cell. Rows and columns are zero indexed.
        row = 0
        col = 0
        
        # Iterate over the data and write it out row by row.
        for item in (present):
            worksheet.write(row, col, item)
            row += 1
        
        
        workbook.close()    
        
    def email_file(self,email):
        file = 'Attendance_Class2.xlsx'
        username='qrcodebased.attendance@gmail.com'
        password='2019bscpe1-2'
        send_from = 'qrcodebased.attendance@gmail.com'
        send_to = email.text
        msg = MIMEMultipart()
        msg['From'] = 'qrcodebased.attendance'
        msg['To'] = email.text
        msg['Cc'] = 'Attendance for Today!'
        msg['Date'] = formatdate(localtime = True)
        msg['Subject'] = ''
        server = smtplib.SMTP_SSL('smtp.gmail.com')
        port = '465'
        fp = open(file, 'rb')
        part = MIMEBase('application','vnd.ms-excel')
        part.set_payload(fp.read())
        fp.close()
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment', filename='Attendance_Class2.xlsx')
        msg.attach(part)
        smtp = smtplib.SMTP_SSL('smtp.gmail.com')
        smtp.ehlo()
        smtp.login(username,password)
        smtp.sendmail(send_from, send_to.split(',') + msg['Cc'].split(','), msg.as_string())
        smtp.quit()
        
    def CreateClassList(self,names):
        fd = open("Class2.txt","w")
        student_names = str(names.text)
        fd.write(student_names)
        fd.close()

#--------------------------------------------------------------------------------------------------------------
#Class 3, same class from the previous one with different class name
#--------------------------------------------------------------------------------------------------------------

class Class3(Screen,GridLayout):
    def update_padding(self, text_input, *args):
        text_width = text_input._get_text_width(
            text_input.text,
            text_input.tab_width,
            text_input._label_cached
        )
        text_input.padding_x = (text_input.width - text_width)/2
   
    names = []
    
    def VKeyboard(VKeyboard): 
        pass
    
    def QRScanner(self):
        cap = cv2.VideoCapture(0)
        
        global names
        
        names=[]
        def enterData(z):
            if z in names:
                pass
            else:
                names.append(z)
    
        print('Reading...')
    
        def checkData(data):
            data=str(data)    
            if data in names:
                print('Already Present')
            else:
                print(data)
                enterData(data)
      
        while True:
            _, frame = cap.read() 
            decodedObjects = pyzbar.decode(frame)
            for obj in decodedObjects:
                checkData(obj.data)
                time.sleep(1)
           
            cv2.imshow("Frame", frame)
    
            if cv2.waitKey(1)& 0xFF == ord('s'):
                cv2.destroyAllWindows()
                break
        
        names = names      
    
        final_names = []
        
        for items in names:
            a = names.index(items)
            b = len(items)
            items = items[2:(b-1)]
            final_names.append(items)
        
        today = date.today()
        date1 = today.strftime("%B %d, %Y")
        
        final_names.sort()
        
        a = open("Class3.txt", "r")
        students = a.read()
        
        for i in final_names:
            if i not in students:
                s = final_names.index(i)
                del final_names[s]
            else:
                continue
            
        present = [date1] + final_names
        
        print(present)
        
        f = open("Class3.txt", "r")
        
        if f.mode == 'r':
            contents = f.read()
            
            for items in names:
                if items in contents:
                    v = contents.index(items)
                    x = len(items)
                    print(x)
                    z = contents[v:(v+x)]
                    present.append(z)

                
        workbook = xlsxwriter.Workbook('Attendance_Class3.xlsx')
        worksheet = workbook.add_worksheet('Data1')
        
        # Start from the first cell. Rows and columns are zero indexed.
        row = 0
        col = 0
        
        # Iterate over the data and write it out row by row.
        for item in (present):
            worksheet.write(row, col, item)
            row += 1
        
        
        workbook.close()    
        
    def email_file(self,email):
        file = 'Attendance_Class3.xlsx'
        username='qrcodebased.attendance@gmail.com'
        password='2019bscpe1-2'
        send_from = 'qrcodebased.attendance@gmail.com'
        send_to = email.text
        msg = MIMEMultipart()
        msg['From'] = 'qrcodebased.attendance'
        msg['To'] = email.text
        msg['Cc'] = 'Attendance for Today!'
        msg['Date'] = formatdate(localtime = True)
        msg['Subject'] = ''
        server = smtplib.SMTP_SSL('smtp.gmail.com')
        port = '465'
        fp = open(file, 'rb')
        part = MIMEBase('application','vnd.ms-excel')
        part.set_payload(fp.read())
        fp.close()
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment', filename='Attendance_Class3.xlsx')
        msg.attach(part)
        smtp = smtplib.SMTP_SSL('smtp.gmail.com')
        smtp.ehlo()
        smtp.login(username,password)
        smtp.sendmail(send_from, send_to.split(',') + msg['Cc'].split(','), msg.as_string())
        smtp.quit()
        
    def CreateClassList(self,names):
        fd = open("Class3.txt","w")
        student_names = str(names.text)
        fd.write(student_names)
        fd.close()

#--------------------------------------------------------------------------------------------------------------
#Class 4, same class from the previous one with different class name
#--------------------------------------------------------------------------------------------------------------

class Class4(Screen,GridLayout):
    def update_padding(self, text_input, *args):
        text_width = text_input._get_text_width(
            text_input.text,
            text_input.tab_width,
            text_input._label_cached
        )
        text_input.padding_x = (text_input.width - text_width)/2
   
    names = []
    
    def VKeyboard(VKeyboard): 
        pass
    
    def QRScanner(self):
        cap = cv2.VideoCapture(0)
        
        global names
        
        names=[]
        def enterData(z):
            if z in names:
                pass
            else:
                names.append(z)
    
        print('Reading...')
    
        def checkData(data):
            data=str(data)    
            if data in names:
                print('Already Present')
            else:
                print(data)
                enterData(data)
      
        while True:
            _, frame = cap.read() 
            decodedObjects = pyzbar.decode(frame)
            for obj in decodedObjects:
                checkData(obj.data)
                time.sleep(1)
           
            cv2.imshow("Frame", frame)
    
            if cv2.waitKey(1)& 0xFF == ord('s'):
                cv2.destroyAllWindows()
                break
        
        names = names      
    
        final_names = []
        
        for items in names:
            a = names.index(items)
            b = len(items)
            items = items[2:(b-1)]
            final_names.append(items)
        
        today = date.today()
        date1 = today.strftime("%B %d, %Y")
        
        final_names.sort()
        
        a = open("Class4.txt", "r")
        students = a.read()
        
        for i in final_names:
            if i not in students:
                s = final_names.index(i)
                del final_names[s]
            else:
                continue
            
        present = [date1] + final_names
        
        print(present)
        
        f = open("Class4.txt", "r")
        
        if f.mode == 'r':
            contents = f.read()
            
            for items in names:
                if items in contents:
                    v = contents.index(items)
                    x = len(items)
                    print(x)
                    z = contents[v:(v+x)]
                    present.append(z)

                
        workbook = xlsxwriter.Workbook('Attendance_Class4.xlsx')
        worksheet = workbook.add_worksheet('Data1')
        
        # Start from the first cell. Rows and columns are zero indexed.
        row = 0
        col = 0
        
        # Iterate over the data and write it out row by row.
        for item in (present):
            worksheet.write(row, col, item)
            row += 1
        
        
        workbook.close()    
        
    def email_file(self,email):
        file = 'Attendance_Class4.xlsx'
        username='qrcodebased.attendance@gmail.com'
        password='2019bscpe1-2'
        send_from = 'qrcodebased.attendance@gmail.com'
        send_to = email.text
        msg = MIMEMultipart()
        msg['From'] = 'qrcodebased.attendance'
        msg['To'] = email.text
        msg['Cc'] = 'Attendance for Today!'
        msg['Date'] = formatdate(localtime = True)
        msg['Subject'] = ''
        server = smtplib.SMTP_SSL('smtp.gmail.com')
        port = '465'
        fp = open(file, 'rb')
        part = MIMEBase('application','vnd.ms-excel')
        part.set_payload(fp.read())
        fp.close()
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment', filename='Attendance_Class4.xlsx')
        msg.attach(part)
        smtp = smtplib.SMTP_SSL('smtp.gmail.com')
        smtp.ehlo()
        smtp.login(username,password)
        smtp.sendmail(send_from, send_to.split(',') + msg['Cc'].split(','), msg.as_string())
        smtp.quit()
        
    def CreateClassList(self,names):
        fd = open("Class4.txt","w")
        student_names = str(names.text)
        fd.write(student_names)
        fd.close()

#--------------------------------------------------------------------------------------------------------------
#Class 5, same class from the previous one with different class name
#--------------------------------------------------------------------------------------------------------------

class Class5(Screen,GridLayout):
    def update_padding(self, text_input, *args):
        text_width = text_input._get_text_width(
            text_input.text,
            text_input.tab_width,
            text_input._label_cached
        )
        text_input.padding_x = (text_input.width - text_width)/2
   
    names = []
    
    def VKeyboard(VKeyboard): 
        pass
    
    def QRScanner(self):
        cap = cv2.VideoCapture(0)
        
        global names
        
        names=[]
        def enterData(z):
            if z in names:
                pass
            else:
                names.append(z)
    
        print('Reading...')
    
        def checkData(data):
            data=str(data)    
            if data in names:
                print('Already Present')
            else:
                print(data)
                enterData(data)
      
        while True:
            _, frame = cap.read() 
            decodedObjects = pyzbar.decode(frame)
            for obj in decodedObjects:
                checkData(obj.data)
                time.sleep(1)
           
            cv2.imshow("Frame", frame)
    
            if cv2.waitKey(1)& 0xFF == ord('s'):
                cv2.destroyAllWindows()
                break
        
        names = names      
    
        final_names = []
        
        for items in names:
            a = names.index(items)
            b = len(items)
            items = items[2:(b-1)]
            final_names.append(items)
        
        today = date.today()
        date1 = today.strftime("%B %d, %Y")
        
        final_names.sort()
        
        a = open("Class5.txt", "r")
        students = a.read()
        
        for i in final_names:
            if i not in students:
                s = final_names.index(i)
                del final_names[s]
            else:
                continue
            
        present = [date1] + final_names
        
        print(present)
        
        f = open("Class5.txt", "r")
        
        if f.mode == 'r':
            contents = f.read()
            
            for items in names:
                if items in contents:
                    v = contents.index(items)
                    x = len(items)
                    print(x)
                    z = contents[v:(v+x)]
                    present.append(z)

                
        workbook = xlsxwriter.Workbook('Attendance_Class5.xlsx')
        worksheet = workbook.add_worksheet('Data1')
        
        # Start from the first cell. Rows and columns are zero indexed.
        row = 0
        col = 0
        
        # Iterate over the data and write it out row by row.
        for item in (present):
            worksheet.write(row, col, item)
            row += 1
        
        
        workbook.close()    
        
    def email_file(self,email):
        file = 'Attendance_Class5.xlsx'
        username='qrcodebased.attendance@gmail.com'
        password='2019bscpe1-2'
        send_from = 'qrcodebased.attendance@gmail.com'
        send_to = email.text
        msg = MIMEMultipart()
        msg['From'] = 'qrcodebased.attendance'
        msg['To'] = email.text
        msg['Cc'] = 'Attendance for Today!'
        msg['Date'] = formatdate(localtime = True)
        msg['Subject'] = ''
        server = smtplib.SMTP_SSL('smtp.gmail.com')
        port = '465'
        fp = open(file, 'rb')
        part = MIMEBase('application','vnd.ms-excel')
        part.set_payload(fp.read())
        fp.close()
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment', filename='Attendance_Class5.xlsx')
        msg.attach(part)
        smtp = smtplib.SMTP_SSL('smtp.gmail.com')
        smtp.ehlo()
        smtp.login(username,password)
        smtp.sendmail(send_from, send_to.split(',') + msg['Cc'].split(','), msg.as_string())
        smtp.quit()
        
    def CreateClassList(self,names):
        fd = open("Class5.txt","w")
        student_names = str(names.text)
        fd.write(student_names)
        fd.close()

#--------------------------------------------------------------------------------------------------------------
#Adding these widgets will display all of the classes that uses kivy language and modules
#--------------------------------------------------------------------------------------------------------------

screen_manager=ScreenManager()
screen_manager.add_widget(ScreenTwo(name="ScreenTwo"))
screen_manager.add_widget(ScreenThree(name="ScreenThree"))
screen_manager.add_widget(ScreenOne(name="ScreenOne"))
screen_manager.add_widget(ScreenFour(name="ScreenFour"))
screen_manager.add_widget(ScreenFive(name="ScreenFive"))
screen_manager.add_widget(Help(name="Help"))
screen_manager.add_widget(Developers(name="Developers"))
screen_manager.add_widget(Class1(name="Class1"))
screen_manager.add_widget(Class2(name="Class2"))
screen_manager.add_widget(Class3(name="Class3"))
screen_manager.add_widget(Class4(name="Class4"))
screen_manager.add_widget(Class5(name="Class5"))

#--------------------------------------------------------------------------------------------------------------
#This is the class to run the screen_manager widgets from above, this will return na screen_manager
#--------------------------------------------------------------------------------------------------------------

class MyApp(App):
    
    title="QR Code-Based Attendance System"
    icon="cords.jpg"
   
    def build(self):
        return screen_manager
         
#--------------------------------------------------------------------------------------------------------------
#This is used to execute codes only if the file was run directly, and not imported
#--------------------------------------------------------------------------------------------------------------
    
if __name__ == '__main__':
    MyApp().run()
