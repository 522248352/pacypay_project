import pytest


def addMark(datas):
    mm = []
    for i in datas:
        mm.append(pytest.param(*i[:-1],marks=i[-1]))
    return mm