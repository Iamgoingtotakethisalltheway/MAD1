def uppercase_dec(function):
    def wrapper():
        func = function()
        make_uppercase = func.upper()
        return make_uppercase
    return wrapper

@uppercase_dec
def say_hi():
    return "hello there"

print(say_hi())
