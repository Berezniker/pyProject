from config import USER_DATABASE_PATH, USER_TABLE_NAME, DATA_TABLE_NAME
import sqlite3


class DataDB:
    def __init__(self, user_id):
        self._connection = sqlite3.connect(USER_DATABASE_PATH)
        self._cursor = self._connection.cursor()
        self._table = DATA_TABLE_NAME
        self._user_id = user_id
        self._create_table()

    def _create_table(self) -> None:
        sql = f"""
            CREATE TABLE IF NOT EXISTS {self._table}
            (user_id INTEGER,
             f1  REAL, f2  REAL, f3  REAL, f4  REAL, f5  REAL, f6  REAL,
             f7  REAL, f8  REAL, f9  REAL, f10 REAL, f11 REAL, f12 REAL,
             f13 REAL, f14 REAL, f15 REAL, f16 REAL, f17 REAL,
             FOREIGN KEY(user_id) REFERENCES {USER_TABLE_NAME}(user_id))
        """
        self._cursor.execute(sql)
        self._connection.commit()
        return

    def get_train_data_size(self) -> int:
        sql = f"""
            SELECT COUNT(*)
            FROM {self._table}
            WHERE user_id = {self._user_id}
        """
        return self._cursor.execute(sql).fetchone()[0]

    def get_train_data(self) -> list:
        sql = f"""
            SELECT *
            FROM {self._table}
            WHERE user_id = {self._user_id}
        """
        return self._cursor.execute(sql).fetchall()

    def add(self, feature: list) -> None:
        sql = f"""
            INSERT INTO {self._table}
            (user_id, f1, f2, f3, f4, f5, f6, f7, f8, f9, f10, f11, f12, f13, f14, f15, f16, f17)
            VALUES ({self._user_id}, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        self._cursor.execute(sql, feature)
        self._connection.commit()
        return

    def _drop(self) -> None:
        sql = f"DROP TABLE IF EXISTS {self._table}"
        self._cursor.execute(sql)
        self._connection.commit()
        return

    # def __print(self) -> None:
    #     import pandas as pd
    #     print(pd.read_sql_query(
    #         sql=f"""SELECT *
    #                 FROM {self._table}
    #                 WHERE user_id = {self._user_id}
    #         """,
    #         con=self._connection,
    #         index_col="user_id"))
    #     return

    def __del__(self):
        self._connection.commit()
        self._connection.close()


if __name__ == '__main__':
    pass
