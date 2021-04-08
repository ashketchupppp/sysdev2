from asyncio.futures import Future
import sys
import os
import asyncio
from types import coroutine

from kivy.event import EventDispatcher

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../OnlineStoreApp')))

from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.properties import ListProperty, DictProperty, BooleanProperty

from data.DataManager import DataManager
from data.Email import EmailTemplate
from ui.ErrorPopup import catch_exceptions
from ui.OrderList import OrderList
from ui.ItemList import ItemList
from ui.AddressLabel import AddressArea

class OrderScreen(GridLayout, EventDispatcher):
    unprocessed_orders = ListProperty([])
    current_order = DictProperty()
    current_order_shipped = BooleanProperty(False)

    def __init__(self, parent, **kwargs):
        super(OrderScreen, self).__init__(**kwargs)
        self.parentApp = parent
        self.register_event_type('on_start_reload')
        self.cols = 4
        self.reloadButton = Button(text="Reload Orders")
        self.orderList = OrderList(itemClickCallback=self.updateCurrentOrder)
        self.addressArea = AddressArea()
        self.setOrderAsProcessedBtn = Button(text="Set order as processed")
        self.itemList = ItemList()
        self.currentOrderLabel = Label(text="Selected order: ")
        self.emailTemplate = TextInput(readonly=True)
        
        self.reloadButton.bind(on_press=self.on_start_reload)
        self.bind(unprocessed_orders=self.orderList.update)
        self.bind(current_order=self.addressArea.updateAddressLabel)
        self.bind(current_order=self.itemList.updateItems)
        self.bind(current_order=self.setCurrentOrderText)
        self.bind(current_order=self.outputOrderShippedEmail)
        self.setOrderAsProcessedBtn.bind(on_press=self.setOrderToShipped)
        self.bind(current_order_shipped=self.on_start_reload)

        self.add_widget(self.orderList)
        self.add_widget(self.setOrderAsProcessedBtn)
        self.add_widget(self.reloadButton)
        self.add_widget(self.addressArea)
        self.add_widget(self.itemList)
        self.add_widget(self.currentOrderLabel)
        self.add_widget(self.emailTemplate)
        
    @catch_exceptions
    def updateCurrentOrder(self, orderID):
        task = OnlineStoreApp.runAsync(self.parentApp.getAllOrderDetails(orderID, callback=self.setCurrentOrder))

    @catch_exceptions
    def on_start_reload(self, instance, value=None):
        task = OnlineStoreApp.runAsync(self.parentApp.reload(self.setUnprocessedOrders))
        
    @catch_exceptions
    def setOrderToShipped(self, instance):
        task = OnlineStoreApp.runAsync(self.parentApp.setOrderAsShipped(orderID=self.current_order['id'],
                                                                        callback=self.setCurrentOrder))
        
    @catch_exceptions
    def outputOrderShippedEmail(self, instance=None, value=None):
        self.emailTemplate.text = EmailTemplate.orderProcessedEmail(self.current_order['name'],
                                                                    self.current_order['items'],
                                                                    self.current_order['id'])
    
    def setCurrentOrderText(self, instance, value):
        self.currentOrderLabel.text = f"Selected order: {value['id']}"
        
    def setCurrentOrder(self, value):
        if type(value) == Future:
            self.current_order = value.result()
        else:
            self.current_order = value
        self.current_order_shipped = True if self.current_order['status'] == "shipped" else False

    def setUnprocessedOrders(self, value):
        if type(value) == Future:
            self.unprocessed_orders = value.result()
        else:
            self.unprocessed_orders = value

class OnlineStoreApp(App):
    """ The main kivy app, acts as an interface between the screens and the DataManager
    """
    eventLoop = None
    coroQueue = asyncio.Queue()
    
    def __init__(self, loop, **kwargs):
        super().__init__(**kwargs)
        OnlineStoreApp.eventLoop = loop
        self.dataManager = DataManager(configFile=DataManager.configOverridesFile)
        
    def runWithBackend(self):
        ''' Runs the kivy app and the backend coroutine queue executor
        '''
        async def run_wrapper():
            # Run the Kivy UI
            await self.async_run()
            exit(0)

        return asyncio.gather(run_wrapper(), self.dataManager.waitForCoroutineQueue(OnlineStoreApp.coroQueue))

    @classmethod
    def runAsync(self, coro) -> asyncio.Task:
        OnlineStoreApp.coroQueue.put_nowait(coro)

    def build(self):
        return OrderScreen(parent=self)
    
    @catch_exceptions
    async def reload(self, callback):
        await self.dataManager.reload()
        callback(await self.dataManager.getUnprocessedOrders(asDict=True))
    
    @catch_exceptions
    async def setOrderAsShipped(self, orderID, callback):
        succeeded = await self.dataManager.setOrderToShipped(orderID)
        if succeeded:
            callback(await self.getAllOrderDetails(orderID))
    
    @catch_exceptions
    async def getAllOrderDetails(self, orderID, callback=None):
        order = dict(await self.dataManager.getOrder(orderID))
        customer = await self.dataManager.getCustomer(order['customerEmail'])
        order['name'] = customer['name']
        order['items'] = await self.dataManager.getOrderPackingList(orderID)
        if callback != None:
            callback(dict(order))
        else:
            return dict(order)
    
    @catch_exceptions
    async def getOrder(self, orderID, callback=None):
        order = await self.dataManager.getOrder(orderID)
        if callback != None:
            callback(dict(order))
        else:
            return dict(order)
    
def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(OnlineStoreApp(loop).runWithBackend())
    loop.close()
    
if __name__ == '__main__':
    main()