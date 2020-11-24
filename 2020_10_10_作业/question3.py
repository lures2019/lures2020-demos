def histogram(ints, sym):
    heights = ints
    char = sym
    # 按列读取不好操作，转换为按行读取
    columns = [[] for i in range(len(heights))]
    for i in range(len(heights)):
        string = heights[i] * char + " "*(max(heights) - heights[i])
        columns[i].append(string)
    last_lists = [[] for i in range(max(heights))]
    for i in range(len(columns)):
        for j in range(len(columns[i][0])):
            last_lists[j].append(columns[i][0][j])
    # 观察图形知道要逆序输出
    for i in last_lists[::-1]:
        print(" ".join(i))

test1 = histogram([4,1,3,5],'$')
test2 = histogram([1,2,3,4],'#')
