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
from kivy.properties import ListProperty, DictProperty

from data.DataManager import DataManager
from data.Util import saveForLater
from ui.ErrorPopup import catch_exceptions
from ui.OrderList import OrderList
from ui.ItemList import ItemList

        
class OrderWindow(GridLayout):
    def __init__(self, **kwargs):
        super(OrderWindow, self).__init__(**kwargs)
        self.cols = 2
        self.rows = 2
        self.info = TextInput()
        self.add_widget(self.info)
        
    def update(self, instance, order):
        self.updateAddressLabel(order)
        
    def updateAddressLabel(self, order):
        addressString = f"""{order['name']}
{order['streetNameAndNumber']}
{order['line1']}
{order['line2']}
{order['country']}
{order['postcode']}"""
        self.info.text = addressString

class OrderScreen(GridLayout, EventDispatcher):
    unprocessed_orders = ListProperty([])
    current_order = DictProperty()

    def __init__(self, parent, **kwargs):
        super(OrderScreen, self).__init__(**kwargs)
        self.parentApp = parent
        self.register_event_type('on_start_reload')
        self.cols = 2
        self.reloadButton = Button(text="Reload Orders")
        self.orderList = OrderList(itemClickCallback=self.updateCurrentOrder)
        self.orderWindow = OrderWindow()
        
        self.reloadButton.bind(on_press=self.on_start_reload)
        self.bind(unprocessed_orders=self.orderList.update)
        self.bind(current_order=self.orderWindow.update)

        self.add_widget(self.orderList)
        self.add_widget(self.reloadButton)
        self.add_widget(self.orderWindow)
        
    @catch_exceptions
    def updateCurrentOrder(self, orderID):
        task = OnlineStoreApp.runAsync(self.parentApp.getAllOrderDetails(orderID, callback=self.setCurrentOrder))

    def on_start_reload(self, instance):
        task = OnlineStoreApp.runAsync(self.parentApp.reload(self.setUnprocessedOrders))
        
    def setCurrentOrder(self, value):
        if type(value) == Future:
            self.current_order = value.result()
        else:
            self.current_order = value

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