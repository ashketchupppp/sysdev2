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
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:
            return  r.json()
