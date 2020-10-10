import pytest
import requests


@pytest.fixture()
def login():
    """
    登录 manage 系统
    :return: session
    """
    sess = requests.session()
    params = {"adminForm.login.loginName":"DW","adminForm.login.loginPass":"123456asd","adminForm.lang":"zh_CN"}
    resu = sess.post(url="https://test-v2.pacypay.com/manage/main.html",data=params)
    print(resu.status_code)
    return sess
# print(resu.text)
