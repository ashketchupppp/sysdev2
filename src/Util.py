
def getFileContents(filepath):
    fileHandle = open(filepath, "r")
    contents = fileHandle.read()
    fileHandle.close()
    return contents

def writeToFile(filepath, contents):
    fileHandle = open(filepath, "w")
    fileHandle.write(contents)
    fileHandle.close()