"""
    Question1:Write a program recital.py that reads numbers from standard input.When the user enters zero,the program recites
            all the numbers entered(excluding the zero)
"""
numbers = []
def function():
    number_input = input('Number：').split('#')[-1]
    try:
        if (float(number_input) == 0):
            pass
        else:
            numbers.append(float(number_input))
            function()
    except Exception as error:
        print('输入的格式错误！')

if __name__ == '__main__':
    function()
    print('Your numbers were：')
    for number in numbers:
        print(number)