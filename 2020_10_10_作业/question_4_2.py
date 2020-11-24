def hist_noloop(ints, sym):
    numbers = ints
    char = sym
    # 代表列表中的最大值
    max_number = max(numbers)
    last = map(lambda x:(','*(max_number-x)+x*char),numbers)
    string = " ".join(last)
    end_lists = list(string.split(' '))
    def digui(i,max_number,end_lists):
        if i < max_number:
            end = map(lambda x: (x[i]), end_lists)
            string1 = " ".join(end).replace(',',' ')
            print(string1)
            i += 1
            digui(i,max_number,end_lists)
    digui(0,max_number,end_lists)


hist_noloop([4,1,3,5], '$')