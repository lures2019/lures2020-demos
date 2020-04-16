num1 = float(input("请输入第一个整数："))
num2 = float(input("请输入第二个整数："))
if(num1<num2):
	num3 = num1
else:
	num3 = num1 - (num1//num2)*num2
print("输入的两个数相加得到%d,相减得到%d，余数是%d"%(num1+num2,num1-num2,num3))