import os
import re

# print('11111111111111')
# print('>>>', os.listdir('testDigits/'))

def file_dir(num, path='testDigits/'):
    dir_list = os.listdir(path)
    dir_str = '-'.join(dir_list)
    gate = re.findall(r'{}_\d+\.txt'.format(str(num)), dir_str)
    # print(type(gate))
    return len(gate)+1

if __name__ == '__main__':
    print(file_dir(6))

