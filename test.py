from threading import Thread
import asyncio
import time
import random
import inspect
import queue

class Worker(Thread):
    def __init__(self):
        self.taskQueue = queue.Queue()
        self.end = False
        super(Worker, self).__init__()
        
    def addTask(self, coro):
        print(f"put {coro} in queue")
        self.taskQueue.put(coro)
        
    def nextTask(self):
        try:
            return self.taskQueue.get()
        except queue.Empty:
            return None
        
    def run(self):
        # discordclient.run()
        print(f"{self.getName()} running")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        while not self.end:
            try:
                task = self.nextTask()
                if task:
                    loop.run_until_complete(task)
            except queue.Empty as e:
                pass
        loop.close()
        print(f"{self.getName()} finished")
        
    def finish(self):
        try:
            while asyncio.current_task():
                pass
        except RuntimeError:
            pass
        self.end = True
        
    def sayHi(self):
        print(f"Hello from {self.getName()}")


bots = [Worker(), Worker(), Worker()]
for bot in bots:
    bot.start()

bot = random.choice(bots)
bot.addTask(bot.sayHi())