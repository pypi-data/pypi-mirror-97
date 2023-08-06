import click as c
import pandas as pd
import pytz
from datetime import datetime
from .connection.connect import *
from .models.config import *
from .models.position import *
from .models.financial import *
from .models.crawler import *
from .models.quant import *


@c.group()
@c.option('--db-user', envvar='DB_CLI_USER', required=True)
@c.option('--db-pwd', envvar='DB_CLI_PWD', required=True)
@c.option('--db-host', envvar='DB_HOST', required=True)
@c.pass_context
def cydb(ctx, db_user, db_pwd, db_host):
    ctx.ensure_object(dict)
    ctx.obj['db_u'] = db_user
    ctx.obj['db_p'] = db_pwd
    ctx.obj['db_h'] = db_host


@cydb.command()
@c.option('--key', type=str, prompt=True, required=True)
@c.option('--secret', type=str, prompt=True, required=True)
@c.password_option(confirmation_prompt=False, required=False)
@c.option('--type',
          type=c.Choice(['okex', 'hbp', 'binance'], case_sensitive=False), prompt=True)
@c.option('--desc', type=str, prompt=True, required=False)
@c.pass_context
def add_ccxt_config(ctx, key, secret, password, type, desc):
    """添加 ccxt 配置"""
    # connect db
    connect_db(ctx.obj['db_u'], ctx.obj['db_p'], ctx.obj['db_h'], DB_CONFIG)
    # save config
    e_type = 0
    if type == 'hbp':
        e_type = CCXTExchangeType.HuobiPro
    elif type == 'okex':
        e_type = CCXTExchangeType.OKEx
    elif type == 'binance':
        e_type = CCXTExchangeType.Binance
    result = CCXTConfiguration(identifier=Sequence.fetch_next_id(CN_CCXT_CONFIG),
                               app_key=key,
                               app_secret=secret,
                               app_pw=password,
                               e_type=e_type,
                               desc=desc).save()
    c.echo('Result: {}(id: {})'.format(result, result.identifier))


@cydb.command()
@c.pass_context
def aims_profit(ctx):
    """AMIS 收益"""
    pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
    # connect db
    connect_db(ctx.obj['db_u'], ctx.obj['db_p'], ctx.obj['db_h'], DB_POSITION)
    connect_db_env(db_name=DB_POSITION)
    selling = list(AIMSPositionSelling.objects.values())
    df = pd.DataFrame(selling)
    df.drop(['_cls', '_id'], axis=1, inplace=True)
    print("""
    {}
    sum: {}
    """.format(df, df['profit_amount'].sum()))


@cydb.command()
@c.pass_context
def aims_position(ctx):
    """AMIS 仓位"""
    pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
    # connect db
    connect_db(ctx.obj['db_u'], ctx.obj['db_p'], ctx.obj['db_h'], DB_POSITION)
    connect_db_env(db_name=DB_POSITION)
    selling = list(AIMSPosition.objects.aggregate({
        '$addFields': {
            'average_costing':
            {
                '$cond': {
                    'if': {'$gt': ['$hold', 0]},
                    'then': {'$divide': ['$cost', '$hold']},
                    'else': 0
                }
            }
        }
    }))
    df = pd.DataFrame(selling)
    df.drop(['_cls', '_id'], axis=1, inplace=True)
    print(df)


@cydb.command()
@c.option('--exchange', type=str, prompt=True, required=True)
@c.option('--coin_pair', type=str, prompt=True, required=True)
@c.option('--cost', type=float, prompt=True, required=True)
@c.option('--amount', type=float, prompt=True, required=True)
@c.pass_context
def add_aip_record(ctx, exchange, coin_pair, cost, amount):
    """添加定投记录"""
    connect_db(ctx.obj['db_u'], ctx.obj['db_p'], ctx.obj['db_h'], DB_POSITION)
    record = AIPRecord()
    record.exchange = exchange
    record.coin_pair = coin_pair.upper()
    record.cost = cost
    record.amount = amount
    record.date = datetime.now()
    record.save()


@cydb.command()
@c.option('--exchange_type', type=c.Choice(["1", "2", "3"]), prompt='抓取类型：[1. 币安合约; 2. OK合约, 3. 币安永续 USDT]', default="1")
@c.option('--coin_pair', type=str, prompt='币对: [币安合约: BTCUSD_201225, OK合约：BTC-USD-201225, 币安永续USDT：随便]', required=True)
@c.option('--time_frame', type=str, prompt='K线间隔：5m, 15m ...', required=True)
@c.pass_context
def add_crawler_config(ctx, exchange_type, coin_pair, time_frame):
    """添加抓K线配置"""
    connect_db(ctx.obj['db_u'], ctx.obj['db_p'], ctx.obj['db_h'], DB_CRAWLER)
    crawler = CrawlerRealtimeConfig()
    if int(exchange_type) == 1:
        crawler.exchange_type = "binance_delivery"
    elif int(exchange_type) == 2:
        crawler.exchange_type = "ok_contract"
    elif int(exchange_type) == 3:
        crawler.exchange_type = 'binance_future'
    crawler.coin_pair = coin_pair
    crawler.time_frame = time_frame
    crawler.save()


@cydb.command()
@c.option('--exchange_type', type=c.Choice(["1", "2", "3"]), prompt='调整类型：[1. 币安合约; 2. OK合约, 3. 币安永续 USDT]', default="1")
@c.option('--type', type=c.Choice(['duplicate', 'delete']), prompt=True, required=True)
@c.option('--from_tail', type=str, prompt=True, required=True)
@c.option('--to_tail', type=str, prompt=True, required=True)
@c.pass_context
def batch_update_crawler_config(ctx, type, exchange_type, from_tail, to_tail):
    """复制抓K线配置"""
    connect_db(ctx.obj['db_u'], ctx.obj['db_p'], ctx.obj['db_h'], DB_CRAWLER)
    __all_crawler_cfgs()
    exchange_type_str = ""
    if int(exchange_type) == 1:
        exchange_type_str = "binance_delivery"
    elif int(exchange_type) == 2:
        exchange_type_str = "ok_contract"
    elif int(exchange_type) == 3:
        exchange_type_str = 'binance_future'
    crawlers = list(CrawlerRealtimeConfig.objects.raw({
        'coin_pair': {"$regex": from_tail, "$options": '-i'},
        'exchange_type': exchange_type_str,
        'active': True
    }))
    if type == 'duplicate':
        for crawler in crawlers:
            n_c = CrawlerRealtimeConfig()
            n_c.active = crawler.active
            n_c.time_frame = crawler.time_frame
            n_c.coin_pair = crawler.coin_pair.replace(from_tail.upper(), to_tail.upper())
            n_c.exchange_type = exchange_type_str
            n_c.save()
    else:
        for crawler in crawlers:
            crawler.delete()
    print('after:')
    __all_crawler_cfgs()


def __all_crawler_cfgs():
    crawlers = list(CrawlerRealtimeConfig.objects.order_by([('active', 1)]))
    print('Index\tEXG_TYPE\tCOIN\tTIME_FRAME\tACTIVE')
    for index, cc in enumerate(crawlers):
        print('{}\t{}\t{}\t{}\t{}'.format(index, cc.exchange_type, cc.coin_pair, cc.time_frame, cc.active))


@cydb.command()
@c.pass_context
def crawler_configs(ctx):
    """所有抓K线配置"""
    connect_db_env(db_name=DB_CRAWLER)
    __all_crawler_cfgs()


@cydb.command()
@c.option('--type', type=c.Choice(['active', 'deactive', 'delete']), prompt=True, required=True)
@c.pass_context
def edit_crawler_configs(ctx, type):
    '''调整抓取配置'''
    connect_db_env(db_name=DB_CRAWLER)
    __all_crawler_cfgs()
    crawlers = list(CrawlerRealtimeConfig.objects)
    while True:
        index_strs = c.prompt("选择要{}的 Index (多个用','隔开)".format('停止' if type == 'deactive' else '恢复' if type == 'deactive' else '删除'))
        try:
            indexes = index_strs.split(',')
        except Exception as _:
            indexes = [indexes]

        indexes = list(map(lambda x: int(x), indexes))

        for index in indexes:
            if index < 0 or index >= len(crawlers):
                print('index {} out of range.'.format(index))
                return
        break

    for index in indexes:
        cc = crawlers[index]
        if type == 'delete':
            cc.delete()
        else:
            cc.active = type == 'active'
            cc.save()
    __all_crawler_cfgs()


def __all_strategies():
    strategies = list(StrategyCfg.objects)
    print("ID\tNAME\tCOIN_PAIR\tTIME_INTERVAL\tLEVERAGE\tPARAMS\tSTOP")
    for s in strategies:
        print("{}\t{}\t{}\t{}\t{}\t{}\t{}".format(s.identifier, s.strategy_name, s.coin_pair, s.time_interval, s.leverage, s.parameters, s.stop))


@cydb.command()
@c.option('--name', type=str, prompt=True, required=True)
@c.option('--coin_pair', type=str, prompt=True, required=True)
@c.option('--leverage', type=float, prompt=True, required=True)
@c.option('--time_interval', type=str, prompt='TimeInterval(5m/15m/1h...)', required=True)
@c.option('--parameters', type=str, prompt='Parameters(2.2,3.0,123...)', required=True)
@c.pass_context
def add_strategy(ctx, name, coin_pair, leverage, time_interval, parameters):
    """添加策略配置"""
    connect_db_env(db_name=DB_CONFIG)
    connect_db_env(db_name=DB_QUANT)
    strategy = StrategyCfg()
    strategy.identifier = Sequence.fetch_next_id(CN_STRATEGY)
    strategy.strategy_name = name
    strategy.coin_pair = coin_pair
    strategy.time_interval = time_interval
    strategy.leverage = leverage

    splitted = parameters.split(',')
    formatted = map(lambda x: float(x), splitted)
    strategy.parameters = list(formatted)
    strategy.save()
    __all_strategies()


@cydb.command()
@c.option('--type', type=c.Choice(['stop', 'resume', 'delete']), prompt=True, required=True)
@c.pass_context
def edit_strategy(ctx, type):
    """调整策略开关"""
    connect_db_env(db_name=DB_CONFIG)
    connect_db_env(db_name=DB_QUANT)

    __all_strategies()

    strategies = list(StrategyCfg.objects)
    while True:
        strategy_id_str = c.prompt("选择要{}策略 ID (多个用','隔开)".format('停止' if type == 'stop' else '恢复' if type == 'resume' else '删除'))
        try:
            strategy_ids = strategy_id_str.split(',')
        except Exception as _:
            strategy_ids = [strategy_id_str]

        strategy_ids = list(map(lambda x: int(x), strategy_ids))
        for id in strategy_ids:
            if id not in list(map(lambda x: x.identifier, strategies)):
                print('strategy id {} not exist.'.format(id))
                return
        break
    for id in strategy_ids:
        s = StrategyCfg.objects.get({'_id': id})
        if type == 'delete':
            s.delete()
        else:
            s.stop = type == 'stop'
            s.save()
    __all_strategies()


@cydb.command()
@c.option('--from_tail', type=str, prompt=True, required=True)
@c.option('--to_tail', type=str, prompt=True, required=True)
@c.pass_context
def update_strategy_coin_pair(ctx, from_tail, to_tail):
    """调整策略开关"""
    connect_db_env(db_name=DB_CONFIG)
    connect_db_env(db_name=DB_QUANT)

    __all_strategies()

    strategies = list(StrategyCfg.objects.raw({
        'coin_pair': {"$regex": from_tail, "$options": '-i'},
    }))
    for st in strategies:
        st.coin_pair = st.coin_pair.replace(from_tail.upper(), to_tail.lower())
        st.save()
    print('after')
    __all_strategies()


@cydb.command()
@c.pass_context
def strategies(ctx):
    """所有策略"""
    connect_db_env(db_name=DB_QUANT)
    __all_strategies()


@cydb.command()
@c.option('--class_name', type=str, prompt=True, required=True)
@c.option('--desc', type=str, prompt=True, required=True)
@c.pass_context
def add_carrier_cfg(ctx, class_name, desc):
    """添加搬砖人配置"""
    connect_db_env(db_name=DB_QUANT)
    connect_db_env(db_name=DB_CONFIG)

    bc_config = BrickCarrierCfg()
    bc_config.class_name = class_name
    bc_config.desc = desc

    ccxt_cfgs = list(CCXTConfiguration.objects)
    for cfg in ccxt_cfgs:
        print("{}\t{}...\t{}\t{}".format(cfg.identifier, cfg.app_key[:5], CCXTExchangeType(cfg.e_type).__str__(), cfg.desc))
    while True:
        ccxt_cfg_id = c.prompt('使用的 ccxt 配置 ID', type=int)
        if ccxt_cfg_id not in list(map(lambda x: x.identifier, ccxt_cfgs)):
            print('ccxt config not exist.')
            continue
        break
    bc_config.ccxt_cfg_id = ccxt_cfg_id

    strategies = list(StrategyCfg.objects)
    for s in strategies:
        print("{}\t{}\t{}\t{}\t{}".format(s.identifier, s.coin_pair, s.time_interval, s.leverage, s.parameters))
    while True:
        strategy_id_str = c.prompt("选择策略 ID (多个用','隔开)")
        try:
            strategy_ids = strategy_id_str.split(',')
        except Exception as _:
            strategy_ids = [strategy_id_str]
        # to float
        strategy_ids = list(map(lambda x: int(x), strategy_ids))

        can_go_on = True
        for id in strategy_ids:
            if id not in list(map(lambda x: x.identifier, strategies)):
                print('strategy id {} not exist.'.format(id))
                can_go_on = False
                break
        if can_go_on:
            break

    bc_config.strategies = strategy_ids
    bc_config.identifier = Sequence.fetch_next_id(CN_BRICK_CARRIER)
    bc_config.save()


@cydb.command()
@c.option('--type', type=c.Choice(['add', 'delete']), prompt=True, required=True)
@c.pass_context
def carrier_edit_strategy(ctx, type):
    """搬砖人添加/删除策略"""
    connect_db_env(db_name=DB_QUANT)
    connect_db_env(db_name=DB_CONFIG)

    cfgs = list(BrickCarrierCfg.objects)
    print("ID\tCCXT\tNAME\tSTRAs\tDESC")
    for s in cfgs:
        print("{}\t{}\t{}\t{}\t{}".format(s.identifier, s.ccxt_cfg_id, s.class_name, s.strategies, s.desc))
    while True:
        bc_cfg_id = c.prompt("选择搬砖人", type=int)
        try:
            bc_cfg = BrickCarrierCfg.objects.get({'_id': bc_cfg_id})
            print("{}\t{}\t{}\t{}\t{}".format(bc_cfg.identifier, bc_cfg.ccxt_cfg_id, bc_cfg.class_name, bc_cfg.strategies, bc_cfg.desc))
            break
        except Exception as _:
            print(bc_cfg_id, "不存在")
            continue

    strategies = list(StrategyCfg.objects)
    print('-' * 15)
    print('策略们:')
    for s in strategies:
        print("{}\t{}\t{}\t{}\t{}".format(s.identifier, s.coin_pair, s.time_interval, s.leverage, s.parameters))
    while True:
        strategy_id_str = c.prompt("选择策略 ID (多个用','隔开)")
        try:
            strategy_ids = strategy_id_str.split(',')
        except Exception as _:
            strategy_ids = [strategy_id_str]

        strategy_ids = list(map(lambda x: int(x), strategy_ids))
        for id in strategy_ids:
            if id not in list(map(lambda x: x.identifier, strategies)):
                print('strategy id {} not exist.'.format(id))
                return
        break

    if type == 'add':
        bc_cfg.strategies = list(set(bc_cfg.strategies + strategy_ids))
    else:
        bc_cfg.strategies = [x for x in bc_cfg.strategies if x not in strategy_ids]
    # remove invalid strategies
    bc_cfg.strategies = [x for x in bc_cfg.strategies if x in [y.identifier for y in strategies]]
    bc_cfg.save()
    print('添加完成:' if type == 'add' else '删除完成')
    print("{}\t{}\t{}\t{}\t{}".format(bc_cfg.identifier, bc_cfg.ccxt_cfg_id, bc_cfg.class_name, bc_cfg.strategies, bc_cfg.desc))


@cydb.command()
@c.pass_context
def brick_carriers(ctx):
    """搬砖人配置"""
    connect_db_env(db_name=DB_QUANT)
    cfgs = list(BrickCarrierCfg.objects)
    print("ID\tCCXT\tNAME\tSTRAs\tDESC")
    for s in cfgs:
        print("{}\t{}\t{}\t{}\t{}".format(s.identifier, s.ccxt_cfg_id, s.class_name, s.strategies, s.desc))


@cydb.command()
@c.option('--cp', required=False, default=None)
@c.pass_context
def strategy_orders(ctx, cp):
    """策略订单信息"""
    connect_db_env(db_name=DB_QUANT)
    pipeline = [{
        "$lookup": {
            "from": "strategy",
            "localField": "strategy_id",
            "foreignField": "_id",
            "as": "strategy"
        },
    }, {
        "$unwind": {
            "path": "$strategy",
            "preserveNullAndEmptyArrays": True
        }
    }]
    for s in list(StrategyOrder.objects.aggregate(*pipeline)):
        if cp is None or cp in s['strategy']['coin_pair']:
            print(s['order_id'], "{}({})".format(s['strategy']['strategy_name'], s['strategy']['coin_pair']))
            desc = s['order_desc']
            for (i, k) in enumerate(desc):
                print("{}: {}".format(k, desc[k]))

# ===================== Financial ============================


@ c.group()
@ c.option('--db-user', envvar='DB_CLI_USER', required=True)
@ c.option('--db-pwd', envvar='DB_CLI_PWD', required=True)
@ c.option('--db-host', envvar='DB_HOST', required=True)
@ c.pass_context
def cyfin(ctx, db_user, db_pwd, db_host):
    ctx.ensure_object(dict)
    ctx.obj['db_u'] = db_user
    ctx.obj['db_p'] = db_pwd
    ctx.obj['db_h'] = db_host
    connect_db(ctx.obj['db_u'], ctx.obj['db_p'], ctx.obj['db_h'], DB_FINANCIAL)
    print("Current holders:")
    for holder in list(Holder.objects.project({'id': 1, "name": 1, 'balance': 1, 'update_date': 1, 'status': 1}).values()):
        print("{}:\t{}\t{}\t{}\t{}".format(holder['_id'], holder['name'], holder['balance'], holder['status'], holder['update_date']))
    print()


@ cyfin.command()
@ c.option('--name', type=str, prompt=True, required=True)
@ c.option('--balance', type=float, prompt=True, default=0, required=True)
@ c.option('--level',
           type=c.Choice(['SSR', 'SUPER', 'A'], case_sensitive=False), default='A', prompt=True)
@ c.pass_context
def add_holder(ctx, name, balance, level):
    """添加持仓人"""
    connect_db(ctx.obj['db_u'], ctx.obj['db_p'], ctx.obj['db_h'], DB_FINANCIAL)
    connect_db(ctx.obj['db_u'], ctx.obj['db_p'], ctx.obj['db_h'], DB_CONFIG)
    if len(list(Holder.objects.raw({'name': {"$regex": name, "$options": '-i'}}))) > 0:
        print('{}已存在'.format(name.upper()))
        return
    holder = Holder()
    holder.id = Sequence.fetch_next_id(CN_FIN_HOLDER)
    holder.name = name
    holder.balance = balance
    holder.level = HolderLevel.level_from(level).value
    holder.create_date = datetime.now().astimezone(tz=pytz.utc)
    holder.update_date = holder.create_date
    holder.save()


@ cyfin.command()
@ c.option('--holder_id', type=int, prompt=True, required=True)
@ c.option('--operation', type=c.Choice(['deposit', 'withdraw'], case_sensitive=False), prompt=True, default='deposit', required=True)
@ c.option('--amount', type=float, prompt='Amount[USDT]')
@ c.pass_context
def update_holder_balance(ctx, holder_id, operation, amount):
    """更新持仓人余额"""
    connect_db(ctx.obj['db_u'], ctx.obj['db_p'], ctx.obj['db_h'], DB_FINANCIAL)
    connect_db(ctx.obj['db_u'], ctx.obj['db_p'], ctx.obj['db_h'], DB_CONFIG)
    try:
        holder = Holder.objects.get({'_id': holder_id})
        # event
        event = Event(id=Sequence.fetch_next_id(CN_FIN_EVENT), content=operation,
                      note=str(amount), date=holder.update_date)
        event.save()
        # record
        record = Record(holder=holder_id, event=event.id, date=holder.update_date)

        record.balance_before = holder.balance
        if operation.lower() == 'deposit':
            holder.balance += amount
        else:
            holder.balance -= amount
        record.balance_after = holder.balance

        holder.update_date = datetime.now().replace(tzinfo=pytz.utc)
        holder.save()
        record.save()
        holder.print_desc()
    except Exception as e:
        print(str(e))
        return


@ cyfin.command()
@ c.option('--holder_id', type=int, prompt=True, required=True)
@ c.option('--status', type=c.Choice(['normal', 'invalid'], case_sensitive=False), prompt=True, default='invalid', required=True)
@ c.pass_context
def update_holder_status(ctx, holder_id, status):
    """更新持仓人状态"""
    connect_db(ctx.obj['db_u'], ctx.obj['db_p'], ctx.obj['db_h'], DB_FINANCIAL)
    connect_db(ctx.obj['db_u'], ctx.obj['db_p'], ctx.obj['db_h'], DB_CONFIG)
    try:
        holder = Holder.objects.get({'_id': holder_id})
        holder.status = HolderStatus.INVALID if status == 'invalid' else HolderStatus.NORMAL
        holder.update_date = datetime.now().replace(tzinfo=pytz.utc)
        holder.save()
        holder.print_desc()
    except Exception as e:
        print(str(e))
        return


@ cyfin.command()
@ c.option('--holder_id', type=int, prompt=True, required=True)
@ c.pass_context
def holder_events(ctx, holder_id):
    """持仓人事件记录"""
    connect_db(ctx.obj['db_u'], ctx.obj['db_p'], ctx.obj['db_h'], DB_FINANCIAL)
    pipeline = [
        {
            '$lookup': {
                'from': 'op_record',
                'localField': '_id',
                'foreignField': 'holder',
                'as': 'record'
            }
        }, {
            '$unwind': {
                'path': '$record',
                'preserveNullAndEmptyArrays': False
            }
        }, {
            '$lookup': {
                'from': 'event',
                'localField': 'record.event',
                'foreignField': '_id',
                'as': 'event'
            }
        }, {
            '$unwind': {
                'path': '$event',
                'preserveNullAndEmptyArrays': False
            }
        }, {
            '$addFields': {
                'event_content': '$event.content',
                'event_note': '$event.note',
                'event_date': '$event.date',
                'balance_before': '$record.balance_before',
                'balance_after': '$record.balance_after',
            }
        }, {
            '$project': {
                '_id': 1,
                'name': 1,
                'balance': 1,
                'event_content': 1,
                'event_note': 1,
                'event_date': 1,
                'balance_before': 1,
                'balance_after': 1
            }
        }
    ]
    records = list(Holder.objects.raw({'_id': holder_id}).aggregate(*pipeline))
    for record in records:
        print("{}: \t{}\t{}\t{}\t{}\t{}\t{}".format(
            holder_id, record['name'], record['balance_before'], record['balance_after'], record['event_content'], record['event_note'], record['event_date']))


@ cyfin.command()
@ c.option('--event_desc', type=str, required=True, prompt=True)
@ c.option('--profit', type=float, required=True, prompt=True)
@ c.option('--fixed_percent', type=float, required=True, prompt=True)
@ c.pass_context
def distribute_profit(ctx, event_desc, profit, fixed_percent):
    """分配利润"""
    connect_db(ctx.obj['db_u'], ctx.obj['db_p'], ctx.obj['db_h'], DB_FINANCIAL)
    connect_db(ctx.obj['db_u'], ctx.obj['db_p'], ctx.obj['db_h'], DB_CONFIG)

    event = Event.event_with(EventType.PROFIT, Sequence.fetch_next_id(
        CN_FIN_EVENT), "{}({} USDT)".format(event_desc, profit))

    if profit < 1e-6:
        print("这么点利润分配啥")

    records = list()
    # 固定利润
    fixed_percent = max(fixed_percent, 0)
    fixed_profit = profit * fixed_percent
    fp_holder = None
    if fixed_percent > 0:
        try:
            fp_holder = Holder.objects.get({
                'level': HolderLevel.SSR.value
            })
            fp_holder.balance += fixed_profit
            fp_holder.update_date = datetime.now().replace(tzinfo=pytz.utc)
            record = Record.profit_record(fp_holder.id, event.id, fp_holder.balance, fixed_profit)
            records.append(record)
        except Exception as e:
            print("分配固定利润错误：", str(e))
            return

    # 剩余利润分配
    profit *= (1 - fixed_percent)

    try:
        filter = {
            'status': HolderStatus.NORMAL.value,
            'level': {
                "$lt": HolderLevel.SSR.value
            }
        }
        holders = list(Holder.objects.raw(filter))
        pipeline = [
            {
                '$group': {
                    '_id': None,
                    'total': {
                        '$sum': '$balance'
                    },
                    'holders': {
                        '$push': {
                            '_id': '$_id',
                            'balance': '$balance',
                        }
                    }
                }
            }, {
                '$unwind': {
                    'path': '$holders',
                    'preserveNullAndEmptyArrays': False
                }
            }, {
                '$project': {
                    '_id': '$holders._id',
                    'balance': '$holders.balance',
                    'percent': {
                        '$divide': [
                            '$holders.balance', '$total'
                        ]
                    }
                }
            }
        ]
        percents = {x['_id']: x['percent'] for x in list(Holder.objects.raw(filter).aggregate(*pipeline))}
        print(percents, sum([percents[x] for x in percents]))
        # 分配
        if abs(sum([percents[x] for x in percents]) - 1) < 1e-5:
            print('分配内容：', event.content, event.note)
            print('拟分配方案：')
            if fp_holder is not None:
                print(fp_holder.name, fixed_profit)
            # holder & records
            for holder in holders:
                percented_profit = profit * percents[holder.id]
                # record
                record = Record.profit_record(holder.id, event.id, holder.balance, percented_profit)
                records.append(record)
                # holder
                holder.balance += percented_profit
                holder.update_date = datetime.now().replace(tzinfo=pytz.utc)
                print(holder.id, holder.name, "{}({}%)".format(
                    round(percented_profit, 4), round(percents[holder.id] * 100, 2)))
            if c.confirm('确认提交?'):
                event.save()
                if fp_holder is not None:
                    fp_holder.save()
                for h in holders:
                    h.save()
                for r in records:
                    r.save()
                print("完事儿")
            else:
                print("取消")
        else:
            print("持仓比例错误，检查一下")
    except Exception as e:
        print("分配持仓人利润错误", str(e))
