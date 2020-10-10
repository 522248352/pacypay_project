from nb_log import LogManager

class Logger(object):
    def __init__(self):
        self.logger = LogManager("diy").get_logger_and_add_handlers(log_filename = 'ApiTest.log')



        print("hello")
        # logger.info("info")
        # logger.warning("warn")
        # logger.debug("debug")
        #
        #
        # logger.error("error")
