from configparser import Error
from inspect import trace
import sys
import os
from pathlib import Path
import traceback
import functools

from kivy.app import App, Builder
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.recycleview import RecycleView
from kivy.properties import ListProperty
from kivy.uix.popup import Popup
from kivy.core.clipboard import Clipboard
from kivy.uix.boxlayout import BoxLayout

def catch_exceptions(job_func):
    @functools.wraps(job_func)
    def wrapper(*args, **kwargs):
        try:
            job_func(*args, **kwargs)
        except:
            e = traceback.format_exc()
            print(e)
            errorMessage = ErrorPopup(title="An error occurred", 
                                      contentText=e)
            errorMessage.open()
    return wrapper

class ErrorPopup(Popup):
    class Content(BoxLayout):
        def __init__(self, parent, contentText, **kwargs):
            super(ErrorPopup.Content, self).__init__(**kwargs)
            self.textInput = TextInput(text=contentText)
            self.copyButton = Button(text='Copy to clipboard')
            self.exitButton = Button(text='Click to close')
            
            self.exitButton.bind(on_press=parent.dismiss)
            self.copyButton.bind(on_press=self.copyError)
            
            self.add_widget(self.textInput)
            self.add_widget(self.copyButton)
            self.add_widget(self.exitButton)
        
        def copyError(self, instance):
            Clipboard.copy(self.textInput.text)
    
    def __init__(self, contentText, **kwargs):
        super(ErrorPopup, self).__init__(**kwargs)
        self.content = ErrorPopup.Content(parent=self, contentText=contentText)

class OrderList(RecycleView):
    def __init__(self, **kwargs):
        super(OrderList, self).__init__(**kwargs)
        self.data = []
    
    def update(self, data):
        for item in data:
            self.data.append({'text' : f'Order {item["id"]}'})
        self.refresh_from_data()

class ReloadButton(Button):
    def __init__(self, text="Reload", **kwargs):
        super().__init__(text=text, **kwargs)


class OrderScreen(GridLayout):
    unprocessedOrders = ListProperty()
    
    def __init__(self, **kwargs):
        super(OrderScreen, self).__init__(**kwargs)
        self.register_event_type('on_start_reload')
        self.cols = 2
        self.reloadButton = ReloadButton()
        self.orderList = OrderList()
        
        self.reloadButton.bind(on_press=self.on_start_reload)
        # self.bind(unprocessedOrders=self.orderList.update) I have no idea why this won't call update :(

        self.add_widget(self.orderList)
        self.add_widget(self.reloadButton)

    @catch_exceptions
    def on_start_reload(self, instance):
        OrderScreen.unprocessedOrders = [{'text' : 'test'}]
        self.orderList.update(OrderScreen.unprocessedOrders)

class OnlineStoreApp(App):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        return OrderScreen()

if __name__ == '__main__':
    OnlineStoreApp().run()