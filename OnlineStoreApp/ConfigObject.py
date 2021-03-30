from abc import ABC, abstractmethod

class ConfigObject(ABC):
    ConfigObjects = [cls.__name__ for cls in ConfigObject.__subclasses__()]
    
    def __init__(self, **kwargs):
        for key in self.defaults():
            if not key in self.__dict__:
                setattr(self, key, self.defaults()[key])
        
        for key in kwargs:
            setattr(self, key, kwargs[key])
            
    @abstractmethod
    def defaults(self):
        pass