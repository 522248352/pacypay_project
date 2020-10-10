import yaml

def get_yamlDataTwo(fileName):
    """
    读取 yaml 文件多数据，获取请求参数
    :param path:
    :return:
    """
    with open("../test_data/"+fileName, "r" ,encoding="utf-8") as fileData:

        yamlData = yaml.load_all(fileData.read(), Loader=yaml.SafeLoader)
        return yamlData

def get_yamlDataOne(fileName):
    """
    读取 yaml 文件单数据，获取请求参数
    :param path:
    :return:
    """
    with open("../test_data/"+fileName, "r" ,encoding="utf-8") as fileData:

        yamlData = yaml.load(fileData.read(), Loader=yaml.SafeLoader)
        return yamlData