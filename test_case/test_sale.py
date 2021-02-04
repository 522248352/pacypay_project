import requests
from nb_log import LogManager
import pytest
import re
from test_tools.newsale import newsale
from test_tools.oracle_database import DB
from test_tools.rw_csv import write_csv
from log.logg_diy import logger

# logger = LogManager("diy").get_logger_and_add_handlers(log_filename = 'ApiTest.log')
"""
safecharge cd ebank 直连交易sale
"""

datas = newsale("commondata_sale.yml","sale.yml")

@pytest.mark.first  # 执行顺序排序，首先执行
@pytest.mark.sale
@pytest.mark.parametrize("casename,head,param", datas)
def test_sale(casename, head, param):
    """

    :param casename1: 案例名-渠道名称
    :param head: 请求头 content-type
    :param param: 请求参数
    :return:
    """
    logger.info('%s 请求参数===：%s'%(casename, param))
    resu = requests.post(url="https://test-v2.pacypay.com/gateway/TPInterface",
                         data=param, headers={"Content-Type":head})
    resus = resu.text
    logger.info("【%s】返回数据开始==========：%s"%(casename, resus))
    logger.info("【%s】返回数据结束==========：%s"%(casename, 'end'))

    # re 获取每笔交易的 transactionId tradeNo
    try:
        transactionId = re.search("<transactionId>(.*?)</transactionId>", resus).group(1)
        tradeNo = re.search("<tradeNo>(.*?)</tradeNo>", resus).group(1)
    except Exception:
        logger.error('========正则错误！！！')
    logger.info("【%s】->transactionId======%s,tradeNo=======%s"%(casename, transactionId, tradeNo))

    # 断言响应结果返回
    orderInfo = re.search("<orderInfo>(.*?)</orderInfo>",resus).group(1)
    logger.info("start断言响应结果返回：实际orderInfo====%s：：预期是：0000:Success"%orderInfo)
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
          " where tr_no ='%s'" %tradeNo

    logger.info("sql============%s"%sql)
    resu_data = db.query(sql)
    logger.info("CCPS_TRADERECORD中查询resu_data====%s"%resu_data)
    db.closes()
    # print(resu1)
    logger.info("币种表中值是resu_data[0][0]=%s，预期值是： %s"%(resu_data[0][0],param["currency"]))
    logger.info("状态表中值是resu_data[0][3]=%s，预期值是： %s"%(resu_data[0][3],'2000'))
    assert resu_data[0][0] == param["currency"]
    assert resu_data[0][3] == "2000"


if __name__ == '__main__':


    # pytest.main(["-sq","test_sale.py",'--alluredir','../allurefiles'])
    # pytest.main(["-vs","--collect-only","test_sale.py","test_checkout_new.py"])
    pytest.main(["-sq","test_sale.py",])
    # pytest.main(["-sq", '-m','sale',"test_sale.py", ])

