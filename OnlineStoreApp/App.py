from types import GetSetDescriptorType
import sys
import os
from typing import List

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../OnlineStoreOnlineStoreApp')))

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.properties import ListProperty

from OnlineStoreApp.DataManager import DataManager

class OrderList(Label):
    unprocessed_orders = ListProperty([])
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def on_unprocessed_orders(self, instance):
        self.text = str(OrderList.unprocessed_orders)

class ReloadButton(Button):
    def __init__(self, text="Reload", **kwargs):
        super().__init__(text=text, **kwargs)
        self.bind(on_press=lambda x : Clock.schedule_once(OnlineStoreApp.on_reload))

class OrderScreen(GridLayout):
    
    def __init__(self, **kwargs):
        super(OrderScreen, self).__init__(**kwargs)
        self.cols = 2
        self.reloadButton = ReloadButton()
        self.orderList = OrderList()
        self.add_widget(self.orderList)
        self.add_widget(self.reloadButton)

class OnlineStoreApp(App):
    dataManager = DataManager()
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.register_event_type('on_reload')

    def build(self):
        return OrderScreen()

    def on_reload(self, *args):
        OnlineStoreApp.dataManager.reload()
        OrderList.unprocessed_orders = OnlineStoreApp.dataManager.getUnprocessedOrders()


if __name__ == '__main__':
    OnlineStoreApp().run()