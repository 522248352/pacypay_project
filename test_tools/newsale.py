import time

from nb_log import LogManager

from test_tools import read_yaml, data_encrypt

logger = LogManager("diy").get_logger_and_add_handlers(log_filename = 'ApiTest.log')

def newsale(comm,sale):
    """
    请求参数 处理逻辑
    :return: 返回 符合 pytest.mark.parametrize 的类型 [(),(),()]
    """

    # 获取公共请求参数 字典类型
    commonData = read_yaml.get_yamlDataOne(comm)

    # 获取 商户信息、特定请求参数（卡号、商户号、URL等）
    saleDatas = read_yaml.get_yamlDataTwo(sale)

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
        logger.info("%s的签名sign===%s"%(i["casenames"],sign))
        i["params"]["sign"] = sign

        casename1.append(i["casenames"])
        heads1.append(i["heads"])
        params1.append(i["params"])

    das = list(zip(casename1,heads1,params1))
    return das