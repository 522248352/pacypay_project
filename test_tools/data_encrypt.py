import hashlib


def dataEncrypt(datas):

    """
    :return:
    """
    s = hashlib.sha256()
    s.update(datas.encode('utf-8'))
    sign = s.hexdigest()

    return sign
