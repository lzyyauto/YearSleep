from datetime import datetime
from typing import Optional

import pandas as pd


class DataMerger:

    def merge_records(self, sleep_df: pd.DataFrame,
                      wakeup_df: pd.DataFrame) -> pd.DataFrame:
        # 通过日期关联两个表
        merged_df = pd.merge(sleep_df,
                             wakeup_df,
                             on='日期',
                             how='outer',
                             suffixes=('_sleep', '_wakeup'))

        # 处理位置信息
        merged_df['city'] = merged_df['城市_sleep'].fillna(
            merged_df['城市_wakeup'])
        merged_df['lng'] = merged_df['经度_sleep'].fillna(merged_df['经度_wakeup'])
        merged_df['lat'] = merged_df['纬度_sleep'].fillna(merged_df['纬度_wakeup'])

        # 计算睡眠时长
        def calculate_duration(row) -> Optional[float]:
            if pd.isna(row['记录时间_sleep']) or pd.isna(row['记录时间_wakeup']):
                return 0
            duration = (row['记录时间_wakeup'] -
                        row['记录时间_sleep']).total_seconds() / 3600
            return round(duration, 2)

        merged_df['duration'] = merged_df.apply(calculate_duration, axis=1)

        # 整理最终数据结构
        result_df = pd.DataFrame({
            'record_date':
            merged_df['日期'],
            'down':
            merged_df['记录时间_sleep'],
            'up':
            merged_df['记录时间_wakeup'],
            'duration':
            merged_df['duration'],
            'city':
            merged_df['city'],
            'lng':
            merged_df['lng'],
            'lat':
            merged_df['lat'],
            'wifi':
            merged_df['WiFi_sleep'].fillna(merged_df['WiFi_wakeup']),
            'record_year':
            merged_df['日期'].dt.year
        })

        return result_df
