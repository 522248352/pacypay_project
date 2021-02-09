import pytest

das1 = [(1,2),(2,3),(3,4)]
a1=b1=c1=d1=e1=f1=None
@pytest.mark.parametrize('a,b',das1)
def test_01(a,b):
    global a1
    global b1

    a1 = a
    b1 = b

def test_02():
    print(a1,b1)


if __name__ == '__main__':
    pytest.main(['-sq','test_demo.py'])
