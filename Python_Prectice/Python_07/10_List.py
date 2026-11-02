numbers = [10, 20, 10, 30, 20, 40, 50, 30]


uniqe = []

for i in numbers:
    if i not in uniqe:
       uniqe.append(i)


print(uniqe)