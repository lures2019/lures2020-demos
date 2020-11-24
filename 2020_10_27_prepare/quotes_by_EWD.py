files = open('quotes_by_EWD.txt').readlines()
for i in range(len(files)):
    values = list(files[i].split(' '))[0]
    if values == 'The':
        print('{} {}'.format(i,values))