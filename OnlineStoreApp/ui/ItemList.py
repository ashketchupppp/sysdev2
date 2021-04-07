from kivy.uix.button import Button
from kivy.uix.recycleview import RecycleView

class ItemListItem(Button):
    def __init__(self, **kwargs):
        super(ItemListItem, self).__init__(**kwargs)

class ItemList(RecycleView):
    def __init__(self, **kwargs):
        super(ItemList, self).__init__(**kwargs)
        self.data = []