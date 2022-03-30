import unittest
import wencai as wc
from pandas import DataFrame


class TestWenCai(unittest.TestCase):

    def setUp(self) -> None:
        wc.set_variable(cn_col=True)

    # def test_get_scrape_report(self):
    #     r = wc.get_scrape_report(query='上证指数上穿10日均线',
    #                              start_date='2019-10-01',
    #                              end_date='2019-10-19',
    #                              period='1,2,3,4',
    #                              benchmark='hs000300')
    #
    #     print(r.report_data)
    #     print(r.backtest_data)
    #     print(r.condition_data)
    #     print(r.history_detail(period='1'))

    def test_get_strategy(self):
        r = wc.get_strategy(query='15天内涨停过；收十字星;非st；市值大小倒叙',
                            start_date='2021-12-09',
                            end_date='2022-03-30',
                            period='2',
                            fall_income=2,
                            lower_income=6,
                            upper_income=10,
                            day_buy_stock_num=1,
                            stock_hold=1)
        print(r.profit_data)
        print(r.backtest_data)
        print(r.condition_data)
        print(r.history_detail(period='1'))
        print(r.history_pick(trade_date='2022-03-30', hold_num=1))

    # def test_get_event_evaluate(self):
    #     r = wc.get_event_evaluate(end_date='2022-03-30',
    #                               index_code="1a0001",
    #                               period='1',
    #                               query="上证指数上穿10日均线",
    #                               start_date="2016-05-16")
    #     print(r.report_data)
    #     print(r.event_list)

    # def test_query(self):
    #     # r = wc.search('上穿15日均线；所属同花顺行业；2022.3.28')
    #     # r = wc.search('行业涨幅倒序排行')
    #     query = '15天内涨停过；收十字星'
    #     r = wc.search(query)
    #     df = DataFrame(r)
    #     df.to_excel(query + '.xlsx')
    #     print(r, '--')


if __name__ == '__main__':
    unittest.main()
