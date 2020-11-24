# Part1
number = input('One positive integer please：').split('#')[-1]
try:
    if(eval(number) <= 1):
        print('{} is not prime!')
    else:
        num = 0
        for i in range(2,eval(number)):
            if(eval(number) % i == 0):
                print('{} is not prime!'.format(eval(number)))
                num = -1
                break
        if(num == 0):
            print('{} is prime：)'.format(eval(number)))
except Exception as error:
    print('输入格式错误！')

# Part2
upper = int(input())
numbers = []
for num in range(1, upper + 1):
    # 素数大于 1
    if num > 1:
        for i in range(2, num):
            if (num % i) == 0:
                break
        else:
            numbers.append(num)
print('Prime numbers：',end='')
print(",".join(str(i) for i in numbers))
