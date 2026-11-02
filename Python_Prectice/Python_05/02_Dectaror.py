def sumNumber(func):
    def wrapper(a, b):
        print('Sum of two numbers:')
        result = func(a, b)
        print('Sum is done')
        return result

    return wrapper


@sumNumber
def sumAdd(a,b):
   return a+b

result = sumAdd(20,40)

print(result)