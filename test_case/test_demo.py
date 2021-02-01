import hashlib
import re
import time
from string import Template

import requests
from pytest_lazyfixture import lazy_fixture
import pytest
import yaml
import pprint

from test_tools.newcheckout import newcheckout,logger

datas = newcheckout('commondata_check.yml','checkout_new.yml')

print(datas)
mm = []
for i in datas:
    mm.append(pytest.param(*i[:-1],marks=i[-1]))

print(mm)

@pytest.mark.parametrize("casename,head,param1,param2",mm)
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
    print('s===%s'%s1)
    # 获取返回的 tradeNo
    # trno = re.search('(.*?)tradeNo=(.*?)\\"', str(resu1.text)).group(2)
    u1 = 'https://test-v2.pacypay.com/gateway/getOrderInfo/'+s1
    logger.info('%s获取u1是：  %s'%(casename,u1))

    #获取cookies
    heas = 'JSESSIONID='+sess.cookies.get_dict()['JSESSIONID']
    print("====hes=%s"%heas)
    logger.info('%s获取heas是：  %s'%(casename,heas))
    trno = sess.get(url=u1,headers={"cookie":'JSESSIONID='+sess.cookies.get_dict()['JSESSIONID']})
    # trno = sess.get(url=u1)

    print('msmsmsmsm=====%s'%trno.text)
    print('trnnnnnn=====%s'%type(trno.text))
    tn = re.search('"tradeNo":"(.*?)",',trno.text).group(1)
    print('tn===========%s'%tn)
    param2['tradeNo'] = tn
    print('parm2======%s'%param2)
    logger.info('param2=====%s'%param2)

    # time.sleep(10)
    resu2 = sess.post(url='https://test-v2.pacypay.com/gateway/SendInterface',data=param2, headers={"content-type":head,"cookie":'JSESSIONID='+sess.cookies.get_dict()['JSESSIONID']})
    print(resu2.text)

if __name__ == '__main__':
    pytest.main(['-sq','test_demo.py'])