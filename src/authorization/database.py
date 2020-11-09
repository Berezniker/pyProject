from typing import Tuple
import sqlite3
import config
import re


def is_valid_name(name: str) -> bool:
    """
    Checks name validity
    len(name) in [4, 16] and chars in [a-zA-Z0-9_]

    :param name: Username
    :return: True if name is valid False otherwise
    """
    return bool(re.fullmatch(pattern=r"\w{4,16}", string=name))


class UserDB:
    def __init__(self):
        self._connection = sqlite3.connect(config.USER_DATABASE_PATH)
        self._cursor = self._connection.cursor()
        self._table = config.USER_TABLE_NAME
        self._create_table()

    def _create_table(self) -> None:
        sql = f"""
            CREATE TABLE IF NOT EXISTS {self._table}
            (user_id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT)
        """
        self._cursor.execute(sql)
        self._connection.commit()
        return

    def _username_exist(self, username: str) -> bool:
        sql = f"""
            SELECT username
            FROM {self._table}
            WHERE username=?
        """
        return bool(self._cursor.execute(sql, [username]).fetchone())

    def add(self, username: str, password: str) -> Tuple[bool, str]:
        if not is_valid_name(username):
            return False, "Invalid username"
            # return False, f"Name `{username}` is not valid\n"\
            #               f"Valid Name:\n"\
            #               f" * 4 <= length name <= 16\n"\
            #               f" * consists only [a-zA-Z0-9_]"
        if self._username_exist(username):
            return False, "Already registered"
            # return False, f"User `{username}` is already registered"

        sql = f"""
            INSERT INTO {self._table}
            (username, password)
            VALUES (?, ?)
        """
        self._cursor.execute(sql, [username, password])
        self._connection.commit()
        return True, "ok"

    def check_login(self, username: str, password: str) -> Tuple[bool, str]:
        sql = f"""
            SELECT username, password
            FROM {self._table}
            WHERE username=? AND password=?
        """

        if not self._username_exist(username):
            return False, "Incorrect username"
        if not bool(self._cursor.execute(sql, [username, password]).fetchone()):
            return False, "Incorrect password"
        else:
            return True, "ok"

    def get_user_id(self, username: str, password: str) -> int:
        sql = f"""
            SELECT user_id
            FROM {self._table}
            WHERE username=? AND password=?
        """
        return self._cursor.execute(sql, [username, password]).fetchone()[0]

    def _drop(self) -> None:
        sql = f"DROP TABLE IF EXISTS {self._table}"
        self._cursor.execute(sql)
        self._connection.commit()
        return

    # def __print(self) -> None:
    #     import pandas as pd
    #     print(pd.read_sql_query(
    #         sql=f"SELECT * FROM {self._table}",
    #         con=self._connection,
    #         index_col="user_id"))
    #     return

    def __del__(self):
        self._connection.commit()
        self._connection.close()


if __name__ == '__main__':
    pass
