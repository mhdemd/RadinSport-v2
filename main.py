from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.clock import Clock, mainthread
from kivy.factory import Factory
from kivy.uix.popup import Popup
from kivy.loader import Loader
from kivy.core.window import Window
from kivymd.app import MDApp

import os
import sys
from pathlib import Path
from functools import partial
from arabic_reshaper import reshape
from bidi.algorithm import get_display
import requests
from threading import Thread

from PYs.my_classes import * 

if getattr(sys, "frozen", False):  # bundle mode with PyInstaller
    os.environ["RADIN_ROOT"] = sys._MEIPASS
else:
    os.environ["RADIN_ROOT"] = str(Path(__file__).parent)

#Window.size = (450, 800)

Window.softinput_mode = "below_target"

Builder.load_file('main.kv')

class DigiApp(MDApp):

    def build(self):
        Loader.loading_image = 'img/loading1.zip'
        Loader.error_image = 'img/Loader_error_image.png'
        self.theme_cls.primary_palette = "Gray"
        self.theme_cls.primary_hue = "900"
        self.theme_cls.accent_palette = "Blue"
        self.theme_cls.accent_hue  = "900"
       #self.theme_cls.theme_style = "Dark"
        return MainScreen()
    
    def on_start(self): 
        self.root.current = 'SplashScreen' 
        # To run animations and processes at the same time
        self.t = Thread(target=self.heavy_processing, daemon = True)
        self.t.start()

    @mainthread
    def Err_connection(self):
        self.root.change_screen('Err_connection.kv', 'Factory.Err_connection()', 'Err_connection')
        self.root.current = 'Err_connection'

    def heavy_processing(self, *args):
        # Get data from APIs 
        url1 = 'http://mahdiemadi.ir/api_1' 
        url2 = 'http://mahdiemadi.ir/api_2' 
        
        try:
            response1 = requests.get(url1, timeout=2)            
            response2 = requests.get(url2, timeout=2)
        except:
            self.Err_connection()
            return

        self.result1 = response1.json()
        self.result2 = response2.json()

        Clock.schedule_once(self.create_first_page, 0.05)
        
        Clock.schedule_once(partial(self.root.change_screen, 'screen_product.kv', 'Factory.Product()', 'product'), .05)
        Clock.schedule_once(partial(self.root.change_screen, 'screen_off.kv', 'Factory.Off()', 'off'), .05)
        Clock.schedule_once(partial(self.root.change_screen, 'screen_account.kv', 'Factory.Account()', 'account'), .05)
        Clock.schedule_once(partial(self.root.change_screen, 'screen_login.kv', 'Factory.Login()', 'login'), .05)
        Clock.schedule_once(partial(self.root.change_screen, 'screen_search.kv', 'Factory.Search()', 'search'), .05)
        Clock.schedule_once(partial(self.root.change_screen, 'screen_grouping.kv', 'Factory.Grouping()', 'grouping'), .05)
        ##Clock.schedule_once(partial(self.root.change_screen, 'screen_order.kv', 'Factory.Order()', 'order'), .05)
        
        self.t = None
        
    def create_first_page(self, arg):  

        # Access the carousel.
        carousel = self.root.get_screen('main').mgr3.mgr1.ids._carousel_
        # Schedule after every 3 seconds.
        Clock.schedule_interval(carousel.load_next, 3.0)

        # Add widget to scrollview1 inf main screen
        list_DKP = [row[0] for row in self.result1]
        list_text_title = [row[1] for row in self.result1]
        list_detail_3 = [row[2] for row in self.result1]
        list_detail_4 = [row[3] for row in self.result1]
        list_off = [row[4] for row in self.result1]
        list_price = [row[5] for row in self.result1]
        list_price_off = [row[6] for row in self.result1]

        j = 5 #len(list_DKP)
        for i in range(j if len(list_DKP) > j else len(list_DKP)):
            dkp = list_DKP[i]
            self.root.get_screen('main').mgr3.mgr2.dkp= dkp
            text_title = list_text_title[i] 
 
            if len(text_title) > 20:
                text_title = '...' + text_title[-17:] 

            self.root.get_screen('main').mgr3.mgr2.text_title= text_title
            # Add image from host  
            self.root.get_screen('main').mgr3.mgr2.source_image= 'http://mahdiemadi.ir/Products/%s/%s-0-v_200-h_200-q_90.jpg'%(str(int(dkp)), str(int(dkp)))
            self.root.get_screen('main').mgr3.mgr2.detail_1= list_detail_3[i]
            self.root.get_screen('main').mgr3.mgr2.detail_2= list_detail_4[i]
            self.root.get_screen('main').mgr3.mgr2.off= list_off[i]
            price = list_price[i]
            self.root.get_screen('main').mgr3.mgr2.price= f'{price:,}'
            price_off = list_price_off[i]
            self.root.get_screen('main').mgr3.mgr2.price_off= f'{price_off:,}'
            self.root.get_screen('main').mgr3.mgr2.mgr1.add_widget(Factory.BoxLayout_mainscroll_scroll1())
        
        # Add widget to scrollview2 in main screen
        list_DKP_Gl = [row[0] for row in self.result2]
        list_text_title_Gl = [row[1] for row in self.result2]
        list_detail_3_Gl = [row[2] for row in self.result2]
        list_detail_4_Gl = [row[3] for row in self.result2]
        list_off_Gl = [row[4] for row in self.result2]
        list_price_Gl = [row[5] for row in self.result2]
        list_price_off_Gl = [row[6] for row in self.result2]
        self.list_version = [row[7] for row in self.result2]

        for i in range(j if len(list_DKP_Gl) > j else len(list_DKP_Gl)):
            dkp_Gl = list_DKP_Gl[i]
            self.root.get_screen('main').mgr3.mgr3.dkp_Gl= dkp_Gl
            text_title = list_text_title_Gl[i]
            if len(text_title) > 20:
                text_title = '...' + text_title[-17:] 
            self.root.get_screen('main').mgr3.mgr3.text_title= text_title
            # Add image from host
            self.root.get_screen('main').mgr3.mgr3.source_image= 'http://mahdiemadi.ir/Products/%s/%s-0-v_200-h_200-q_90.jpg'%(str(int(dkp_Gl)), str(int(dkp_Gl)))
            self.root.get_screen('main').mgr3.mgr3.detail_1= list_detail_3_Gl[i]
            self.root.get_screen('main').mgr3.mgr3.detail_2= list_detail_4_Gl[i]
            self.root.get_screen('main').mgr3.mgr3.off= list_off_Gl[i]
            price = list_price_Gl[i]            
            self.root.get_screen('main').mgr3.mgr3.price= f'{price:,}'
            price_off = list_price_off_Gl[i]
            self.root.get_screen('main').mgr3.mgr3.price_off= f'{price_off:,}'
            self.root.get_screen('main').mgr3.mgr3.mgr1.add_widget(Factory.BoxLayout_mainscroll_scroll2())

        Clock.schedule_once(self.change_screen_to_main, .05) 
        Clock.schedule_once(self.check_for_update, 1)       

    def check_for_update(self, *arg):
        # Check for update
        self.version = 1.8
        self.last_version = self.list_version[0]
        if self.last_version != self.version:           
            content = BoxLayout(orientation= 'horizontal')
            bt1 = Button(text= get_display(reshape('خیر')), font_name= 'font/IRANSansXFaNum-Medium.ttf', size_hint=(.5, None), size=('20mm', '6mm'))
            bt1callback = partial(self.update, 'No')
            bt2 = Button(text= get_display(reshape('بلی')), font_name= 'font/IRANSansXFaNum-Medium.ttf', size_hint=(.5, None), size=('20mm', '6mm'))
            bt2callback = partial(self.update, 'Yes')
            content.add_widget(bt1)
            content.add_widget(bt2)
            self.pop = Popup(title= get_display(reshape('آیا مایل به بروزرسانی نرم افزار هستید؟')), title_font = 'font/IRANSansXFaNum-Medium.ttf', content= content,
            title_align= 'center', size_hint=(1, None), height= '20mm',separator_height= 0)
            bt1.bind(on_press= bt1callback)
            bt2.bind(on_press= bt2callback)
            self.pop.open()

    def change_screen_to_main(self, *arg):
        self.root.current = 'main'

    def update(self, *arg):
        self.pop.dismiss()
        if arg[0] == 'Yes':
            MainScreen.main_scroll_gridLayout1_items('', 'bazar')
            self.root.current = 'SplashScreen'

    def on_stop(self):
        return True
    
if __name__== "__main__":
    DigiApp().run()
 
