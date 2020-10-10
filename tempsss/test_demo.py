import pytest

from tempsss.notestddd import pay

dic1 = {"name":"lili"}
dic2 = {"age":"56"}
dic3 = dic1.update(dic2)

print(dic1)

def test_pay():
    result = {"code":"1"}
    assert pay(result) == "success"


if __name__ == '__main__':
    pytest.main(["--cov","test_demo.py"])
