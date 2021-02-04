import time
from random import randint

from common.myconfig import dic1
from test_tools import read_yaml, data_encrypt
import pytest

from test_tools.addmark import addMark


def newcheckout(commondata_check,checkout):

    commdatas = read_yaml.get_yamlDataOne(commondata_check)
    commdata1 = commdatas["comdata1"]
    commdata2 = commdatas["comdata2"]

    specdatas = read_yaml.get_yamlDataTwo(checkout)

    casename = []
    head = []
    param1 = []
    param2 = []
    mark1 = []
    for i in specdatas:

        i["params1"].update(commdata1)
        i["params2"].update(commdata2)

        t = time.time()
        i["params1"]["transactionId"] = str(randint(0, 99999999)).zfill(8) #str(int(round(t * 1000)))

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
        marklist = i['mark']
        for x,y in enumerate(marklist):
            marklist[x] = dic1[y]
        mark1.append(marklist)

    das = list(zip(casename, head, param1, param2, mark1))
    # 转换成 pytest.param（）
    datasMark = addMark(das)
    return datasMark