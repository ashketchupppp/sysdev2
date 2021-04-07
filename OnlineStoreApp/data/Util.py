from urllib.request import urlopen
import aiohttp

def getFileContents(filepath):
    fileHandle = open(filepath, "r")
    contents = fileHandle.read()
    fileHandle.close()
    return contents

def writeToFile(filepath, contents):
    fileHandle = open(filepath, "w")
    fileHandle.write(contents)
    fileHandle.close()
    
def doGet(url):
    response = urlopen(url)
    return response.read().decode()
    
async def doGetAsync(url):
    """ Performs a HTTP GET request asynchronously using aiohttp
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:
            return await r.json()
        
def saveForLater(f, **kwargs):
    """ Returns a new function that calls the one passed with the args passed.
        You're "saving the function for later" so that you can pass the function around, with its arguments,
        and not have to pass the arguments around with it for when you want it to be called.
        Useful for kivy, where lots of your code is processed by kivy which makes getting your arguments in the right place somtimes difficult,
        it is easier to package a function into a new one, with the arguments, and have kivy call it.
    """
    def wrapper():
        return f(**kwargs)
    setattr(wrapper, 'localVars', {})
    for k in kwargs:
        wrapper.localVars[k] = kwargs[k]
    return wrapper