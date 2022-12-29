from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout


class MyApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        answer = TextInput(multiline=False, text="", size_hint=(1, 0.5))
        ansLen = Label(bold=True, halign="center", text="", size_hint=(1, 0.5))

        answer.bind(text=lambda instance, text: setattr(ansLen, "text", str(len(text))))
        layout.add_widget(answer)
        layout.add_widget(ansLen)
        return layout


if __name__ == '__main__':
    MyApp().run()