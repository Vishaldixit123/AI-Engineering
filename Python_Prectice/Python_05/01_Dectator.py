def log(func):
    def wrapper():
     print('Hello start')
     func()
     print('Stop')
    return wrapper


@log
def call():
  print('call')


call()