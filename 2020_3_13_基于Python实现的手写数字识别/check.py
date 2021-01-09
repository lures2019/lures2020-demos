import os
import kNN

def rename_file(old, new):
    src = './{}'.format(old)
    dst = './{}'.format(new)
    os.rename(src, dst)


def check():
    rename_file('testDigits', 'test_temp')
    rename_file('testDigits(测试)', 'testDigits')
    test_number, error_sum, mistakes_num, total_time, result_list, testFileList = kNN.main()
    rename_file('testDigits', 'testDigits(测试)')
    rename_file('test_temp', 'testDigits')
    return test_number, error_sum, mistakes_num, total_time, result_list, testFileList

if __name__ == '__main__':
    pass