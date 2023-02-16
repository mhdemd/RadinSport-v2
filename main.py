#from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
#from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.core.window import Window
#from kivy.uix.widget import Widget
from kivy.factory import Factory
from kivy.uix.recycleview import RecycleView
#from kivy.utils import rgba
from kivy.uix.popup import Popup
#from kivy.uix.label import Label
from kivy.uix.image import Image, AsyncImage
from kivy.uix.carousel import Carousel
from kivy.uix.behaviors import ButtonBehavior
from kivy.loader import Loader

import os
from kivymd.app import MDApp
import arabic_reshaper 
from bidi.algorithm import get_display 
#from kivymd.uix.behaviors.toggle_behavior import MDToggleButton
import pandas as pd #openpyxl
from kivymd.uix.swiper import MDSwiperItem
from kivymd.uix.button import MDRoundFlatIconButton
import random
import webbrowser
from ftpretty import ftpretty

f = ftpretty('31.7.73.165', 'mahdiem3', '2(v3Hj(6InRxG9')
f.get('/domains/mahdiemadi.ir/public_html/excel/products.xls', 'products.xls')

dataframe_products = pd.read_excel (r'products.xls')
dataframe_products = dataframe_products.astype({"price_off": int})
dataframe_products = dataframe_products[dataframe_products['stock'] != 0]

global error_list

items_in_order_screen = []
items_in_category_screen = []
error_list = []



#Window.size = (350, 610)

Builder.load_file('main.kv')
Builder.load_file('main_searchbar.kv')
Builder.load_file('main_searchbar_screen.kv')
Builder.load_file('main_scroll.kv')
Builder.load_file('main_scroll_scroll1.kv')
Builder.load_file('main_scroll_gridLayout1.kv')
Builder.load_file('main_scroll_carousel1.kv')
Builder.load_file('main_scroll_gridLayout2.kv')
Builder.load_file('main_scroll_scroll2.kv')
Builder.load_file('main_scroll_gridLayout3.kv')
Builder.load_file('main_bottom_navigation.kv')
Builder.load_file('screen_product.kv')
Builder.load_file('screen_product_scroll3.kv')
Builder.load_file('screen_product_scroll3_scroll5.kv')
Builder.load_file('screen_off.kv') 
Builder.load_file('screen_order.kv')
Builder.load_file('screen_grouping.kv')
Builder.load_file('screen_account.kv')
Builder.load_file('screen_account_sign_up.kv')

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

    def __init__(self, **kwargs):
        super(RV_Order, self).__init__(**kwargs)
        #self.data = [{'text': str(x)} for x in range(100)]
        self.data = [item for item in items_in_order_screen]

    def add_to_order(self):
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
                'color_fa': get_display(arabic_reshaper.reshape(self.color_fa)),
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

    def add_remove_count(self, *arg):
        a = list(filter(lambda items_in_order_screen: items_in_order_screen['p_code'] == arg[2], items_in_order_screen)) if arg[0] != '*' else 0
        if arg[1] == '+':
            # Increasing the number of orders if it does not exceed the stock and it does not zero 
            if int(a[0]['num_order']) < int(a[0]['stock']):
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
            
        self.total = 0
        for i in range(len(items_in_order_screen)):
            self.total += items_in_order_screen[i]['Total'] * int(items_in_order_screen[i]['num_order']) 
        total = self.total
        self.total = f'{total:,}'

        self.data = [item for item in items_in_order_screen]
        self.refresh_from_data()
               
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

class MainScreen(ScreenManager):
    category_dict = {'H': 'کلاه و نقاب', 'SH': 'قمقمه و شیکر', 'SW': 'لوازم شنا', 'GL': 'دستکش', 'R': 'طناب', 'PI': 'پیلاتس و بدنسازی'}
    order_on= ''
    # Deine back bottom in android
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        Window.bind(on_keyboard=self.on_key)

    def on_key(self, window, key, *args):
        if key == 27:  # the esc key
            if self.current_screen.name == "product" or  self.current_screen.name == 'search' or  self.current_screen.name == 'signup':
                self.current = self.active_page
                self.mgr2.source= ''
                return True  # exit the app from this page
            elif self.current_screen.name == "order" or self.current_screen.name == "grouping" or self.current_screen.name == "off" or self.current_screen.name == "account":
                self.current = 'main'
                return True
            elif self.current_screen.name == "mian":
                DigiApp.get_running_app().root_window.minimize()
                return True

    def open_product_screen(self, DKP, arg): 
        try:
            DKP = int(DKP.split('/')[4])
        except:
            pass

        stock = dataframe_products[dataframe_products['DKP'] == DKP]['stock'].tolist()

        if sum(stock) > 0:
            self.mgr5.mgr1.mgr2.scroll_x = 1
            self.mgr5.mgr1.scroll_y = 1
            self.mgr5.mgr1.mgr3.scroll_x = 1
            self.mgr5.dkp = DKP
            self.mgr7.mgr2.dkp = DKP
            self.mgr5.mgr1.sizee = dataframe_products[(dataframe_products['DKP'] == DKP) ]['size'].values[0]
            self.mgr5.icon = "cards-heart-outline"
            # Delete all carousel's children
            try:
                self.mgr5.mgr1.ids._carousel_.clear_widgets()
            except:
                pass
            # Add title
            self.mgr5.title = dataframe_products[(dataframe_products['DKP'] == DKP) ]['title'].values[0]
            self.mgr7.mgr2.title = self.mgr5.title
            # Calculate the number of photos
            No_of_files = len(f.list('/my_upload/%s'%(DKP))) - 3
            # Add photos to carousel
            self.mgr5.mgr1.slide_len = No_of_files
            self.mgr5.mgr1.slide_num = '1'
            self.mgr5.mgr1.ids._carousel_.temp = 1
            for i in range(No_of_files):
                self.mgr5.mgr1.ids._carousel_.add_widget(AsyncImage(source= 'http://mahdiemadi.ir/Products/%s/%s-%s.jpg'%(DKP, DKP, i), size_hint= (1, 1), allow_stretch= True ))
            self.mgr5.mgr1.ids._carousel_.load_slide((self.mgr5.mgr1.ids._carousel_.slides)[0])
            # Creating a list of colors in Farsi and English
            list_colors = dataframe_products[(dataframe_products['DKP'] == DKP) & (dataframe_products['stock'] != 0) ]['color'].tolist()
            list_colors_fa = dataframe_products[(dataframe_products['DKP'] == DKP) & (dataframe_products['stock'] != 0) ]['color-fa'].tolist()
            # Calculate the number of colors in stock
            self.mgr5.mgr1.mgr1.cols= len(list_colors)
            self.number_of_color= len(list_colors)
            # Delete all color_scrollview's children
            try:
                self.mgr5.mgr1.mgr1.clear_widgets()
            except: 
                pass
            # Add colors button to scrollview3
            for i in range(len(list_colors)):
                self.mgr5.mgr1.mgr1.add_widget(Factory.color_buttom(title= str(list_colors_fa[i]), ic_color= list_colors[i]))#(int(a[0]), int(a[2]), int(a[4]), int(a[6]))))#(list_colors[i])))
            # Add the first color label
            self.mgr5.mgr1.color= get_display(arabic_reshaper.reshape(str(list_colors_fa[len(list_colors_fa) - 1]))) 
            self.mgr7.mgr2.color_fa = self.mgr5.mgr1.color
            # Add material, country of manufacture and product type & details
            self.mgr5.mgr1.material= dataframe_products[(dataframe_products['DKP'] == DKP) ]['material'].values[0]
            self.mgr5.mgr1.made_in= dataframe_products[(dataframe_products['DKP'] == DKP)  ]['made_in'].values[0]
            self.mgr5.mgr1.type= dataframe_products[(dataframe_products['DKP'] == DKP)  ]['type'].values[0]
            self.mgr5.mgr1.detail_1= dataframe_products[(dataframe_products['DKP'] == DKP)  ]['detail_1'].values[0]
            self.mgr5.mgr1.detail_2= dataframe_products[(dataframe_products['DKP'] == DKP)  ]['detail_2'].values[0]
            # Add first price & price_off & off
            self.mgr5.icon_color = list_colors[len(list_colors) - 1]
            a = self.mgr5.icon_color
            self.mgr7.mgr2.icon_color = a
            price = int(dataframe_products[(dataframe_products['DKP'] == DKP) & (dataframe_products['color'] == a) ]['price'].values[0])
            self.mgr5.price = f'{price:,}'
            price_off = int(dataframe_products[(dataframe_products['DKP'] == DKP) & (dataframe_products['color'] == a) ]['price_off'].values[0])
            self.mgr5.price_off = f'{price_off:,}'
            self.mgr7.mgr2.price_off = self.mgr5.price_off
            self.mgr7.mgr2.price = self.mgr5.price
            self.mgr5.off = int(dataframe_products[(dataframe_products['DKP'] == DKP) & (dataframe_products['color'] == a) ]['off'].values[0])
            # Add similar product
            ## Drop all children
            try:
                self.mgr5.mgr1.mgr2.ids._GridLayout.clear_widgets()
            except:
                pass
        ## Get categories
            cat = dataframe_products[(dataframe_products['DKP'] == DKP) ]['cat'].values[0]   
            ## Create list of DKPs in our category without repeat
            list_cat = dataframe_products[(dataframe_products['cat'] == cat) & (dataframe_products['stock'] != 0) ]['DKP'].drop_duplicates().tolist()
            ## Drop current category
            list_cat = [ele for ele in list_cat if ele != DKP]
            ## Select 5 category randomly
            List_similar_product = random.sample(list_cat, 5 if len(list_cat) >= 5 else len(list_cat))
            for i in range(len(List_similar_product)):
                self.mgr5.mgr1.mgr2.ids._GridLayout.add_widget(Factory.Button_scroll5(image_source= 'http://mahdiemadi.ir/Products/%s/%s-0-v_200-h_200-q_90.jpg'%(List_similar_product[i], List_similar_product[i]) ))
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
            content = Button(text= get_display(arabic_reshaper.reshape('بازگشت')), font_name= 'font/IRANSansXFaNum-Medium.ttf', size_hint=(1, None), size=('20mm', '6mm'))
            pop = Popup(title= get_display(arabic_reshaper.reshape('موجودی کالا به اتمام رسیده است.')), title_font = 'font/IRANSansXFaNum-Medium.ttf', content= content,
            title_align= 'center', size_hint=(None, None), size=(self.width , '20mm'),separator_height= 0)
            # bind the on_press event of the button to the dismiss function
            content.bind(on_press=pop.dismiss)
            pop.open()

    def Price_change_with_variety_change(self, icon_color, color_fa):
        price = int(dataframe_products[(dataframe_products['DKP'] == self.mgr5.dkp) & (dataframe_products['color'] == icon_color) ]['price'].values[0])
        self.mgr5.price = f'{price:,}'
        price_off = int(dataframe_products[(dataframe_products['DKP'] == self.mgr5.dkp) & (dataframe_products['color'] == icon_color) ]['price_off'].values[0])
        self.mgr5.price_off = f'{price_off:,}'
        self.mgr7.mgr2.price_off = self.mgr5.price_off
        self.mgr7.mgr2.price = self.mgr5.price
        self.mgr5.off = int(dataframe_products[(dataframe_products['DKP'] == self.mgr5.dkp) & (dataframe_products['color'] == icon_color) ]['off'].values[0])
        self.mgr7.mgr2.icon_color = icon_color
        self.mgr7.mgr2.color_fa = color_fa

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
            webbrowser.open('https://cafebazaar.ir/app/com.radinafzar.radinsport')

    def changeـheartـicon(self):
        self.mgr5.icon = 'cards-heart'

    def open_category(self, cat, arg):
        self.mgr6.ids._RecycleView_category.scroll_y=1 

        self.items_in_category_screen = []
        try:
            self.mgr6.title= get_display(arabic_reshaper.reshape(self.category_dict[cat]))
        except:
            # list out keys and values separately
            key_list = list(self.category_dict.keys())
            val_list = list(self.category_dict.values())

            # get position of value 2 in second list
            position = val_list.index(cat)

            # get key with position calculated above
            cat = key_list[position]
            self.mgr6.title= get_display(arabic_reshaper.reshape(self.category_dict[cat]))

        filtered_df = dataframe_products[(dataframe_products['stock'] != 0) & (dataframe_products['cat'] == cat)]
        filtered_df.drop_duplicates(subset="DKP",keep='first', inplace=True)

        temp_len = len(filtered_df.index)
        for i in range(temp_len):
            title = filtered_df.iloc[i]['title']
            if len(title) > 20:
                title = title[:17] + '...'
            price_off = filtered_df.iloc[i]['price_off']
            price_off = f'{price_off:,}'
            price = filtered_df.iloc[i]['price']
            price = f'{price:,}'

            self.items_in_category_screen.append(
                {'title1': get_display(arabic_reshaper.reshape(title)),
                'source1': 'http://mahdiemadi.ir/Products/%s/%s-0-v_200-h_200-q_90.jpg'%(filtered_df.iloc[i]['DKP'], filtered_df.iloc[i]['DKP']),
                  'detail_3_1': get_display(arabic_reshaper.reshape(filtered_df.iloc[i]['detail_3'])),
                    'detail_4_1': get_display(arabic_reshaper.reshape(filtered_df.iloc[i]['detail_4'])),
                      'price1': price,
                        'off1': str(filtered_df.iloc[i]['off']),
                          'price_off1': price_off}
            )
        RV_Category.data = [item for item in self.items_in_category_screen]
        self.mgr6.mgr2.refresh_from_data()
        self.current = "off"
        #self.active_page = 'off'
        self.active_page_variable = cat

        try:
            if self.pop_up:
                self.pop_up.dismiss()
        except: 
            pass

    def Search_in_search_bar(self, word, arg):
        #if dataframe_products['titleـfa']:
        #    pass
        #else:
        dataframe_products['titleـfa'] = dataframe_products.apply(lambda row : get_display(arabic_reshaper.reshape(row['title'])), axis = 1)
        try:
            df = dataframe_products[dataframe_products['titleـfa'].str.contains('.*%s.*'%(word), regex=True)]['cat'].drop_duplicates()        
            self.open_category(df.values[0], '')
        except:
            self.mgr2.source= 'img/App/not_find.jpg'
            try:
                if self.pop_up:
                    self.pop_up.dismiss()
            except: 
                pass

    def show_keyboard(self, arg):
        self.mgr2.ids._MDTextFieldPersian2.focus= True
    
    def open_grouping(self, arg):
        
        if self.mgr8.mgr2.children != []:
            self.mgr8.ids._sc.scroll_y=1 
        else:
            # Forming a list of category dictionary keys
            list_ = list(self.category_dict.keys())
            for i in range(len(list_)):
                
                category_boxlayout = Category_boxlayout(size_hint_y= None, height= '25mm',
                        cat= self.category_dict[list_[i]]
                    )
                cat_ = Cat()

                DKP_list = dataframe_products[dataframe_products['cat'] == list_[i]]['DKP'].drop_duplicates().to_list()  

                for j in range(len(DKP_list) if len(DKP_list) < 5 else 5):
                    cat_.ids._grid.add_widget(AsyncImage(
                    source= 'http://mahdiemadi.ir/Products/%s/%s-%s-v_200-h_200-q_90.jpg'%(DKP_list[j], DKP_list[j], 0),
                    size_hint= (None, None), width= '17mm', height= '17mm', allow_stretch= True
                        ))

                category_boxlayout.add_widget(cat_)

                self.mgr8.mgr2.add_widget(category_boxlayout)
        try:
            if self.pop_up:
                self.pop_up.dismiss()
        except: 
            pass

    def show_popup(self, args):
        reshaped_loading = arabic_reshaper.reshape("لطفاً شکیبا باشید")
        bidi_loading = get_display(reshaped_loading)
        self.pop_up = Factory.PopupBox()
        self.pop_up.update_pop_up_text(bidi_loading)
        self.pop_up.open()
    
    def open_account_xls(self, *args):
        try:
            self.df_account = pd.read_excel (r'Personal_Information.xls')
            self.mgr9.text1 = self.df_account['Name'][0]
        except:
            self.mgr9.text1 = '-'

    def sign_up(self):
        if self.mgr10.ids._name.text == '' or \
        self.mgr10.ids._last_name.text == '' or \
        self.mgr10.ids._mobile_number.text == '' or \
        self.mgr10.ids._address.text == '' or \
        self.mgr10.ids._postal_code.text == '':

            # create content and add to the popup
            content = Button(text= get_display(arabic_reshaper.reshape('بازگشت')), font_name= 'font/IRANSansXFaNum-Medium.ttf', size_hint=(1, None), size=('20mm', '6mm'))
            pop = Popup(title= get_display(arabic_reshaper.reshape('لطفاً موارد الزامی پر شود')), title_font = 'font/IRANSansXFaNum-Medium.ttf', content= content,
            title_align= 'center', size_hint=(None, None), size=(self.width , '20mm'),separator_height= 0)
            # bind the on_press event of the button to the dismiss function
            content.bind(on_press=pop.dismiss)
            pop.open()

        else:
            d = {'Name': [self.mgr10.ids._name.text],
            'Last name': [self.mgr10.ids._last_name.text],
            'Mobile number': [self.mgr10.ids._mobile_number.text],
            'Home number': [self.mgr10.ids._home_number.text],
            'Address': [self.mgr10.ids._address.text],
            'Postal code': [self.mgr10.ids._postal_code.text],
            'Email': [self.mgr10.ids._email.text],
            }
            df = pd.DataFrame(data=d)
            df.to_excel("Personal_Information.xls")
            if self.order_on == True:
                self.current= 'order'
            else:
                self.current= 'account'

    def delete_Personal_Information(self):
        # create content and add to the popup
        content = BoxLayout(orientation= 'horizontal')
        bt1 = Button(text= get_display(arabic_reshaper.reshape('خیر')), font_name= 'font/IRANSansXFaNum-Medium.ttf', size_hint=(.5, None), size=('20mm', '6mm'))
        bt2 = Button(text= get_display(arabic_reshaper.reshape('بلی')), font_name= 'font/IRANSansXFaNum-Medium.ttf', size_hint=(.5, None), size=('20mm', '6mm'))
        #self.ids['bt2'] = bt2
        content.add_widget(bt1)
        content.add_widget(bt2)

        pop = Popup(title= get_display(arabic_reshaper.reshape('آیا از حذف کامل مشخصات اطمینان دارید؟')), title_font = 'font/IRANSansXFaNum-Medium.ttf', content= content,
        title_align= 'center', size_hint=(None, None), size=(self.width , '20mm'),separator_height= 0)
        bt1.bind(on_press= pop.dismiss)
        bt2.bind(on_press= self.delete_Personal_Information_OK)
        bt2.bind(on_press= pop.dismiss)
        bt2.bind(on_press= self.open_account_xls)
        pop.open()

    def delete_Personal_Information_OK(self, *args):
        os.remove("Personal_Information.xls")
        self.current= 'main'

    def load_account_data(self):
        self.mgr10.ids._name.text = str(self.df_account['Name'][0])
        self.mgr10.ids._last_name.text = str(self.df_account['Last name'][0])
        self.mgr10.ids._mobile_number.text = str(self.df_account['Mobile number'][0])
        self.mgr10.ids._home_number.text = str(self.df_account['Home number'][0])
        self.mgr10.ids._address.text = str(self.df_account['Address'][0])
        self.mgr10.ids._postal_code.text = str(self.df_account['Postal code'][0])
        self.mgr10.ids._email.text = str(self.df_account['Email'][0])

    def clear_account_data(self):
        self.mgr10.ids._name.str = ''
        self.mgr10.ids._name.text = ''
        self.mgr10.ids._last_name.str = ''
        self.mgr10.ids._last_name.text = ''
        self.mgr10.ids._mobile_number.str = ''
        self.mgr10.ids._mobile_number.text = ''
        self.mgr10.ids._home_number.str = ''
        self.mgr10.ids._home_number.text = ''
        self.mgr10.ids._address.str = ''
        self.mgr10.ids._address.text = ''
        self.mgr10.ids._postal_code.str = ''
        self.mgr10.ids._postal_code.text = ''
        self.mgr10.ids._email.str = ''
        self.mgr10.ids._email.text = ''

    def check_registration(self):
        # Check if the cart is empty or not
        if len(items_in_order_screen) == 0:
            content = Button(text= get_display(arabic_reshaper.reshape('بازگشت')), font_name= 'font/IRANSansXFaNum-Medium.ttf', size_hint=(1, None), size=('20mm', '6mm'))
            pop = Popup(title= get_display(arabic_reshaper.reshape('سبد خالی است!')), title_font = 'font/IRANSansXFaNum-Medium.ttf', content= content,
            title_align= 'center', size_hint=(None, None), size=(self.width , '20mm'),separator_height= 0)
            content.bind(on_release=pop.dismiss)
            pop.open()
        else:
            # Checking the registration for the next step of the order
            if os.path.isfile('Personal_Information.xls'):
                # Checking if the host has stock or not
                f.get('/domains/mahdiemadi.ir/public_html/excel/products.xls', 'products.xls')
                dataframe_products = pd.read_excel (r'products.xls')
                dataframe_products = dataframe_products.astype({"price_off": int})
                for i in range(len(items_in_order_screen)):
                    if int(items_in_order_screen[i]['num_order']) <= dataframe_products[dataframe_products['code'] == items_in_order_screen[i]['p_code']]['stock'].tolist()[0]:
                        pass
                    else:
                        error_list.append([items_in_order_screen[i]['p_code'], dataframe_products[dataframe_products['code'] == items_in_order_screen[i]['p_code']]['stock'].tolist()[0]])
                if error_list == []:
                    content = Label(text= get_display(arabic_reshaper.reshape('با شما تماس گرفته خواهد شد')), size_hint=(1, None), size=('20mm', '6mm'), font_name='font/IRANSansXFaNum-Medium.ttf')
                    pop = Popup(title= get_display(arabic_reshaper.reshape('سفارش با موفقیت ثبت شد')), title_font = 'font/IRANSansXFaNum-Medium.ttf', content= content,
                    title_align= 'center', size_hint=(None, None), size=(self.width , '20mm'),separator_height= 5)
                    pop.open()

                    # Subtract from the host data frame & upload to host
                    for i in range(len(items_in_order_screen)):                        
                        cond = dataframe_products['code'] == items_in_order_screen[i]['p_code']
                        dataframe_products.loc[cond,'stock'] = dataframe_products.loc[cond,'stock'] - int(items_in_order_screen[i]['num_order'])
                    dataframe_products.to_excel('products.xls')
                    f.put('products.xls', '/domains/mahdiemadi.ir/public_html/excel/products.xls')

                else:
                    for i in range(len(error_list)):
                        filter_list = list(filter(lambda items_in_order_screen: items_in_order_screen['p_code'] == error_list[i][0], items_in_order_screen))
                        filter_list[0]['num_order'] = str(error_list[i][1])
                        filter_list[0]['error_text'] = get_display(arabic_reshaper.reshape('موجودی ندارد')) if error_list[i][1] == 0 else get_display(arabic_reshaper.reshape('حداکثر موجودی تغییر کرده است'))
                        
                    print(error_list)
                dataframe_products = dataframe_products[dataframe_products['stock'] != 0]


            else:
                content = Button(text= get_display(arabic_reshaper.reshape('ثبت نام')), font_name= 'font/IRANSansXFaNum-Medium.ttf', size_hint=(1, None), size=('20mm', '6mm'))
                pop = Popup(title= get_display(arabic_reshaper.reshape('لطفاٌ ابتدا ثبت نام کنید')), title_font = 'font/IRANSansXFaNum-Medium.ttf', content= content,
                title_align= 'center', size_hint=(None, None), size=(self.width , '20mm'),separator_height= 0)
                content.bind(on_press=self.change_screen_signup)
                content.bind(on_release=pop.dismiss)
                pop.open()

    def change_screen_signup(self,arg):
        # Opening the registration form if not registered
        self.order_on= True
        self.mgr9.mgr1.canvas.after.get_group('a')[0].source='img/App/nav1.jpg'
        self.mgr9.text1 = '-'
        self.current= 'signup' 

    def print(self):
        self.pos_scroll_main = (self.height - self.mgr1.mgr5.height) / self.height 
        print(self.pos_scroll_main, self.mgr1.mgr5.height)
        print(self.category_dict)
    def printt(self, arg):
        print('OK')
    def print1(self):
        print('OK1')
    def print2(self):
        print('OK2')
    def print3(self):
        print('OK3')
    def print4(self):
        print('OK4')

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
        Clock.schedule_once(self.change_screen, .1)
    
    def change_screen(self, arg):
        self.root.current = 'main'
        # Access the carousel.
        carousel = self.root.mgr1.mgr3.mgr1.ids._carousel_
        # Schedule after every 3 seconds.
        Clock.schedule_interval(carousel.load_next, 3.0)

        # Add widget to scrollview1 in main screen
        list_DKP = dataframe_products[(dataframe_products['off'] != 0) & (dataframe_products['cat'] == 'H')]['DKP'].drop_duplicates().to_list()  
        j = 6 #len(list_DKP)
        for i in range(j):
            dkp = list_DKP[i]
            self.root.mgr1.mgr3.mgr2.dkp= dkp
            text_title = dataframe_products[(dataframe_products['DKP'] == dkp)]['title'].tolist()[0]
            if len(text_title) > 20:
                text_title = text_title[:17] + '...'
            self.root.mgr1.mgr3.mgr2.text_title= text_title
            # Add image from host  
            self.root.mgr1.mgr3.mgr2.source_image= 'http://mahdiemadi.ir/Products/%s/%s-0-v_200-h_200-q_90.jpg'%(dkp, dkp)
            self.root.mgr1.mgr3.mgr2.detail_1= dataframe_products[(dataframe_products['DKP'] == dkp)]['detail_3'].tolist()[0]
            self.root.mgr1.mgr3.mgr2.detail_2= dataframe_products[(dataframe_products['DKP'] == dkp)]['detail_4'].tolist()[0]
            self.root.mgr1.mgr3.mgr2.off= str(dataframe_products[(dataframe_products['DKP'] == dkp)]['off'].tolist()[0])
            price = int(dataframe_products[(dataframe_products['DKP'] == dkp)]['price'].tolist()[0])
            self.root.mgr1.mgr3.mgr2.price= f'{price:,}'
            price_off = dataframe_products[(dataframe_products['DKP'] == dkp)]['price_off'].tolist()[0]
            self.root.mgr1.mgr3.mgr2.price_off= f'{price_off:,}'
            self.root.mgr1.mgr3.mgr2.mgr1.add_widget(Factory.BoxLayout_mainscroll_scroll1())
        
        # Add widget to scrollview2 in main screen
        list_DKP_Gl = dataframe_products[(dataframe_products['off'] != 0) & (dataframe_products['cat'] == 'GL')]['DKP'].drop_duplicates().to_list()  
        for i in range(j):
            dkp_Gl = list_DKP_Gl[i]
            self.root.mgr1.mgr3.mgr3.dkp_Gl= dkp_Gl
            text_title = dataframe_products[(dataframe_products['DKP'] == dkp_Gl)]['title'].tolist()[0]
            if len(text_title) > 20:
                text_title = text_title[:17] + '...'
            self.root.mgr1.mgr3.mgr3.text_title= text_title
            # Add image from host
            self.root.mgr1.mgr3.mgr3.source_image= 'http://mahdiemadi.ir/Products/%s/%s-0-v_200-h_200-q_90.jpg'%(dkp_Gl, dkp_Gl)
            self.root.mgr1.mgr3.mgr3.detail_1= dataframe_products[(dataframe_products['DKP'] == dkp_Gl)]['detail_3'].tolist()[0]
            self.root.mgr1.mgr3.mgr3.detail_2= dataframe_products[(dataframe_products['DKP'] == dkp_Gl)]['detail_4'].tolist()[0]
            self.root.mgr1.mgr3.mgr3.off= str(dataframe_products[(dataframe_products['DKP'] == dkp_Gl)]['off'].tolist()[0])
            price = int(dataframe_products[(dataframe_products['DKP'] == dkp_Gl)]['price'].tolist()[0])
            self.root.mgr1.mgr3.mgr3.price= f'{price:,}'
            price_off = dataframe_products[(dataframe_products['DKP'] == dkp_Gl)]['price_off'].tolist()[0]
            self.root.mgr1.mgr3.mgr3.price_off= f'{price_off:,}'
            self.root.mgr1.mgr3.mgr3.mgr1.add_widget(Factory.BoxLayout_mainscroll_scroll2())
        
if __name__== "__main__":
    DigiApp().run()
 