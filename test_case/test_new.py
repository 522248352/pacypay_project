import requests
from nb_log import LogManager

from test_tools import data_encrypt, oracle_database, read_yaml, rw_csv
import time
import pytest
import re
from test_tools.oracle_database import DB
from test_tools.rw_csv import write_csv

logger = LogManager("diy").get_logger_and_add_handlers(log_filename = 'ApiTest.log')
"""
safecharge cd ebank 直连交易sale
"""
def newsale():
    """
    请求参数 处理逻辑
    :return: 返回 符合 pytest.mark.parametrize 的类型 [(),(),()]
    """

    # 获取公共请求参数 字典类型
    commonData = read_yaml.get_yamlDataOne("commondata_sale.yml")

    # 获取 商户信息、特定请求参数（卡号、商户号、URL等）
    saleDatas = read_yaml.get_yamlDataTwo("sale.yml")

    casename1 = []
    heads1 = []
    params1 = []
    for i in saleDatas:

        i["params"].update(commonData)

        # 获取时间戳，生成transactionID
        t = time.time()
        i["params"]["transactionId"] = str(int(round(t * 1000)))

        # 组合待加签的数据
        waitencrypt = i["params"]["merchantNo"] + i["params"]["subAccount"] + \
                      i["params"]["transactionId"] + commonData["currency"] + \
                      i["params"]["amount"] + commonData["firstName"] + \
                      commonData["lastName"] + i["params"]["cardNumber"] + \
                      commonData["year"] + commonData["month"] + commonData["cvv"] + \
                      commonData["email"] + i["keys"]

        sign = data_encrypt.dataEncrypt(waitencrypt)
        logger.info(sign)
        i["params"]["sign"] = sign

        casename1.append(i["casenames"])
        heads1.append(i["heads"])
        params1.append(i["params"])
    logger.info("=========================")
    das = list(zip(casename1,heads1,params1))
    return das


@pytest.mark.first  # 执行顺序排序，首先执行
@pytest.mark.sale
@pytest.mark.parametrize("casename1,head,param",newsale())
def test_sale(casename1,head,param):
    """

    :param casename1: 案例名-渠道名称
    :param head: 请求头 content-type
    :param param: 请求参数
    :return:
    """

    resu = requests.post(url="https://test-v2.pacypay.com/gateway/TPInterface",
                         data=param,headers={"Content-Type":head})
    dd = resu.text
    logger.info("【%s】开始响应结果返回数据=：%s"%(casename1,dd))
    logger.info("【%s】结束响应结果返回数据。。。："%(casename1))
    # re 获取每笔交易的 transactionId tradeNo
    transactionId = re.search("<transactionId>(.*?)</transactionId>",dd).group(1)
    tradeNo = re.search("<tradeNo>(.*?)</tradeNo>",dd).group(1)

    # 断言响应结果返回
    orderInfo = re.search("<orderInfo>(.*?)</orderInfo>",dd).group(1)
    assert orderInfo == "0000:Success"

    # 获取 订单号 和 流水号存入csv文件，供后续 capture接口调用
    data = [(transactionId,tradeNo)]
    write_csv("transaction.csv", data)

    # 数据库断言
    db = DB()

    sql = "select TR_CURRENCY,TR_AMOUNT,TR_STATUS," \
          "TR_PAYMENT_STATUS,TR_BANKCURRENCY,TR_BANKAMOUT," \
          "TR_BANK_CODE,TR_BANKRETURNCODE,TR_BANKINFO,TR_NOTIFYURL," \
          "TR_CAPTURED,TR_CAPTURE_TIME,TR_INF_TYPE,TR_CARDTYPE from CCPS_TRADERECORD" \
          " where tr_no =" + tradeNo
    resu_data = db.query(sql)
    db.closes()
    # print(resu1)
    assert resu_data[0][0] == param["currency"]
    assert resu_data[0][3] == "2000"


if __name__ == '__main__':
    # pytest.main(["-sq","test_new.py",'--alluredir','../report'])
    # pytest.main(["-vs","--collect-only","test_new.py"])
    pytest.main(["-sq","test_new.py"])

