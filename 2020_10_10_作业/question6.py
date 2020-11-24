def flatten(lst):
    my_list = lst
    # 存放等级数据
    level_dict = {}
    level = 0
    for element in my_list:
        # 首先将level=0的存放到新列表
        if type(element) == int or type(element) == float:
            level_dict[element] = level
        elif element == None:
            level_dict[element] = level
        elif type(element) == bool:
            level_dict[str(element)] = level
        else:
            def digui(element,level):
                level += 1
                for j in element:
                    if type(j) == int or type(j) == float:
                        level_dict[j] = level
                    elif type(j) == str and len(j) == 1:
                        level_dict[j] = level
                    elif j == None:
                        level_dict[j] = level
                    elif type(j) == bool:
                        level_dict[str(j)] = level
                    else:
                        digui(j,level)
            digui(element,level)
    # 使用lambda根据字典的值进行排序
    nums = sorted(level_dict.items(),key=lambda item:item[1],reverse=False)
    end_list = []
    for num in nums:
        if num[0] == 'True' or num[0] == 'False':
            end_list.append(bool(num[0]))
        else:
            end_list.append(num[0])
    print(end_list)

flatten([[1, ''], ('w', 'xy'), 'abc', 4.5, 2])
flatten([1, 2.0, [None,[3,True]], 'ab', [100, 200], ('o', 12)])
