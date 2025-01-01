from typing import Optional

import pandas as pd
# 在创建 engine 之前添加
import pymysql
from sqlalchemy import create_engine

pymysql.install_as_MySQLdb()


class DataStorage:

    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)

    def save_to_db(self, df: pd.DataFrame) -> None:
        df.to_sql('sleep_record', self.engine, if_exists='append', index=False)

    def verify_data(self, df: pd.DataFrame) -> bool:
        # 验证数据完整性
        required_columns = [
            'record_date', 'down', 'up', 'duration', 'city', 'lng', 'lat',
            'record_year'
        ]

        return all(col in df.columns for col in required_columns)
