from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivymd.toast.kivytoast import toast
from kivy.uix.screenmanager import Screen

#These lines of code will import the module for database, camera, QR code reader, excel file generator and time
import qrcode
from PIL import Image, ImageDraw, ImageFont

Builder.load_file('./libs/kv/generate.kv')

class GenerateScreen(Screen):
    #This function will generate and show a QR Code based on user input
    def genQR(self, full_name):
        qr_data = full_name

        if qr_data == "":
            return toast('Please enter your name to create a QR code.')
        else:
            image = Image.new('RGB', (1280, 720), (255, 255, 255))
            draw = ImageDraw.Draw(image)
            font = ImageFont.truetype('arial.ttf', size=40)

            img = qrcode.make(str(qr_data))
            img.save(str(qr_data) + '.jpg')

            self.ids['qr_data'].text = ""

            return toast('Your QR code is successfully created!')