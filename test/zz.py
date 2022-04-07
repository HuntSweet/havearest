import tushare as ts
import datetime
import time


if __name__ == '__main__':
    pro = ts.pro_api('47500d30cf11f9dba8eb6cf03fbd43cdccc666d6d8f6d2bc11ad5b91')
    df = pro.query('trade_cal', start_date='20180101', end_date='20181231')
    print(df)