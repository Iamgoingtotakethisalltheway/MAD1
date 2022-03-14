import functools

def split_str(function):
    @functools.wraps(function)
    def wrapper():
        func = function()
        splitted_str = func.split()
        return splitted_str
    return wrapper

def uppercase_dec(function):
    @functools.wraps(function)
    def wrapper():
        func = function()
        make_uppercase = func.upper()
        return make_uppercase
    return wrapper

@split_str
@uppercase_dec
def say_hi():
    return "hello there"

print(say_hi())
