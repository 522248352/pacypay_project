
import re
import csv
from test_tools import rw_csv


data = [["transactionId","tradeNo"]]
with open("../test_data/transaction.csv","w",newline='') as f:
    fs = csv.writer(f)
    for i in data:
        fs.writerow(i)