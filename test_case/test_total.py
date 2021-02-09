from test_case import test_sale, test_checkout_new


class Test_all(object):
    def test_sale(self):
        test_sale.test_sale()
    def test_check(self):
        test_checkout_new.test_checkout()