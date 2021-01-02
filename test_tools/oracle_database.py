import cx_Oracle
from nb_log import LogManager
from test_tools.rw_csv import read_csv


logger = LogManager("diy").get_logger_and_add_handlers(log_filename = 'ApiTest.log')

csv_param = read_csv("database.csv")
print(csv_param)

# conn = cx_Oracle.connect("pay","he7qNGuS5Hu19Igz","192.168.200.247:1521/orcl")
# conn = cx_Oracle.connect("pay/he7qNGuS5Hu19Igz@192.168.200.247:1521/orcl")

class DB(object):

    csv_param = read_csv("database.csv")

    def __init__(self):

        self.conn = cx_Oracle.connect(DB.csv_param[0]["username"],DB.csv_param[0]["password"],DB.csv_param[0]["host_port_database"])
        # self.conn = cx_Oracle.connect("pay","he7qNGuS5Hu19Igz","192.168.200.247:1521/orcl")
        logger.info("======连接 success======")
        self.cursor_en = self.conn.cursor()

    def query(self,sql):
        try:

            self.cursor_en.execute(sql)
            return self.cursor_en.fetchall()
        except Exception as e:
            logger.error("查询query方法报错%s"%e)

        # finally:
        #     self.conn.close()
        #     print("=========close success==============")
    def closes(self):
        self.conn.close()
        logger.info("======关闭 success======")

# print("lianjie")
# cur = conn.cursor()
# sql1="SELECT TR_CAPTURED,TR_BANKORDERNO,TR_CHECKED,TR_CHECKDATETIME,TR_STATUS,TR_IS_REPAY FROM CCPS_TRADERECORD
# where TR_NO='3668353024890372096'"
#
# cur.execute(sql1)
#
# resu = cur.fetchall()
# print(resu)
#
# for i in resu:
#     print(i)
#
# cur.close()
# conn.close()


if __name__ == "__main__":

    db = DB()
    sql1 = "SELECT TR_CAPTURED,TR_BANKORDERNO,TR_CHECKED,TR_CHECKDATETIME,TR_STATUS,TR_IS_REPAY " \
           "FROM CCPS_TRADERECORD where TR_NO='3668430309045829632'"
    ss1 = db.query(sql1)

    print(ss1)
    sql2 = "select TR_CURRENCY,TR_AMOUNT,TR_STATUS,TR_PAYMENT_STATUS,TR_BANKCURRENCY,TR_BANKAMOUT," \
           "TR_BANK_CODE,TR_BANKRETURNCODE,TR_BANKINFO,TR_NOTIFYURL,TR_CAPTURED,TR_CAPTURE_TIME,TR_INF_TYPE," \
           "TR_CARDTYPE from CCPS_TRADERECORD where tr_no ='3668430309045829632'"
    ss2 = db.query(sql2)
    db.closes()
    print(ss2)
    print(type(ss2))