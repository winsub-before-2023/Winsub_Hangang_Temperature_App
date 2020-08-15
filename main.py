# -*- coding: utf-8 -*-
import kivy
kivy.require('1.9.1')

from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.config import Config

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import AsyncImage
from kivy.uix.behaviors import CoverBehavior
from kivy.uix.image import Image

from kivy.uix.label import Label
from kivy.lang import Builder

import os
from bs4 import BeautifulSoup
import requests
import webbrowser

# Main app
class Main(FloatLayout):
    pass
class MainApp(App):

    def build(self):
        self.title = f'{program_name.replace(" ", "_")} V.{version}'
        try:
            data = requests.get(HanGang)
        except:
            Builder.load_string(f"""
<Main>
    CoverImage:
        source: 'image/background.jpg'
    Label:
        text: "네트워크 에러!"
        font_name: '{font_path}'
        font_size: '40sp'

<CoverImage@CoverBehavior+Image>:
    reference_size: self.texture_size
""")

        else:
            soup = BeautifulSoup(data.text, 'lxml')
            temp = soup.find('p', {'id' : 'tem'}).get_text().replace(' °C', '°C') # 온도
            tempdate = soup.find('p', {'id' : 'time_date'}).get_text() #날짜
            temptime = soup.find('p', {'id' : 'time_time'}).get_text() #시간
            

            Builder.load_string(f"""
<Main>
    CoverImage:
        source: 'image/background.jpg'
    BoxLayout:
        orientation:"vertical"
        FloatLayout:
            size_hint: 1, .2
        BoxLayout:
            size_hint: 1, .5
            orientation:"vertical"
            Label:
                text: "한강수온"
                font_name: '{font_path}'
                font_size: '50sp'
            Label:
                text: "{tempdate} {temptime}에 측정함"
                font_name: '{font_path}'
                font_size: '20sp'
            Label:
                text: "{temp}"
                font_name: '{font_path}'
                font_size: '30sp'
        FloatLayout:
            orientation:"vertical"
            Button:
                text: "Made by 천상의나무 for Winsub"
                font_name: '{font_path}'
                size_hint: 1, .1
                font_size: '15sp'
                background_normal: 'image/button.png'
                background_down: 'image/button.png'
                on_release: app.opensite()

<CoverImage@CoverBehavior+Image>:
    reference_size: self.texture_size
""")

        return Main()
    
    def opensite(self):
        webbrowser.open_new("https://hangang.life")

if __name__ == '__main__':

    # Main program version
    version = "1.1"

    # Set program name
    program_name = "Winsub Hangang Temperature"

    # Font path
    font_path = 'font/NanumBarunGothic.ttf'

    # Button path

    normal_button = "image/button.png"
    pushed_button = "image/pushed_button.png"

    # Link
    HanGang = 'https://hangang.life/api/'

    MainApp().run()
