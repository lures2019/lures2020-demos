# Part1
number = input('Integer：')
try:
    if(eval(number) < 0 and eval(number) % 2 == 1):
        print('{} passes the test!'.format(eval(number)))
    elif((eval(number) >= 20 and eval(number) < 200) and eval(number) % 2 == 0):
        print('{} passes the test!'.format((eval(number))))
    else:
        print('{} fails the test：('.format(eval(number)))
except Exception as error:
    print('输入格式错误！')


# Part2
def function():
    number = input('Integer：').split('#')[-1]
    try:
        if(eval(number) == 0):
            pass
        else:
            if (eval(number) < 0 and eval(number) % 2 == 1):
                print('{} passes the test!'.format(eval(number)))
            elif ((eval(number) >= 20 and eval(number) < 200) and eval(number) % 2 == 0):
                print('{} passes the test!'.format((eval(number))))
            else:
                print('{} fails the test：('.format(eval(number)))
            function()
    except Exception as error:
        print('输入格式错误！')

function()
print('Bye!')