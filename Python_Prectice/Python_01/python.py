#print("Hello")

print("Hello",True,344,66858.56, sep = '_');

# print number after passing inside the function
def add_name(name):
    return name

# store number inside the variable
name1= add_name('Vishal');

print(name1)

# Store the list of names
name = ['vishal', 'Dixit','ramya']

for n in name:
    if n == 'vishal':
       name.append('ok')
    print(n)