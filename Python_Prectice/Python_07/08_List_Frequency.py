numbers = [10, 20, 10, 30, 20, 10, 40]


feq = {}

for i in numbers:
    if i in feq:
        feq[i] = feq[i]+1
    else :
       feq[i] = 1


print(feq) 