# -*- coding: utf-8 -*-
import kivy
kivy.require('1.11.1')

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
from kivy.uix.popup import Popup

import pyperclip

import os
from bs4 import BeautifulSoup
import requests
import webbrowser

class InternetError(FloatLayout):
    pass

# Internet error
class InternetErrorApp(App):
    def build(self):
        Builder.load_string(f"""
<InternetError>
    CoverImage:
        source: 'image/background.jpg'
    Label:
        text: "네트워크 에러!"
        font_name: '{font_path}'
        font_size: '50sp'

<CoverImage@CoverBehavior+Image>:
    reference_size: self.texture_size
 """)
        return InternetError()

# Main app
class Main(FloatLayout):
    def on_clipboard(self, *args):
        copy_txt = str(args).replace("'", "").replace("(", "").replace(")", "").replace(",", "")
        pyperclip.copy(copy_txt)

class MainAndroid(FloatLayout):
    pass

class MainApp(App):

    def build(self):
        self.title = f'{program_name.replace(" ", "_")} V.{version}'

        Builder.load_string(f"""
#:import Factory kivy.factory.Factory

<HelpPop@Popup>:
    size_hint: 0.4, 0.4
    title: 'Copy complete :)'
    auto_dismiss: False
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: '복사완료!'
            font_name: '{font_path}'
        Button:
            text: '닫기'
            font_name: '{font_path}'
            background_normal: '{normal_button}'
            background_down: '{pushed_button}'

            on_press:
                root.dismiss()
            size_hint_y: None
            height: '40dp'

<Main>
    CoverImage:
        source: 'image/background.jpg'
    BoxLayout:
        orientation:"vertical"
        FloatLayout:
            size_hint: 1, .2
        BoxLayout:
            size_hint: 1, .9
            orientation:"vertical"
            Label:
                text: "한강수온"
                font_name: '{font_path}'
                font_size: '50sp'
            BoxLayout:
                size_hint: 1, .6
                orientation:"vertical"
                Label:
                    text: "{tempdate}"
                    font_name: '{font_path}'
                    font_size: '20sp'
                Label:
                    text: "{temptime}에 측정함"
                    font_name: '{font_path}'
                    font_size: '20sp'
            Label:
                text: "{temp}"
                font_name: '{font_path}'
                font_size: '30sp'
            BoxLayout:
                FloatLayout:
                Button:
                    text: "복사하기 :)"
                    size_hint: .5, .7
                    font_name: '{font_path}'
                    background_normal: '{normal_button}'
                    background_down: '{pushed_button}'
                    on_release:
                        root.on_clipboard('{tempdate}의 한강수온은 {temp} 입니다')
                        Factory.HelpPop().open()

                FloatLayout:
        FloatLayout:
            orientation:"vertical"
            Button:
                text: "Made by 천상의나무 for Winsub"
                font_name: '{font_path}'
                size_hint: 1, .1
                font_size: '15sp'
                background_normal: '{transparent_button}'
                background_down: '{transparent_button}'
                on_release: app.opensite()

<MainAndroid>
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
            BoxLayout:
                size_hint: 1, .6
                orientation:"vertical"
                Label:
                    text: "{tempdate}"
                    font_name: '{font_path}'
                    font_size: '20sp'
                Label:
                    text: "{temptime}에 측정함"
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

        if kivy.utils.platform == "android":
            return MainAndroid()
        else:
            return Main()
    
    def opensite(self):
        webbrowser.open_new("https://hangang.life")

if __name__ == '__main__':

    # Main program version
    version = "1.2"

    # Set program name
    program_name = "Winsub Hangang Temperature"

    # Font path
    font_path = 'font/NanumBarunGothic.ttf'

    # Button path

    transparent_button = "image/button.png"
    normal_button = "image/normal_button.png"
    pushed_button = "image/pushed_button.png"

    # Link
    HanGang = 'https://hangang.life/api/'

    try:
        data = requests.get(HanGang)
    except:
        InternetErrorApp().run()

    soup = BeautifulSoup(data.text, 'lxml')
    temp = soup.find('p', {'id' : 'tem'}).get_text().replace(' °C', '°C') # 온도
    tempdate = soup.find('p', {'id' : 'time_date'}).get_text() #날짜
    temptime = soup.find('p', {'id' : 'time_time'}).get_text() #시간

    MainApp().run()
