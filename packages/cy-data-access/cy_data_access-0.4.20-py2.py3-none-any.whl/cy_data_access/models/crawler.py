from ..connection.connect import *
from pymodm import fields, MongoModel


class CrawlerRealtimeConfig(MongoModel):
    """ 实时抓取的配置 """

    exchange_type = fields.CharField()
    coin_pair = fields.CharField()
    time_frame = fields.CharField()
    active = fields.BooleanField(default=True)

    class Meta:
        connection_alias = DB_CRAWLER
        collection_name = CN_REALTIME_CRAWLER_CFG
