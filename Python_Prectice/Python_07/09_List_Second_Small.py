numbers = [10, 50, 30, 80, 20, 60]

largest = numbers[0]

second_largest = numbers[0]

for i in numbers:
    if i > largest:
        second_largest = largest
        largest = i
    elif   i > second_largest and i!= largest :

        second_largest = i


print(f'Largest number is {largest} and second largest is {second_largest}' )