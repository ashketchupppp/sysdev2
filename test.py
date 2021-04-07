
def saveForLater(f, *args, **kwargs):
    def wrapper():
        return f(**kwargs)
    setattr(wrapper, 'localVars', {})
    for k in kwargs:
        wrapper.localVars[k] = kwargs[k]
    return wrapper

def add(x, y):
    return x + y

x = add(1, 1)
y = saveForLater(add, x=2, y=1)
z = saveForLater(add, x=5, y=5)
print(x)
print(z())
print(y())