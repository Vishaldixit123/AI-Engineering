text = 'madam'

# reverse = text[::1]

# if text == reverse:
#     print('Its palindrome')




start = 0
last = len(text)-1

while start< last:
    if text[start] != text[last]:
        print ('Not correcr')
        break
    start+=1
    last-=1
else:
    print('correct')



    