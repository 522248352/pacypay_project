import requests
from test_tools import read_yaml
from test_tools.oracle_database import DB
import pytest


def test_refund_first(login):

    """
    refund -初审操作
    :param login: session
    :return:
    """
    # 读取yml文件获取数据
    dats = read_yaml.get_yamlDataOne("safecharge_refund.yml")

    params2 = dats
    merchantNo="21677"
    subAccount="21677001"

    # 需要退款审核的订单号 和 UPID
    params2["C_REFUND_TRNO"]="3668441229501399040"
    params2["C_REFUND_UPID"]="536154"

    # 链接数据库查询订单相关数据，用来后续组装
    db = DB()
    sql = "SELECT TR_NOTIFYURL,TR_MER_ORDERNO,TR_AMOUNT,TR_REMARK " \
          "FROM  CCPS_TRADERECORD " \
          "WHERE TR_NO='3668433182615666688'"
    data_resu = db.query(sql)

    # 进行组装数据
    c_refund_checkdata= data_resu[0][0]+"|"+merchantNo+"|"+subAccount+"|"+"3668441229501399040"+"|"+\
                        data_resu[0][1]+"|"+str(data_resu[0][2])+"|"+"null|1|0000|Success|"+data_resu[0][3]+"|null"
    print(c_refund_checkdata)

    # 将组装的数据传到请求参数中
    params2["C_REFUND_REFERENCETRNO"]=c_refund_checkdata

    # 根据前面登录的session发送POST请求
    sssss = login.post("https://test-v2.pacypay.com/manage/backdispute/processCheckExceptionTradeRecord.html?moduleId=212",data=params2)

    print(sssss.text)

def test_refund_second():
    """
    refund -复审操作 同上用session
    :return:
    """


if __name__=="__main__":
    pytest.main(["-vs","test_login.py"])