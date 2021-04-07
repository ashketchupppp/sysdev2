import traceback
import functools

from kivy.uix.popup import Popup
from kivy.core.clipboard import Clipboard
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

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
        
def catch_exceptions(job_func):
    """ Decorator that wraps the function in a try except block, if the function throws 
        then it is displayed in an error popup rather than allowing everything to burn to the ground.
    """
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