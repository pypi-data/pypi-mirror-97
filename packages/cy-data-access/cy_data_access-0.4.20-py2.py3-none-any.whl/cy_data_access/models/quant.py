from ..connection.connect import *
from pymodm import fields, MongoModel


class BrickCarrierCfg(MongoModel):
    """搬砖人配置"""
    identifier = fields.IntegerField(primary_key=True)
    ccxt_cfg_id = fields.IntegerField()  # CCXT 配置 ID
    class_name = fields.CharField()  # 对应 BC 类的类名
    strategies = fields.ListField()  # 策略 ID 数组
    desc = fields.CharField()

    class Meta:
        connection_alias = DB_QUANT
        collection_name = CN_BRICK_CARRIER


class StrategyCfg(MongoModel):
    """策略配置"""
    identifier = fields.IntegerField(primary_key=True)
    coin_pair = fields.CharField()
    leverage = fields.FloatField()
    strategy_name = fields.CharField()
    parameters = fields.ListField()
    time_interval = fields.CharField()
    stop = fields.BooleanField()

    class Meta:
        connection_alias = DB_QUANT
        collection_name = CN_STRATEGY


class StrategyOrder(MongoModel):
    """策略订单"""
    strategy_id = fields.IntegerField()
    order_id = fields.IntegerField()
    order_desc = fields.DictField()
    date = fields.DateTimeField()

    class Meta:
        connection_alias = DB_QUANT
        collection_name = CN_STRATEGY_ORDER

    @classmethod
    def order_with(cls, strategy_id, order_id):
        try:
            return cls.objects.get({'strategy_id': strategy_id, 'order_id': order_id})
        except Exception:
            order = StrategyOrder()
            order.strategy_id = strategy_id
            order.order_id = order_id
            return order
