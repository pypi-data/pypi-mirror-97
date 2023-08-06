# -*- coding: utf-8 -*-
import os, sys, json
import time
import logging
import hashlib
import clr
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


class CommonAPI():

    def __init__(self, debug=False):
        self.RecoverMap = {}

        if debug:
            self.ServerHost = "iquotetest.kgi.com.tw"
            self.ServerPort = 8000
        else:
            self.ServerHost = "quoteapi.kgi.com.tw"
            self.ServerPort = 443

        self.conn = QuoteCom(self.ServerHost, self.ServerPort, 'API', 'b6eb')
        self.is_login = False
        
        # register event handler
        self.conn.OnRcvMessage += self.receive_msg_handler   #資料接收事件
        self.conn.OnGetStatus += self.get_status_handler            #狀態通知事件
        self.conn.OnRecoverStatus += self.recover_status_handler    #回補狀態通知

    # 登入
    def login(self, id_no, pwd):
        self.is_login = False

        # login
        logging.info("Login with {}".format(id_no))
        self.conn.Connect2Quote(self.ServerHost, self.ServerPort, id_no, pwd, ' ', "")
        # self.conn.ShowLogin()
        for i in range(100):
            if self.is_login:
                break
            time.sleep(0.1)

        return True
    
    def get_status_handler(self, sender, status, msg):
        logging.debug("[GetStatus] {} {} {}.".format(sender, status, msg))

        if status==COM_STATUS.LOGIN_READY:
            logging.info("[GetStatus] 登入成功: {}".format(sender.Accounts))
            self.is_login = True
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
            logging.info("[GetStatus] QuoteCom: {}, IP={}".format(smsg, self.conn.MyIP))
        elif status==COM_STATUS.CONNECT_FAIL:   # 連線失敗
            smsg = UTF8Encoding().GetString(msg)
            logging.error("[GetStatus] 連線失敗: {} {}:{}".format(smsg, sender.ServerHost, sender.ServerPort))
        elif status==COM_STATUS.DISCONNECTED:   # 斷線
            smsg = UTF8Encoding().GetString(msg)
            logging.info("[GetStatus] 斷線: {}".format(smsg))
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
            logging.info("[GetStatus] 註冊:[{0}]".format(smsg))
        elif status==COM_STATUS.UNSUBSCRIBE:
            smsg = UTF8Encoding().GetString(msg)
            logging.info("[GetStatus] 取消註冊:[{0}]".format(smsg))
        elif status==COM_STATUS.ACK_REQUESTID:  # 下單或改單第一次回覆
            request_id = BitConverter.ToInt64(msg, 0)
            ack_status = msg[8]
            logging.info("[GetStatus] 序號回覆: {} 狀態={}.".format(request_id, "收單" if ack_status==1 else "失敗"))
        elif status==COM_STATUS.RECOVER_DATA:
            smsg = UTF8Encoding().GetString(msg[1:])
            if (msg[0] == 0):
                self.RecoverMap[smsg] = 0
                logging.info("開始回補 Topic:[{0}]".format(smsg))
            elif (msg[0] == 1):
                logging.info("結束回補 Topic:[{0} 筆數:{1}]".format(smsg, self.RecoverMap[smsg]))

    def recover_status_handler(self, sender, topic, status, recover_count):
        logging.debug("[RecoverStatus] {} {} {} {}.".format(sender, topic, status, recover_count))
        
        if status==RECOVER_STATUS.RS_DONE:  #回補資料結束
            logging.info("[RecoverStatus] 結束回補 Topic:[{0} 筆數:{1}]".format(topic, recover_count))
        elif status==RECOVER_STATUS.RS_BEGIN:   #開始回補資料
            logging.info("[RecoverStatus] 開始回補 Topic:[{0}]".format(topic))
        elif status==RECOVER_STATUS.RS_NOAUTHRITY:
            logging.info("無回補權限 Topic:[{0}]".format(Topic))

    def __del__(self):
        self.conn.Logout()
        logging.debug('[Logout] Success.')


