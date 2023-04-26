from kivy.lang import Builder#
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock, mainthread
from kivy.factory import Factory
from kivy.uix.recycleview import RecycleView
from kivy.uix.popup import Popup
from kivy.uix.image import AsyncImage
from kivy.uix.carousel import Carousel
from kivy.uix.behaviors import ButtonBehavior
from kivy.loader import Loader
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.swiper import MDSwiperItem
from kivymd.uix.button import MDRoundFlatIconButton
from kivy.animation import Animation


import os#
import sys#
from pathlib import Path#
#import pandas as pd #
#from ftpretty import ftpretty#
from functools import partial#
from arabic_reshaper import reshape
from bidi.algorithm import get_display
from time import gmtime, strftime
#from random import sample
import webbrowser
#from mysql import connector
import requests
from threading import Thread

if getattr(sys, "frozen", False):  # bundle mode with PyInstaller
    os.environ["RADIN_ROOT"] = sys._MEIPASS
else:
    os.environ["RADIN_ROOT"] = str(Path(__file__).parent)

global error_list
global items_in_order_screen

items_in_order_screen = []
items_in_category_screen = []
error_list = []

#Window.size = (400, 800)
#Window.softinput_mode = "below_target"

Builder.load_file('main.kv')


class ScrollMain(ScrollView):
    mgr1 = ObjectProperty()
    def on_scroll_stop(self, touch, check_children=True):
        super().on_scroll_stop(touch, check_children=False)

class ScrollView1(ScrollView):
    def on_scroll_move(self, touch):
        super().on_scroll_move(touch)
        touch.ud['sv.handled']['y'] = False 

class ScrollView2(ScrollView):
    def on_scroll_move(self, touch):
        super().on_scroll_move(touch)
        touch.ud['sv.handled']['y'] = False 
 
class ScrollView3(ScrollView):
    material = ObjectProperty()
    made_in = ObjectProperty()
    type = ObjectProperty()
    detail_1 = ObjectProperty()
    detail_2 = ObjectProperty()
    color = ObjectProperty()
    price = ObjectProperty()
    price_off = ObjectProperty()
    off = ObjectProperty()
    sizee = ObjectProperty()
    slide_num = ObjectProperty()
    slide_len = ObjectProperty()

    def on_scroll_move(self, touch):
        super().on_scroll_move(touch)
        touch.ud['sv.handled']['y'] = False 

    def on_touch_down(self, touch):
        self.ids._carousel_.on_touch_down(touch)
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        self.ids._carousel_.on_touch_up(touch)
        return super().on_touch_up(touch)

class ScrollView4(ScrollView):
    # screen_product_scroll3.kv
    def on_scroll_move(self, touch):
        super().on_scroll_move(touch)
        touch.ud['sv.handled']['y'] = False 

class ScrollView5(ScrollView):
    # screen_product_scroll3.kv
    def on_scroll_move(self, touch):
        super().on_scroll_move(touch)
        touch.ud['sv.handled']['y'] = False 

class Carousel_product(Carousel):
    temp = 1
    x1 = 0
    def on_scroll_move(self, touch):
        super().on_scroll_move(touch)
        touch.ud['sv.handled']['y'] = False 

    def on_touch_down(self, touch):
        self.x1 = touch.pos[0]

    def on_touch_up(self, touch):
        self.x2 = touch.pos[0]
        if (self.x1 - self.x2) > 0 and touch.spos[1] > 0.43: 
            if self.index >= len(self.slides) - 1:
                pass
            else:
                self.load_slide((self.slides)[ self.index + 1])
                self.temp = self.temp + 1
                self.parent.parent.slide_num = self.temp
                
        elif (self.x1 - self.x2) < 0 and touch.spos[1] > 0.43: 
            if self.index <= 0:
                pass
            else:
                self.load_slide((self.slides)[ self.index - 1])
                self.temp = self.temp - 1
                self.parent.parent.slide_num = self.index

class Cat(ScrollView):
    # screen_product_scroll3.kv
    def on_scroll_move(self, touch):
        super().on_scroll_move(touch)
        touch.ud['sv.handled']['y'] = False 

class Category_boxlayout(BoxLayout):
    cat = ObjectProperty()
    title_text = ObjectProperty()

class RV_Order(RecycleView):
    dkp = ObjectProperty()
    title = ObjectProperty()
    price_off = ObjectProperty()
    price = ObjectProperty()
    icon_color = ObjectProperty()
    color_fa = ObjectProperty()
    total = ObjectProperty()
    stock = ObjectProperty()
    num_order = ObjectProperty()
    error_text_height = ObjectProperty()
    error_text = ObjectProperty()
    err = ''

    def __init__(self, **kwargs):
        super(RV_Order, self).__init__(**kwargs)
        self.data = [item for item in items_in_order_screen]

    def show_popup(self, args):
        reshaped_loading = reshape("لطفاً شکیبا باشید")
        bidi_loading = get_display(reshaped_loading)
        self.pop_up = Factory.PopupBox()
        self.pop_up.update_pop_up_text(bidi_loading)
        self.pop_up.open()

    def add_to_order(self):

        # If one color not select dont continue
        if self.err == 'True':
            return

        p_code = 0
        # Get the code
        p_code = self.code  #result[0][0]                                                       
                                         
        # Get the stock
        stock = self.stock   #result[0][1]       
        
        # Forming a list to determine if it is available or not in the orders
        a = list(filter(lambda items_in_order_screen: items_in_order_screen['p_code'] == p_code, items_in_order_screen))

        if len(a) == 0:
            items_in_order_screen.append(
                {"DKP": '%s'%(self.dkp),
                'image': 'http://mahdiemadi.ir/Products/%s/%s-0-v_200-h_200-q_90.jpg'%(self.dkp, self.dkp), 
                'title': self.title, 
                'price_off': str(self.price_off), 
                'price': str(self.price), 
                'color_en': self.icon_color, 
                'color_fa': get_display(reshape(self.color_fa)),
                'stock': str(stock),
                'p_code': str(p_code),
                'num_order': '1',          
                'Total': int(self.price.replace(",","")) if  int(self.price_off.replace(",","")) == 0 else int(self.price_off.replace(",","")),  
                'error_text': ''
                }
            )
            import datetime as dt
            # Add orders to the orders table     
            Orderـnumber = strftime("%Y%m%d%H%M%S", gmtime())[3:]   
            f = open('customer_id.txt', 'r')
            self.id = f.read().split('-')[0]   
            
            my_dict = {'code': str(p_code)}
                #'order_num': Orderـnumber, 
                #'code': str(p_code),
                #'num_order': 1,
                #'image': 'http://mahdiemadi.ir/Products/%s/%s-0-v_200-h_200-q_90.jpg'%(self.dkp, self.dkp), 
                #'title': self.title,
                #'total': int(self.price.replace(",","")) if  int(self.price_off.replace(",","")) == 0 else int(self.price_off.replace(",","")),  
                #'color_en': self.icon_color, 
                #'color_fa': get_display(reshape(self.color_fa)),
                #'id': self.id,
                #'total_price': 0
                #}
            # Update stock on database
            url5 = 'http://mahdiemadi.ir/add_to_cart' 
            response = requests.post(url5, json=my_dict)

            self.total = 0
            for i in range(len(items_in_order_screen)):
                self.total += items_in_order_screen[i]['Total'] * int(items_in_order_screen[i]['num_order']) 
            total = self.total
            self.total = f'{total:,}'
            self.data = [item for item in items_in_order_screen]
        else:
            if stock > 0:
                self.add_remove_count('temp' ,'+', p_code)   
        
    def add_remove_count(self, *arg):#arg[1]= +or-or*  agr[2] = code 
        a = list(filter(lambda items_in_order_screen: items_in_order_screen['p_code'] == arg[2], items_in_order_screen)) if arg[1] != '*' else 0
        if arg[1] == '+':
            # Grt new stock from database
            url = 'http://mahdiemadi.ir/get_new_stock_to_add' 
            params = {
                'variable': arg[2]
            }
            response = requests.get(url, params=params)
            result = response.json()
            
            # Increasing the number of orders if it does not exceed the stock and it does not zero 
            if  result != [] and result[0][0] > 0:
                if int(a[0]['num_order']) != 0:
                    b = int(a[0]['num_order']) + 1
                else: 
                    b = 0
            else:
                b = int(a[0]['num_order'])
                return

            a[0]['num_order'] = str(b)

            # Update stock on database
            url = 'http://mahdiemadi.ir/orders_balance_add' 
            params = {
                'variable1': arg[2],
            }
            response = requests.post(url, params=params)
            #result = response.json()

        elif arg[1] == '-':

            if int(a[0]['num_order']) > 1:
                # Decreasing the number of orders if it does not exceed the stock
                b = int(a[0]['num_order']) - 1 
                a[0]['num_order'] = str(b)

            else:
                index = (next((i for i, item in enumerate(items_in_order_screen) if item["p_code"] == arg[2]), None))
                del items_in_order_screen[index]

            # Update stock on database
            url = 'http://mahdiemadi.ir/orders_balance_remove' 
            params = {
                'variable1': arg[2],
            }
            response = requests.get(url, params=params)

        elif arg[1] == '*':
            if error_list == []:
                items_in_order_screen.clear()
            else: 
                error_list.clear()
     
        self.total = 0
        for i in range(len(items_in_order_screen)):
            self.total += items_in_order_screen[i]['Total'] * int(items_in_order_screen[i]['num_order']) 
        total = self.total
        self.total = f'{total:,}'

        self.data = [item for item in items_in_order_screen]
        self.refresh_from_data()

    def check_registration(self, *arg):
        # Check if the cart is empty or not
        if len(items_in_order_screen) == 0:
            self.pop_up.dismiss()
            content = Button(text= get_display(reshape('بازگشت')), font_name= 'font/IRANSansXFaNum-Medium.ttf', size_hint=(1, None), size=('20mm', '6mm'))
            pop = Popup(title= get_display(reshape('سبد خالی است!')), title_font = 'font/IRANSansXFaNum-Medium.ttf', content= content,
            title_align= 'center', size_hint=(None, None), size=(self.width , '20mm'),separator_height= 0)
            content.bind(on_release=pop.dismiss)
            pop.open()
        else:

            # Checking if the host has stock or not
            for i in range(len(items_in_order_screen)):
                # Grt new stock from database
                url = 'http://mahdiemadi.ir/check_registration_1' 
                params = {
                    'variable': items_in_order_screen[i]['p_code']
                }
                response = requests.get(url, params=params)
                result_host = response.json()
                
                if int(items_in_order_screen[i]['num_order']) <= result_host[0][0]:
                    pass
                else:
                    error_list.append([items_in_order_screen[i]['p_code'], result_host[0][0]])
            if error_list == []:
                Orderـnumber = strftime("%Y%m%d%H%M%S", gmtime())[3:]
                self.pop_up.dismiss()
                l = BoxLayout(orientation= 'vertical')
                l.add_widget(Label(text= get_display(reshape('شماره سفارش:  %s'%(Orderـnumber))), size_hint_y= None, height= '6mm', halign= 'right', font_name='font/IRANSansXFaNum-Medium.ttf'))
                l.add_widget(Label(text= get_display(reshape('مشاهده سفارش ها در بخش \'فروشگاه من\'\n ')), size_hint_y= None, height= '12mm', font_name='font/IRANSansXFaNum-Medium.ttf'))
                l.add_widget(Label(text= get_display(reshape('با شما تماس گرفته خواهد شد')), size_hint_y= None, height= '6mm', font_name='font/IRANSansXFaNum-Medium.ttf'))
                content = l
                content.opacity = 0
                pop = Popup(title= get_display(reshape('از حسن انتخاب شما سپاسگزاریم')), title_font = 'font/IRANSansXFaNum-Medium.ttf', content= content,
                title_align= 'center', size_hint=(None, None), size=(self.width , '40mm'),separator_height= 5)
                pop.open()
                Animation(opacity = 1, duration = 1).start(content)

                # Update stock on database & Add orders to the orders table 
                total_price = 0
                for i in range(len(items_in_order_screen)): 
                    total_price += items_in_order_screen[i]['Total'] * int(items_in_order_screen[i]['num_order'])

                    # Add orders to the orders table               
                    my_dict = {
                        'order_num': Orderـnumber, 
                        'code': items_in_order_screen[i]['p_code'],
                        'num_order': items_in_order_screen[i]['num_order'],
                        'date_time': '',#strftime("%Y/%m/%d_%H%M%S", gmtime()), 
                        'image': items_in_order_screen[i]['image'], 
                        'title': items_in_order_screen[i]['title'], 
                        'total': items_in_order_screen[i]['Total'], 
                        'color_en': items_in_order_screen[i]['color_en'], 
                        'color_fa': items_in_order_screen[i]['color_fa'],
                        'id': self.id,
                        'total_price': '%s'%(total_price)
                        }

                    # Update stock on database
                    url = 'http://mahdiemadi.ir/check_registration_2' 
                    response = requests.post(url, json=my_dict)
                                                        
            else:
                for i in range(len(error_list)):
                    filter_list = list(filter(lambda items_in_order_screen: items_in_order_screen['p_code'] == error_list[i][0], items_in_order_screen))
                    filter_list[0]['num_order'] = str(error_list[i][1])
                    filter_list[0]['stock'] = str(error_list[i][1])
                    filter_list[0]['error_text'] = get_display(reshape('موجودی ندارد')) if error_list[i][1] == 0 else get_display(reshape('حداکثر موجودی تغییر کرده است'))
                self.pop_up.dismiss()

            self.add_remove_count('*', '*', '*', '*')

class Det_order_boxLayout(BoxLayout):
    order_num = ObjectProperty()
    receiver = ObjectProperty()
    tel = ObjectProperty()
    address = ObjectProperty()
    total = ObjectProperty()

class Det_order_box_box(BoxLayout):
    title = ObjectProperty()
    image = ObjectProperty()
    total = ObjectProperty()
    color_en = ObjectProperty()
    color_fa = ObjectProperty()
    num_order = ObjectProperty()
    num_order = ObjectProperty()

class ImageButton(ButtonBehavior, AsyncImage):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class RV_Category(RecycleView):
    #ObjectProperty()

    def __init__(self, **kwargs):
        super(RV_Category, self).__init__(**kwargs)
        #self.data = [{'text': str(x)} for x in range(100)]
        self.data = [item for item in items_in_category_screen]               

class MySwiper(MDSwiperItem):
    source = ObjectProperty()

class color_buttom(MDRoundFlatIconButton):
    title= ObjectProperty()
    ic_color= ObjectProperty()

class Product(Screen):
    dkp = ObjectProperty()
    title = ObjectProperty()
    price = ObjectProperty()
    price_off = ObjectProperty()
    off = ObjectProperty()
    icon = ObjectProperty()
    
class Search(Screen):
    source = ObjectProperty()

class Button_scroll5(ButtonBehavior, AsyncImage):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    image_source = ObjectProperty()

class BoxLayout_mainscroll_scroll1(ButtonBehavior, BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class BoxLayout_mainscroll_scroll2(ButtonBehavior, BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class MyBoxLayoutCat(ButtonBehavior, BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class Off(Screen):
    title = ObjectProperty() 

class PopupBox(Popup):
    pop_up_text = ObjectProperty()
    def update_pop_up_text(self, p_message):
        self.title = p_message
        self.title_font = 'font/IRANSansXFaNum-Medium.ttf'

class WrappedLabel(Label):
    # Based on Tshirtman's answer
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(
            width=lambda *x:
            self.setter('text_size')(self, (self.width, None)),
            texture_size=lambda *x: self.setter('height')(self, self.texture_size[1]))

class Account(Screen):
    name= ObjectProperty('account')
    mgr1= ObjectProperty('_bot_nav')

class Off(Screen):
    pass

class MainScreen(ScreenManager):
    category_dict = {'H': 'کلاه و نقاب', 'SH': 'قمقمه و شیکر', 'SW': 'لوازم شنا', 'GL': 'دستکش', 'R': 'طناب', 'PI': 'پیلاتس و بدنسازی'}
    grouping_type = ''
    # For return screen from sign un to product
    previous_screen = ''
    icon_color = ''
    color_fa = ''
    kv = []
    # Deine back bottom in android
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        Window.bind(on_keyboard=self.on_key)

    def on_key(self, window, key, *args):
        if key == 27:  # the esc key
            if self.current_screen.name == "product" or  self.current_screen.name == 'search' or  self.current_screen.name == 'signup' or  self.current_screen.name == 'det_order':
                self.current = self.active_page
                self.get_screen('search').source= ''
                return True  # exit the app from this page
            elif self.current_screen.name == "order" or self.current_screen.name == "off" or self.current_screen.name == "account":
                self.current = 'main'
                return True
            elif self.current_screen.name == "grouping" or self.current_screen.name == 'privacy':
                if self.active_page == 'account':
                    self.current = 'account'
                else:
                    self.current = 'main'
                return True
            elif self.current_screen.name == "main":
                # create content and add to the popup
                content = BoxLayout(orientation= 'horizontal')
                bt1 = Button(text= get_display(reshape('خیر')), font_name= 'font/IRANSansXFaNum-Medium.ttf', size_hint=(.5, None), size=('20mm', '6mm'))
                bt2 = Button(text= get_display(reshape('بلی')), font_name= 'font/IRANSansXFaNum-Medium.ttf', size_hint=(.5, None), size=('20mm', '6mm'))
                #self.ids['bt2'] = bt2
                content.add_widget(bt1)
                content.add_widget(bt2)
                pop = Popup(title= get_display(reshape('آیا از خروج اطمینان دارید؟')), title_font = 'font/IRANSansXFaNum-Medium.ttf', content= content,
                title_align= 'center', size_hint=(None, None), size=(self.width , '20mm'),separator_height= 0)
                bt1.bind(on_press= pop.dismiss)
                bt2.bind(on_press= pop.dismiss)
                bt2.bind(on_press= self.exit_app)
                pop.open() 
                #stopTouchApp()

                return True

    def exit_app(self, *arg):
        MDApp.get_running_app().stop()
        Window.close()

    def reload(self):
        self.current = 'main'

    def open_product_screen(self, DKP, arg): 

        try:
            DKP = int(DKP.split('/')[4])
        except:
            if type(DKP) == float:
                DKP = int(DKP)

        # Get data from APIs 
        url3 = 'http://mahdiemadi.ir/api_3' 

        # Define the request parameters
        params = {'variable': DKP}

        try:
            response3 = requests.get(url3, params=params, timeout=2)            
        except:
            self.change_screen('Err_connection.kv', 'Factory.Err_connection()', 'Err_connection.kv' )
            MDApp.get_running_app().Err_connection()
            try:
                if self.pop_up:
                    self.pop_up.dismiss()
            except: 
                pass
            return

        result = response3.json()

        self.color_price = {}
        for sub_lst in result:
            self.color_price[sub_lst[10]] = [sub_lst[5], sub_lst[6], sub_lst[7], sub_lst[1], sub_lst[4]]#price, price_off, off, code, stock

        sum_stock = sum([row[4] for row in result])

        if sum_stock > 0: # check for sum stock
            self.get_screen('product').mgr1.mgr2.scroll_x = 1
            self.get_screen('product').mgr1.mgr3.scroll_x = 1
            self.get_screen('product').dkp = DKP
            #self.get_screen('product').mgr1.sizee = 'hhhhhhhhhhhhhhhhhhhhhhhh'#dataframe_products[(dataframe_products['DKP'] == DKP) ]['size'].values[0]
            self.get_screen('product').icon = "cards-heart-outline"
            # Delete all carousel's children
            try:
                self.get_screen('product').mgr1.ids._carousel_.clear_widgets()
            except:
                pass
            # Add title
            self.get_screen('product').title = result[0][0]
            # Calculate the number of photos
            try:
                # Get data from APIs 
                url = 'http://mahdiemadi.ir/count_files' 

                # Define the request parameters
                params = {'variable': DKP}

                try:
                    response = requests.get(url, params=params, timeout=2)            
                except:
                    self.change_screen('Err_connection.kv', 'Factory.Err_connection()', 'Err_connection.kv' )
                    MDApp.get_running_app().Err_connection()
                    try:
                        if self.pop_up:
                            self.pop_up.dismiss()
                    except: 
                        pass
                    return

                No_of_files = response.json()
                #f = ftpretty('ftp.mahdiemadi.ir', 'test@mahdiemadi.ir', 'C9{c%nJIm)El', timeout=2)
                #No_of_files = len(f.list('/public_html/Products/%s'%(DKP))) - 3
            except:
                Clock.schedule_once(partial(self.change_screen, 'screen_Err.kv', 'Factory.Err_connection()', 'Err_connection'), .5)
                self.current = 'Err_connection'
                if self.pop_up:
                    self.pop_up.dismiss()
                return
            # Add photos to carousel
            self.get_screen('product').mgr1.slide_len = No_of_files
            self.get_screen('product').mgr1.slide_num = '1'
            self.get_screen('product').mgr1.ids._carousel_.temp = 1
            for i in range(No_of_files):
                self.get_screen('product').mgr1.ids._carousel_.add_widget(AsyncImage(source= 'http://mahdiemadi.ir/Products/%s/%s-%s.jpg'%(DKP, DKP, i), size_hint= (1, 1), allow_stretch= True ))
            self.get_screen('product').mgr1.ids._carousel_.load_slide((self.get_screen('product').mgr1.ids._carousel_.slides)[0])
            # Creating a list of colors in Farsi and English
            list_colors = [row[10] for row in result]
            list_colors_fa = [row[9] for row in result]
            # Calculate the number of colors in stock
            self.get_screen('product').mgr1.mgr1.cols= len(list_colors)
            self.number_of_color= len(list_colors)
            # Delete all color_scrollview's children
            try:
                self.get_screen('product').mgr1.mgr1.clear_widgets()
            except: 
                pass
            # Add colors button to scrollview3
            for i in range(len(list_colors)):
                self.get_screen('product').mgr1.mgr1.add_widget(Factory.color_buttom(title= str(list_colors_fa[i]), ic_color= list_colors[i]))
            # Add the first color label
            self.get_screen('product').mgr1.color= '' 
            # Add material, country of manufacture and product type & details
            self.get_screen('product').mgr1.material= result[0][11]                
            self.get_screen('product').mgr1.made_in= result[0][12]                  
            self.get_screen('product').mgr1.type= result[0][13]                          
            self.get_screen('product').mgr1.detail_1= result[0][14]                               
            self.get_screen('product').mgr1.detail_2= result[0][15]      

            # Add first price & price_off & off
            self.get_screen('product').icon_color = list_colors[0]#[len(list_colors) - 1]
            #a = self.get_screen('product').icon_color
            price = result[0][5]                           
            self.get_screen('product').price = f'{price:,}'
            price_off = result[0][6]              
            self.get_screen('product').price_off = f'{price_off:,}'
            self.get_screen('product').off = result[0][7]                  
            
            # Add similar product
            ## Drop all children
            try:
                self.get_screen('product').mgr1.mgr2.ids._GridLayout.clear_widgets()
            except:
                pass
            ## Get categories
            cat = result[0][2]  

            # Get data from APIs 
            url3 = 'http://mahdiemadi.ir/api_4' 

            # Define the request parameters
            params = {'variable1': DKP, 'variable2': cat }

            try:
                response3 = requests.get(url3, params=params, timeout=2)            
            except:
                self.change_screen('Err_connection.kv', 'Factory.Err_connection()', 'Err_connection.kv' )
                MDApp.get_running_app().Err_connection()
                try:
                    if self.pop_up:
                        self.pop_up.dismiss()
                except: 
                    pass
                return

            result = response3.json()

            ## Create list of DKPs in our category without repeat
            list_cat = [row[0] for row in result]                          
            for i in range(len(list_cat)):
                self.get_screen('product').mgr1.mgr2.ids._GridLayout.add_widget(Factory.Button_scroll5(image_source= 'http://mahdiemadi.ir/Products/%s/%s-0-v_200-h_200-q_90.jpg'%(list_cat[i], list_cat[i])))
            # Set current screen
            self.current= "product"
            try:
                if self.pop_up:
                    self.pop_up.dismiss()
            except: 
                pass

            self.get_screen('product').mgr1.scroll_y=1
        else:
            if self.pop_up:
                self.pop_up.dismiss()
            # create content and add to the popup
            content = Button(text= get_display(reshape('بازگشت')), font_name= 'font/IRANSansXFaNum-Medium.ttf', size_hint=(1, None), size=('20mm', '6mm'))
            pop = Popup(title= get_display(reshape('موجودی کالا به اتمام رسیده است.')), title_font = 'font/IRANSansXFaNum-Medium.ttf', content= content,
            title_align= 'center', size_hint=(None, None), size=(self.width , '20mm'),separator_height= 0)
            # bind the on_press event of the button to the dismiss function
            content.bind(on_press=pop.dismiss)
            pop.open()

    def Price_change_with_variety_change(self, icon_color, color_fa):
        RV_Order.err = ''
        self.icon_color = icon_color
        self.color_fa = color_fa

        self.color_price#price, price_off, off, code, stock
        price = self.color_price[icon_color][0]                   
        self.get_screen('product').price = f'{price:,}'
        price_off = self.color_price[icon_color][1]                               
        self.get_screen('product').price_off = f'{price_off:,}'
        self.get_screen('product').off = self.color_price[icon_color][2] 
        self.get_screen('product').code = self.color_price[icon_color][3] 
        self.get_screen('product').stock = self.color_price[icon_color][4]                             

    def Adding_values_to_the_order_screen(self):
        # Checking the registration 
        if os.path.isfile('customer_id.txt'):
            pass
        else:
            self.previous_screen = 'product'
            content = Button(text= get_display(reshape('ثبت نام')), font_name= 'font/IRANSansXFaNum-Medium.ttf', size_hint=(1, None), size=('20mm', '6mm'))
            pop = Popup(title= get_display(reshape('لطفاٌ ابتدا ثبت نام کنید')), title_font = 'font/IRANSansXFaNum-Medium.ttf', content= content,
            title_align= 'center', size_hint=(None, None), size=(self.width , '20mm'),separator_height= 0)
            content.bind(on_press=self.change_screen_signup)
            content.bind(on_release=pop.dismiss)
            pop.open()
            return

        if self.icon_color  == '':
            RV_Order.err = 'True'
            content = Button(text= get_display(reshape('بازگشت')), font_name= 'font/IRANSansXFaNum-Medium.ttf', size_hint=(1, None), size=('20mm', '6mm'))
            pop = Popup(title= get_display(reshape('لطفاً یک رنگ/سایز انتخاب نمایید')), title_font = 'font/IRANSansXFaNum-Medium.ttf', content= content,
            title_align= 'center', size_hint=(None, None), size=(self.width , '20mm'),separator_height= 0)
            # bind the on_press event of the button to the dismiss function
            content.bind(on_press=pop.dismiss)
            pop.open()
            return

        self.get_screen('order').mgr2.dkp = self.get_screen('product').dkp
        self.get_screen('order').mgr2.title = self.get_screen('product').title
        self.get_screen('order').mgr2.color_fa = self.get_screen('product').mgr1.color
        a = self.get_screen('product').icon_color
        self.get_screen('order').mgr2.icon_color = a
        self.get_screen('order').mgr2.price_off = self.get_screen('product').price_off
        self.get_screen('order').mgr2.price = self.get_screen('product').price
        self.get_screen('order').mgr2.price_off = self.get_screen('product').price_off
        self.get_screen('order').mgr2.price = self.get_screen('product').price
        self.get_screen('order').mgr2.icon_color = self.icon_color
        self.get_screen('order').mgr2.color_fa = self.color_fa
        self.get_screen('order').mgr2.code = self.get_screen('product').code
        self.get_screen('order').mgr2.stock = self.get_screen('product').stock


        #RV_Order.add_to_order('dfgdfg')
        self.icon_color = ''

    def change_screen_signup(self, *arg):
        # load acount and signup kv file and add screen to screen manager
        self.change_screen('screen_account_sign_up.kv', 'Factory.Sign_up()', 'signup')
        self.change_screen('screen_account.kv', 'Factory.Account()', 'account')
        # Opening the registration form if not registered
        self.get_screen('account').mgr1.canvas.after.get_group('a')[0].source='img/App/nav1.jpg'
        self.get_screen('account').text1 = '-'
        self.current= 'signup' 

    def main_scroll_gridLayout1_items(self,name):
        if name == 'instagram':
            webbrowser.open('https://www.instagram.com/radin__sprt/')
        elif name == 'digikala':
            webbrowser.open('https://www.digikala.com/seller/aygzu/')
        elif name == 'digistal':
            webbrowser.open('https://www.digistyle.com/')
        elif name == 'weblog':
            webbrowser.open('https://radinsport.blog.ir/')
        elif name == 'contact_us':
            webbrowser.open('https://www.digikala.com/seller/aygzu/')
        elif name == 'kalands':
            webbrowser.open('https://www.kalands.ir/seller/aygzu/')
        elif name == 'bazar':
            webbrowser.open('https://cafebazaar.ir/app/com.radinsport.radinsport')

    def changeـheartـicon(self):
        self.get_screen('product').icon = 'cards-heart'

    def open_category(self, cat, arg):

        self.get_screen('off').mgr2.scroll_y=1 
        self.items_in_category_screen = []

        try:
            self.get_screen('off').title= get_display(reshape(self.category_dict[cat]))
        except:
            # list out keys and values separately
            key_list = list(self.category_dict.keys())
            val_list = list(self.category_dict.values())

            # get position of value 2 in second list
            val_list = [reshape(i) for i in val_list]
            # Checking whether the request came from the grouping page or from the orders report?
            try:
                position = val_list.index(get_display(reshape(cat)))
            except:
                self.see_order_detail(cat)
                return
            # get key with position calculated above
            cat = key_list[position]
            self.get_screen('off').title= get_display(reshape(self.category_dict[cat]))

        # Get data from APIs 
        url = 'http://mahdiemadi.ir/open_category' 

        # Define the request parameters
        params = {'variable': cat}

        try:
            response3 = requests.get(url, params=params, timeout=2)            
        except:
            self.change_screen('Err_connection.kv', 'Factory.Err_connection()', 'Err_connection.kv' )     
            MDApp.get_running_app().Err_connection()
            try:
                if self.pop_up:
                    self.pop_up.dismiss()
            except: 
                pass
            return

        result = response3.json()

        temp_len = len(result)
        for i in range(temp_len):
            title = result[i][1]
            if len(title) > 20:
                title = '...' +title[-17:] 
            price_off = result[i][6]
            price_off = f'{price_off:,}'
            price = result[i][4]
            price = f'{price:,}'

            self.items_in_category_screen.append(
                {'title1': title,
                'source1': 'http://mahdiemadi.ir/Products/%s/%s-0-v_200-h_200-q_90.jpg'%(result[i][0], result[i][0]),
                  'detail_3_1': get_display(reshape(result[i][2])),
                    'detail_4_1': get_display(reshape(result[i][3])),
                      'price1': price,
                        'off1': result[i][5],
                          'price_off1': price_off}
            )
        RV_Category.data = [item for item in self.items_in_category_screen]
        self.get_screen('off').mgr2.refresh_from_data()
        self.current = "off"
        #self.active_page = 'off'
        self.active_page_variable = cat

        try:
            if self.pop_up:
                self.pop_up.dismiss()
        except: 
            pass

    def Search_in_search_bar(self, word_encoded, arg):
        # Decode the input text from UTF-8
        word = word_encoded#.decode('utf-8')# to string

        # Get data from APIs 
        url = 'http://mahdiemadi.ir/Search_in_search_bar' 

        # Define the request parameters
        params = {'variable': word}

        try:
            response3 = requests.get(url, params=params, timeout=2)            
        except:
            self.change_screen('Err_connection.kv', 'Factory.Err_connection()', 'Err_connection.kv' )
            MDApp.get_running_app().Err_connection()
            try:
                if self.pop_up:
                    self.pop_up.dismiss()
            except: 
                pass
            return

        result = response3.json()

        if result == []:
            self.get_screen('search').source= 'img/App/not_find.jpg'
            try:
                if self.pop_up:
                    self.pop_up.dismiss()
            except: 
                pass
        else:
            self.open_category(result[0][0], '')

    def show_keyboard(self, arg):
        self.get_screen('search').ids._MDTextFieldPersian2.focus= True
    
    def open_grouping(self, arg):

        self.grouping_type = 'grouping'
        self.get_screen('grouping').mgr2.clear_widgets()
        self.get_screen('grouping').ids._sc.scroll_y=1 

        # Forming a list of category dictionary keys
        list_ = list(self.category_dict.keys())
        for i in range(len(list_)):
            # Get data from APIs 
            url = 'http://mahdiemadi.ir/open_grouping' 

            # Define the request parameters
            params = {'variable': list_[i]}

            try:
                response3 = requests.get(url, params=params, timeout=2)            
            except:
                self.change_screen('Err_connection.kv', 'Factory.Err_connection()', 'Err_connection.kv' ) 
                MDApp.get_running_app().Err_connection()
                try:
                    if self.pop_up:
                        self.pop_up.dismiss()
                except: 
                    pass
                return

            DKP_list = response3.json()

            if DKP_list == []:
                continue

            category_boxlayout = Category_boxlayout(size_hint_y= None, height= '27mm',
                    cat= get_display(reshape(self.category_dict[list_[i]])), title_text= get_display(reshape('مشاهده همه'))
                )
            cat_ = Cat()

            for j in range(len(DKP_list) if len(DKP_list) < 5 else 5):
                cat_.ids._grid.add_widget(AsyncImage(
                source= 'http://mahdiemadi.ir/Products/%s/%s-%s-v_200-h_200-q_90.jpg'%(str(int(DKP_list[j][0])), str(int(DKP_list[j][0])), 0),
                size_hint= (None, None), width= '15mm', height= '15mm', allow_stretch= True
                    ))

            category_boxlayout.add_widget(cat_)
            category_boxlayout.add_widget(Factory.Widget1())
            category_boxlayout.add_widget(Factory.Widget1())

            self.get_screen('grouping').mgr2.add_widget(category_boxlayout)
        try:
            if self.pop_up:
                self.pop_up.dismiss()
        except: 
            pass

    def show_popup(self, args):        
        reshaped_loading = ''
        #reshaped_loading = reshape("لطفاً شکیبا باشید")
        bidi_loading = get_display(reshaped_loading)
        self.pop_up = Factory.PopupBox()
        self.pop_up.update_pop_up_text(bidi_loading)
        self.pop_up.open()
    
    def open_account_xls(self, *args):
        try:
            f = open('customer_id.txt', 'r')
            name = f.read().split('-')[1]        
            self.get_screen('account').text1 = name      
        except:
            self.get_screen('account').text1 = '-'

    def sign_up(self):
        if self.get_screen('signup').ids._name.text == '' or \
        self.get_screen('signup').ids._last_name.text == '' or \
        self.get_screen('signup').ids._mobile_number.text == '' or \
        self.get_screen('signup').ids._address.text == '' or \
        self.get_screen('signup').ids._address1.text == '' or \
        self.get_screen('signup').ids._address2.text == '' or \
        self.get_screen('signup').ids._address3.text == '' or \
        self.get_screen('signup').ids._postal_code.text == '':

            # create content and add to the popup
            content = Button(text= get_display(reshape('بازگشت')), font_name= 'font/IRANSansXFaNum-Medium.ttf', size_hint=(1, None), size=('20mm', '6mm'))
            pop = Popup(title= get_display(reshape('لطفاً موارد الزامی پر شود')), title_font = 'font/IRANSansXFaNum-Medium.ttf', content= content,
            title_align= 'center', size_hint=(None, None), size=(self.width , '20mm'),separator_height= 0)
            # bind the on_press event of the button to the dismiss function
            content.bind(on_press=pop.dismiss)
            pop.open()

        else:
            try:
                f = open('customer_id.txt', 'r')
                customer_id = f.read().split('-')[0]        
            except:

                # Get data from APIs 
                url = 'http://mahdiemadi.ir/sign_up_1' 

                try:
                    response3 = requests.get(url, timeout=2)            
                except:
                    self.change_screen('Err_connection.kv', 'Factory.Err_connection()', 'Err_connection.kv' )         
                    MDApp.get_running_app().Err_connection()
                    try:
                        if self.pop_up:
                            self.pop_up.dismiss()
                    except: 
                        pass
                    return

                result = response3.json()
                
                try:
                    customer_id = int(result[-1][0]) + 1
                    
                except:   
                    customer_id = 1001

            # Create Personal_Information dict
            my_dict = {
                'name': '%s'%(self.get_screen('signup').ids._name.text),
                'last_name': '%s'%(self.get_screen('signup').ids._last_name.text),
                'mobile_num': '%s'%(self.get_screen('signup').ids._mobile_number.text),
                'home_num': '%s'%(self.get_screen('signup').ids._home_number.text),
                'address': '%s, %s, %s, %s'%(
                                self.get_screen('signup').ids._address.text,
                                self.get_screen('signup').ids._address1.text,
                                self.get_screen('signup').ids._address2.text,
                                self.get_screen('signup').ids._address3.text,
                ),
                'postal_code': '%s'%(self.get_screen('signup').ids._postal_code.text),
                'email': '%s'%(self.get_screen('signup').ids._email.text),
                'id': '%s'%(customer_id),
            }
            
            # Add data to customers database
            url = 'http://mahdiemadi.ir/sign_up_2' 
            response = requests.post(url, json=my_dict)
            print(response.text)
               
            if self.previous_screen == 'product':
                self.current= 'product'
            else:
                self.current= 'account'

            # Add customer_id to txt file in app directory

            ## define the file path and name
            file_path = os.path.join(os.getcwd(), 'customer_id.txt')

            ## define the string to be written to the file
            my_string = '%s-%s'%(customer_id, my_dict['name'])

            ## open the file in write mode
            with open(file_path, 'w') as file:
                # write the string to the file
                file.write(my_string)
            
            # For return screen from sign un to product
            self.previous_screen = ''
            
    def delete_Personal_Information(self):
        # create content and add to the popup
        content = BoxLayout(orientation= 'horizontal')
        bt1 = Button(text= get_display(reshape('خیر')), font_name= 'font/IRANSansXFaNum-Medium.ttf', size_hint=(.5, None), size=('20mm', '6mm'))
        bt2 = Button(text= get_display(reshape('بلی')), font_name= 'font/IRANSansXFaNum-Medium.ttf', size_hint=(.5, None), size=('20mm', '6mm'))
        #self.ids['bt2'] = bt2
        content.add_widget(bt1)
        content.add_widget(bt2)
        pop = Popup(title= get_display(reshape('آیا از حذف کامل مشخصات اطمینان دارید؟')), title_font = 'font/IRANSansXFaNum-Medium.ttf', content= content,
        title_align= 'center', size_hint=(None, None), size=(self.width , '20mm'),separator_height= 0)
        bt1.bind(on_press= pop.dismiss)
        bt2.bind(on_press= self.delete_Personal_Information_OK)
        bt2.bind(on_press= pop.dismiss)
        bt2.bind(on_press= self.open_account_xls)
        pop.open()

    def delete_Personal_Information_OK(self, *args):
        os.remove("customer_id.txt")
        self.current= 'main'

    def load_account_data(self):
        # Get id of customer
        f = open('customer_id.txt', 'r')
        customer_id = f.read().split('-')[0]        

        # Get data from APIs 
        url = 'http://mahdiemadi.ir/load_account_data' 

        # Define the request parameters
        params = {'variable': customer_id}

        try:
            response3 = requests.get(url, params=params, timeout=2)            
        except:
            self.change_screen('Err_connection.kv', 'Factory.Err_connection()', 'Err_connection.kv' )
            MDApp.get_running_app().Err_connection()
            try:
                if self.pop_up:
                    self.pop_up.dismiss()
            except: 
                pass
            return

        result = response3.json()

        self.get_screen('signup').ids._name.text = result[0][0]                   #str(self.df_account['Name'][0])
        self.get_screen('signup').ids._last_name.text = result[0][1]              #str(self.df_account['Last name'][0])
        self.get_screen('signup').ids._mobile_number.text = result[0][2]                       #str(self.df_account['Mobile number'][0])
        self.get_screen('signup').ids._home_number.text = result[0][3]                           #str(self.df_account['Home number'][0])
        self.get_screen('signup').ids._address.text = result[0][4].split(', ')[0]
        self.get_screen('signup').ids._address1.text = result[0][4].split(', ')[1]
        self.get_screen('signup').ids._address2.text = result[0][4].split(', ')[2]
        self.get_screen('signup').ids._address3.text = result[0][4].split(', ')[3]
        self.get_screen('signup').ids._postal_code.text = result[0][5]                          #  str(self.df_account['Postal code'][0])
        self.get_screen('signup').ids._email.text = result[0][6]                                #str(self.df_account['Email'][0])

    def clear_account_data(self):
        self.get_screen('signup').ids._name.str = ''
        self.get_screen('signup').ids._name.text = ''
        self.get_screen('signup').ids._last_name.str = ''
        self.get_screen('signup').ids._last_name.text = ''
        self.get_screen('signup').ids._mobile_number.str = ''
        self.get_screen('signup').ids._mobile_number.text = ''
        self.get_screen('signup').ids._home_number.str = ''
        self.get_screen('signup').ids._home_number.text = ''
        self.get_screen('signup').ids._address.str = ''
        self.get_screen('signup').ids._address.text = ''
        self.get_screen('signup').ids._postal_code.str = ''
        self.get_screen('signup').ids._postal_code.text = ''
        self.get_screen('signup').ids._email.str = ''
        self.get_screen('signup').ids._email.text = ''

    def see_orders(self):

        self.active_page = 'account'
        self.get_screen('grouping').mgr2.clear_widgets()
        self.get_screen('grouping').mgr1.canvas.after.get_group('a')[0].source='img/App/nav1.jpg'
        self.get_screen('grouping').ids._sc.scroll_y=1 

        # Get id of customer
        f = open('customer_id.txt', 'r')
        self.customer_id = f.read().split('-')[0]        

        # Get data from APIs 
        url = 'http://mahdiemadi.ir/see_orders' 

        # Define the request parameters
        params = {'variable': self.customer_id}

        try:
            response3 = requests.get(url, params=params, timeout=2)            
        except:
            self.change_screen('Err_connection.kv', 'Factory.Err_connection()', 'Err_connection.kv' )
            MDApp.get_running_app().Err_connection()
            try:
                if self.pop_up:
                    self.pop_up.dismiss()
            except: 
                pass
            return

        results = response3.json()

        if results == []:
            content = Button(text= get_display(reshape('بازگشت')), font_name= 'font/IRANSansXFaNum-Medium.ttf', size_hint=(1, None), size=('20mm', '6mm'))
            pop = Popup(title= get_display(reshape('سفارشی ثبت نشده است!')), title_font = 'font/IRANSansXFaNum-Medium.ttf', content= content,
            title_align= 'center', size_hint=(None, None), size=(self.width , '20mm'),separator_height= 0)
            content.bind(on_release=pop.dismiss)
            pop.open()
            return


        list_orders = list(set([item[0] for item in results]))
        list_orders.sort()

        # Forming a list of order_numbers
        for i in range(len(list_orders)):
            category_boxlayout = Category_boxlayout(size_hint_y= None, height= '27mm',
                    cat= get_display(reshape('شماره سفارش: %s'%(list_orders[i]))), title_text= get_display(reshape('جزییات سفارش'))
                )
            cat_ = Cat()

            # Add images to orders  
            list_image = [row[1] for row in results if row[0] == list_orders[i]]

            for j in range(len(list_image) if len(list_image) < 5 else 5):
                cat_.ids._grid.add_widget(AsyncImage(
                source= list_image[j],
                size_hint= (None, None), width= '15mm', height= '15mm', allow_stretch= True
                    ))

            category_boxlayout.add_widget(cat_)
            category_boxlayout.add_widget(Factory.Widget1())
            category_boxlayout.add_widget(Factory.Widget1())

            self.get_screen('grouping').mgr2.add_widget(category_boxlayout)

        self.current = 'grouping' if list_orders != [] else None

        try:
            if self.pop_up:
                self.pop_up.dismiss()
        except: 
            pass

    def see_order_detail(self, *arg):
        self.active_page = 'grouping'
        self.get_screen('det_order').mgr1.clear_widgets()
        order_number = arg[0].split(':')[0].strip()

        # Get data from APIs 
        url = 'http://mahdiemadi.ir/see_order_detail' 

        # Define the request parameters
        params = {'variable1': order_number, 'variable2': self.customer_id}

        try:
            response3 = requests.get(url, params=params, timeout=2)            
        except:
            self.change_screen('Err_connection.kv', 'Factory.Err_connection()', 'Err_connection.kv' )
            MDApp.get_running_app().Err_connection()
            try:
                if self.pop_up:
                    self.pop_up.dismiss()
            except: 
                pass
            return

        results = response3.json()
        print(results['order'][0][0], 0)
        print(results['order'][0][1], 1)
        print(results['order'][0][2], 2)
        print(results['order'][0][3], 3)
        print(results['order'][0][4], 4)
        print(results['order'][0][5], 5)
        print(results['order'][0][6], 6)
        print(results['order'][0][7], 7)
        print(results['order'][0][8], 8)
        print(results['order'][0][9], 9)
        print(results['order'][0][10], 10)
        print(results['order'][0][11], 11)
        
        address1 = results['customer'][0][3].split(', ')[1:3]
        address2 = results['customer'][0][3].split(', ')[3:4] 
        
        tot = 0
        for item in results['order']:
            tot += item[2] * item[6]

        det_order_boxLayout = Det_order_boxLayout(
            order_num='%s'%(order_number), 
            receiver= '%s %s'%(get_display(reshape(results['customer'][0][0])), get_display(reshape(results['customer'][0][1]))),
            tel= int(results['customer'][0][2]), 
            address= get_display(reshape('%s, %s\n%s\n%s'
                        %(address1[1], address1[0], address2[0], results['customer'][0][4]))),
            total= f'{tot:,}', 
        )
        for i in range(len(results['order'])):
            price = results['order'][i][6]      
            det_order_box_box = Det_order_box_box(
                title= results['order'][i][5], 
                image= results['order'][i][4],
                total= f'{price:,}',
                num_order= results['order'][i][2], 
                color_en= results['order'][i][7], 
                color_fa= results['order'][i][8], 
            )

            det_order_boxLayout.add_widget(det_order_box_box)
            det_order_boxLayout.add_widget(Factory.Widget1())

        self.get_screen('det_order').mgr1.add_widget(det_order_boxLayout)

        self.current = 'det_order'

        try:
            if self.pop_up:
                self.pop_up.dismiss()
        except: 
            pass
    
    #@mainthread
    def change_screen(self, screen_kv, screen_Factory, screen_name, *arg):
        if screen_kv not in self.kv:
            if screen_name == 'product':
                Builder.load_file(f"{os.environ['RADIN_ROOT']}/libs/kv/screen_product_scroll3_scroll5.kv")
                Builder.load_file(f"{os.environ['RADIN_ROOT']}/libs/kv/screen_product_scroll3.kv")
                Builder.load_file(f"{os.environ['RADIN_ROOT']}/libs/kv/screen_product.kv")
                self.kv.append(screen_kv)
                self.add_widget(eval(screen_Factory))
                #print('%s was loaded'%(screen_name))
                
            else:
                Builder.load_file(f"{os.environ['RADIN_ROOT']}/libs/kv/{screen_kv}")                
                self.kv.append(screen_kv)
                self.add_widget(eval(screen_Factory))
                #print('%s was loaded'%(screen_name))

class DigiApp(MDApp):

    def build(self):
        Loader.loading_image = 'img/loading1.zip'
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
        Clock.schedule_once(partial(self.root.change_screen, 'screen_search.kv', 'Factory.Search()', 'search'), .05)
        ##Clock.schedule_once(partial(self.root.change_screen, 'screen_grouping.kv', 'Factory.Grouping()', 'grouping'), .05)
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
        self.version = 1.7
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
 
