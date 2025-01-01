import json
import os

from analyzer import SleepAnalyzer
from data_loader import DataLoader
from data_merger import DataMerger
from data_storage import DataStorage


def main():
    # 配置参数
    sleep_file = 'data/sleep_2024_all.csv'
    wakeup_file = 'data/wakeup_2024_all.csv'
    db_url = 'mysql://user:password@localhost/sleep_db'
    output_dir = 'output'

    # 数据加载和预处理
    loader = DataLoader(sleep_file, wakeup_file)
    sleep_df, wakeup_df = loader.load_and_process()

    # 数据合并
    merger = DataMerger()
    merged_df = merger.merge_records(sleep_df, wakeup_df)

    # 数据存储
    storage = DataStorage(db_url)
    if storage.verify_data(merged_df):
        storage.save_to_db(merged_df)

    # 统计分析
    analyzer = SleepAnalyzer(merged_df)
    stats = {
        'annual': analyzer.annual_stats(),
        'quarterly': analyzer.quarterly_stats(),
        'time_periods': analyzer.time_period_analysis()
    }

    # 输出结果
    os.makedirs(output_dir, exist_ok=True)
    with open(f'{output_dir}/stats.json', 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2, default=str)


if __name__ == '__main__':
    main()
