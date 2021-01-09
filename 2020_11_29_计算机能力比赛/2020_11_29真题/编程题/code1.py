nums = [int(i) for i in list(input().split(' '))]
N = nums[0]
M = nums[1]

total = []
for i in range(N+1,M):
    value = i * (i+1) * (i-1)
    if i % 5 == 0:
        total.append(i)
if (len(total) >= 3):
    print("{} {} {}".format(total[0],total[1],total[2]))
elif (len(total) == 1):
    print("{} {} {}".format(total[0],-1,-1))
elif (len(total) == 2):
    print("{} {} {}".format(total[0], total[1], -1))
else:
    print("{} {} {}".format(-1, -1, -1))