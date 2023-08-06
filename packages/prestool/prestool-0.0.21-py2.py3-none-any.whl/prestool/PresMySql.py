from .util import format_quot_str_util
import pymysql


class PresMySql:
    def __init__(self):
        self.mysql_host = ''
        self.mysql_port = ''
        self.mysql_user = ''
        self.mysql_pwd = ''
        self.mysql_db_name = ''
        self.mysql_charset = ''

    def connect(self):
        return pymysql.connect(
            host=self.mysql_host, user=self.mysql_user, password=self.mysql_pwd,
            db=self.mysql_db_name, charset=self.mysql_charset, port=self.mysql_port,
            cursorclass=pymysql.cursors.DictCursor)

    @staticmethod
    def sql_str(table, target, where):
        sql = f'select {", ".join(target) if target else "*"} from {table}'
        sql += f" where {' and '.join([f'{k}={format_quot_str_util(v)}' for k, v in where.items()])};" if where else ';'
        return sql

    def get_db_info(self, table, target=None, where=None):
        sql = self.sql_str(table, target, where)
        with self.connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
                return result, sql
