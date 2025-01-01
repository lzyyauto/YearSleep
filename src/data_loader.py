import logging
from datetime import datetime
from typing import Optional, Tuple

import pandas as pd


class DataLoader:

    def __init__(self, sleep_file: str, wakeup_file: str):
        self.sleep_file = sleep_file
        self.wakeup_file = wakeup_file
        logging.info(
            f"初始化数据加载器: sleep_file={sleep_file}, wakeup_file={wakeup_file}")

    def read_csv(self, file_path: str) -> pd.DataFrame:
        logging.info(f"开始读取CSV文件: {file_path}")
        df = pd.read_csv(file_path)
        logging.info(f"成功读取 {len(df)} 条记录")
        # 转换日期列
        df['日期'] = pd.to_datetime(df['日期'])

        # 处理带时区的时间字符串
        def parse_datetime(dt_str: str) -> datetime:
            # 移除时区信息 "(GMT+8)" 后解析
            dt_str = dt_str.split(' (')[0]
            return pd.to_datetime(dt_str, format='%Y/%m/%d %H:%M')

        # 转换记录时间列
        df['记录时间'] = df['记录时间'].apply(parse_datetime)

        return df

    def deduplicate(self, df: pd.DataFrame) -> pd.DataFrame:
        before_count = len(df)
        df = df.sort_values('记录时间').drop_duplicates('日期', keep='last')
        after_count = len(df)
        logging.info(f"数据去重: {before_count} -> {after_count} 条记录")
        return df

    def load_and_process(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        sleep_df = self.read_csv(self.sleep_file)
        wakeup_df = self.read_csv(self.wakeup_file)

        # 去重处理
        sleep_df = self.deduplicate(sleep_df)
        wakeup_df = self.deduplicate(wakeup_df)

        return sleep_df, wakeup_df
