from pymodm import MongoModel, fields
from bson.codec_options import CodecOptions
from ..connection.connect import *


class BacktestOverview(MongoModel):
    """所有回测的结果概览"""

    # 一次回测的整体统一标识
    task_identifier = fields.CharField()
    # 策略标识 「Bolling|m:20;n:2;5T|20200202,20201022」
    param_identifier = fields.CharField()
    equity_curve = fields.FloatField()
    statics_info = fields.OrderedDictField()

    def signal_collection_name(self):
        """策略对应信号数据表名"""
        return "{}_{}".format(self.task_identifier, self.param_identifier)

    class Meta:
        connection_alias = DB_BACKTEST
        codec_options = CodecOptions(tz_aware=True)
        collection_name = CN_BACKTEST_OVERVIEW


class BacktestSignalResult(MongoModel):
    """OHLCV + signal + pos"""

    candle_begin_time = fields.DateTimeField(primary_key=True)
    open_price = fields.Decimal128Field(mongo_name='open')
    high_price = fields.Decimal128Field(mongo_name='high')
    low_price = fields.Decimal128Field(mongo_name='low')
    close_price = fields.Decimal128Field(mongo_name='close')
    volume = fields.Decimal128Field()
    signal = fields.FloatField()
    pos = fields.FloatField()

    class Meta:
        connection_alias = DB_BACKTEST_SIGNAL
        codec_options = CodecOptions(tz_aware=True)

    @classmethod
    def bulk_upsert_records(cls, json_list, key_name='_id'):
        """Bulk upsert candle records"""
        coll = cls._mongometa.collection
        bulkOp = coll.initialize_unordered_bulk_op()
        for doc in json_list:
            if isinstance(key_name, list):
                filter_dict = dict(map(lambda k: (k, doc[k]), key_name))
            else:
                filter_dict = {key_name: doc[key_name]}
            doc['_cls'] = cls.__module__ + '.' + cls.__name__
            bulkOp.find(filter_dict).upsert().update({'$set': doc})
        results = bulkOp.execute()
        return results


def backtest_signal_candle_class(collection_name) -> BacktestSignalResult:
    assert collection_name is not None and isinstance(collection_name, str)
    _cls = type(collection_name, BacktestSignalResult.__bases__, dict(BacktestSignalResult.__dict__))
    _cls._mongometa.collection_name = collection_name
    return _cls
