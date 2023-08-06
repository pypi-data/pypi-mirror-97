# -*- coding: utf-8 -*-
import os, sys, json
import time
import logging
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
from Intelligence import Login, DT, COM_STATUS, RECOVER_STATUS
from Smart import AccountItem, AccountQuery, TaiFexCom, TBasicSymbol

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')


class CommonAPI():

    def __init__(self, debug=False):
        self.conn = TaiFexCom("10.4.99.71", 8000, "API")
        self.is_login = False
        logging.info("[KGI] Api version is {}".format(self.conn.version))
        
        # register event handler
        self.conn.OnRcvMessage += self.receive_msg_handler   #資料接收事件
        self.conn.OnGetStatus += self.get_status_handler            #狀態通知事件
        self.conn.OnRcvServerTime += self.receive_time_handler    #接收主機時間
        self.conn.OnRecoverStatus += self.recover_status_handler    #回補狀態通知

        if debug:
            self.conn.ServerHost = "itradetest.kgi.com.tw"
            self.conn.ServerPort = 443
            self.conn.ServerHost2 = "itradetest.kgi.com.tw"
            self.conn.ServerPort2 = 8000
        else:
            self.conn.ServerHost = "tradeapi.kgi.com.tw"
            self.conn.ServerPort = 443
            self.conn.ServerHost2 = "tradeapi.kgi.com.tw"
            self.conn.ServerPort2 = 8000
        
    # 登入
    def login(self, id_no, pwd):
        self.is_login = False
        self.conn.AutoRedirectPushLogin = True

        self.conn.AutoRetriveProductInfo = True     ## 是否載入商品檔
        self.conn.AutoSubReport = True          ## 是否回補回報&註冊即時回報(國內)
        self.conn.AutoSubReportForeign = True   ## 是否回補回報&註冊即時回報(國外)

        ## 2015.7 原來註冊回報一定要回補回報, 原改為可擇一
        ## 若AutoRecoverReportSecurity 未特別設定時, 則預設值等於 AutoSubReportSecurity
        self.conn.AutoSubReportSecurity = True  ## 是否回補回報&註冊即時回報(證券)
        self.conn.AutoRecoverReport = True
        self.conn.AutoRecoverReportForeign = False
        self.conn.AutoRecoverReportSecurity = True

        # login
        logging.info("Login with {}".format(id_no))
        self.conn.LoginDirect(self.conn.ServerHost, UInt16(self.conn.ServerPort), "{},,{}".format(id_no, pwd))
        for i in range(100):
            if self.is_login:
                break
            time.sleep(0.1)

        if self.is_login:
            self.get_account_info()

        return True

    def get_account_info(self):
        header = ['分公司','帳號','帳號別','營業員代號','戶別','信用狀態','是否簽章','借券戶狀態','不使用','可否內部下單','可下單的內部IP','可當沖','觸價下單','IB代號','受任狀態']
        dictAccount = self.conn.GetAccountList()
        for identity in dictAccount.Values:
            logging.debug('身分證號:{}'.format(identity.ID))
            logging.debug('姓名:{}'.format(identity.Name))
            logging.debug('憑證到期日:{}'.format(identity.CA_YMD))
            logging.debug('帳號筆數:{}'.format(identity.Count))
            for package in identity.p001503_2:
                dictAccount = dict(zip(header, [package.BrokeId, package.Account, package.AccountFlag, package.AE, package.ACClass, package.AC_CREDITION, package.ISCASIGN, package.AC_SBL_STUS, package.Center, package.InternalOrder, package.InternalOrderIP, package.DayTrade, package.MIT, package.IB, package.AUTHORIZED]))
                dictAccount['戶別'] = {'1':'一般客戶','2':'行員','3':'優良員工'}[dictAccount['戶別']]
                dictAccount['可下單的內部IP'] = [ x for x in dictAccount['可下單的內部IP']]
                logging.debug(dictAccount)

    def receive_msg_handler(self, sender, package):
        logging.debug("[ReceiveMessage] {} {}".format(sender, package))
        
        if package.DT==DT.MESSAGE_MAP: # 1200 錯誤代碼訊息對應表
            logging.info("[ReceiveMessage]({0})：{1}".format(package.ToLog()))
        elif package.DT==DT.BROKER_MAP: # 1201 公司代碼與代號對照
            logging.info("[ReceiveMessage]({0})：{1}".format(package.ToLog()))
        elif package.DT==DT.LOGIN:    # 1503 登入
            if package.Code==0:
                logging.info("[ReceiveMessage]({0}) {1} 登入成功".format(package.DT, package.Code))
            else:
                logging.error("[ReceiveMessage]({0}) {1} 登入失敗 {2}".format(package.DT, package.Code, self.conn.GetMessageMap(package.Code)))
        elif package.DT==DT.AUTH_EXCHANGE:
            logging.info("[ReceiveMessage] {}".format(package.ToLog()))


        #region 公告 2014.12.12 ADD
        elif package.DT==DT.NOTICE_RPT: # P001701 公告(被動查詢)
            logging.info("[ReceiveMessage] 公告：{}".format(package.ToLog()))
        elif package.DT==DT.NOTICE: # P001702公告(主動)
            logging.info("[ReceiveMessage] 公告：{}".format(package.ToLog()))

    def get_status_handler(self, sender, status, msg):
        logging.debug("[GetStatus] {} {} {}.".format(sender, status, msg))

        if status==COM_STATUS.LOGIN_READY:
            logging.info("[GetStatus] 登入成功: {}".format(sender.Accounts))
            self.is_login = True
            self.Account =[acc.split(',') for acc in sender.Accounts.split('\r\n') if acc]
        elif status==COM_STATUS.ACCTCNT_NOMATCH:
            smsg = UTF8Encoding().GetString(msg)
            logging.info("[GetStatus] 部份帳號取得失敗: {}".format(smsg))
        elif status==COM_STATUS.LOGIN_FAIL: #登入失敗
            smsg = UTF8Encoding().GetString(msg)
            logging.info("[GetStatus] 登入失敗:[{0}]".format(smsg))
        elif status==COM_STATUS.LOGIN_UNKNOW:   # 登入狀態不明
            smsg = UTF8Encoding().GetString(msg)
            logging.warning("[GetStatus] 登入狀態不明:[{0}]".format(smsg))
        elif status==COM_STATUS.CONNECT_READY:  # 連線成功
            smsg = UTF8Encoding().GetString(msg)
            logging.info("[GetStatus] 伺服器 {}:{}\n伺服器回應: [{}]\n本身為{}部 IP:{}".format(sender.ServerHost, sender.ServerPort, smsg, "內" if sender.isInternal else "外", sender.MyIP))
        elif status==COM_STATUS.CONNECT_FAIL:   # 連線失敗
            smsg = UTF8Encoding().GetString(msg)
            logging.error("[GetStatus] 連線失敗: {} {}:{}".format(smsg, sender.ServerHost, sender.ServerPort))
        elif status==COM_STATUS.DISCONNECTED:   # 斷線
            smsg = UTF8Encoding().GetString(msg)
            logging.info("[GetStatus] 斷線: {}".format(smsg))
            self.is_login = False
        elif status==COM_STATUS.AS400_CONNECTED:
            smsg = UTF8Encoding().GetString(msg)
            logging.info("[GetStatus] AS400 連線成功: {}".format(smsg))
        elif status==COM_STATUS.AS400_CONNECTFAIL:
            smsg = UTF8Encoding().GetString(msg)
            logging.info("[GetStatus] AS400 連線失敗: {}".format(smsg))
        elif status==COM_STATUS.AS400_DISCONNECTED:
            smsg = UTF8Encoding().GetString(msg)
            logging.info("[GetStatus] AS400 連線斷線: {}".format(smsg))
        elif status==COM_STATUS.SUBSCRIBE:
            smsg = UTF8Encoding().GetString(msg)
            sender.WriterLog("msg=" + smsg)
            logging.info("[GetStatus] 註冊:[{0}]".format(smsg))
        elif status==COM_STATUS.UNSUBSCRIBE:
            smsg = UTF8Encoding().GetString(msg)
            logging.info("[GetStatus] 取消註冊:[{0}]".format(smsg))
        elif status==COM_STATUS.ACK_REQUESTID:  # 下單或改單第一次回覆
            request_id = BitConverter.ToInt64(msg, 0)
            ack_status = msg[8]
            logging.info("[GetStatus] 序號回覆: {} 狀態={}.".format(request_id, "成功" if ack_status==1 else "失敗"))

    def receive_time_handler(self, sender, server_time, conn_quality):
        # conn_quality : 本次與上次 HeatBeat 之時間差(milliseconds)
        logging.info("[ReceiveServerTime] {0:hh:mm:ss.fff}, time_diff={} ms.".format(server_time, conn_quality))
        
    def recover_status_handler(self, sender, topic, status, recover_count):
        logging.debug("[RecoverStatus] {} {} {} {}.".format(sender, topic, status, recover_count))
        
        if status==RECOVER_STATUS.RS_DONE:  #回補資料結束
            logging.info("[RecoverStatus] 結束回補 Topic:[{0} 筆數:{1}]".format(topic, recover_count))
        elif status==RECOVER_STATUS.RS_BEGIN:   #開始回補資料
            logging.info("[RecoverStatus] 開始回補 Topic:[{0}]".format(topic))

    def __del__(self):
        self.conn.Logout()
        logging.debug('[Logout] Success.')


