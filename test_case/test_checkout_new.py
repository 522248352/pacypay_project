import re
from log.logg_diy import logger
import requests
import pytest

from test_tools.addmark import addMark
from test_tools.newcheckout import newcheckout
from test_tools.oracle_database import DB

datas = newcheckout('commondata_check.yml','checkout_new.yml')

@pytest.mark.checkout
@pytest.mark.parametrize("casename,head,param1,param2",datas)
def test_checkout(casename, head, param1, param2):
    """

    :return:
    """
    logger.info('%s==请求参数1是： %s'%(casename,param1))
    sess = requests.session()
    resu1 = sess.post(url="https://test-v2.pacypay.com/gateway/Interface",
                      data=param1, headers={"content-type":head})

    logger.info('%s重定向url是：  %s'%(casename,resu1.url))
    logger.info('%s获取cookie是：  %s'%(casename,sess.cookies.get_dict()))


    url_new = resu1.url
    s1 = re.search('checkout/(.*)',url_new).group(1)

    # 获取返回的 tradeNo
    # trno = re.search('(.*?)tradeNo=(.*?)\\"', str(resu1.text)).group(2)
    u1 = 'https://test-v2.pacypay.com/gateway/getOrderInfo/'+s1
    logger.info('%s获取订单信息的url是：  %s'%(casename,u1))

    #获取cookies
    heas = 'JSESSIONID='+sess.cookies.get_dict()['JSESSIONID']
    logger.info('%s获取heas是：  %s'%(casename,heas))
    trno = sess.get(url=u1,headers={"cookie":heas})
    # trno = sess.get(url=u1)
    tn = re.search('"tradeNo":"(.*?)",',trno.text).group(1)
    logger.info('tn===========%s'%tn)
    param2['tradeNo'] = tn
    logger.info('param2=====%s'%param2)

    # time.sleep(10)
    resu2 = sess.post(url='https://test-v2.pacypay.com/gateway/SendInterface',
                      data=param2,
                      headers={"content-type":head,"cookie":'JSESSIONID='+sess.cookies.get_dict()['JSESSIONID']})
    print(resu2.text)
    db = DB()
    sql = "SELECT TS_CODE FROM CCPS_TRADERECORD_STATUS " \
          "where TR_NO='%s' " \
          "order by TS_CODE desc"%tn
    dbResu = db.query(sql)
    db.closes()
    logger.info('db预期值是: %s,实际值是：%s'%(['1000','2000'],dbResu[0][0]))
    assert dbResu[0][0] in ['1000','2000']

if __name__ == '__main__':
    # pytest.main(['-sq','test_checkout_new.py','--alluredir','../allurefiles'])
    # pytest.main(['-sq','-m','ecpNew','test_checkout_new.py'])
    pytest.main(['-sq', 'test_checkout_new.py', '--alluredir', '../allurefiles'])