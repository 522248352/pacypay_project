import csv
from collections import Iterable
import os

"""
读 写 操作
"""
current_path = os.path.dirname(__file__)
current_path_up = os.path.dirname(current_path)
def read_csv(filename):
    """
    读 csv 文件
    :param filename:
    :return:
    """
    with open(current_path_up+"/test_data/"+filename,"r") as csvfile:

        files = csv.DictReader(csvfile)

        # 判断返回是否可迭代对象
        # print(isinstance(files,Iterable))
        data = list(files)
        return data

def write_csv(filename, data):
    """
    写入 csv 文件
    :param filename:
    :return:
    """
    with open(current_path_up+"/test_data/"+filename,"a+",newline='') as f:

        dataf = csv.writer(f)
        for i in data:
            dataf.writerow(i)

if __name__=="__main__":

    s = read_csv("database.csv")
    print(s)