from configparser import Error
from inspect import trace
import sys
import os
from pathlib import Path
import traceback
import functools
import asyncio

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../OnlineStoreApp')))

from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.recycleview import RecycleView
from kivy.properties import ListProperty
from kivy.uix.popup import Popup
from kivy.core.clipboard import Clipboard
from kivy.uix.boxlayout import BoxLayout

from data.DataManager import DataManager

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

class OrderListItem(Button):
    def __init__(self, **kwargs):
        super(OrderListItem, self).__init__(**kwargs)

class OrderList(RecycleView):
    def __init__(self, itemClickEvent, **kwargs):
        super(OrderList, self).__init__(**kwargs)
        self.data = []
        self.itemClickEvent = itemClickEvent
    
    def update(self, data):
        for item in data:
            self.data.append({'text' : f'Order {item["id"]}'})
        self.refresh_from_data()
        
class OrderWindow(GridLayout):
    def __init__(self, **kwargs):
        super(OrderWindow, self).__init__(**kwargs)
        self.cols = 2
        self.rows = 2
        self.info = TextInput()
        self.add_widget(self.info)
        
    def update(self, order):
        self.info.text = str(order)

class ReloadButton(Button):
    def __init__(self, text="Reload", **kwargs):
        super().__init__(text=text, **kwargs)

class OrderScreen(GridLayout):
    unprocessedOrders = ListProperty([])
    
    def __init__(self, **kwargs):
        super(OrderScreen, self).__init__(**kwargs)
        self.register_event_type('on_start_reload')
        self.register_event_type('on_order_item_selected')
        self.cols = 2
        self.reloadButton = ReloadButton()
        self.orderList = OrderList(itemClickEvent=self.on_order_item_selected)
        self.orderWindow = OrderWindow()
        
        self.reloadButton.bind(on_press=self.on_start_reload)
        # \/ This doesn't work \/
        # self.bind(unprocessedOrders=self.orderList.update)

        self.add_widget(self.orderList)
        self.add_widget(self.reloadButton)
        self.add_widget(self.orderWindow)
        
    @catch_exceptions
    def on_order_item_selected(self, instance):
        pass
        # order = OnlineStoreApp.dataManager.getOrder(instance.id)
        # self.orderWindow.update(order)

    @catch_exceptions
    def on_start_reload(self, instance):
        OnlineStoreApp.dataManager.reload()
        OrderScreen.unprocessedOrders = OnlineStoreApp.dataManager.getUnprocessedOrders(asDict=True)
         # calling update manually, couldn't figure out how to get it be called when unprocessedOrders changes
        self.orderList.update(OrderScreen.unprocessedOrders)

class OnlineStoreApp(App):
    dataManager = DataManager()
    ordersList = ListProperty([])
    
    def app_func(self):
        '''Wrapper functions for the async processes.
        '''
        def run_wrapper():
            # Run the Kivy UI
             self.async_run()
            exit(0)

        return asyncio.gather(run_wrapper())
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        return OrderScreen()
    
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    onlineStoreApp = OnlineStoreApp()
    loop.run_until_complete(onlineStoreApp.app_func())
    loop.close()