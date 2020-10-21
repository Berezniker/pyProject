from typing import Tuple, Any
import pandas as pd
import sqlite3
import config


class UserDB:
    def __init__(self,
                 table_name: str = "login",
                 database_path: str = config.USER_DATABASE_PATH):
        self._connection = sqlite3.connect(database_path)
        self._cursor = self._connection.cursor()
        self.table = table_name
        self._create_table()

    def __exists(func) -> Any:
        def wrapper(self, *args) -> Any:
            sql = """
                SELECT count(*) AS exist
                FROM sqlite_master
                WHERE type='table' AND name=?
            """
            if bool(self._cursor.execute(sql, [self.table]).fetchone()[0]):
                return func(self, *args)
            else:
                print(f"No such table: {self.table}")
                return
        return wrapper

    def _create_table(self) -> None:
        sql = f"""
            CREATE TABLE IF NOT EXISTS {self.table}
            (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT)
        """
        self._cursor.execute(sql)
        self._connection.commit()
        return

    @__exists
    def _username_exist(self, username: str) -> bool:
        sql = f"""
            SELECT username
            FROM {self.table}
            WHERE username=?
        """
        return bool(self._cursor.execute(sql, [username]).fetchone())

    @__exists
    def add(self, username: str, password: str) -> Tuple[bool, str]:
        if self._username_exist(username):
            return False, f"User '{username}' is already registered"

        sql = f"""
            INSERT INTO {self.table}
            (username, password)
            VALUES (?, ?)
        """
        self._cursor.execute(sql, (username, password))
        self._connection.commit()
        return True, "ok"

    @__exists
    def check_login(self, username: str, password: str) -> Tuple[bool, str]:
        sql = f"""
            SELECT username, password
            FROM {self.table}
            WHERE username=? AND password=?
        """

        if not self._username_exist(username):
            return False, "Incorrect username"
        if not bool(self._cursor.execute(sql, (username, password)).fetchone()):
            return False, "Incorrect password"
        else:
            return True, "ok"

    @__exists
    def _drop(self) -> None:
        sql = f"DROP TABLE {self.table}"
        self._cursor.execute(sql)
        self._connection.commit()
        return

    @__exists
    def _print(self) -> None:
        print(pd.read_sql_query(
            sql=f"SELECT * FROM {self.table}",
            con=self._connection,
            index_col="id"))
        return

    def __del__(self):
        self._connection.commit()
        self._connection.close()


if __name__ == '__main__':
    pass
