import allure
import pytest

@allure.feature('前台子系统')
def test_01():
    print("01")
    assert 1==1

def test_02():
    print("02")

    return 1==2

@pytest.mark.xfail
def test_03():


    print("03")
    print("执行案例3")

    assert 1==2



if __name__ == '__main__':
    # pytest.main(["-m",'HttpRequest','--alluredir=../report/allure','--html=../report/a.html',"test_demo1.py"])
    pytest.main(['-s','test_demo1.py','-q','--alluredir','../report'])