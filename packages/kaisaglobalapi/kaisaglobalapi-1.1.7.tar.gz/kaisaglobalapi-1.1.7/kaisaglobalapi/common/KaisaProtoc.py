# -*- coding: utf-8 -*-

import sys, json
from os.path import dirname, abspath

project_path = dirname(dirname(abspath(__file__)))
projec_full_path = project_path + r'\py_protoc'
sys.path.append(projec_full_path)

from py_protoc import msg_stock_pb2 as msg_stock
from py_protoc import msg_stock_pb2 as msg_stock
from py_protoc import msg_stock_common_pb2 as msg_stock_common


class KaisaProtoc(object):

    def __init__(self):
        pass

    @staticmethod
    def get_ping_bstring(reqId=1):

        pb_reqhead = msg_stock_common.ReqHead()
        pb_reqhead.reqId = str(reqId)
        pb_reqhead.reqType = 3
        pb_string = pb_reqhead.SerializeToString()
        return pb_string

    @staticmethod
    def get_subscribe_bstring(symbollist, reqId=1):

        pb_rule = msg_stock.Rule()
        pb_stockcode = msg_stock.StockCode()
        for secucode_dict in symbollist:
            pb_stockcode_one = pb_rule.stockCodes.add()
            pb_stockcode_one.code = secucode_dict['code']
            pb_stockcode_one.market = 2
            pb_stockcode_one.language = 0

        pb_rule.types.append(1)
        pb_rule.types.append(2)

        pb_reqhead = msg_stock_common.ReqHead()
        pb_reqhead.reqId = str(reqId)
        pb_reqhead.reqType = 1
        pb_reqhead.data = pb_rule.SerializeToString()

        pb_string = pb_reqhead.SerializeToString()
        return pb_string

    @staticmethod
    def get_unsubscribe_bstring(symbollist, reqId=1):

        pb_rule = msg_stock.Rule()
        pb_stockcode = msg_stock.StockCode()
        for secucode_dict in symbollist:
            pb_stockcode_one = pb_rule.stockCodes.add()
            pb_stockcode_one.code = secucode_dict['code']
            pb_stockcode_one.market = 2
            pb_stockcode_one.language = 0

        pb_rule.types.append(1)
        pb_rule.types.append(2)

        pb_reqhead = msg_stock_common.ReqHead()
        pb_reqhead.reqId = str(reqId)
        pb_reqhead.reqType = 2
        pb_reqhead.data = pb_rule.SerializeToString()

        pb_string = pb_reqhead.SerializeToString()
        return pb_string


    @staticmethod
    def rec_bstring_to_json(bstring):

        pb_reshead = msg_stock_common.ResHead()
        pb_reshead.ParseFromString(bstring)

        if (pb_reshead.msg=='SUCCESS'):
            pass
        else:
            print("error.")
            print(pb_reshead.msg)
            return None

        if (pb_reshead.type==1):
            quote = msg_stock.Quote()
            quote.ParseFromString(pb_reshead.data)
            body_json = KaisaProtoc.quote_bstring_to_json(quote)
            data_type = 'quote'

        elif (pb_reshead.type==2):
            ticklist = msg_stock.TickList()
            ticklist.ParseFromString(pb_reshead.data)
            body_json = KaisaProtoc.ticklist_bstring_to_json(ticklist)
            data_type = 'tick'

        return {'type': data_type,
                'data': body_json}

    @staticmethod
    def quote_bstring_to_json(quote):

        return {'market':quote.market,
                'code':quote.code,
                'now':quote.now,
                'high': quote.high,
                'low': quote.low,
                'volume': quote.volume,
                'amount': quote.amount,
                'quote_time': quote.quote_time.seconds+quote.quote_time.nanos/1000000000.0
                }

    @staticmethod
    def ticklist_bstring_to_json(ticklist):

        return {'market': ticklist.market,
                'code': ticklist.code,
                'tick': [KaisaProtoc.tick_bstring_to_json(item) for item in ticklist.tick]
                }

    @staticmethod
    def tick_bstring_to_json(tick):

        return {'now': tick.now,
                'cur_volume': tick.cur_volume,
                'tick_flag': tick.tick_flag,
                'tick_vi': tick.tick_vi,
                'tick_time': tick.tick_time.seconds+tick.tick_time.nanos/1000000000.0
                }

if __name__=='__main__':

    print('start.')

