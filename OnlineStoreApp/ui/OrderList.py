from kivy.uix.button import Button
from kivy.uix.recycleview import RecycleView

from data.Util import saveForLater

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