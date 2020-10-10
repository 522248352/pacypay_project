import pytest
import requests
from test_tools import data_encrypt
from test_tools import read_yaml
from tempsss import test_safecharge_sale


@pytest.mark.run(order=3)
def test_safecharge_capture():
    """
    接口 发起 cancel 操作，支持单订单 多订单，根据yml配置文件决定
    :return:
    """
    tu1 = test_safecharge_sale.test_safecharge_sale()
    # 读取yml文件中参数
    data_yaml = read_yaml.get_yamlDataOne("safecharge_capture.yml")

    # 获取请求头 json格式
    head = data_yaml["head"]

    # 获取请求参数params
    params = data_yaml["params"]
    # merchantNo + subAccount + tradeNo1 + tradeNo2 ...+ signkey);加密后的签名转大写

    # 获取商户秘钥key
    key = data_yaml["key"]

    # 获取请求参数中，所有需要操作的订单数据
    trnos_all = data_yaml["params"]["captureOrders"]

    # 循环所有需要操作的订单数据，获取每个订单的trno编号，以便后续加签
    trno = ""
    for i in trnos_all:
        trno += i["tradeNo"]
    trno +=tu1[0]
    data_yaml["params"]["captureOrders"][0]["transactionId"]=tu1[1]
    data_yaml["params"]["captureOrders"][0]["tradeNo"] = tu1[0]
    print("trno%s"%trno)
    print("transcid%s"%data_yaml["params"]["captureOrders"][0]["transactionId"])
    # 拼装所有需要加签的数据，按顺序
    waitEncrypt = data_yaml["params"]["merchantNo"]+data_yaml["params"]["subAccount"]+trno+key

    # 进行加签，并且转换成大写
    sign = str(data_encrypt.dataEncrypt(waitEncrypt)).upper()

    # 把签名更新到请求参数params中
    data_yaml["params"]["sign"] = sign

    # POST请求
    resu = requests.post(url=data_yaml["url"], json=params, headers={"Content-Type":head})
    print(resu.text)

if __name__ == "__main__":
    pytest.main(["-vs", "test_safecharge_capture.py"])
    # test_safecharge_capture()

