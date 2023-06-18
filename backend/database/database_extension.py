from injector import Binder, singleton

from database.db_user_handler import DbUserHandler
from database.postgresql_connection import PostgresqlConnection
from database.postgresql_connection_interface import IPostgresqlConnection


def add_database(binder: Binder):
    binder.bind(IPostgresqlConnection, PostgresqlConnection, scope=singleton)
    binder.bind(DbUserHandler, DbUserHandler, scope=singleton)
