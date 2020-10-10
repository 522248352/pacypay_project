from test_tools import data_encrypt,read_yaml
import requests
import time
import re
import logging
from test_tools.oracle_database import DB
import pytest


def newcheckout():

    commdatas = read_yaml.get_yamlDataOne("commondata_check.yml")
    commdata1 = commdatas["comdata1"]
    commdata2 = commdatas["comdata2"]

    specdatas = read_yaml.get_yamlDataTwo("checkout.yml")

    casename = []
    head = []
    param1 = []
    param2 = []
    for i in specdatas:

        i["params1"].update(commdata1)
        i["params2"].update(commdata2)

        t = time.time()
        i["params1"]["transactionId"] = str(int(round(t * 1000)))

        # 获取需要加密的顺序数据
        waitencrypt = i["params1"]["merchantNo"] + i["params1"]["subAccount"] + \
                      i["params1"]["transactionId"] + i["params1"]["currency"] + \
                      i["params1"]["amount"] + i["params1"]["returnUrl"] + i["kyes"]

        sign = data_encrypt.dataEncrypt(waitencrypt)
        i["params1"]["sign"] = sign

        param1.append(i["params1"])
        param2.append(i["params2"])
        casename.append(i["casename"])
        head.append(i["head"])

    return list(zip(casename,head,param1,param2))

@pytest.mark.parametrize("casename,head,param1,param2",newcheckout())
def test_checkout(casename,head,param1,param2):
    """
    SafeCharge 跳转支付
    :return:
    """
    sess = requests.session()
    resu1 = sess.post(url="https://test-v2.pacypay.com/gateway/Interface",
                      data=param1, headers={"content-type":head})
    print(resu1.headers)
    # 获取返回的 tradeNo
    trno = re.search('(.*?)tradeNo=(.*?)\\"', str(resu1.text)).group(2)
    print("trno==============================%s" % trno)

    # 判断第一步返回信息
    assert trno != ""

    print("【%s】第一步执行结束.................."%(casename))
    param2["tradeNo"] = trno

    resu2 = sess.post(url="https://test-v2.pacypay.com/gateway/SendInterface",
                      data=param2, headers={"content-type":head})
    print(resu2.status_code)
    print(param2)
    # print(resu2.text)

    # 判断第二步返回信息
    db1 = DB()

    # 交易记录表 CCPS_TRADERECORD

    sql1 = "select TR_CURRENCY,TR_AMOUNT,TR_STATUS," \
           "TR_PAYMENT_STATUS,TR_BANKCURRENCY,TR_BANKAMOUT," \
           "TR_BANK_CODE,TR_BANKRETURNCODE,TR_BANKINFO,TR_NOTIFYURL," \
           "TR_CAPTURED,TR_CAPTURE_TIME,TR_INF_TYPE,TR_CARDTYPE FROM CCPS_TRADERECORD" \
           " where tr_no ="+trno

    resuf = db1.query(sql1)
    db1.closes()

    print("交易记录表CCPS_TRADERECORD查询结果是： %s"%resuf)
    assert len(resuf) == 1

    assert resuf[0][0] == param1["currency"]
    assert resuf[0][1] == float(param1["amount"])
    assert resuf[0][2] == 1
    assert resuf[0][3] == "2000"
    assert resuf[0][4] == "USD"

    # 订单状态表 CCPS_TRADERECORD_STATUS

    # 持卡人信息表 CCPS_CREDITINFO

if __name__=="__main__":

    pytest.main(["-vs","test_checkout.py"])

