# -*- coding: utf-8 -*-
import os, sys, json
import time
import logging
import clr
from .common import CommonAPI
dir_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(dir_path)
clr.AddReference(os.path.join(dir_path, "Package.dll"))
clr.AddReference(os.path.join(dir_path, "QuoteCom.dll"))
from System import Decimal, UInt16
from System import Enum
from System import AppDomain
from System import BitConverter
from System.Text import UTF8Encoding
from Package import *
from Intelligence import QuoteCom, DT, COM_STATUS, RECOVER_STATUS

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')


class QuoteAPI(CommonAPI):

    def subscribe(self, topic, is_match=True, is_depth=True, is_odd=False):
        if is_match:
            if is_odd:
                status = self.conn.SubQuotesMatchOdd(topic)
            else:
                status = self.conn.SubQuotesMatch(topic)

            if status < 0:
                logging.info("成交:{}".format(self.conn.GetSubQuoteMsg(status)))
        if is_depth:
            if is_odd:
                status = self.conn.SubQuotesDepthOdd(topic)
            else:
                status = self.conn.SubQuotesDepth(topic)

            if status < 0:
                logging.info("五檔:{}".format(self.conn.GetSubQuoteMsg(status)))

    def unsubscribe(self, topic, is_match=True, is_depth=True, is_odd=False):
        if is_match:
            if is_odd:
                self.conn.UnSubQuotesMatchOdd(topic)
            else:
                self.conn.UnSubQuotesMatch(topic)
        if is_depth:
            if is_odd:
                self.conn.UnSubQuotesDepthOdd(topic)
            else:
                self.conn.UnSubQuotesDepth(topic)

    def get_t30(self):
        status = self.conn.RetriveProductTSE()
        if status < 0:
            print(status)
            logging.info(self.conn.GetSubQuoteMsg(status))
        else:
            logging.info("上市商品檔下載完成")
            list_t30 = self.conn.GetProductListTSC()
            if not list_t30:
                logging.warning("無法取得上市商品列表,可能未連線/未下載!!")
            else:
                logging.info("上市商品列表")
                for i in range(list_t30.Count):
                    logging.info(list_t30[i])

    def get_o30(self):
        status = self.conn.RetriveProductOTC()
        if status < 0:
            logging.info(self.conn.GetSubQuoteMsg(status))
        else:
            logging.info("上櫃商品檔下載完成")
            list_o30 = self.conn.GetProductListOTC()
            if not list_o30:
                logging.warning("無法取得上櫃商品列表,可能未連線/未下載!!")
            else:
                logging.info("上櫃商品列表")
                for i in range(list_o30.Count):
                    logging.info(list_o30[i])

    def get_etf(self):
        status = self.conn.RetriveETFStock()
        if status < 0:
            logging.info(self.conn.GetSubQuoteMsg(status))
        else:
            logging.info("ETF成份股檔下載完成")
            for stock_no in ['0050', '0051']:
                list_stock = self.conn.GetETFStocks(stock_no)
                if not list_stock:
                    logging.warning("無法取得成份股商品列表,可能未連線/未下載!!")
                else:
                    logging.info("{}成份股商品列表".format(stock_no))
                    logging.info([list_stock[i] for i in range(list_stock.Count)])

    def get_last_price(self, stock_no, is_odd=False):
        if is_odd:
            status = self.conn.RetriveLastPriceStockOdd(stock_no)
        else:
            status = self.conn.RetriveLastPriceStock(stock_no)
        if status < 0:
            logging.info(self.conn.GetSubQuoteMsg(status))
 
    def get_basic_info(self, stock_no):   # PI30001 基本資料
        package = self.conn.GetProductSTOCK(stock_no)
        if not package:
            logging.info("無法取得該商品明細,可能商品檔未下載或該商品不存在!!")
        else:
            logging.info("股票代碼: {0}  股票名稱: {1}  市場別: {2}  漲停價: {3}  參考價: {4}  跌停價: {5}  上次交易日: {6}"\
                        .format(package.StockNo,
                                package.StockName,
                                package.Market,
                                package.Bull_Price,
                                package.Ref_Price,
                                package.Bear_Price,
                                package.LastTradeDate))

    def get_basic_info(self, stock_no):   # PI30001 基本資料
        package = self.conn.GetProductSTOCK(stock_no)
        if not package:
            logging.info("無法取得該商品明細,可能商品檔未下載或該商品不存在!!")
        else:
            logging.info("股票代碼: {0}  股票名稱: {1}  市場別: {2}  漲停價: {3}  參考價: {4}  跌停價: {5}  上次交易日: {6}"\
                        .format(package.StockNo,
                                package.StockName,
                                package.Market,
                                package.Bull_Price,
                                package.Ref_Price,
                                package.Bear_Price,
                                package.LastTradeDate))

    def receive_msg_handler(self, sender, package):
        logging.debug("[ReceiveMessage] {} {}.".format(sender, package))

        if package.TOPIC and package.TOPIC in self.RecoverMap:
            self.RecoverMap[package.TOPIC] += 1

        if package.DT==DT.LOGIN:    # P001503
            if package.Code==0:
                logging.info("可註冊檔數：" + package.Qnum)
                if self.conn.QuoteFuture:
                    logging.info("可註冊期貨報價")
                if self.conn.QuoteStock:
                    logging.info("可註冊證券報價")                
        elif package.DT==DT.QUOTE_STOCK_MATCH1 or package.DT==DT.QUOTE_STOCK_MATCH2:   # PI31001 上市成交, 上櫃成交
            logging.info("<{0}> {1} 商品代號: {2} 更新時間: {3} 成交價: {4} 單量: {5} 總量: {6} 來源: {7}"\
                        .format("上市" if package.DT==DT.QUOTE_STOCK_MATCH1 else "上櫃",
                                "[試撮]" if package.Status==0 else "",
                                package.StockNo,
                                package.Match_Time,
                                package.Match_Price,
                                package.Match_Qty,
                                package.Total_Qty,
                                package.Source))

        elif package.DT==DT.QUOTE_STOCK_MATCH3:   # PI31001 成交回補 : 2018.7 Add
            logging.info("<{0}> {1} 商品代號: {2}  更新時間: {3}, 成交價: {4}  單量: {5} 總量: {6}  來源: {7}"\
                        .format(package.DT,
                                "[試撮]" if package.Status==0 else "",
                                package.StockNo,
                                package.Match_Time,
                                package.Match_Price,
                                package.Match_Qty,
                                package.Total_Qty,
                                package.Source))

        elif package.DT==DT.QUOTE_STOCK_DEPTH1 or package.DT==DT.QUOTE_STOCK_DEPTH2: # PI31002 上市五檔 or 上櫃五檔
            logging.info("<{0}> {1} 商品代號: {2} 更新時間: {3}  來源: {4}"\
                        .format("上市" if package.DT==DT.QUOTE_STOCK_DEPTH1 else "上櫃",
                                "[試撮]" if package.Status==0 else "",
                                package.StockNo,
                                package.Match_Time,
                                package.Source))
            for i in range(5):
                logging.info("五檔[{0}] 買[價:{1} 量:{2}]    賣[價:{3} 量:{4}]"\
                            .format(i + 1,
                                    package.BUY_DEPTH[i].PRICE,
                                    package.BUY_DEPTH[i].QUANTITY,
                                    package.SELL_DEPTH[i].PRICE,
                                    package.SELL_DEPTH[i].QUANTITY))
        elif package.DT==DT.QUOTE_LAST_PRICE_STOCK: # PI30026
            logging.info("商品代號: {0} 最後價格: {1} 當日最高成交價格: {2} 當日最低成交價格: {3} 開盤價: {4} 開盤量: {5} 參考價: {6} 成交單量: {7} 成交總量: {8}"\
                        .format(package.StockNo,
                                package.LastMatchPrice,
                                package.DayHighPrice,
                                package.DayLowPrice,
                                package.FirstMatchPrice,
                                package.FirstMatchQty,
                                package.ReferencePrice,
                                package.LastMatchQty,
                                package.TotalMatchQty))
            for i in range(5):
                logging.info("五檔[{0}] 買[價:{1} 量:{2}]    賣[價:{3} 量:{4}]"\
                            .format(i + 1,
                                    package.BUY_DEPTH[i].PRICE,
                                    package.BUY_DEPTH[i].QUANTITY,
                                    package.SELL_DEPTH[i].PRICE,
                                    package.SELL_DEPTH[i].QUANTITY))
        #region 2020.9.2 盤中零股
        elif package.DT==DT.QUOTE_ODD_MATCH1 or package.DT==DT.QUOTE_ODD_MATCH2:    # PI35001 上市成交-零股 or 上櫃成交-零股
            logging.info("<{0}> {1} 商品代號: {2}  更新時間:  {3} 成交價: {4}  單量:  {5} 總量: {6}"\
                        .format("上市零股" if package.DT == DT.QUOTE_ODD_MATCH1 else "上櫃零股",
                        "[試撮]" if package.Status==0 else "",
                        package.StockNo,
                        package.Match_Time,
                        package.Match_Price,
                        package.Match_Qty,
                        package.Total_Qty))
        elif package.DT==DT.QUOTE_ODD_DEPTH1 or package.DT==DT.QUOTE_ODD_DEPTH2: # PI31002 上市五檔 or 上櫃五檔
            logging.info("<{0}> {1} 商品代號: {2}  更新時間:  {3}"\
                        .format("上市零股" if package.DT == DT.QUOTE_ODD_DEPTH1 else "上櫃零股",
                                "[試撮]" if package.Status==0 else "",
                                package.StockNo,
                                package.Match_Time))
            for i in range(5):
                logging.info("五檔[{0}] 買[價:{1} 量:{2}]    賣[價:{3} 量:{4}]"\
                            .format(i + 1,
                                    package.BUY_DEPTH[i].PRICE,
                                    package.BUY_DEPTH[i].QUANTITY,
                                    package.SELL_DEPTH[i].PRICE,
                                    package.SELL_DEPTH[i].QUANTITY))
        elif package.DT==DT.QUOTE_LAST_PRICE_ODD:   # PI30026
            logging.info("商品代號: {0} <零股>最後價格: {1} 當日最高成交價格: {2} 當日最低成交價格: {3} 開盤價: {4} 開盤量: {5} 參考價: {6} 成交單量: {7} 成交總量: {8}"\
                        .format(package.StockNo,
                                package.LastMatchPrice,
                                package.DayHighPrice,
                                package.DayLowPrice,
                                package.FirstMatchPrice,
                                package.FirstMatchQty,
                                package.ReferencePrice,
                                package.LastMatchQty,
                                package.TotalMatchQty))
            for i in range(5):
                logging.info("五檔[{0}] 買[價:{1} 量:{2}]    賣[價:{3} 量:{4}]"\
                    .format(i + 1,
                            package.BUY_DEPTH[i].PRICE,
                            package.BUY_DEPTH[i].QUANTITY,
                            package.SELL_DEPTH[i].PRICE,
                            package.SELL_DEPTH[i].QUANTITY))
        #endregion
        elif package.DT==DT.QUOTE_STOCK_INDEX1 or package.DT==DT.QUOTE_STOCK_INDEX2: # PI31011 上市指數 or 上櫃指數
            logging.info("[{0}指數]更新時間： {1}   筆數: {2}".format("上市" if package.DT==DT.QUOTE_STOCK_INDEX1 else "上櫃", package.Match_Time, package.COUNT))
            for i in package.COUNT:
                logging.info(" [{0}] {1}".format(i + 1, package.IDX[i].VALUE))
        elif package.DT==DT.QUOTE_STOCK_NEWINDEX1:  # PI31021 上市新編指數 or 上櫃新編指數
            logging.info("{0}新編指數[{1}] 時間:{2} 指數: {3}".format("上市" if package.DT==DT.QUOTE_STOCK_NEWINDEX1 else "上櫃", package.IndexNo, package.IndexTime, package.LatestIndex))
        elif package.DT==DT.QUOTE_LAST_INDEX1 or package.DT==DT.QUOTE_LAST_INDEX2:  # PI31026 上市最新指數查詢 or 上櫃最新指數查詢
            logging.info("最新{0}指數  筆數: {1}".format("上市" if package.DT == DT.QUOTE_LAST_INDEX1 else "上櫃", package.COUNT))
            for i in package.COUNT:
                logging.info("[{0}]  昨日收盤指數: {1} 開盤指數: {2} 最新指數: {3} 最高指數: {4} 最低指數: {5}"\
                            .format(i + 1,
                                    package.IDX[i].RefIndex,
                                    package.IDX[i].FirstIndex,
                                    package.IDX[i].LastIndex,
                                    package.IDX[i].DayHighIndex,
                                    package.IDX[i].DayLowIndex))
        elif package.DT==DT.QUOTE_STOCK_AVGINDEX:   # PI31022 加權平均指數 2014.8.6 ADD
            logging.info("加權平均指數[{0}] 時間:{1} 最新指數: {2}".format(package.IndexNo, package.IndexTime, package.LatestIndex))

