import random as rm
# star  = 0

# while star <100:
#     star+=1
#     if star == 95:
#         break

# print(star)

attempt = 1

correctNumber = 121

while attempt<=3 :
   number = int(input('Enter Number : '))
   if number == correctNumber:
      print('Congratulation')
      break
   elif number < correctNumber:
      print('Number is short try agian')
   else:
       print('Number is high try agian')
   attempt+=1
else :
      print('Try your luck next time ')
      

