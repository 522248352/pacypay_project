import pytest
import requests
from test_tools import data_encrypt
from test_tools import read_yaml

def test_safecharge_cancel():
    """

    :return:
    """
    data_yaml = read_yaml.get_yamlDataOne("safecharge_cancel.yml")
    head = data_yaml["head"]
    params = data_yaml["params"]
    # merchantNo + subAccount + tradeNo1 + tradeNo2 ...+ signkey);加密后的签名转大写
    key = data_yaml["key"]

    trnos_all = data_yaml["params"]["cancelOrders"]
    trno = ""
    for i in trnos_all:
        trno += i["tradeNo"]


    waitEncrypt = data_yaml["params"]["merchantNo"]+data_yaml["params"]["subAccount"]+trno+key

    sign = str(data_encrypt.dataEncrypt(waitEncrypt)).upper()

    data_yaml["params"]["sign"] = sign

    resu = requests.post(url=data_yaml["url"], json=params, headers={"Content-Type":head})
    print(resu.text)


if __name__ == "__main__":
    pytest.main(["-vs", "test_safecharge_cancel.py"])


