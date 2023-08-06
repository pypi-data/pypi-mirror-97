
from enum import Enum
from Intelligence import Security_OrdType, Security_Lot, Security_Class, Security_PriceFlag, SIDE_FLAG, TIME_IN_FORCE
from Intelligence import DT, MARKET_FLAG, SIDE_FLAG, TIME_IN_FORCE, PRICE_FLAG, POSITION_EFFECT, OFFICE_FLAG, ORDER_TYPE, ORDER_KIND

# 委託種類
class SecurityAction(Enum):
    NEW_ORDER = Security_OrdType.OT_NEW  # 新單
    CANCEL_ORDER = Security_OrdType.OT_CANCEL    # 刪單
    MODIFY_QUANTITY = Security_OrdType.OT_MODIFY_QTY   # 改量
    MODIFY_PRICE = Security_OrdType.OT_MODIFY_PRICE    # 改價

class Action(Enum):
    NEW_ORDER = ORDER_TYPE.OT_NEW
    CANCEL_ORDER = ORDER_TYPE.OT_CANCEL
    MODIFY = ORDER_TYPE.OT_MODIFY
    MODIFY_QUANTITY = ORDER_TYPE.OT_MODIFY_QTY
    MODIFY_PRICE = ORDER_TYPE.OT_MODIFY_PRICE

# 交易別
class LotType(Enum):
    ROUND_LOT = Security_Lot.Even_Lot  # 整股
    BLOCK_LOT = Security_Lot.Block_Trade  # 鉅額
    ODD_LOT = Security_Lot.Odd_Lot      # 零股
    FIX_PRICE = Security_Lot.Fixed_Price    # 定價
    ODD_LOT_INTRA = Security_Lot.Odd_InTraday    # 2020.8.11 Lynn Add : 盤中零股

# 委託別
class OrderType(Enum):
    ORDINARY = Security_Class.SC_Ordinary   # 0 現股
    MARGIN  = Security_Class.SC_SelfMargin  # 3 融資
    SHORT   = Security_Class.SC_SelfShort   # 4 融券
    SHORT_LIMIT = Security_Class.SC_ShortLimit    # 5 借券賣出 2020.3.10 Lynn Add 5, 6
    SHORT_UNLIMIT = Security_Class.SC_ShortUnLimit  # 6 借券賣出(盤下限制豁免)
    DAY_MARGIN = Security_Class.SC_DayMargin  # 7 當沖融資
    DAY_SHORT = Security_Class.SC_DayShort   # 8 當沖融券
    DAY_TRADE = Security_Class.SC_DayTrade   # 9 現先賣

# 買賣別
class Side(Enum):
    # 2019.1.2 Add: 國內複式單以 第二支腳為主
    BUY = SIDE_FLAG.SF_BUY  # 買進
    SELL = SIDE_FLAG.SF_SELL    # 賣出

# 價格註記(委託方式)
class SecurityPriceFlag(Enum):
    FIX = Security_PriceFlag.SP_FixedPrice  # 0 限價
    MARKET  = Security_PriceFlag.SP_MarketPrice  # 2 市價
    LIMIT_UP = Security_PriceFlag.SP_RiseStopPrice    # 9 漲停
    LIMIT_DOWN  = Security_PriceFlag.SP_FallStopPrice   # 1 跌停
    UNCHANGED   = Security_PriceFlag.SP_UnchangePrice    # 5 平盤

class PriceFlag(Enum):
    LIMIT = PRICE_FLAG.PF_SPECIFIED # 限價
    MARKET = PRICE_FLAG.PF_MARKET   # 市價
    STOP_MARKET = PRICE_FLAG.PF_STOP_MARKET # 停損市價
    STOP_SPECIFIED = PRICE_FLAG.PF_STOP_SPECIFIED   # # 停損限價
    MARKET_RANGE = PRICE_FLAG.PF_MARKET_RANGE   # 2014.4.2 ADD 一定範圍市價單

# 委託條件
class TimeInForce(Enum):
    ROD = TIME_IN_FORCE.TIF_ROD # 當盤有效
    IOC = TIME_IN_FORCE.TIF_IOC # 立即成交其餘刪除
    FOK = TIME_IN_FORCE.TIF_FOK # 全部立即成交否則刪除


class Market(Enum):
    FUTURES = MARKET_FLAG.MF_FUT
    OPTION = MARKET_FLAG.MF_OPT

class WriteOff(Enum):
    OPEN = POSITION_EFFECT.PE_OPEN  # 新倉
    CLOSE = POSITION_EFFECT.PE_CLOSE # 平倉
    DAY_TRADE = POSITION_EFFECT.PE_DAY_TRADE # 當沖
    AUTO = POSITION_EFFECT.PE_AUTO  # 自動

