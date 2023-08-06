from pymodm import MongoModel, fields
from bson.codec_options import CodecOptions
from ..connection.connect import *


class CandleRecord(MongoModel):
    """OHLCV"""

    candle_begin_time = fields.DateTimeField(primary_key=True)
    open_price = fields.Decimal128Field(mongo_name='open')
    high_price = fields.Decimal128Field(mongo_name='high')
    low_price = fields.Decimal128Field(mongo_name='low')
    close_price = fields.Decimal128Field(mongo_name='close')
    volume = fields.Decimal128Field()
    quote_volume = fields.Decimal128Field()
    trade_num = fields.Decimal128Field()
    taker_buy_base_asset_volume = fields.Decimal128Field()
    taker_buy_quote_asset_volume = fields.Decimal128Field()

    class Meta:
        connection_alias = DB_MARKET
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


def candle_record_class_with_components(exchange_name, coin_pair, time_frame, coin_tail=''):
    """Convenience"""
    return candle_record_class('{}_{}{}_{}'.format(exchange_name.lower(), coin_pair.formatted('_').lower(), coin_tail, time_frame.value.lower()))


def candle_record_class_with_str_components(exchange_name, symbol, time_frame_str, market_type):
    """Convenience"""
    return candle_record_class('{}_{}_{}_{}'.format(exchange_name, symbol, time_frame_str, market_type).lower())


def candle_record_class(collection_name) -> CandleRecord:
    """Define a record class with a specify collection name"""
    assert collection_name is not None and isinstance(collection_name, str)
    class_name = collection_name + "_candle"
    _cls = type(class_name, CandleRecord.__bases__, dict(CandleRecord.__dict__))
    _cls._mongometa.collection_name = collection_name
    return _cls


class NeutralPanelCandleRecord(MongoModel):
    """中性策略原始数据"""

    candle_begin_time = fields.DateTimeField()
    symbol = fields.CharField()
    open = fields.FloatField()
    high = fields.FloatField()
    low = fields.FloatField()
    close = fields.FloatField()
    volume = fields.FloatField()
    quote_volume = fields.FloatField()
    trade_num = fields.FloatField()
    taker_buy_base_asset_volume = fields.FloatField()
    taker_buy_quote_asset_volume = fields.FloatField()
    avg_price = fields.FloatField()

    class Meta:
        connection_alias = DB_MARKET
        collection_name = CN_NEUTRAL_PANEL
        codec_options = CodecOptions(tz_aware=True)

    @classmethod
    def bulk_insert_records(cls, json_list):
        """批量插入"""
        def map_func(rec):
            ins = NeutralPanelCandleRecord()
            for key in rec:
                setattr(ins, key, rec[key])
            return ins
        inses = list(map(map_func, list(json_list)))
        NeutralPanelCandleRecord.objects.bulk_create(inses)
