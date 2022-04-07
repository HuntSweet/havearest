import datetime
import time
from chinese_calendar import is_workday
from datetime import datetime
# import requests
import wencai as wc
from pandas import DataFrame
import pymysql
from sqlalchemy import create_engine

time_format = "%Y-%m-%d"
pymysql.install_as_MySQLdb()
DB_STRING = 'mysql+mysqldb://root:123456@127.0.0.1/2to100?charset=utf8'
engine = create_engine(DB_STRING)

# wc.set_variable(cn_col=True)
def write_to_mysql(df,type,date):
    engToCnDict = {'所属概念':'concept','总市值':'total_value','a股市值(不含限售股)':'circulating_value','最新价':'price','最新涨跌幅':'gain',
                   '市盈率(pe)':'pe','股票代码':'code','所属同花顺行业':'industry','股票简称':'name'}
    dateArray = time.strptime(date,time_format)
    date = time.mktime(dateArray)

    df.drop(columns=['总股本','收盘价创新高(条件说明)','最新dde大单净额'],inplace=True)
    df.rename(columns=engToCnDict,inplace=True)
    df['date'] = date
    df['created_on'] = int(time.time())
    df['type'] = type
    #print(df)

    df.to_sql('up',con=engine,if_exists='append',index=False)

def test_query(type,date):
    # r = wc.search('上穿15日均线；所属同花顺行业；2022.3.28')
    # r = wc.search('行业涨幅倒序排行')
    if type == '60日新高':
        query = '收盘价创60日新高；所属同花顺行业；市值；流通市值;'+date
        r = wc.search(query)
        df = DataFrame(r)
        write_to_mysql(df,'60日新高',date)
    if type == '15日均线':
        query = '收盘价上穿15日均线；所属同花顺行业；市值；流通市值'+date
        r = wc.search(query)
        df = DataFrame(r)
        write_to_mysql(df,'15日均线',date)
    # df.to_excel(query + '.xlsx')
    # print(r, '--')

def get_range_date(startStr,endStr):
    list = []
    start = datetime.datetime.strptime(startStr,time_format)
    end = datetime.datetime.strptime(endStr,time_format)
    list.append(start.strftime(time_format))
    while start < end:
        start += datetime.timedelta(days=1)
        if is_trading_day(start.strftime(time_format)):
            list.append(start.strftime(time_format))
    return list

def is_trading_day(date):
    # # url = 'http://tool.bitefu.net/jiari/?d=' + query_date
    # # 上面的url接口  工作日对应结果为 0, 休息日对应结果为 1, 节假日对应的结果为 2；
    # # url = 'http://www.easybots.cn/api/holiday.php?d=' + query_date  需要实名认证
    # url = 'https://api.goseek.cn/Tools/holiday?date=' + day
    # # 返回数据：正常工作日对应结果为 0, 法定节假日对应结果为 1, 节假日调休补班对应的结果为 2，休息日对应结果为 3
    # # 20190528
    # response = requests.get(url=url)
    # content = response.text  # str 类型的
    # # {"code":10000,"data":0}
    # # 返回数据：正常工作日对应结果为 0, 法定节假日对应结果为 1, 节假日调休补班对应的结果为 2，休息日对应结果为 3
    # return content['data'] == 0
    if is_workday(date):
        if date.isoweekday() < 6:
            return True
    return False

def get_range_data(startStr,endStr):
    list = get_range_date(startStr,endStr)
    for day in list:
        test_query('60日新高', day)

if __name__ == '__main__':
    get_range_data('2019-12-1','2022-2-6')

