import time
#start_time = time.time()

from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.factory import Factory
from kivy.uix.recycleview import RecycleView
from kivy.uix.popup import Popup
from kivy.uix.image import Image, AsyncImage
from kivy.uix.carousel import Carousel
from kivy.uix.behaviors import ButtonBehavior
from kivy.loader import Loader
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.swiper import MDSwiperItem
from kivymd.uix.button import MDRoundFlatIconButton
from kivy.animation import Animation

import os
import sys
from pathlib import Path
from arabic_reshaper import reshape
from bidi.algorithm import get_display 
import pandas as pd 
from random import sample
import webbrowser
from ftpretty import ftpretty
from time import gmtime, strftime
from functools import partial

if getattr(sys, "frozen", False):  # bundle mode with PyInstaller
    os.environ["RADIN_ROOT"] = sys._MEIPASS
else:
    os.environ["RADIN_ROOT"] = str(Path(__file__).parent)

global error_list
global items_in_order_screen

items_in_order_screen = []
items_in_category_screen = []
error_list = []

#Window.size = (300, 600)

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
        #self.data = [{'text': str(x)} for x in range(100)]
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

        DigiApp.get_running_app().root.current = 'order'
        p_code = 0
        # Get the code
        p_code = dataframe_products[(dataframe_products['DKP'] == self.dkp) & (dataframe_products['color'] == self.icon_color)]['code'].tolist()[0] if self.icon_color != 'white' else dataframe_products[(dataframe_products['DKP'] == self.dkp) & (dataframe_products['color-fa'] == self.color_fa)]['code'].tolist()[0]
        # Get the stock
        stock = dataframe_products[(dataframe_products['DKP'] == self.dkp) & (dataframe_products['color'] == self.icon_color)]['stock'].tolist()[0] if self.icon_color != 'white' else dataframe_products[(dataframe_products['DKP'] == self.dkp) & (dataframe_products['color-fa'] == self.color_fa)]['stock'].tolist()[0]
        
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
            # Subtract from the data frame
            cond = (dataframe_products['DKP'] == self.dkp) & (dataframe_products['color'] == self.icon_color) if self.icon_color != 'white' else (dataframe_products['DKP'] == self.dkp) & (dataframe_products['color-fa'] == self.color_fa)
            dataframe_products.loc[cond,'stock'] = stock - 1
            
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
            # Increasing the number of orders if it does not exceed the stock and it does not zero 
            if int(a[0]['num_order']) < int(a[0]['stock'].split('.')[0]):
                if int(a[0]['num_order']) != 0:
                    b = int(a[0]['num_order']) + 1
                else: 
                    b = 0
            else:
                b = int(a[0]['num_order'])

            a[0]['num_order'] = str(b)

            # Subtract from the data frame
            cond = dataframe_products['code'] == arg[2] 
            dataframe_products.loc[cond,'stock'] -= 1 if int(dataframe_products.loc[cond,'stock'].tolist()[0]) > 0 else 0 
            
        elif arg[1] == '-':
            if int(a[0]['num_order']) > 1:
                # Decreasing the number of orders if it does not exceed the stock
                b = int(a[0]['num_order']) - 1 
                a[0]['num_order'] = str(b)

            else:
                index = (next((i for i, item in enumerate(items_in_order_screen) if item["p_code"] == arg[2]), None))
                del items_in_order_screen[index]

            # Add to the data frame
            cond = dataframe_products['code'] == arg[2] 
            dataframe_products.loc[cond,'stock'] += 1

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
            # Checking the registration for the next step of the order
            if os.path.isfile('Personal_Information.xlsx'):
                # Checking if the host has stock or not
                f.get('/domains/mahdiemadi.ir/public_html/excel/products.xlsx', 'products.xlsx')
                dataframe_products = pd.read_excel (r'products.xlsx', engine='openpyxl')
                for i in range(len(items_in_order_screen)):
                    if int(items_in_order_screen[i]['num_order']) <= dataframe_products[dataframe_products['code'] == items_in_order_screen[i]['p_code']]['stock'].tolist()[0]:
                        pass
                    else:
                        error_list.append([items_in_order_screen[i]['p_code'], dataframe_products[dataframe_products['code'] == items_in_order_screen[i]['p_code']]['stock'].tolist()[0]])
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
                    # Subtract from the main data frame & Save orders in order ata frame
                    df_personal = pd.read_excel (r'Personal_Information.xlsx', engine='openpyxl')
                    try:
                        df_order = pd.read_excel (r'orders.xlsx', engine='openpyxl')
                        del df_order['Unnamed: 0']
                    except:
                        d = {  
                            'Orderـnumber': [],                         
                            'code': [],
                            'num_order': [],
                            'date&time': [],
                            'image': [],
                            'title': [],
                            'Total': [],
                            'color_en': [],
                            'color_fa': [],
                            'color_fa': [],
                            'Name': [],
                            'Last name': [],
                            'Mobile number': [],
                            'Home number': [],
                            'Address': [],
                            'Postal code': [],
                            'Email': [],
                            'total_price': [],
                            }
                        df_order = pd.DataFrame(data=d)
                    total_price = 0
                    for i in range(len(items_in_order_screen)): 
                        total_price += items_in_order_screen[i]['Total'] * int(items_in_order_screen[i]['num_order'])
                        # Change the values in the main data frame                       
                        cond = dataframe_products['code'] == items_in_order_screen[i]['p_code']
                        dataframe_products.loc[cond,'stock'] = dataframe_products.loc[cond,'stock'] - int(items_in_order_screen[i]['num_order'])
                        # Add orders to the orders data frame                        
                        df_order.loc[len(df_order.index)] = {
                            'Orderـnumber': Orderـnumber, 
                            'code': items_in_order_screen[i]['p_code'],
                            'num_order': items_in_order_screen[i]['num_order'],
                            'date&time': strftime("%Y/%m/%d_%H%M%S", gmtime()), 
                            'image': items_in_order_screen[i]['image'], 
                            'title': items_in_order_screen[i]['title'], 
                            'Total': items_in_order_screen[i]['Total'], 
                            'color_en': items_in_order_screen[i]['color_en'], 
                            'color_fa': items_in_order_screen[i]['color_fa'],
                            'color_fa': items_in_order_screen[i]['color_fa'],
                            'Name': df_personal.tail(1)['Name'].tolist()[0],
                            'Last name': df_personal.tail(1)['Last name'].tolist()[0],
                            'Mobile number': df_personal.tail(1)['Mobile number'].tolist()[0],
                            'Home number': df_personal.tail(1)['Home number'].tolist()[0],
                            'Address': df_personal.tail(1)['Address'].tolist()[0],
                            'Postal code': df_personal.tail(1)['Postal code'].tolist()[0],
                            'Email': df_personal.tail(1)['Email'].tolist()[0],
                            'total_price': total_price
                            }
                    # Save main data frame & order data frame  to excel files 
                    dataframe_products.to_excel('products.xlsx')
                    df_order.to_excel('orders.xlsx')
                    
                    # Save Excel products on the host
                    f.put('products.xlsx', '/domains/mahdiemadi.ir/public_html/excel/products.xlsx')
                    f.put('orders.xlsx', '/domains/mahdiemadi.ir/public_html/Orders/%s.xlsx'%(df_order.tail(1)['date&time'].tolist()[0]))
                    
                else:
                    for i in range(len(error_list)):
                        filter_list = list(filter(lambda items_in_order_screen: items_in_order_screen['p_code'] == error_list[i][0], items_in_order_screen))
                        filter_list[0]['num_order'] = str(error_list[i][1])
                        filter_list[0]['stock'] = str(error_list[i][1])
                        filter_list[0]['error_text'] = get_display(reshape('موجودی ندارد')) if error_list[i][1] == 0 else get_display(reshape('حداکثر موجودی تغییر کرده است'))
                    self.pop_up.dismiss()

                self.add_remove_count('*', '*', '*', '*')
                dataframe_products = dataframe_products[dataframe_products['stock'] != 0]

            else:
                self.pop_up.dismiss()
                content = Button(text= get_display(reshape('ثبت نام')), font_name= 'font/IRANSansXFaNum-Medium.ttf', size_hint=(1, None), size=('20mm', '6mm'))
                pop = Popup(title= get_display(reshape('لطفاٌ ابتدا ثبت نام کنید')), title_font = 'font/IRANSansXFaNum-Medium.ttf', content= content,
                title_align= 'center', size_hint=(None, None), size=(self.width , '20mm'),separator_height= 0)
                content.bind(on_press=self.change_screen_signup)
                content.bind(on_release=pop.dismiss)
                pop.open()

    def change_screen_signup(self, *arg):
        # load acount and signup kv file and add screen to screen manager
        DigiApp.get_running_app().root.change_screen('screen_account_sign_up.kv', 'Factory.Sign_up()', 'signup')
        DigiApp.get_running_app().root.change_screen('screen_account.kv', 'Factory.Account()', 'account')
        # Opening the registration form if not registered
        DigiApp.get_running_app().root.get_screen('account').mgr1.canvas.after.get_group('a')[0].source='img/App/nav1.jpg'
        DigiApp.get_running_app().root.get_screen('account').text1 = '-'
        DigiApp.get_running_app().root.current= 'signup' 

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
            elif self.current_screen.name == "mian":
                DigiApp.get_running_app().root_window.minimize()
                return True

    def open_product_screen(self, DKP, arg): 
        
        self.change_screen('screen_product.kv', 'Factory.Product()', 'product')

        self.get_screen('product').mgr1.scroll_y=1

        try:
            DKP = int(DKP.split('/')[4])
        except:
            if type(DKP) == float:
                DKP = int(DKP)
            
        stock = dataframe_products[dataframe_products['DKP'] == DKP]['stock'].tolist()
        if sum(stock) > 0:
            self.get_screen('product').mgr1.mgr2.scroll_x = 1
            self.get_screen('product').mgr1.scroll_y = 1
            self.get_screen('product').mgr1.mgr3.scroll_x = 1
            self.get_screen('product').dkp = DKP
            self.get_screen('product').mgr1.sizee = dataframe_products[(dataframe_products['DKP'] == DKP) ]['size'].values[0]
            self.get_screen('product').icon = "cards-heart-outline"
            # Delete all carousel's children
            try:
                self.get_screen('product').mgr1.ids._carousel_.clear_widgets()
            except:
                pass
            # Add title
            self.get_screen('product').title = dataframe_products[(dataframe_products['DKP'] == DKP) ]['title'].values[0]
            # Calculate the number of photos
            No_of_files = len(f.list('/my_upload/%s'%(DKP))) - 3
            # Add photos to carousel
            self.get_screen('product').mgr1.slide_len = No_of_files
            self.get_screen('product').mgr1.slide_num = '1'
            self.get_screen('product').mgr1.ids._carousel_.temp = 1
            for i in range(No_of_files):
                self.get_screen('product').mgr1.ids._carousel_.add_widget(AsyncImage(source= 'http://mahdiemadi.ir/Products/%s/%s-%s.jpg'%(DKP, DKP, i), size_hint= (1, 1), allow_stretch= True ))
            self.get_screen('product').mgr1.ids._carousel_.load_slide((self.get_screen('product').mgr1.ids._carousel_.slides)[0])
            # Creating a list of colors in Farsi and English
            list_colors = dataframe_products[(dataframe_products['DKP'] == DKP) & (dataframe_products['stock'] != 0) ]['color'].tolist()
            list_colors_fa = dataframe_products[(dataframe_products['DKP'] == DKP) & (dataframe_products['stock'] != 0) ]['color-fa'].tolist()
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
                self.get_screen('product').mgr1.mgr1.add_widget(Factory.color_buttom(title= str(list_colors_fa[i]), ic_color= list_colors[i]))#(int(a[0]), int(a[2]), int(a[4]), int(a[6]))))#(list_colors[i])))
            # Add the first color label
            self.get_screen('product').mgr1.color= ' - '#get_display(reshape(str(list_colors_fa[len(list_colors_fa) - 1]))) 
            # Add material, country of manufacture and product type & details
            self.get_screen('product').mgr1.material= dataframe_products[(dataframe_products['DKP'] == DKP) ]['material'].values[0]
            self.get_screen('product').mgr1.made_in= dataframe_products[(dataframe_products['DKP'] == DKP)  ]['made_in'].values[0]
            self.get_screen('product').mgr1.type= dataframe_products[(dataframe_products['DKP'] == DKP)  ]['type'].values[0]
            self.get_screen('product').mgr1.detail_1= dataframe_products[(dataframe_products['DKP'] == DKP)  ]['detail_1'].values[0]
            self.get_screen('product').mgr1.detail_2= dataframe_products[(dataframe_products['DKP'] == DKP)  ]['detail_2'].values[0]
            # Add first price & price_off & off
            self.get_screen('product').icon_color = list_colors[len(list_colors) - 1]
            a = self.get_screen('product').icon_color
            price = int(dataframe_products[(dataframe_products['DKP'] == DKP) & (dataframe_products['color'] == a) ]['price'].values[0])
            self.get_screen('product').price = f'{price:,}'
            price_off = int(dataframe_products[(dataframe_products['DKP'] == DKP) & (dataframe_products['color'] == a) ]['price_off'].values[0])
            self.get_screen('product').price_off = f'{price_off:,}'
            self.get_screen('product').off = int(dataframe_products[(dataframe_products['DKP'] == DKP) & (dataframe_products['color'] == a) ]['off'].values[0])
            # Add similar product
            ## Drop all children
            try:
                self.get_screen('product').mgr1.mgr2.ids._GridLayout.clear_widgets()
            except:
                pass
        ## Get categories
            cat = dataframe_products[(dataframe_products['DKP'] == DKP) ]['cat'].values[0]   
            ## Create list of DKPs in our category without repeat
            list_cat = dataframe_products[(dataframe_products['cat'] == cat) & (dataframe_products['stock'] != 0) ]['DKP'].drop_duplicates().tolist()
            ## Drop current category
            list_cat = [ele for ele in list_cat if ele != DKP]
            ## Select 5 category randomly
            List_similar_product = sample(list_cat, 5 if len(list_cat) >= 5 else len(list_cat))
            for i in range(len(List_similar_product)):
                self.get_screen('product').mgr1.mgr2.ids._GridLayout.add_widget(Factory.Button_scroll5(image_source= 'http://mahdiemadi.ir/Products/%s/%s-0-v_200-h_200-q_90.jpg'%(str(int(List_similar_product[i])), str(int(List_similar_product[i]))) ))
            # Set current screen
            self.current= "product"
            try:
                if self.pop_up:
                    self.pop_up.dismiss()
            except: 
                pass
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
        price = int(dataframe_products[(dataframe_products['DKP'] == self.get_screen('product').dkp) & (dataframe_products['color'] == icon_color) ]['price'].values[0])
        self.get_screen('product').price = f'{price:,}'
        price_off = int(dataframe_products[(dataframe_products['DKP'] == self.get_screen('product').dkp) & (dataframe_products['color'] == icon_color) ]['price_off'].values[0])
        self.get_screen('product').price_off = f'{price_off:,}'
        self.get_screen('product').off = int(dataframe_products[(dataframe_products['DKP'] == self.get_screen('product').dkp) & (dataframe_products['color'] == icon_color) ]['off'].values[0])

    def Adding_values_to_the_order_screen(self):
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

        if self.icon_color  == '':
            RV_Order.err = 'True'
            content = Button(text= get_display(reshape('بازگشت')), font_name= 'font/IRANSansXFaNum-Medium.ttf', size_hint=(1, None), size=('20mm', '6mm'))
            pop = Popup(title= get_display(reshape('لطفاً یک رنگ/سایز انتخاب نمایید')), title_font = 'font/IRANSansXFaNum-Medium.ttf', content= content,
            title_align= 'center', size_hint=(None, None), size=(self.width , '20mm'),separator_height= 0)
            # bind the on_press event of the button to the dismiss function
            content.bind(on_press=pop.dismiss)
            pop.open()
        self.icon_color = ''

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
        self.change_screen('screen_off.kv', 'Factory.Off()', 'off')
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

        filtered_df = dataframe_products[(dataframe_products['stock'] != 0) & (dataframe_products['cat'] == cat)]
        filtered_df.drop_duplicates(subset="DKP",keep='first', inplace=True)

        temp_len = len(filtered_df.index)
        for i in range(temp_len):
            title = filtered_df.iloc[i]['title']
            if len(title) > 20:
                title = title[:17] + '...'
            price_off = int(filtered_df.iloc[i]['price_off'])
            price_off = f'{price_off:,}'
            price = int(filtered_df.iloc[i]['price'])
            price = f'{price:,}'

            self.items_in_category_screen.append(
                {'title1': get_display(reshape(title)),
                'source1': 'http://mahdiemadi.ir/Products/%s/%s-0-v_200-h_200-q_90.jpg'%(str(int(filtered_df.iloc[i]['DKP'])), str(int(filtered_df.iloc[i]['DKP']))),
                  'detail_3_1': get_display(reshape(filtered_df.iloc[i]['detail_3'])),
                    'detail_4_1': get_display(reshape(filtered_df.iloc[i]['detail_4'])),
                      'price1': price,
                        'off1': str(int(filtered_df.iloc[i]['off'])),
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

    def Search_in_search_bar(self, word, arg):
        dataframe_products['titleـfa'] = dataframe_products.apply(lambda row : get_display(reshape(row['title'])), axis = 1)
        try:
            df = dataframe_products[dataframe_products['titleـfa'].str.contains('.*%s.*'%(word), regex=True)]['cat'].drop_duplicates()        
            self.open_category(df.values[0], '')
        except:
            self.get_screen('search').source= 'img/App/not_find.jpg'
            try:
                if self.pop_up:
                    self.pop_up.dismiss()
            except: 
                pass

    def show_keyboard(self, arg):
        self.get_screen('search').ids._MDTextFieldPersian2.focus= True
    
    def open_grouping(self, arg):
        self.grouping_type = 'grouping'
        self.get_screen('grouping').mgr2.clear_widgets()
        self.get_screen('grouping').ids._sc.scroll_y=1 
        # Forming a list of category dictionary keys
        list_ = list(self.category_dict.keys())
        for i in range(len(list_)):
            DKP_list = dataframe_products[dataframe_products['cat'] == list_[i]]['DKP'].drop_duplicates().to_list()
            if DKP_list == []:
                continue

            category_boxlayout = Category_boxlayout(size_hint_y= None, height= '27mm',
                    cat= get_display(reshape(self.category_dict[list_[i]])), title_text= get_display(reshape('مشاهده همه'))
                )
            cat_ = Cat()

            for j in range(len(DKP_list) if len(DKP_list) < 5 else 5):
                cat_.ids._grid.add_widget(AsyncImage(
                source= 'http://mahdiemadi.ir/Products/%s/%s-%s-v_200-h_200-q_90.jpg'%(str(int(DKP_list[j])), str(int(DKP_list[j])), 0),
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
        reshaped_loading = reshape("لطفاً شکیبا باشید")
        bidi_loading = get_display(reshaped_loading)
        self.pop_up = Factory.PopupBox()
        self.pop_up.update_pop_up_text(bidi_loading)
        self.pop_up.open()
    
    def open_account_xls(self, *args):
        try:
            self.df_account = pd.read_excel (r'Personal_Information.xlsx', engine='openpyxl')
            self.get_screen('account').text1 = self.df_account['Name'][0]
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
            d = {'Name': [self.get_screen('signup').ids._name.text],
            'Last name': [self.get_screen('signup').ids._last_name.text],
            'Mobile number': [self.get_screen('signup').ids._mobile_number.text],
            'Home number': [self.get_screen('signup').ids._home_number.text],
            'Address': ['%s, %s, %s, %s'%(
                self.get_screen('signup').ids._address.text,
                self.get_screen('signup').ids._address1.text,
                self.get_screen('signup').ids._address2.text,
                self.get_screen('signup').ids._address3.text,
                )],
            'Postal code': [self.get_screen('signup').ids._postal_code.text],
            'Email': [self.get_screen('signup').ids._email.text],
            }
            df = pd.DataFrame.from_dict(d)
            df.to_excel("Personal_Information.xlsx")
            if len(items_in_order_screen) != 0:
                self.current= 'order'
            else:
                self.current= 'account'

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
        os.remove("Personal_Information.xlsx")
        try:
            os.remove("orders.xlsx")
        except:
            None
        self.current= 'main'

    def load_account_data(self):
        self.get_screen('signup').ids._name.text = str(self.df_account['Name'][0])
        self.get_screen('signup').ids._last_name.text = str(self.df_account['Last name'][0])
        self.get_screen('signup').ids._mobile_number.text = str(self.df_account['Mobile number'][0])
        self.get_screen('signup').ids._home_number.text = str(self.df_account['Home number'][0])
        self.get_screen('signup').ids._address.text = str(self.df_account['Address'][0].split(', ')[0])
        self.get_screen('signup').ids._address1.text = str(self.df_account['Address'][0].split(', ')[1])
        self.get_screen('signup').ids._address2.text = str(self.df_account['Address'][0].split(', ')[2])
        self.get_screen('signup').ids._address3.text = str(self.df_account['Address'][0].split(', ')[3])  
        self.get_screen('signup').ids._postal_code.text = str(self.df_account['Postal code'][0])
        self.get_screen('signup').ids._email.text = str(self.df_account['Email'][0])

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

        try:
            df_order = pd.read_excel (r'orders.xlsx', engine='openpyxl')
        except:
            content = Button(text= get_display(reshape('بازگشت')), font_name= 'font/IRANSansXFaNum-Medium.ttf', size_hint=(1, None), size=('20mm', '6mm'))
            pop = Popup(title= get_display(reshape('سفارشی ثبت نشده است!')), title_font = 'font/IRANSansXFaNum-Medium.ttf', content= content,
            title_align= 'center', size_hint=(None, None), size=(self.width , '20mm'),separator_height= 0)
            content.bind(on_release=pop.dismiss)
            pop.open()
            return

        # Forming a list of order_numbers
        list_orders = df_order["Orderـnumber"].drop_duplicates().tolist()
        for i in range(len(list_orders)):
            category_boxlayout = Category_boxlayout(size_hint_y= None, height= '27mm',
                    cat= get_display(reshape('شماره سفارش: %s'%(list_orders[i]))), title_text= get_display(reshape('جزییات سفارش'))
                )
            cat_ = Cat()

            # Add images to orders
            list_image = df_order[df_order['Orderـnumber'] == list_orders[i]]["image"].tolist()
                
            for j in range(len(list_image) if len(list_image) < 5 else 5):
                cat_.ids._grid.add_widget(AsyncImage(
                source= list_image[j],
                size_hint= (None, None), width= '15mm', height= '15mm', allow_stretch= True
                    ))

            category_boxlayout.add_widget(cat_)
            category_boxlayout.add_widget(Factory.Widget1())
            category_boxlayout.add_widget(Factory.Widget1())

            self.get_screen('grouping').mgr2.add_widget(category_boxlayout)

        self.current = 'grouping' if os.path.isfile('orders.xlsx') else None

        try:
            if self.pop_up:
                self.pop_up.dismiss()
        except: 
            pass

    def see_order_detail(self, *arg):
        self.active_page = 'grouping'
        self.get_screen('det_order').mgr1.clear_widgets()
        order_number = arg[0].split(':')[0].strip()
        df_order = pd.read_excel (r'orders.xlsx', engine='openpyxl')
        address1 = df_order[df_order['Orderـnumber'] == int(order_number)]['Address'].tolist()[0].split(', ')[1:3]
        address2 = df_order[df_order['Orderـnumber'] == int(order_number)]['Address'].tolist()[0].split(', ')[3:4] 
        tot= df_order[df_order['Orderـnumber'] == int(order_number)]['total_price'].tolist()[-1]
        
        det_order_boxLayout = Det_order_boxLayout(
            order_num='%s'%(order_number), 
            receiver= '%s %s'%(
                        get_display(reshape(df_order[df_order['Orderـnumber'] == int(order_number)]['Name'].tolist()[-1])),
                        get_display(reshape(df_order[df_order['Orderـnumber'] == int(order_number)]['Last name'].tolist()[-1]))
                        ), 
            tel= df_order[df_order['Orderـnumber'] == int(order_number)]['Mobile number'].tolist()[-1],
            address= get_display(reshape('%s, %s\n%s\n%s'
                        %(address1[1], address1[0], address2[0], str(df_order['Postal code'].tolist()[-1])))),
            total= f'{tot:,}', 
        )
        for i in range(len(df_order[df_order['Orderـnumber'] == int(order_number)].index)):
            price = df_order[df_order['Orderـnumber'] == int(order_number)]['Total'].tolist()[i]      
            det_order_box_box = Det_order_box_box(
                title= df_order[df_order['Orderـnumber'] == int(order_number)]['title'].tolist()[i],
                image= df_order[df_order['Orderـnumber'] == int(order_number)]['image'].tolist()[i],
                total= f'{price:,}',
                num_order= str(df_order[df_order['Orderـnumber'] == int(order_number)]['num_order'].tolist()[i]),
                color_en= str(df_order[df_order['Orderـnumber'] == int(order_number)]['color_en'].tolist()[i]),
                color_fa= str(df_order[df_order['Orderـnumber'] == int(order_number)]['color_fa'].tolist()[i]),
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

    def stop(self):
        DigiApp.get_running_app().stop()
        Window.close()

    def change_screen(self, screen_kv, screen_Factory, screen_name, *arg):
        if screen_kv not in self.kv:
            if screen_name == 'product':
                Builder.load_file(f"{os.environ['RADIN_ROOT']}/libs/kv/screen_product_scroll3_scroll5.kv")
                Builder.load_file(f"{os.environ['RADIN_ROOT']}/libs/kv/screen_product_scroll3.kv")
                Builder.load_file(f"{os.environ['RADIN_ROOT']}/libs/kv/screen_product.kv")
                self.kv.append(screen_kv)
                self.add_widget(eval(screen_Factory))
                print('%s was loaded'%(screen_name))
                
            else:
                Builder.load_file(f"{os.environ['RADIN_ROOT']}/libs/kv/{screen_kv}")                
                self.kv.append(screen_kv)
                self.add_widget(eval(screen_Factory))
                print('%s was loaded'%(screen_name))

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
        Clock.schedule_once(self.after_start, 0.01)

    def after_start(self, arg):
        global f
        global dataframe_products

        try:
            f = ftpretty('31.7.73.165', 'mahdiem3', '2(v3Hj(6InRxG9')
            f.get('/domains/mahdiemadi.ir/public_html/excel/products.xlsx', 'products.xlsx')

            dataframe_products = pd.read_excel (r'products.xlsx', engine='openpyxl')

            self.version = 1.3
            self.last_version = dataframe_products['version'].tolist()[0]

            dataframe_products = dataframe_products[dataframe_products['stock'] != 0]
            Clock.schedule_once(self.change_screen, 0.01)
        except:
            self.root.current = 'Err_connection'

    def change_screen(self, arg):
        # Check for update
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

        # Access the carousel.
        carousel = self.root.get_screen('main').mgr3.mgr1.ids._carousel_
        # Schedule after every 3 seconds.
        Clock.schedule_interval(carousel.load_next, 3.0)

        # Add widget to scrollview1 in main screen
        list_DKP = dataframe_products[(dataframe_products['off'] != 0) & (dataframe_products['cat'] == 'H')]['DKP'].drop_duplicates().to_list()  
        j = 6 #len(list_DKP)
        for i in range(j if len(list_DKP) > j else len(list_DKP)):
            dkp = list_DKP[i]
            self.root.get_screen('main').mgr3.mgr2.dkp= dkp
            text_title = dataframe_products[(dataframe_products['DKP'] == dkp)]['title'].tolist()[0]
            if len(text_title) > 20:
                text_title = text_title[:17] + '...'
            self.root.get_screen('main').mgr3.mgr2.text_title= text_title
            # Add image from host  
            self.root.get_screen('main').mgr3.mgr2.source_image= 'http://mahdiemadi.ir/Products/%s/%s-0-v_200-h_200-q_90.jpg'%(str(int(dkp)), str(int(dkp)))
            self.root.get_screen('main').mgr3.mgr2.detail_1= dataframe_products[(dataframe_products['DKP'] == dkp)]['detail_3'].tolist()[0]
            self.root.get_screen('main').mgr3.mgr2.detail_2= dataframe_products[(dataframe_products['DKP'] == dkp)]['detail_4'].tolist()[0]
            self.root.get_screen('main').mgr3.mgr2.off= str(int(dataframe_products[(dataframe_products['DKP'] == dkp)]['off'].tolist()[0]))
            price = int(dataframe_products[(dataframe_products['DKP'] == dkp)]['price'].tolist()[0])
            self.root.get_screen('main').mgr3.mgr2.price= f'{price:,}'
            price_off = int(dataframe_products[(dataframe_products['DKP'] == dkp)]['price_off'].tolist()[0])
            self.root.get_screen('main').mgr3.mgr2.price_off= f'{price_off:,}'
            self.root.get_screen('main').mgr3.mgr2.mgr1.add_widget(Factory.BoxLayout_mainscroll_scroll1())
        
        # Add widget to scrollview2 in main screen
        list_DKP_Gl = dataframe_products[(dataframe_products['off'] != 0) & (dataframe_products['cat'] == 'GL')]['DKP'].drop_duplicates().to_list()  
        for i in range(j if len(list_DKP_Gl) > j else len(list_DKP_Gl)):
            dkp_Gl = list_DKP_Gl[i]
            self.root.get_screen('main').mgr3.mgr3.dkp_Gl= dkp_Gl
            text_title = dataframe_products[(dataframe_products['DKP'] == dkp_Gl)]['title'].tolist()[0]
            if len(text_title) > 20:
                text_title = text_title[:17] + '...'
            self.root.get_screen('main').mgr3.mgr3.text_title= text_title
            # Add image from host
            self.root.get_screen('main').mgr3.mgr3.source_image= 'http://mahdiemadi.ir/Products/%s/%s-0-v_200-h_200-q_90.jpg'%(str(int(dkp_Gl)), str(int(dkp_Gl)))
            self.root.get_screen('main').mgr3.mgr3.detail_1= dataframe_products[(dataframe_products['DKP'] == dkp_Gl)]['detail_3'].tolist()[0]
            self.root.get_screen('main').mgr3.mgr3.detail_2= dataframe_products[(dataframe_products['DKP'] == dkp_Gl)]['detail_4'].tolist()[0]
            self.root.get_screen('main').mgr3.mgr3.off= str(int(dataframe_products[(dataframe_products['DKP'] == dkp_Gl)]['off'].tolist()[0]))
            price = int(dataframe_products[(dataframe_products['DKP'] == dkp_Gl)]['price'].tolist()[0])
            self.root.get_screen('main').mgr3.mgr3.price= f'{price:,}'
            price_off = int(dataframe_products[(dataframe_products['DKP'] == dkp_Gl)]['price_off'].tolist()[0])
            self.root.get_screen('main').mgr3.mgr3.price_off= f'{price_off:,}'
            self.root.get_screen('main').mgr3.mgr3.mgr1.add_widget(Factory.BoxLayout_mainscroll_scroll2())

        #print("--- %s seconds ---" % (time.time() - start_time))
        print(time.time())
        Clock.schedule_once(partial(self.root.change_screen, 'screen_search.kv', 'Factory.Search()', 'search'), 1)
        Clock.schedule_once(partial(self.root.change_screen, 'screen_product.kv', 'Factory.Product()', 'product'), 3)
        Clock.schedule_once(partial(self.root.change_screen, 'screen_off.kv', 'Factory.Off()', 'off'), 15)
        #Clock.schedule_once(partial(self.root.change_screen, 'screen_grouping.kv', 'Factory.Grouping()', 'grouping'), 11)
        #Clock.schedule_once(partial(self.root.change_screen, 'screen_order.kv', 'Factory.Order()', 'order'), 11)
        #Clock.schedule_once(partial(self.root.change_screen, 'screen_account.kv', 'Factory.Account()', 'account'), 13)
        Clock.schedule_once(self.change_screen_to_main, 2.9)

    def change_screen_to_main(self, *arg):
        self.root.current = 'main'

    def update(self, *arg):
        self.pop.dismiss()
        if arg[0] == 'Yes':
            MainScreen.main_scroll_gridLayout1_items('', 'bazar')
            self.root.current = 'SplashScreen'

if __name__== "__main__":
    DigiApp().run()
 
