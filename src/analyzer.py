import logging
from datetime import datetime
from typing import Any, Dict

import pandas as pd

# 配置基础日志
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


class SleepAnalyzer:

    def __init__(self, df: pd.DataFrame):
        self.df = df
        # 只分析有效的睡眠记录
        self.valid_df = df[df['duration'] > 0]
        logging.info(f"总记录数: {len(df)}, 有效记录数: {len(self.valid_df)}")

    def annual_stats(self) -> Dict[str, Any]:
        logging.info("开始计算年度统计数据...")
        max_sleep_idx = self.valid_df['duration'].idxmax()
        min_sleep_idx = self.valid_df['duration'].idxmin()

        stats = {
            'avg_duration': round(self.valid_df['duration'].mean(), 2),
            'max_sleep': {
                'date':
                self.valid_df.loc[max_sleep_idx]['record_date'].strftime(
                    '%Y-%m-%d'),
                'duration':
                round(self.valid_df['duration'].max(), 2),
                'city':
                self.valid_df.loc[max_sleep_idx]['city']
            },
            'min_sleep': {
                'date': self.valid_df.loc[min_sleep_idx]['record_date'],
                'duration': self.valid_df['duration'].min(),
                'city': self.valid_df.loc[min_sleep_idx]['city']
            },
            'earliest_down': {
                'date':
                self.valid_df.loc[
                    self.valid_df['down'].dt.time.idxmin()]['record_date'],
                'time':
                self.valid_df['down'].dt.time.min(),
                'city':
                self.valid_df.loc[self.valid_df['down'].dt.time.idxmin()]
                ['city']
            },
            'latest_down': {
                'date':
                self.valid_df.loc[self.valid_df['down'].dt.time.idxmax()]
                ['record_date'],
                'time':
                self.valid_df['down'].dt.time.max(),
                'city':
                self.valid_df.loc[
                    self.valid_df['down'].dt.time.idxmax()]['city']
            },
            'earliest_up': {
                'date':
                self.valid_df.loc[self.valid_df['up'].dt.time.idxmin()]
                ['record_date'],
                'time':
                self.valid_df['up'].dt.time.min(),
                'city':
                self.valid_df.loc[self.valid_df['up'].dt.time.idxmin()]['city']
            },
            'latest_up': {
                'date':
                self.valid_df.loc[self.valid_df['up'].dt.time.idxmax()]
                ['record_date'],
                'time':
                self.valid_df['up'].dt.time.max(),
                'city':
                self.valid_df.loc[self.valid_df['up'].dt.time.idxmax()]['city']
            }
        }

        logging.info(f"平均睡眠时长: {stats['avg_duration']} 小时")
        logging.info(
            f"最长睡眠: {stats['max_sleep']['duration']} 小时 ({stats['max_sleep']['date']}, {stats['max_sleep']['city']})"
        )
        logging.info(
            f"最短睡眠: {stats['min_sleep']['duration']} 小时 ({stats['min_sleep']['date']}, {stats['min_sleep']['city']})"
        )
        return stats

    def quarterly_stats(self) -> Dict[int, float]:
        logging.info("开始计算季度统计数据...")
        stats = self.valid_df.groupby(
            self.valid_df['record_date'].dt.quarter)['duration'].mean().round(
                2).to_dict()
        logging.info(f"季度统计结果: {stats}")
        return stats

    def time_period_analysis(self) -> Dict[str, Any]:
        logging.info("开始分析时间段数据...")
        # 将时间分成小时段
        down_hours = self.valid_df['down'].dt.hour.value_counts().sort_index()
        up_hours = self.valid_df['up'].dt.hour.value_counts().sort_index()

        result = {
            'common_down_period': down_hours.idxmax(),
            'common_up_period': up_hours.idxmax()
        }
        logging.info(f"最常见入睡时间: {result['common_down_period']}时")
        logging.info(f"最常见起床时间: {result['common_up_period']}时")
        return result
