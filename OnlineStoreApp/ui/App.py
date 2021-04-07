from asyncio.futures import Future
from asyncio.locks import Event
from configparser import Error
from inspect import trace
import sqlite3
import sys
import os
from pathlib import Path
import traceback
import functools
import asyncio

from kivy.event import EventDispatcher

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
from data.Util import saveForLater

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
    def __init__(self, itemClickCallback, **kwargs):
        super(OrderList, self).__init__(**kwargs)
        self.data = []
        self.itemClickCallback = itemClickCallback
    
    def update(self, instance, value):
        for item in value:
            self.data.append({'text' : f'Order {item["id"]}', 'on_press' : saveForLater(self.itemClickCallback, orderID=item["id"])})
        self.refresh_from_data()
        
class OrderWindow(GridLayout):
    def __init__(self, **kwargs):
        super(OrderWindow, self).__init__(**kwargs)
        self.cols = 2
        self.rows = 2
        self.info = TextInput()
        self.add_widget(self.info)
        
    def updateAddressLabel(self, order):
        addressString = f"""{order['name']}
{order['streetNameAndNumber']}
{order['line1']}
{order['line2']}
{order['country']}
{order['postcode']}"""
        self.info.text = addressString

class ReloadButton(Button):
    def __init__(self, text="Reload", **kwargs):
        super().__init__(text=text, **kwargs)

class OrderScreen(GridLayout, EventDispatcher):
    unprocessed_orders = ListProperty([])

    def __init__(self, parent, **kwargs):
        super(OrderScreen, self).__init__(**kwargs)
        self.parentApp = parent
        self.register_event_type('on_start_reload')
        self.cols = 2
        self.reloadButton = ReloadButton()
        self.orderList = OrderList(itemClickCallback=self.updateCurrentOrder)
        self.orderWindow = OrderWindow()
        
        self.reloadButton.bind(on_press=self.on_start_reload)
        self.bind(unprocessed_orders=self.orderList.update)

        self.add_widget(self.orderList)
        self.add_widget(self.reloadButton)
        self.add_widget(self.orderWindow)
        
    @catch_exceptions
    def updateCurrentOrder(self, orderID):
        task = OnlineStoreApp.runAsync(self.parentApp.getAllOrderDetails(orderID, callback=self.orderWindow.updateAddressLabel))

    @classmethod
    def updateOrderList(self):
        self.orderList.update()

    def on_start_reload(self, instance):
        task = OnlineStoreApp.runAsync(self.parentApp.reload(self.setUnprocessedOrders))

    def setUnprocessedOrders(self, value):
        if type(value) == Future:
            self.unprocessed_orders = value.result()
        else:
            self.unprocessed_orders = value

class OnlineStoreApp(App):
    """ The main kivy app, acts as an interface between the screens and the DataManager
    """
    eventLoop = None
    
    def __init__(self, loop, **kwargs):
        super().__init__(**kwargs)
        OnlineStoreApp.eventLoop = loop
        self.dataManager = DataManager()
        
    def app_func(self):
        '''Wrapper functions for the async processes.
        '''
        async def run_wrapper():
            # Run the Kivy UI
            await self.async_run()  
            exit(0)

        return asyncio.gather(run_wrapper())
    
    @classmethod
    def runAsync(self, coro) -> asyncio.Task:
        return OnlineStoreApp.eventLoop.create_task(coro)

    def build(self):
        return OrderScreen(parent=self)
    
    async def reload(self, callback):
        await self.dataManager.reload()
        callback(await self.dataManager.getUnprocessedOrders(asDict=True))
        
    async def getAllOrderDetails(self, orderID, callback=None):
        order = dict(await self.dataManager.getOrder(orderID))
        customer = await self.dataManager.getCustomer(order['customerEmail'])
        order['name'] = customer['name']
        order['items'] = await self.dataManager.getOrderPackingList(orderID)
        if callback != None:
            callback(dict(order))
        else:
            return dict(order)
        
    async def getOrder(self, orderID, callback=None):
        order = await self.dataManager.getOrder(orderID)
        if callback != None:
            callback(dict(order))
        else:
            return dict(order)
    
def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(OnlineStoreApp(loop).app_func())
    loop.close()
    
if __name__ == '__main__':
    main()