from abc import ABC, abstractmethod

class ConfigObject(ABC):
    """ !!! This class is a work in progress and not used anywhere !!!
        This is an abstract class whose purpose is to allow an inheritor to be created from a JSON file.
        This would automate the process of loading and dumping of the application configuration.
        
        The idea is that you provide a dictionary (that could be loaded from a JSON file) and the classes are created with the variables passed
        MyClass(**{
            "x" : 8,
            "MyOtherClass" : {
                "b" : "No"
            }
        })
        Would produce an instance of MyClass that has the variable "x" and another config object called "MyOtherClass".
        
        This would automate the process of adding new configurable options to the configuration JSON file.
        Instead of adding logic to create objects and give them values from a config, 
        you define a ConfigObject and it's configurable variables are automatically added to the configuration file.
        
        NOTE
            This implementation is half-baked =P
        
        TODO
            Need to think about how to deal with config objects that may be hidden in lists
    """
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

if __name__ == "__main__":
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