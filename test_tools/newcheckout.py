import time

from nb_log import LogManager
from test_tools import read_yaml, data_encrypt

logger = LogManager("diy").get_logger_and_add_handlers(log_filename = 'ApiTest.log')

def newcheckout(commondata_check,checkout):

    commdatas = read_yaml.get_yamlDataOne(commondata_check)
    commdata1 = commdatas["comdata1"]
    commdata2 = commdatas["comdata2"]

    specdatas = read_yaml.get_yamlDataTwo(checkout)

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