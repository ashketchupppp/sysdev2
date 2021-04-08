from kivy.uix.button import Button
from kivy.uix.recycleview import RecycleView

class ItemListItem(Button):
    def __init__(self, **kwargs):
        super(ItemListItem, self).__init__(**kwargs)
        self.size_hint = self.size_hint_max

class ItemList(RecycleView):
    def __init__(self, **kwargs):
        super(ItemList, self).__init__(**kwargs)
        self.data = []
        
    def updateItems(self, instance, order):
        items = [{'text' : f'{item["name"]} - Location: {item["location"]}'} for item in order['items']]
        self.data = items
        self.refresh_from_data()