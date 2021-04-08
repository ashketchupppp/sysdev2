from typing import Text
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.core.clipboard import Clipboard

class AddressArea(GridLayout):
    def __init__(self, **kwargs):
        super(AddressArea, self).__init__(**kwargs)
        self.cols = 1
        self.rows = 2
        self.textBox = TextInput()
        self.copyAddressBtn = Button(text="Copy Address Label")
        self.copyAddressBtn.bind(on_press=self.copyAddressToClipboard)
        
        self.add_widget(self.textBox)
        self.add_widget(self.copyAddressBtn)
        
    def copyAddressToClipboard(self, instance):
        Clipboard.copy(self.textBox.text)
        
    def updateAddressLabel(self, instance, order):
        addressString = f"""{order['name']}
{order['streetNameAndNumber']}
{order['line1']}
{order['line2']}
{order['country']}
{order['postcode']}"""
        self.textBox.text = addressString