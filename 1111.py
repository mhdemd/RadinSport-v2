# Sample Python application demonstrating the
# working of Dynamic placement in FloatLayout in Kivy
  
import kivy
  
# base Class of your App inherits from the App class.  
# app:always refers to the instance of your application  
from kivy.app import App
  
# creates the button in kivy 
# if not imported shows the error 
from kivy.uix.button import Button
  
# module consist the floatlayout
# to work with FloatLayout first
# you have to import it
from kivy.uix.floatlayout import FloatLayout
  
# To change the kivy default settings 
# we use this module config 
from kivy.config import Config 
    
# 0 being off 1 being on as in true / false 
# you can use 0 or 1 && True or False 
Config.set('graphics', 'resizable', True) 
  
# creating the App class
class MyApp(App):
  
    def build(self):
  
        # creating Floatlayout
        Fl = FloatLayout()
  
        # creating button
        # a button 30 % of the width and 50 %
        # of the height of the layout and
        # positioned at 20 % right and 20 % up
        # from bottom left, i.e x, y = 200, 200 from bottom left:
        btn = Button(text ='first', size_hint =(.3, .5),
                     background_color =(.3, .6, .7, 1),
                    pos_hint ={'x':.2, 'y':.2 })
        btn1 = Button(text ='second', size_hint =(.3, .5),
                     background_color =(.3, .6, .7, 1),
                    pos_hint ={'x':.3, 'y':.2 })
        # adding widget i.e button
        Fl.add_widget(btn)
        Fl.add_widget(btn1)
        # return the layout
        return Fl
  
# run the App
if __name__ == "__main__":
    MyApp().run()