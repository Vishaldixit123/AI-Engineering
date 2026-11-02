opreator = input('Enter you opretion : ')

num1 = int(input('Enter your number 1 : '))
num2 = int(input('Enter your number 2 : '))


def calculation (opreator,num1,num2)->int:
    if opreator == 'Sum':
        return num1+num2
    elif opreator == 'MultiPly':
        return num1*num2
    elif opreator == 'Devided':
        return num1/num2
    elif opreator == 'Quotient':
        return num1//num2
    elif opreator == 'remainder':
        return num1%num2
    else :
        return num1 - num2



result = calculation(opreator,num1,num2)

print(result)