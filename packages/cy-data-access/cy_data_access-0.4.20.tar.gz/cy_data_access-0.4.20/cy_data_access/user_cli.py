import click as c
from cy_data_access.connection.connect import *
from cy_data_access.models.user import *


@c.group()
@c.pass_context
def cyusr(ctx):
    connect_db_env(DB_USER)
    connect_db_env(DB_CONFIG)


@cyusr.command()
@c.option('--account', prompt=True, required=True)
@c.password_option()
@c.option('--secret', prompt=True, required=True)
def add_user(account, password, secret):
    try:
        create_user(account, password, secret)
    except ValueError as err:
        print(str(err))


@cyusr.command()
@c.option('--account', prompt=True, required=True)
@c.option('--password', prompt=True, required=True)
@c.option('--secret', prompt=True, required=True)
def login(account, password, secret):
    print(login_with(account, password, secret).to_son().to_dict())


@cyusr.command()
@c.option('--account', prompt=True, required=True)
@c.option('--token', prompt=True, required=True)
def auth(account, token):
    print(auth_token(account, token))
