from nb_log import LogManager
import os
p = os.path.abspath(__file__)
m = os.path.dirname(__file__)
print(p)
print(m)
logger = LogManager("diy").get_logger_and_add_handlers(log_filename = 'ApiTest.log',log_path=m)

# log_path='/pythonlogs'