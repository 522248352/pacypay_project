
import re
import csv
from test_tools import rw_csv
import os

current_path = os.path.dirname(__file__)
current_path_up = os.path.dirname(current_path)

data = [["transactionId","tradeNo"]]
with open(current_path_up+"/test_data/transaction.csv","w",newline='') as f:
    fs = csv.writer(f)
    for i in data:
        fs.writerow(i)