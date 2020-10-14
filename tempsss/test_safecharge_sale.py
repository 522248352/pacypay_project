from test_tools import read_yaml,data_encrypt
import time
import requests
import re
from test_tools.oracle_database import DB
import pytest


@pytest.mark.run(order=2)
def test_safecharge_sale():
    """
    SafeCharge 直连支付
    :return:
    """

    # 读取yml文件得到一个dict
    caseData = read_yaml.get_yamlDataOne("safecharge_sale.yml")

    # 案例名称
    casenames = caseData["casenames"]

    # url 秘钥 请求头 请求参数
    urls = caseData["urls"]
    keys = caseData["keys"]
    heads = caseData["heads"]
    params = caseData["params"]

    # 获取时间戳，生成transactionID
    t = time.time()
    caseData["params"]["transactionId"] = str(int(round(t * 1000)))
    print(int(round(t * 1000)))

    # 组合待加签的数据
    waitencrypt = caseData["params"]["merchantNo"]+caseData["params"]["subAccount"]+\
                  caseData["params"]["transactionId"]+caseData["params"]["currency"]+\
                  caseData["params"]["amount"]+caseData["params"]["firstName"]+\
                  caseData["params"]["lastName"]+caseData["params"]["cardNumber"]+\
                  caseData["params"]["year"]+caseData["params"]["month"]+caseData["params"]["cvv"]+\
                  caseData["params"]["email"]+keys

    # 进行加签
    sign = data_encrypt.dataEncrypt(waitencrypt)
    print(sign)

    # 把签名放到请求参数中
    caseData["params"]["sign"] = sign
    # print(caseData["params"])

    # POST请求
    resu = requests.post(url=urls,data=params,headers={"content-type":heads})
    #
    print(resu.text)

    # re 提取数据并断言
    re_merchanno = "<merchantNo>(.*?)</merchantNo>"
    re_amount = "<amount>(.*?)</amount>"
    re_tradeNo = "<tradeNo>(.*?)</tradeNo>"

    merchanno = re.search(re_merchanno,resu.text).group(1)
    amount = re.search(re_amount,resu.text).group(1)
    tradeNo = re.search(re_tradeNo, resu.text).group(1)

    assert merchanno == caseData["params"]["merchantNo"]
    assert amount == caseData["params"]["amount"]

    # 数据库断言
    db = DB()

    sql = "select TR_CURRENCY,TR_AMOUNT,TR_STATUS," \
          "TR_PAYMENT_STATUS,TR_BANKCURRENCY,TR_BANKAMOUT," \
          "TR_BANK_CODE,TR_BANKRETURNCODE,TR_BANKINFO,TR_NOTIFYURL," \
          "TR_CAPTURED,TR_CAPTURE_TIME,TR_INF_TYPE,TR_CARDTYPE from CCPS_TRADERECORD" \
          " where tr_no ="+tradeNo
    resu1 = db.query(sql)
    db.closes()
    print(resu1)
    assert resu1[0][0] == caseData["params"]["currency"]
    assert resu1[0][3] == "2000"
    print(tradeNo,caseData["params"]["transactionId"])
    return (tradeNo,caseData["params"]["transactionId"])
    # globals()["ss"] = tradeNo
    # globals()["sss"] = caseData["params"]["transactionId"]
    # print("globals()['ss']%s"%globals()["ss"])
    # print ("globals()['sss']%s" % globals ()["sss"])

if __name__ == "__main__":

    # test_safecharge_sale()

    # pytest.main(["-vs","test_safecharge_sale.py"])
    pytest.main(["-vs","test_safecharge_sale.py"])
    # test_safecharge_sale()
