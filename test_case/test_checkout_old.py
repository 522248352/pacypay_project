
import requests
import re
from nb_log import LogManager
from test_tools.newcheckout import newcheckout
from test_tools.oracle_database import DB
import pytest
from log.logg_diy import logger


datas = newcheckout('commondata_check.yml','checkout.yml')

@pytest.mark.parametrize("casename,head,param1,param2",datas)
def test_checkout(casename, head, param1, param2):
    """
    SafeCharge 跳转支付
    :return:
    """
    sess = requests.session()
    resu1 = sess.post(url="https://test-v2.pacypay.com/gateway/Interface",
                      data=param1, headers={"content-type":head})

    logger.info('第一步返回的请求头数据=====%s'%resu1.headers)
    logger.info('第一步的请求参数=====%s'%param1)
    logger.info('第一步返回的请求头cookie数据=====%s'%resu1.cookies['JSESSIONID'])
    logger.info('第一步返回的请求头cookie数据类型=====%s'%type(resu1.cookies))
    # 获取返回的 tradeNo
    trno = re.search('(.*?)tradeNo=(.*?)\\"', str(resu1.text)).group(2)
    logger.info("trno==============================%s" % trno)

    # 判断第一步返回信息
    assert trno != ""

    logger.info("【%s】第一步执行结束.................."%(casename))
    param2["tradeNo"] = trno

    resu2 = sess.post(url="https://test-v2.pacypay.com/gateway/SendInterface",
                      data=param2, headers={"content-type":head})
    logger.info('第二步返回====%s'%resu2.status_code)
    logger.info('第二步请求参数====%s'%param2)
    # print(resu2.text)

    # 判断第二步返回信息
    db1 = DB()

    # 交易记录表 CCPS_TRADERECORD

    sql1 = "select TR_CURRENCY,TR_AMOUNT,TR_STATUS," \
           "TR_PAYMENT_STATUS,TR_BANKCURRENCY,TR_BANKAMOUT," \
           "TR_BANK_CODE,TR_BANKRETURNCODE,TR_BANKINFO,TR_NOTIFYURL," \
           "TR_CAPTURED,TR_CAPTURE_TIME,TR_INF_TYPE,TR_CARDTYPE FROM CCPS_TRADERECORD" \
           " where tr_no ='%s'"%trno

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

