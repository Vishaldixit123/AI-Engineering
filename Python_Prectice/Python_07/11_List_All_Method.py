numbers = [10, 20, 30, 40, 50]

# 1. Access - First element
print(numbers[0])       # 10

# 2. Negative indexing - Last element
print(numbers[-1])      # 50

# 3. Slicing - Specific elements
print(numbers[1:4])     # [20, 30, 40]

# 4. Update - Change value
numbers[0] = 100
print(numbers)          # [100, 20, 30, 40, 50]

# 5. Membership - Check value exists
print(20 in numbers)    # True

# 6. Not membership - Check value absent
print(60 not in numbers) # True

# 7. Concatenation - Combine two lists
list1 = [10, 20]
list2 = [30, 40]
print(list1 + list2)    # [10, 20, 30, 40]

# 8. Repetition - Repeat elements
print(list1 * 2)        # [10, 20, 10, 20]

# 9. Length - Total elements
print(len(numbers))     # 5

# 10. Delete - Delete by index
del numbers[0]
print(numbers)          # [20, 30, 40, 50]