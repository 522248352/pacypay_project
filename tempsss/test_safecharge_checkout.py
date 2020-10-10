from test_tools import data_encrypt,read_yaml
import requests
import time
import re
import logging
from test_tools.oracle_database import DB
import pytest

@pytest.mark.skip
def test_safecharge_checkout():
    """
    SafeCharge 跳转支付
    :return:
    """
    # 读取请求参数
    caseData = read_yaml.get_yamlDataOne("safecharge_checkout.yml")

    # 获取url key秘钥 入参param
    casename1 = caseData["casename1"]
    casename2 = caseData["casename2"]
    urls1 = caseData["urls1"]
    keys = caseData["kyes"]
    params1 = caseData["params1"]
    head = caseData["head"]

    sess = requests.session()
    head = {"content-type":head}
    t = time.time()
    caseData["params1"]["transactionId"] = str(int(round(t * 1000)))
    print(int(round(t * 1000)))

    # 获取需要加密的顺序数据
    waitencrypt = caseData["params1"]["merchantNo"]+caseData["params1"]["subAccount"]+\
                  caseData["params1"]["transactionId"]+caseData["params1"]["currency"]+\
                  caseData["params1"]["amount"]+caseData["params1"]["returnUrl"]+keys

    sign = data_encrypt.dataEncrypt(waitencrypt)

    caseData["params1"]["sign"] = sign
    resu1 = sess.post(url=urls1, data=params1, headers=head)
    print(resu1.headers)
    # 获取返回的 tradeNo
    trno = re.search('(.*?)tradeNo=(.*?)\\"', str(resu1.text)).group(2)
    print("trno=%s" % trno)

    # 判断第一步返回信息
    assert trno != ""

    print("【%s】执行结束，准备开始执行【%s】"%(casename1,casename2))



    urls2 = caseData["urls2"]
    params2 = caseData["params2"]
    caseData["params2"]["tradeNo"] = trno

    resu2 = sess.post(url=urls2, data=params2, headers=head)
    print(resu2.status_code)
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

    print(resuf)
    assert len(resuf) == 1
    print("===========")

    print(type(trno))
    print(resuf[0][3],type(caseData["params1"]["amount"]))
    assert resuf[0][0] == caseData["params1"]["currency"]
    assert resuf[0][1] == float(caseData["params1"]["amount"])
    assert resuf[0][2] == 1
    assert resuf[0][3] == "2000"
    assert resuf[0][4] == "USD"

    # 订单状态表 CCPS_TRADERECORD_STATUS

    # 持卡人信息表 CCPS_CREDITINFO

if __name__=="__main__":

    pytest.main(["-vs","test_safecharge_checkout.py"])