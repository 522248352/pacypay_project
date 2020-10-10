import pytest
import sys
from cove.pay import pay
print(sys.path)

def test_pay_success():

    result={"code":"1"}

    assert pay(result) == "success"

def test_pay_fail():

    result={"code":"2"}

    assert pay(result) == "fail"

# --cov接受目录或软件包名称，而不是单个文件。这意味着将--cov=sample.py查找一个名为的包（目录），
# sample并在其中查找一个名为py.py记录覆盖率的模块（文件），然后失败。无论使用
#
# $ pytest --cov=sample
# 要么
#
# $ pytest --cov=.

if __name__ == '__main__':
    # pytest.main(['--cov=cove','--cov-report=html'])
    pass
