import os
from pymodm.connection import connect
from pymongo import MongoClient

# ==== Configuration ====

DB_CONFIG = 'cfg'

CN_SEQUENCE = 'sequence'
CN_CCXT_CONFIG = 'cxt'

# ==== User ====

DB_USER = 'user'

CN_USER_AUTH = 'auth'
CN_USER_INFO = 'info'

# ==== Market ====

DB_MARKET = 'market'

CN_NEUTRAL_PANEL = 'neutral_candle_data'

# ==== Strategy ====

DB_QUANT = 'quant'

CN_STRATEGY = 'strategy'  # 交易策略
CN_BRICK_CARRIER = 'brick_carrier'  # 搬砖器配置
CN_STRATEGY_ORDER = 's_order'  # 策略订单

# ==== Position ====

DB_POSITION = 'position'

CN_AIMS_POS = 'aims'
CN_AIMS_POS_CLOSE = 'aims_close'

CN_AIP_RECORDS = 'aip_record'

CN_STRATEGY_POS = 'strategy_position '

CN_NEUTRAL_SELECTION = 'neutral_selection'

# ==== Backtest ====

DB_BACKTEST = 'backtest'
DB_BACKTEST_SIGNAL = 'bt_signals'

CN_BACKTEST_OVERVIEW = 'overview'

# ==== Log ====

DB_LOG = 'log'

CN_COMMON_LOG = 'common'

# ==== Financial ====

DB_FINANCIAL = 'financial'

CN_FIN_HOLDER = 'holder'
CN_FIN_RECORD = 'op_record'
CN_FIN_EVENT = 'event'

# ==== Crawler ====

DB_CRAWLER = 'crawler'

CN_REALTIME_CRAWLER_CFG = 'realtime_cfg'
CN_FULL_CRAWLER_CFG = 'full_cfg'


def connect_db(user, password, host='127.0.0.1:27017', db_name=None):
    # 连接到数据库
    uri = "mongodb://{}:{}@{}/{}?authSource=admin".format(user, password, host, db_name)
    connect(uri, db_name)


def connect_db_env(db_name=None):
    connect_db(os.environ['DB_MNR_USER'], os.environ['DB_MNR_PWD'], os.environ['DB_HOST'], db_name)


def connect_db_client_by_env():
    uri = "mongodb://{}:{}@{}/?authSource=admin".format(os.environ['DB_MNR_USER'], os.environ['DB_MNR_PWD'], os.environ['DB_HOST'])
    client = MongoClient(uri)
    return client


def connect_db_and_save_json_list(db_name, collection_name, json_list, drop=True):
    client = connect_db_client_by_env()
    db = client[db_name]
    if drop:
        db.drop_collection(collection_name)
    collection = db[collection_name]
    collection.insert_many(json_list)


def connect_db_and_read_df(db_name, collection_name, find_qeury={}, projection={"_id": 0}):
    client = connect_db_client_by_env()
    db = client[db_name]
    collection = db[collection_name]
    return collection.find(find_qeury, projection)
