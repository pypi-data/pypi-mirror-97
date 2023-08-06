# -*- coding: utf-8 -*-
import os, sys, json
import time
import logging
from datetime import datetime
import pandas as pd
from .common import CommonAPI
import clr
dir_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(dir_path)
clr.AddReference(os.path.join(dir_path, "Package.dll"))
clr.AddReference(os.path.join(dir_path, "TradeCom.dll"))
from System import Decimal, UInt16
from System import Enum
from System import AppDomain
from System import BitConverter
from System.Text import UTF8Encoding
from Package import *
from Intelligence import DT, MARKET_FLAG, SIDE_FLAG, TIME_IN_FORCE, PRICE_FLAG, POSITION_EFFECT, OFFICE_FLAG, ORDER_TYPE, ORDER_KIND, CreditQType
from Smart import AccountItem, AccountQuery, TaiFexCom, TBasicSymbol

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')


class TradeAPI(CommonAPI):

    def __init__(self, debug=False):
        super().__init__(debug=debug)
        self.conn.OnRcvMessage += self.stock_order_handler
        self.conn.OnRcvMessage += self.stock_financial_handler
        self.conn.OnRcvMessage += self.futures_order_handler
        self.conn.OnRcvMessage += self.foreign_futures_order_handler
        self.conn.OnRcvMessage += self.futures_financial_handler

    def stock_order(self, action, broker_no, account_no, lot_type, order_type, side, 
                symbol, quantity, price, price_flag, time_in_force, sub_account_no='', agent_id='', order_id=''):
        logging.info('[Stock_Order] Send order to server.')
        request_id = self.conn.GetRequestId()   # 取得送單序號
        rtn = self.conn.SecurityOrder(request_id, action.value, lot_type.value, order_type.value, broker_no, account_no, symbol, side.value,
                                      UInt16(quantity), Decimal(price), price_flag.value, sub_account_no, agent_id, order_id, time_in_force.value)

        logging.info('[Stock_Order] RequestId={}, receive reply:{}'.format(request_id, self.conn.GetOrderErrMsg(rtn)))

    def futures_order(self, action, branch_no, account_no, sub_account_no, market_type, tb_20_code,
                      time_in_force, writeoff, order_type, side, quantity, price, web_id='', orig_net_no='', order_id=''):
        logging.info('[Futures_Order] Send order to server.')
        officeFlag = OFFICE_FLAG.OF_SPEEDY

        request_id = self.conn.GetRequestId()   # 取得送單序號
        if action.value == ORDER_TYPE.OT_NEW:    # 新單
            rtn = self.conn.Order(action.value, market_type.value, request_id, branch_no, account_no, sub_account_no,
                                tb_20_code, side.value, order_type.value, Decimal(price), time_in_force.value, UInt16(quantity), writeoff.value, officeFlag)
        else:   # 刪/改單
            rtn = self.conn.Order(action.value, market_type.value, request_id, branch_no, account_no, sub_account_no,
                               tb_20_code, side.value, order_type.value, Decimal(price), time_in_force.value, UInt16(quantity), writeoff.value, officeFlag, web_id, orig_net_no, order_id)

        logging.info(self.conn.GetOrderErrMsg(rtn))

    def foreign_futures_order(self, action, market_type, branch_no, account_no, sub_account_no, exchange, 
                              symbol, side1, ComYM1, strike_price1, cp1, symbol2, side2, ComYM2, strike_price2, cp2,
                              order_type, daytrade, writeoff, time_in_force, order_price, stop_price, quantity, isMLeg='N',
                              FCM_idno='', FCM='', FCMAccount='', orig_source='', orig_seq='', orig_net_no='', trade_date='', web_id='', key_in=''):
        ord_kind = ORDER_KIND.OK_CONTROL
 
        request_id = self.conn.GetRequestId()   # 取得送單序號
        rtn = self.conn.FOrder(ord_kind, action.value, request_id, market_type.value, branch_no, account_no, sub_account_no, exchange,
                               symbol, ComYM1, Decimal(strike_price1), cp1, side1.value, order_type.value, daytrade, writeoff.value, time_in_force.value, Decimal(order_price), Decimal(stop_price), int(quantity), FCM_idno,
                               FCM, FCMAccount, orig_source, orig_seq, orig_net_no, trade_date, web_id, key_in,
                                isMLeg, symbol2, side2.value, ComYM2, Decimal(strike_price2), cp2)
        logging.info(self.conn.GetOrderErrMsg(rtn))

    
    def stock_settlement_trial(self, broker_no, account_no, format_type='M', symbol=''):
        '''
        當日交割金額試算
        format_type: M :股票+交易類別彙總
                     D :明細
                     S :台幣彙總(不含外幣)
                     SS:彙總多筆(客戶+幣別)
        '''
        rtn = self.conn.RetrieveWsSettleAmtTrial(format_type, broker_no, account_no, symbol)
        logging.info(self.conn.GetOrderErrMsg(rtn))

    def stock_settlement_detail(self, broker_no, account_no, format_type='M', symbol='', seq_no=''):
        # 當日交割金額_沖銷明細(非當沖)
        rtn = self.conn.RetrieveWsSettleAmtDetail(format_type, broker_no, account_no, symbol, seq_no)
        logging.info(self.conn.GetOrderErrMsg(rtn))

    def stock_settlement(self, broker_no, account_no, format_type='M'):
        # 交割金額查詢(3日)
        rtn = self.conn.RetrieveWsSettleAmt(format_type, broker_no, account_no)
        logging.info(self.conn.GetOrderErrMsg(rtn))

    def stock_inventory(self, broker_no, account_no, format_type='M', symbol=''):
        # 整庫存損益及即時維持率試算
        '''
        format_type: S :  帳號彙總 (換算成台幣彙總)  (現資券合併)
                    SS : 帳號彙總成多筆 (客戶+幣別)  (現資券合併)
                    M : 股票+交易類別小計 (現資券合併) 
                    M1 : 股票+交易類別小計 (資券分開，無現股)
                    D : 明細 (現資券合併) 
                    D1 : 明細 (資券分開，無現股)
        '''
        rtn = self.conn.RetrieveWsInventory(format_type, broker_no, account_no, symbol)
        logging.info(self.conn.GetOrderErrMsg(rtn))

    def stock_inventory_summary(self, broker_no, account_no, format_type='B', symbol=''):
        # 證券庫存滙總
        '''
        format_type: A:現股以張數顯示 
                     B:現股以股數顯示
        '''
        rtn = self.conn.RetrieveWsInventorySum(format_type, broker_no, account_no, symbol)
        logging.info(self.conn.GetOrderErrMsg(rtn))

    def balance_statement(self, broker_no, account_no, format_type='M', symbol='', data_type='T', start_time=datetime.now(), end_time=datetime.now(), days=0):
        # 證券對帳單查詢
        rtn = self.conn.RetrieveWsBalanceStatement(format_type, broker_no, account_no, symbol, data_type, start_time.strftime('YYYYMMDD'), end_time.strftime('YYYYMMDD'), days)
        logging.info(self.conn.GetOrderErrMsg(rtn))

    def stock_credit(self, broker_no, stock_no, query_type=CreditQType.Stk):
        # 證券資券餘額查詢(2017.1 Add)
        rtn = self.conn.RetrieveTSECreditInfo(broker_no, query_type, stock_no)
        logging.info(self.conn.GetOrderErrMsg(rtn))

    def realized_profit(self, broker_no, account_no, format_type='M', symbol='', data_type='T', start_time=datetime.now(), end_time=datetime.now(), days=0):
        # 證券已實現損益查詢(2017.9)
        rtn = self.conn.RetrieveWsRealizePL(format_type, broker_no, account_no, symbol, data_type, start_time.strftime('YYYYMMDD'), end_time.strftime('YYYYMMDD'), days)
        logging.info(self.conn.GetOrderErrMsg(rtn))


    def stock_order_handler(self, sender, package):
        # 證券下單回報
        if package.DT==DT.SECU_ORDER_RPT: # 4010 (證)委託回報
            logging.info("[ReceiveMessage]({}) 委託回報 count={}, order_no={}.".format(package.DT, package.CNT, package.OrderNo))
            header = ["委託型態", "分公司代號", "帳號", "綜合帳戶", "營業員代碼", "委託書號", "交易日期", "回報時間", "委託日期時間", "商品代號", "下單序號", "委託來源別", "市場別", "買賣", "委託別", "委託種類", "委託價格", "改量前數量", "改量後數量", "錯誤代碼", "錯誤訊息"]
            data = [package.OrderFunc, package.BrokerId, package.Account, package.SubAccount, package.OmniAccount, package.AgentId, package.OrderNo, package.TradeDate, package.ReportTime, package.ClientOrderTime, package.StockID, package.CNT, package.Channel, package.Market, package.Side, package.OrdLot, package.OrdClass, package.Price, package.BeforeQty, package.AfterQty, package.ErrCode, package.ErrMsg, package.ReportTimeN, package.ClientOrderTimeN, package.CNTN, package.ChannelN, package.PriceFlagN, package.TimeInForceN, package.PriceN, package.Qty, package.BeforeQtyN, package.AfterQtyN]
            logging.info(dict(zip(header, data)))
        elif package.DT==DT.SECU_DEAL_RPT:  # 4011 (證)成交回報
            logging.info("[ReceiveMessage]({}) 成交回報 count={}.".format(package.DT, package.CNT))
            header = ["委託型態", "分公司代號", "帳號", "綜合帳戶", "營業員代碼", "委託書號", "交易日期", "回報時間", "電子單號", "來源別", "市場別", "商品代碼","買賣別","委託別","委託種類","成交價格","成交數量","市場成交序號"]
            data = [package.OrderFunc, package.BrokerId, package.Account, package.SubAccount, package.OmniAccount, package.AgentId, package.OrderNo, package.TradeDate, package.ReportTime, package.CNT, package.Channel, package.Market, package.StockID, package.Side, package.OrdLot, package.OrdClass, package.Price, package.DealQty, package.MarketNo, package.ReportTimeN, package.CNTN, package.ChannelN, package.PriceFlagN, package.TimeInForceN, package.PriceN, package.DealQtyN, package.AvgPriceN, package.SumQtyN, package.MarketNoN]
            logging.info(dict(zip(header, data)))
        elif package.DT==DT.SECU_ORDER_ACK or package.DT==DT.SECU_ORDER_ACK_N:   # 4002, 6002 下單第二回覆 2019.3. 13 Lynn Add
            logging.info("[ReceiveMessage]({}) 下單第二回覆{} 訊息: {}.".format(package.DT, package.ToLog(), self.conn.GetMessageMap(package.ErrorCode)))
        elif package.DT==DT.SECU_EARMARK_SET:  # 4031 圈存
            logging.info("[ReceiveMessage]({}) EarMark Set: {}".format(package.DT, package.ErrCode))
            header = ["Requestid", "webid", "1.圈/D.解圈", "分公司代號", "帳號", "證券代號", "申請張數", "回覆張數", "申請日期" ,"申請時間","回覆時間","序號","代碼","訊息"]
            data = [package.RequestId,package.Webid,package.TCode,package.BrokerId,package.Account,package.StockNO,package.ApplyQTY,package.ReplyQTY,package.ApplyDate,package.ApplyTime,package.ReplyTime,package.Seqno,package.ErrCode,package.ErrMsg]
            logging.info(dict(zip(header, data)))
        elif package.DT==DT.SECU_CREDITINFO: # 4033 資券餘額查詢 2017.1.5 Add
            header = ["代碼","錯誤訊息" ,"證券代號", "證券名稱", "來源別", "現股交易狀態", "融資狀況", "融券狀況", "市場別", "證券分類", "上市分類", "停資日起", "停資日迄", "停券日起", "停券日迄", "停資券註記", "融資配額張數", "融卷配額張數", "高融成數", "低融成數", "保證金成數", "平盤下可否放空;", "可否融券當沖", "融券最後回補日", "融資成數", "融券成數", "券商警示", "現股當沖碼", "市場控管", "預收款券", "交易單位股數", "價金乘數","幣別","幣別名稱"]
            data = [package.ErrCode, package.ErrMsg, package.StockNO, package.StockName, package.Source, package.DealStatus, package.MarginStatus, package.ShortStatus, package.Market, package.StockType, package.TransType, package.MarginDateB, package.MarginDateE, package.ShortDateB, package.ShortDateE, package.StopMark, package.MarignQty, package.ShortQty, package.HPercent, package.LPercent, package.DepositRate, package.MarkM, package.MarkT, package.ShortLastDate, package.MarginRate, package.ShortRate, package.BrokerWarn, package.DTCode, package.MarketControl, package.PGCL, package.TradeUnit, package.TradeUT2, package.Currency, package.CurrName]
            logging.info(dict(zip(header, data)))
        # 子帳額度控管: 回補
        elif package.DT==DT.SECU_ALLOWANCE_RPT: # 5002
            logging.info("[ReceiveMessage]({}) {}".format(package.DT, package.ToLog()))
        elif package.DT==DT.SECU_ALLOWANCE: # 5003
            logging.info("[ReceiveMessage]({}) {}".format(package.DT, package.ToLog()))
    
    def stock_financial_handler(self, sender, package):
        # 帳務中台WebSerivce 查詢
        if package.DT==DT.FINANCIAL_WSSETAMTTRIAL:    # 4302 當日交割金額試算查詢
            logging.info("[ReceiveMessage]({}) 當日交割金額試算查詢 {} {} 筆數: {},{}".format(package.DT, package.Code,  package.CodeDesc, package.Rows1, package.Rows2))
            if package.Code==0:
                logging.info(package.Detail1)
                logging.info(package.Detail2)
        elif package.DT==DT.FINANCIAL_WSSETAMTDETAIL:   # 4304 當日交割金額_沖銷明細(非當沖)查詢
            logging.info("[ReceiveMessage]({}) 當日交割金額_沖銷明細(非當沖)查詢 {}-{} {} {} 筆數: {}".format(package.DT, package.BrokerID, package.Account, package.Code, package.CodeDesc, package.Rows))
            if package.Code==0:
                logging.info(package.Detail)
        elif package.DT==DT.FINANCIAL_WSSETTLEAMT:  # 4306 交割金額查詢(3日)查詢
            logging.info("[ReceiveMessage]({}) 交割金額查詢(3日)查詢 {}-{} {} {} 筆數: {}".format(package.DT, package.BrokerID, package.Account, package.Code, package.CodeDesc, package.Rows))
            if package.Code==0:
                logging.info(package.Detail)
        elif package.DT==DT.FINANCIAL_WSINVENTORY:  # 4308 庫存損益及即時維持率試算查詢
            logging.info("[ReceiveMessage]({}) 庫存損益及即時維持率試算查詢 {}-{} {} {} 筆數: {}".format(package.DT, package.BrokerID, package.Account, package.Code, package.CodeDesc, package.Rows))
            if package.Code==0:
                logging.info(package.Detail)
        elif package.DT==DT.FINANCIAL_WSINVENTORYSUM:   # 4310 證券庫存彙總查詢 
            # 庫存資料量大, 分多筆送回, 故須自行判斷是否傳送完畢(NowCount = TotalCount)
            # 須注意, 若同一時間查詢多次時, 會造成封包穿插送回, 資料會異常
            if package.Code!=0:
                logging.warning("[ReceiveMessage]({}) 證券庫存彙總查詢 {} {}".format(package.DT, package.Code, package.CodeDesc))
            else:
                logging.debug("[ReceiveMessage]({}) 證券庫存彙總查詢 {}-{} {} {}[{}/{}]".format(package.DT, package.BrokerID, package.Account, package.Code, package.CodeDesc, package.NowCount, package.TotalCount))
                if package.NowCount==1:
                    self.list_data = []
                for i in range(package.Detail.Length):
                    row = package.Detail[i]
                    data = [row.Symbol, row.SymbolName, row.BrokerID, row.Account, row.RQTY0, row.IORDQTY, row.IMATQTY0, row.OORDQTY0, row.OMATQTY0, row.SALEQTY0, row.AORDQTY0, row.NETQTY0, row.IRQTY0, row.ORQTY0, row.SRQTY0  , row.ICTLQTY0, row.OCTLQTY0, row.RQTY9, row.IORDQTY9, row.IMATQTY9, row.OORDQTY9  , row.OMATQTY9  , row.SALEQTY9, row.AORDQTY9, row.NETQTY9, row.RQTY3, row.IORDQTY3, row.IMATQTY3, row.OORDQTY3, row.OMATQTY3, row.SALEQTY3, row.AORDQTY3, row.NETQTY3, row.OCTLQTY3, row.ICTLQTY3, row.RQTY4, row.IORDQTY4, row.IMATQTY4, row.OORDQTY4, row.OMATQTY4, row.SALEQTY4, row.AORDQTY4  , row.NETQTY4, row.OCTLQTY4  , row.ICTLQTY4, row.DTRQTY, row.RLPRICE, row.ASSET, row.ASSETREAL, row.NETPL, row.MKTYPE, row.OAVGPRICE0, row.OAVGPRICE3, row.OAVGPRICE4, row.AVGPRICE0, row.AVGPRICE3, row.AVGPRICE4, row.EXPDATE, row.QUNIT, row.DTQTY0, row.DTCHECK0, row.PRICE_RATE, row.CURRENCY, row.CURRNAME, row.NETPLTWD, row.EXRATEB, row.B_RQTY, row.O_ORDQTY5, row.LSML04001, row.O_MATQTY5, row.LSML04003, row.SALEQTY5, row.LSSL0400, row.AORDQTY5, row.R_QTY5, row.NETQTY5]
                    self.list_data.append(data)
                if package.NowCount==package.TotalCount:
                    header = ["商品代碼","商品名稱","分公司","帳號","昨日餘額","當日新增-委託","當日新增-成交","當日出清-委託","當日出清-成交","現股-可出清餘額","現股-可下單餘額","今日餘額股數","券差數量","出借數量","可賣出借數量","滙撥(股數)","扣押(股數)","昨日餘額(零股)","當日新增-委託(零股)","當日新增-成交(零股)","當日出清-委託(零股)","當日出清-成交(零股)","可出清餘額(零股)","可下單餘額(零股)","今日餘額股數(零股)","昨日餘額(融資)","當日新增-委託(融資)","當日新增-成交(融資)","當日出清-委託(融資)","當日出清-成交(融資)","可出清餘額(融資)","可下單餘額","今日餘額股數(融資)","處份(融資)","解處份(融資)","昨日餘額(融券)","當日新增-委託","當日新增-成交(融券)","當日出清-委託(融券)","當日出清-成交(融券)","可出清餘額(融券)","可下單餘額(融券)","今日餘額股數(融券)","處份(融券)","解處份(融券)","資券當沖數量","即時價","庫存市值","帳面收入","未實現損益","市場別","成交均價(現)","成交均價(資)","成交均價(券)","成本均價(現)","成本均價(資)","成本均價(券)","權證到期日","交易單位股數","現股當沖數量","可現股當沖","價格比率","幣別","約當台幣損益","約當台幣損益","(買進)滙率","券差出借","當日借券賣出-委託","客戶出借1日還券","當日借券賣出-成交","客戶出借3日還券","借入可下單數量","客戶借券","借入可出清數量","昨日餘額(原始借券庫存)","今日餘額股數"]
                    df = pd.DataFrame(self.list_data, columns=header)
                    logging.info(df)
        elif package.DT==DT.FINANCIAL_WSBALANCESTATEMENT:   # 4312 證券庫存彙總查詢
            # 資料量大, 分多筆送回, 故須自行判斷是否傳送完畢(NowCount = TotalCount)
            # 須注意, 若同一時間查詢多次時, 會造成封包穿插送回, 資料會異常
            if package.Code!=0:
                logging.warning("[ReceiveMessage]({}) 證券對帳單查詢 {} {}".format(package.DT, package.Code, package.CodeDesc))
            else:
                logging.debug("[ReceiveMessage]({}) 證券對帳單查詢 {}-{} {} {}[{}/{}]".format(package.DT, package.BrokerID, package.Account, package.Code, package.CodeDesc, package.NowCount, package.TotalCount))
                if package.NowCount==1:
                    self.list_data = []
                for i in range(package.Detail.Length):
                    row = package.Detail[i]
                    data = [row.TradeDate, row.ordClass, row.BS, row.DayTrade, row.Descript, row.Symbol, row.SymbolName, row.TERMSEQNO, row.QTY, row.PRICE, row.AMT, row.FEE, row.TAX, row.CRDBAMT, row.CRSFAMT, row.GTAMT, row.DNAMT, row.CRDBINT, row.BONDINT, row.INSUFEE, row.DBDLFEE, row.CSRECAMT, row.CSPAYAMT, row.NETAMT, row.NETPL, row.SOURCE, row.MKTYPE, row.PNLDTRADE, row.CURRENCY, row.CURRNAME]
                    self.list_data.append(data)
                if package.NowCount==package.TotalCount:
                    header = ["交易日期","交易類別","買賣","當沖","交易類別說明","商品代碼","商品名稱","櫃員序號","成交股數","成交價","成交金額","手續費","交易稅","融資金額/沖銷融資金","融資自備款","融券保證金","融券擔保品","融資/券利息","債息(現股)","證所稅/二代健保補充保費","融券手續費","客戶應收","客戶應付","客戶應收金額","損益","下單來源","市埸別","當沖損益","交割幣別","幣別中文名稱"]
                    df = pd.DataFrame(self.list_data, columns=header)
                    logging.info(df)
        elif package.DT==DT.FINANCIAL_WSREALIZEPL:  # 4314 證券已實現損益查詢 <2017.9.18>
            # 資料量大, 分多筆送回, 故須自行判斷是否傳送完畢(NowCount = TotalCount)
            # 須注意, 若同一時間查詢多次時, 會造成封包穿插送回, 資料會異常
            if package.Code!=0:
                logging.debug("[ReceiveMessage]({}) 證券已實現損益 {} {}".format(package.DT, package.Code, package.CodeDesc))
            else:
                logging.debug("[ReceiveMessage]({}) 證券已實現損益 {}-{} {} {}[{}/{}]".format(package.DT, package.BrokerID, package.Account, package.Code, package.CodeDesc, package.NowCount, package.TotalCount))
                if package.NowCount==1:
                    self.list_data = []
                for i in range(package.Detail.Length):
                    row = package.Detail[i]
                    data = [row.TradeDate, row.ordClass, row.BS, row.DayTrade, row.Descript, row.Symbol, row.SymbolName, row.TERMSEQNO, row.QTY, row.ORIPRICE, row.PRICE, row.AMT, row.TAX, row.FEE, row.CRSFAMT, row.CRDBAMT, row.DNAMT, row.GTAMT, row.BONDINT, row.CRDBINT, row.DBDLFEE, row.INSUFEE, row.NETPL, row.NETAMT, row.COST, row.SFCOST, row.SFPNLRATE, row.PNLRATE, row.SFPNL, row.SFMARK, row.CURRENCY, row.PRICERATE, row.CURRNAME]
                    self.list_data.append(data)
                if package.NowCount==package.TotalCount:
                    header = ["交易日期","交易類別","買賣","當沖註記","交易類別說明","商品代碼","商品名稱","櫃員序號","成交股數","成交價","成交價(均價)","價金","交易稅","手續費","融資自備款","融資金額","融券擔保品","融券保證金","債息(現股)","融資/融券利息","融券手續費","證所稅/二代健保補充保費","損益(客戶立埸)","客戶應收","投資成本金額","自設投資成本金額","自設損益率","損益率","自設損益","自設成本註記","交割幣別","價格比例","幣別中文名稱"]
                    df = pd.DataFrame(self.list_data, columns=header)
                    logging.info(df)


    def futures_order_handler(self, sender, package):
        #region 國內下單回報
        if package.DT==DT.FUT_ORDER_ACK:  # PT02002 下單第二回覆
            logging.info("[ReceiveMessage] {} 訊息: {}".format(package.ToLog(), self.conn.GetMessageMap(package.ErrorCode)))

        elif package.DT==DT.FUT_ORDER_RPT: # PT02010 委託回報
            logging.info("[ReceiveMessage] 2010 [" + package.CNT + "," + package.OrderNo + "]")
            header = ["委託型態", "FrontOffice", "分公司代號", "帳號", "委託書號", "交易日期", "回報時間", "委託日期時間", "主機別", "電子單號", "委託方式", "商品代碼", "買賣別", "市/限價", "委託價格", "新/平倉", "改量前數量", "改量後數量", "委託錯誤碼", "錯誤訊息", "子帳號(Trader)"]
            data = [package.OrderFunc, package.FrontOffice, package.BrokerId, package.Account, package.OrderNo, package.TradeDate, package.ReportTime, package.ClientOrderTime, package.WebID, package.CNT, package.TimeInForce, package.Symbol, package.Side, package.PriceMark, package.Price, package.PositionEffect, package.BeforeQty, package.AfterQty, package.Code, package.ErrMsg, package.Trader]
            logging.info(dict(zip(header, data)))
        elif package.DT==DT.FUT_DEAL_RPT:   # PT02011 成交回報
            logging.info("[ReceiveMessage] 2011 [" + package.OrderNo + "]")
            header = ["委託型態", "FrontOffice", "分公司代號", "帳號", "委託書號", "交易日期", "回報時間", "主機別", "電子單號", "商品代碼", "買賣別", "Market", "成交價格", "成交數量", "已成交總量", "剩餘成交量", "市場成交序號", "商品代號1", "成交價格1", "成交數量1", "買賣別1", "商品代號2", "成交價格2", "成交數量2", "買賣別2", "子帳號(Trader)"]
            data = [package.OrderFunc, package.FrontOffice, package.BrokerId, package.Account, package.OrderNo, package.TradeDate, package.ReportTime, package.WebID, package.CNT, package.Symbol, package.Side, package.Market, package.DealPrice, package.DealQty, package.CumQty, package.LeaveQty, package.MarketNo, package.Symbol1, package.DealPrice1, package.Qty1, package.BS1, package.Symbol2, package.DealPrice2, package.Qty2, package.BS2, package.Trader]

    def foreign_futures_order_handler(self, sender, package):
        #region 國外下單回報
        if package.DT==DT.FFUT_ORDER_ACK: # PT03302 下單第二回覆
            logging.info("[ReceiveMessage] {} 訊息: {}".format(package.ToLog(), self.conn.GetMessageMap(package.ErrorCode)))
        elif package.DT==DT.FFUT_ORDER_RPT: # PT03310 委託回報
            logging.info("[ReceiveMessage] 3310 [" + package.CNT + "," + package.ASorderNo  + "]")
            header = ["委託型態", "交易所", "上手券商", "上手帳號", "上手委託書號", "AS400委託書號", "分公司代號", "帳號", "子帳帳號", "交易日期", "回報時間", "委託平台", "來源別", "原委託網路單號", "委託網路單號", "商品代碼", "商品年月", "履約價", "CP", "BS", "F/I/R", "市/限價", "新/平倉", "當日沖銷", "價格", "停損價", "改量前數量", "改量後數量", "交易員", "錯誤碼", "錯誤訊息"]
            data = [package.OrderFunc, package.Exchange, package.FCM, package.FFUT_ACCOUNT, package.ORDNO, package.ASorderNo, package.BrokerId, package.Account, package.AE, package.TradeDate, package.ReportTime, package.WEBID, package.SOURCE, package.OrgCnt, package.CNT, package.Symbol, package.ComYM, package.StrikePrice, package.CP, package.BS, package.TimeInForce, package.PriceFlag, package.PositionEffect, package.DayTrade, package.Price, package.StopPrice, package.BeforeQty, package.AfterQty, package.KeyIn, package.ErrCode, package.ErrMsg]
            logging.info(dict(zip(header, data)))
        elif package.DT==DT.FFUT_DEAL_RPT:  # PT03311 成交回報
            logging.info("[ReceiveMessage] 3311 [" + package.CNT  + "]")
            header = ["委託型態", "交易所", "上手券商", "上手帳號", "上手委託書號", "AS400委託書號", "分公司代號", "帳號", "子帳帳號", "交易日期", "回報時間", "委託平台", "來源別", "委託網路單號", "商品代碼", "商品年月", "履約價", "CP", "BS", "F/I/R", "市/限價", "新/平倉", "當日沖銷", "成交價格", "成交均價", "成交口數", "成交序號", "剩餘有效口數", "總成交口數", "keyin"]
            data = [package.OrderFunc, package.Exchange, package.FCM, package.FFUT_ACCOUNT, package.ORDNO, package.ASorderNo, package.BrokerId, package.Account, package.AE, package.TradeDate, package.ReportTime, package.WEBID, package.SOURCE, package.CNT, package.Symbol, package.ComYM, package.StrikePrice, package.CP, package.BS, package.TimeInForce, package.PriceFlag, package.PositionEffect, package.DayTrade, package.DealPrice, package.AvgPrice, package.DealQty, package.PATSNo, package.LeavesQty, package.CumQty, package.KeyIn]
            logging.info(dict(zip(header, data)))
        elif package.DT==DT.FFUT_ORDER_RPT2:    # PT03314 委託回報-複式單
            logging.info("[ReceiveMessage] 3314 [" + package.CNT + "," + package.ASorderNo + "]")
            header = ["委託型態", "交易所", "上手券商", "上手帳號", "上手委託書號", "AS400委託書號", "分公司代號", "帳號", "子帳帳號", "交易日期", "回報時間", "委託平台", "來源別", "原委託網路單號", "委託網路單號", "商品代碼", "商品年月", "履約價", "CP", "BS", "商品代碼2", "商品年月2", "履約價2", "CP2", "BS2", "F/I/R", "市/限價", "新/平倉", "當日沖銷", "價格", "停損價", "改量前數量", "改量後數量", "原交易員","交易員", "錯誤碼", "錯誤訊息"]
            data = [package.OrderFunc, package.Exchange, package.FCM, package.FFUT_ACCOUNT, package.ORDNO, package.ASorderNo, package.BrokerId, package.Account, package.AE, package.TradeDate, package.ReportTime, package.WEBID, package.SOURCE, package.OrgCnt, package.CNT, package.Symbol, package.ComYM, package.StrikePrice, package.CP, package.BS, package.Symbol2,package.ComYM2,package.StrikePrice2,package.CP2,package.BS2, package.TimeInForce, package.PriceFlag, package.PositionEffect, package.DayTrade, package.Price, package.StopPrice, package.BeforeQty, package.AfterQty,package.OrgKeyin, package.KeyIn, package.ErrCode, package.ErrMsg]
            logging.info(dict(zip(header, data)))
        elif package.DT==DT.FFUT_DEAL_RPT2:     # PT03315 成交回報-複式單
            logging.info("[ReceiveMessage] 3315 [" + package.CNT + "]")
            header = ["委託型態", "交易所", "上手券商", "上手帳號", "上手委託書號", "AS400委託書號", "分公司代號", "帳號", "子帳帳號", "交易日期", "回報時間", "委託平台", "來源別", "委託網路單號", "商品代碼", "商品年月", "履約價", "CP", "BS", "F/I/R", "市/限價", "新/平倉", "當日沖銷", "成交價格", "成交均價", "成交口數", "成交序號", "剩餘有效口數", "總成交口數", "keyin"]
            data = [package.OrderFunc, package.Exchange, package.FCM, package.FFUT_ACCOUNT, package.ORDNO, package.ASorderNo, package.BrokerId, package.Account, package.AE, package.TradeDate, package.ReportTime, package.WEBID, package.SOURCE, package.CNT, package.Symbol, package.ComYM, package.StrikePrice, package.CP, package.BS, package.TimeInForce, package.PriceFlag, package.PositionEffect, package.DayTrade, package.DealPrice, package.AvgPrice, package.DealQty, package.PATSNo, package.LeavesQty, package.CumQty, package.KeyIn]
            logging.info(dict(zip(header, data)))
        #endregion

    def futures_financial_handler(self, sender, package):
        #region 帳務查詢
        if package.DT==DT.FINANCIAL_COVER_TRADER:    # P001614
            logging.info("[ReceiveMessage] 1614 [" + package.Rows + "]")
            header = ["分公司", "帳號", "組別", "交易員", "交易所", "商品代碼", "商品年月", "履約價", "CP", "幣別", "平倉損益", "交易稅", "手續費", "淨損益", "平倉口數", "平倉損益(TWD)"]
            if package.Rows > 0:
                for row in package.p001614_2:
                    data = [row.BrokerId, row.Account, row.Group, row.Trader, row.Exchange, row.ComID, row.ComYM, row.StrikePrice, row.CP, row.CURRENCY, row.PRTLOS, row.CTAXAMT, row.ORIGNFEE, row.OSPRTLOS, row.Qty, row.OSPRTLOS_TWD]
                    logging.info(dict(zip(header, data)))
        elif package.DT==DT.INVENTORY_TRADER:   # P001616
            logging.info("[ReceiveMessage] 1616 [" + package.Rows  + "]")
            header = ["分公司", "帳號", "組別", "交易員", "交易所", "期/權", "商品代碼", "商品年月", "履約價", "CP", "BS", "交割日期(外)", "幣別", "未平倉量", "結算價", "即時價", "未平倉損益", "成交均價"]
            if package.Rows > 0:
                for row in package.p001616_2:
                    data = [row.BrokerId, row.Account, row.Group, row.Trader, row.Exchange, row.ComType, row.ComID, row.ComYM, row.StrikePrice, row.CP, row.BS, row.DeliveryDate, row.Currency, row.OTQty, row.TrdPrice, row.MPrice, row.PRTLOS, row.DealPrice]
                    logging.info(dict(zip(header, data)))
        elif package.DT==DT.INVENTORY_DETAIL_TRADER:    # P001618
            logging.info("[ReceiveMessage] 1618 [" + package.Rows  + "]")
            header = ["分公司", "帳號", "組別", "交易員", "交易所", "場內編號(外)", "上手帳號(外)", "交易方式", "上手券商", "交割日期(外)", "結算日期(外)", "下單方式", "電子單號", "委託書號", "成交序號", "拆單序號", "成交日期", "商品代碼", "BS", "期/權", "CP", "履約價", "商品年月", "未平倉量", "結算價", "即時價", "未平倉損益", "原始保證金", "維持保證金", "幣別", "成交價", "混合口數一", "當日沖銷 ", "SPREAD", "複式組合單號", "委託書號2", "成交序號2", "拆單序號2", "成交日期2", "商品代碼2", "BS2", "期/權2", "CP2", "履約價2", "商品年月2", "未平倉量2", "結算價2", "即時價2", "未平倉損益2", "原始保證金2", "維持保證金2", "幣別2", "成交價2", "混合口數2", "當日沖銷2"]
            if package.Rows > 0:
                for row in package.p001618_2:
                    data = [row.BrokerId, row.Account, row.Group, row.Trader, row.Exchange, row.SeqNo, row.FcmActNo, row.TradeType, row.FCM, row.DeliveryDate, row.CloseDate, row.WEB, row.Cnt, row.OrdNo, row.MarketNo, row.sNo, row.TradeDate, row.ComID, row.BS, row.ComType, row.CP, row.StrikePrice, row.ComYM, row.Qty, row.TrdPrice, row.MPrice, row.PRTLOS, row.InitialMargin, row.MTMargin, row.Currency, row.DealPrice, row.MixQty, row.DayTrade, row.SPREAD, row.spKey, row.OrdNo2, row.MarketNo2, row.sNo2, row.TradeDate2, row.ComID2, row.BS2, row.ComType2, row.CP2, row.StrikePrice2, row.ComYM2, row.Qty2, row.TrdPrice2, row.MPrice2, row.PRTLOS2, row.InitialMargin2, row.MTMargin2, row.Currency2, row.DealPrice2, row.MixQty2, row.DayTrade2]
                    logging.info(dict(zip(header, data)))
        elif package.DT==DT.FINANCIAL_COVER_TRADER_Detail:  # P001624
            logging.info("[ReceiveMessage] 1624 [" + package.Rows  + "]")
            header = ["分公司", "帳號", "組別", "交易員", "交易所", "平倉日期", "平倉成交日期", "平倉委託編號", "平倉成交序號", "平倉拆單序號", "被平成交日期", "被平委託編號", "被平成交序號", "被平拆單序號", "指定平倉碼", "互抵", "BS", "商品代號", "商品年月", "履約價 ", "CP", "被平商品代號", "平倉口數", "被平口數", "平倉成交價", "被平成交價", "平倉損益", "業務員代號", "幣別", "交易稅", "手續費", "平倉權利金", "被平權利金", "平倉場內編號", "被平場內編號", "平倉電子單號", "被平電子單號", "淨損益"]
            if package.Rows > 0:
                for row in package.p001624_2:
                    data = [row.BrokerId, row.Account, row.Group, row.Trader, row.Exchange, row.OccDT, row.TrdDT1, row.OrdNo1, row.FirmOrd1, row.OffsetSpliteSeqNo,
                            row.TrdDT2, row.OrdNo2, row.FirmOrd2, row.OffsetSpliteSeqNo2, row.OffsetCode, row.offset, row.BS,
                            row.ComID, row.ComYM, row.StrikePrice, row.CP, row.ComID2, row.Qty1, row.Qty2, row.TrdPrice1, row.TrdPrice2,
                            row.PRTLOS, row.AENO, row.Currency, row.CTAXAMT, row.ORIGNFEE, row.Premium1, row.Premium2, row.InNo1, row.InNo2, row.Cnt1, row.Cnt2, row.OSRTLOS]
                    logging.info(dict(zip(header, data)))
        elif package.DT==DT.FINANCIAL_TRADERN:    # P001626 可出金金額
            logging.info("[ReceiveMessage] 1626 [" + package.Count  + "]")
            header = ["分公司", "帳號", "組別", "交易員", "幣別", "前日餘額", "手續費", "匯率", "期交稅", "存提", "平倉損益", "未平倉損益", "未沖銷買方選擇權市值", "未沖銷賣方選擇權市值", "委託權利金", "權利金收入與支出", "權益數", "原始保證金", "維持保證金", "可用餘額", "可動用(出金)保證金", "委託保證金", "到期履約損益", "變動權利金", "洗價時間", "未沖銷期貨浮動損益", "昨日未沖銷期貨浮動損益", "到期結算保證金", "足額原始保證金", "足額維持保證金", "當沖原始保證金", "多空減收保證金", "當沖應補保證金", "本日餘額", "本日權利金收入", "本日權利金支出", "有價証券價值", "有價証券抵繳金額", "委託抵繳保證金", "剩餘可抵繳金額", "足額風險指標", "足額權益比例", "追繳金額", "賣方垂直價差市價", "履約價款", "權益總值", "本日期貨平倉損益淨額", "超額/追繳保證金", "加收保證金", "可動用(不含 CN$超額)" ,"可出金金額"]
            if package.Count > 0:
                for row in package.p001626_2:
                    data = [row.BrokerId, row.Account, row.Group, row.Trader, row.Currency, row.LCTDAB, row.ORIGNFEE, row.TAXAMT, row.CTAXAMT, row.DWAMT,
                            row.OSPRTLOS, row.PRTLOS, row.BMKTVAL, row.SMKTVAL, row.OPREMIUM, row.TPREMIUM, row.EQUITY, row.IAMT, row.MAMT, row.EXCESS,
                            row.ORDEXCESS, row.ORDAMT, row.ExProfit, row.Premium, row.PTime, row.FloatProfit, row.LASSPRTLOS, row.CLOSEAMT,
                            row.ORDIAMT, row.ORDMAMT, row.DayTradeAMT, row.ReductionAMT, row.CreditAMT, row.balance, row.IPremium, row.OPremium,
                            row.Securities, row.SecuritiesOffset, row.OffsetAMT, row.Offset, row.FULLMTRISK, row.FULLRISK, row.MarginCall,
                            row.SellVerticalSpread, row.StrikePrice, row.ActMarketValue, row.TPRTLOS, row.MarginCall1, row.AddMargin, row.ORDAMTNOCN,row.WithdrawMnt]
                    logging.info(dict(zip(header, data)))                   
        elif package.DT==DT.FINANCIAL_CURRENCY: # P001628
            logging.info("[ReceiveMessage] 1628 CODE= " + package.Code + " MSG=" + package.ErrorMsg)
        elif package.DT==DT.FINANCIAL_STRIKE:  # 2017.2.4 P001643  無效履約查詢
            header = ["分公司", "帳號", "組別", "交易員","履約日期","成交日期","委託單號","成交序號","拆單序號", "交易所", "商品代碼", "商品年月", "履約價", "CP", "BS", "口數", "交易稅幣別","交易稅","手續費幣別","手續費","交易幣別","權利金收支/履約盈虧","結算價"]
            logging.info("[ReceiveMessage] 1643 Code =  " + package.Code +  "   Rows[" + package.Rows + "]")
            if package.Rows > 0:
                for row in package.Detail:
                    data = [row.BrokerId, row.Account, row.Group, row.Trader, row.DueDate, row.TrdDate, row.OrdNo, row.FirmOrd, row.SeqNo,
                            row.Exchange, row.ComID, row.ComYM, row.StrikePrice, row.CP, row.BS,
                            row.Qty, row.TaxCurr, row.TaxAmt, row.FeeCurr, row.FeeAmt, row.TrdCurr,row.Premium,row.TrdPre]
                    logging.info(dict(zip(header, data)))
        elif package.DT==DT.FINANCIAL_COVERDH: # 2017.2.14  P001645 平倉明細歷史查詢
            logging.info("[ReceiveMessage] 1645 Code =  " + package.Code + "   Rows[" + package.Rows + "]")
            header = ["市場別","分公司", "帳號", "組別", "交易員", "交易所", "平倉日期", "平倉成交日期", "平倉委託編號", "平倉成交序號", "平倉拆單序號", "被平成交日期", "被平委託編號", "被平成交序號", "被平拆單序號", "指定平倉碼", "互抵", "BS", "商品代號", "商品年月", "履約價 ", "CP", "被平商品代號", "平倉口數", "被平口數", "平倉成交價", "被平成交價", "平倉損益", "業務員代號", "幣別", "交易稅", "手續費", "平倉權利金", "被平權利金", "平倉場內編號", "被平場內編號", "平倉電子單號", "被平電子單號"]
            if package.Rows > 0:
                for row in package.Detail:
                    data = [row.Market, row.BrokerId, row.Account, row.Group, row.Trader, row.Exchange, row.OccDT, row.TrdDT1, row.OrdNo1, row.FirmOrd1, 
                            row.OffsetSpliteSeqNo, row.TrdDT2, row.OrdNo2, row.FirmOrd2, row.OffsetSpliteSeqNo2, row.OffsetCode, row.offset,
                            row.BS, row.ComID, row.ComYM, row.StrikePrice, row.CP, row.ComID2, row.Qty1, row.Qty2, row.TrdPrice1, row.TrdPrice2,
                            row.PRTLOS, row.AENO, row.Currency, row.CTAXAMT, row.ORIGNFEE, row.Premium1, row.Premium2, row.InNo1, row.InNo2, row.Cnt1, row.Cnt2]
                    logging.info(dict(zip(header, data)))                  
        elif package.DT==DT.FINANCIAL_RECIPROCATE:  # 2018.12 P001647: 大小台互抵
            if package.Status == "0":
                logging.info(package.BrokerId + package.Account + "大小台互抵成功: 大台 " + package.Qty1 + " ,小台 " + package.Qty2)
            else:
                logging.info(package.BrokerId + package.Account + " 大小台互抵失敗") 
        elif package.DT==DT.FINANCIAL_SERVICECHARGE: # P001631 手續費
            logging.info("[ReceiveMessage] 1631 [" + package.Count + "]")
            header = ["分公司", "帳號", "組別", "交易員", "特定費用分類", "費用分類", "口數", "計算方式", "定額/率", "金額", "定率比率", "幣別"]
            if package.Count > 0:
                for row in package.p001631_2:
                    data = [row.BrokerId, row.Account, row.Group, row.Trader, row.Kind, row.Class, row.Qty, row.Method, row.Rule, row.Amt, row.Rate, row.Currency] 
                    logging.info(dict(zip(header, data)))
        elif package.DT==DT.FINANCIAL_APPLYWITHDRAW:  # P001633 出金申請 
            logging.info("[ReceiveMessage] 1633 ")
            header = ["Webid", "網路序號", "出金批號", "後台異動時間", "申請日期", "申請時間", "可用餘額", "ErrorCode", "訊息"]
            data = [package.Webid, package.Seqno, package.ApplyNo, package.UpdateTime, package.ApplyDate, package.ApplyTime, package.AMT, package.Code, package.ErrorMsg]
            logging.info(dict(zip(header, data)))
        elif package.DT==DT.FINANCIAL_WITHDRAW: # P001635
            logging.info("[ReceiveMessage] 1635 [" + package.Count + "]")
            header = ["Webid", "網路序號", "國內/外","存提類別C/D","異動日期","存提單號","存解款銀行","存解款帳號","幣別","原幣金額","台幣金額","已出磁片否"]
            if package.Count > 0:
                for row in package.p001635_2:
                    data = [row.Webid, row.Seqno, row.Market, row.Type, row.UpdateDate, row.WithdrawNo, row.BankNo, row.BankAccount, row.Currency, row.Amt, row.NTAmt, row.Status]
                    logging.info(dict(zip(header, data)))


