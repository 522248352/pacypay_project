import json

import pytest
import requests
from nb_log import LogManager

from test_tools import read_yaml, rw_csv, data_encrypt
logger = LogManager("diy").get_logger_and_add_handlers(log_filename = 'ApiTest.log')

def newcapture():

    captureDatas = read_yaml.get_yamlDataTwo("capture.yml")

    try:
        csvdata = rw_csv.read_csv("transaction.csv")
        if len(csvdata) < 1:
            print("读取交易数据错误")
    except Exception as e:
        print("自己定义异常")
    casename = []
    head = []
    param = []
    j = 0
    for i in captureDatas:

        i["params"]["captureOrders"][0]["tradeNo"]=csvdata[j]["tradeNo"]
        i["params"]["captureOrders"][0]["transactionId"] = csvdata[j]["transactionId"]
        j +=1
        waitEncrypt = i["params"]["merchantNo"] + i["params"]["subAccount"] + i["params"]["captureOrders"][0]["tradeNo"]\
                      + i["key"]

        # 进行加签，并且转换成大写
        sign = str (data_encrypt.dataEncrypt(waitEncrypt)).upper()

        # 把签名更新到请求参数params中
        i["params"]["sign"] = sign
        head.append(i["head"])
        param.append(i["params"])
        casename.append(i["casename"])
    ss = list(zip(casename,head,param))
    return ss

@pytest.mark.parametrize("casename,head,param",newcapture())
def test_capture(casename,head,param):

    resu = requests.post(url="https://test-v2.pacypay.com/merchant/api/capture",json=param,headers={"Content-Type":head})
    logger.info("【"+casename+"】"+"请求参数param============"+str(param))
    # print(resu.status_code)
    logger.info(resu.text)

    # 断言响应结果
    dic1 = json.loads(resu.text)
    assert dic1["captureOrders"][0]["errorMsg"] == ""


if __name__ == '__main__':
    pytest.main(["-vs","test_cap.py"])
    # print(newcapture())