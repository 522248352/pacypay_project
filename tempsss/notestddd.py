import time
import functools
from nb_log import LogManager

from tempsss.logg_diy import Logger

# logger = LogManager.get_logger_and_add_handlers('mymail_logger_name',  is_add_mail_handler=True)
logger = LogManager("diy").get_logger_and_add_handlers(log_filename = 'ApiTest.log',
                                                       is_add_stream_handler=True,
                                                       is_add_mail_handler=False)
# for _ in range(100):
#     logger.warning('测试邮件日志的内容。。。。')
#     time.sleep(10)

def bigadd(args1):

    if isinstance(args1,str):
        def to2s(funs):
            @functools.wraps(funs)
            def wrapper(*args, **kw):
                logger.info("this is "+args1)
                logger.info("begin")
                logger.info(funs(*args, **kw))
                logger.info("end")
            return wrapper
        return to2s
    else:
        @functools.wraps(args1)
        def wrapper(*args, **kw):
            logger.info ("this is fun")
            logger.info ("begin")
            logger.info (args1 (*args, **kw))
            logger.info ("end")
        return wrapper

@bigadd
def s(x,y):
    return x+y

@bigadd("text")
def m(x,y):
    return x+y

if __name__ == '__main__':
    s(7,8)
    m(9,10)