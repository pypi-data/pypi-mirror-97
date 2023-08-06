import hashlib
import time
from datetime import datetime, timedelta
from pymodm import fields, MongoModel
from ..connection.connect import *
from .config import *


class UserAuth(MongoModel):
    """用户认证"""
    account = fields.CharField(min_length=6, primary_key=True)
    password = fields.CharField()  # md5(password+secret)
    uid = fields.IntegerField()
    token = fields.CharField()  # md5(account+timestamp)
    expire_date = fields.DateTimeField()

    def renew_expire_date(self):
        # 3天过期
        self.expire_date = datetime.now() + timedelta(days=3)
        self.save()

    class Meta:
        connection_alias = DB_USER
        collection_name = CN_USER_AUTH


class UserInfo(MongoModel):
    """用户信息"""
    identifier = fields.IntegerField(primary_key=True)
    nickname = fields.CharField()
    token = fields.CharField()

    class Meta:
        connection_alias = DB_USER
        collection_name = CN_USER_INFO


def create_user(account, pwd, secr):
    """创建用户"""
    account = account.strip()
    md5 = hashlib.md5()
    md5.update(f'{pwd.strip()}{secr.strip()}'.encode(encoding='utf-8', errors='strict'))
    encoded_pwd = md5.hexdigest()
    all_accounts = UserAuth.objects.all()._collection.distinct('_id')
    if account is None or encoded_pwd is None:
        raise ValueError("账号/密码 不能为空")
    elif account in all_accounts:
        raise ValueError("账号已存在")
    else:
        uid = Sequence.fetch_next_id(CN_USER_INFO)
        UserAuth(account=account, password=encoded_pwd, uid=uid).save()
        UserInfo(identifier=uid, nickname=account).save()


def login_with(account, encoded_pwd):
    """验证登录"""
    account = account.strip()
    encoded_pwd = encoded_pwd.strip()
    try:
        # 登录
        acc = UserAuth.objects.get({'_id': account, 'password': encoded_pwd})
        # 生成 Token
        md5 = hashlib.md5()
        md5.update(f'{account}{time.time()}'.encode(encoding='utf-8', errors='strict'))
        acc.token = md5.hexdigest()
        acc.renew_expire_date()  # 更新过期时间
        # 生成 Token
        user_info = UserInfo.objects.raw({'_id': acc.uid}).project({'_id': 0, '_cls': 0}).limit(1).values()[0]
        user_info['id'] = acc.uid
        user_info['token'] = acc.token
        return user_info
    except Exception as e:
        print(str(e))
        raise ValueError('账号或密码错误')


def auth_token(account, token):
    """验证 token
    0: 成功
    -1: 错误 token
    -1000: 过期
    """
    try:
        acc = UserAuth.objects.get({'_id': account})
        if acc.token is None:
            return -1
        elif (acc.expire_date - datetime.now()).total_seconds() < 0:
            return -1000
        else:
            md5 = hashlib.md5()
            md5.update(acc.token.encode(encoding='utf-8', errors='strict'))
            if md5.hexdigest() == token:
                acc.renew_expire_date()
                return 0
            else:
                return -1

    except Exception as e:
        print(str(e))
        return -1
