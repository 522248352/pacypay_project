import yaml
import os

current_path = os.path.dirname(__file__)
current_path_up = os.path.dirname(current_path)
def get_yamlDataTwo(fileName):
    """
    读取 yaml 文件多数据，获取请求参数
    :param path:
    :return:
    """
    with open(current_path_up+"/test_data/"+fileName, "r" ,encoding="utf-8") as fileData:

        yamlData = yaml.load_all(fileData.read(), Loader=yaml.SafeLoader)
        return yamlData

def get_yamlDataOne(fileName):
    """
    读取 yaml 文件单数据，获取请求参数
    :param path:
    :return:
    """
    with open(current_path_up+"/test_data/"+fileName, "r" ,encoding="utf-8") as fileData:

        yamlData = yaml.load(fileData.read(), Loader=yaml.SafeLoader)
        return yamlData