from abc import ABC, abstractclassmethod, abstractmethod

class ConfigObject(ABC):
    ConfigObjects = []
    
    class NonexistantConfigKey(Exception):
        pass
    
    def __init__(self, **kwargs):
        # setup the list of all config objects
        ConfigObject.ConfigObjects = [cls.__name__ for cls in ConfigObject.__subclasses__()]
        defaults = self.setToDefault()
        for key in kwargs:
            if not key in defaults:
                raise ConfigObject.NonexistantConfigKey(key)
            self.setValue(key, kwargs[key])

        ConfigObject.ConfigObjects.append(self)
        
    def setValue(self, key, value):
        # if the key is itself a config object, make sure we create it as one, otherwise just set the attribute
        if type(value) == dict and key in ConfigObject.ConfigObjects:
            setattr(self, key, globals()[key](**value))
        else:
            setattr(self, key, value)
            
    def setToDefault(self):
        """ This sets the object to its default values 
        """
        defaults = self.defaults()
        for key in defaults:
            self.setValue(key, defaults[key])
        return defaults
    
    @abstractmethod
    def defaults(self):
        """ This method must return a dictionary containing all of the possible configurable values this object can have
        """
        pass

class MyOtherClass(ConfigObject):
    defaultConfig = {
            "b" : "hello"
        }
    
    def defaults(self):
        return MyOtherClass.defaultConfig
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
class MyClass(ConfigObject):
    defaultConfig = {
            "x" : 10,
            "MyOtherClass" : {}
        }
    
    def defaults(self):
        return MyClass.defaultConfig
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

t = MyClass()
a = MyClass(**{"x" : 9})
s = MyClass(**{
    "x" : 8,
    "MyOtherClass" : {
        "b" : "No"
    }
})
x = MyClass(**{
    "x" : 8,
    "MyOtherClass" : {}
})
print(t.x)
print(a.x)
print(s.MyOtherClass)
print(s.MyOtherClass.b)
print(x.MyOtherClass)
print(x.MyOtherClass.b)
    
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