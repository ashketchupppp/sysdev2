from urllib.request import urlopen
import sqlite3

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

class Struct:
    """ In JavaScript you can load dictionaries as JavaScript objects and access their values
        using dot notation "class.attribute" instead of "class['attribute']".
        There's no functional difference between the two, however the dot notation is alot nicer to read.
        
        This is Utility class that can be created from a dictionary.
        Every item in the dictionary is added to this class's __dict__, thus being able to be
        accessed using dot notation. All nested dictionaries are also converted into Structs, so you could do this:
            exampleDict = {
                "a" : 1,
                "b" : {
                    "c" : "string"
                }
            }
            d = Struct(**exampleDict)
            
            # both of these work
            print(d.b.c)
            print(d["b"]["c"])
        
        You can use it in place of an actual dictionary because it implements all the magic methods a dict does!
        I'm basically just adding dot notation to the python dictionary :)
    """
    def __init__(self, **kwargs):
        for kw in kwargs.keys():
            if type(kwargs[kw]) == dict:
                setattr(self, kw, Struct(**kwargs[kw]))
            else:
                setattr(self, kw, kwargs[kw])
    
    def __setitem__(self, key, item):
        self.__dict__[key] = item

    def __getitem__(self, key):
        return self.__dict__[key]

    def __repr__(self):
        return repr(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __delitem__(self, key):
        del self.__dict__[key]

    def clear(self):
        return self.__dict__.clear()

    def copy(self):
        return self.__dict__.copy()

    def has_key(self, k):
        return k in self.__dict__

    def update(self, *args, **kwargs):
        return self.__dict__.update(*args, **kwargs)

    def keys(self):
        return self.__dict__.keys()

    def values(self):
        return self.__dict__.values()

    def items(self):
        return self.__dict__.items()

    def pop(self, *args):
        return self.__dict__.pop(*args)

    def __cmp__(self, dict_):
        return self.__cmp__(self.__dict__, dict_)

    def __contains__(self, item):
        return item in self.__dict__

    def __iter__(self):
        for item in self.__dict__:
            if type(item) == Struct:
                yield dict(item)
            else:
                yield item

    def __unicode__(self):
        return unicode(repr(self.__dict__))