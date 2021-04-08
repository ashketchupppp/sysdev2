import asyncio
from re import S
from types import coroutine

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button

coroutineQueue : asyncio.Queue = asyncio.Queue()

class DataManager:
    async def someTask(self):
        await asyncio.sleep(3)
        print([1, 2, 3])
    
    async def waitForCoroutineQueue(self):
        while True:
            if coroutineQueue.empty():
                await asyncio.sleep(0.1)
            else:
                coro = await coroutineQueue.get()
                await coro

class TestApp(App, GridLayout):
    def __init__(self, loop, **kwargs):
        super(TestApp, self).__init__(**kwargs)
        self.eventLoop = loop
        self.cols = 1
        self.rows = 1
        self.btn = Button()
        self.btn.bind(on_press=self.doSomeTask)
        self.add_widget(self.btn)
        self.dataManager = DataManager()
        
    def build(self):
        return self
        
    def app_func(self):
        '''Wrapper functions for the async processes.
        '''
        async def run_wrapper():
            # Run the Kivy UI
            await self.async_run()  
            exit(0)

        return asyncio.gather(run_wrapper(), self.dataManager.waitForCoroutineQueue())
        
    def doSomeTask(self, value):
        coroutineQueue.put_nowait(self.dataManager.someTask())

def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(TestApp(loop).app_func())
    loop.close()
    
if __name__ == '__main__':
    main()