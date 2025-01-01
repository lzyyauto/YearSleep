# YearSleep

这是一个用于分析个人睡眠数据的Python项目,可以处理和分析来自CSV文件的睡眠记录,生成统计报告。

## 功能特点

- 支持处理入睡和起床两个数据源
- 自动处理数据重复和清洗
- 计算睡眠时长和位置信息
- 生成详细的统计分析报告
- 支持数据存储到MySQL数据库
- 完整的日志记录

## 项目结构

```
sleep_analysis/
├── src/                # 源代码
│   ├── data_loader.py  # 数据加载模块
│   ├── data_merger.py  # 数据合并模块
│   ├── data_storage.py # 数据存储模块
│   ├── analyzer.py     # 统计分析模块
│   └── main.py         # 主程序入口
├── data/               # 数据文件目录
├── output/            # 输出结果目录
└── tests/             # 测试代码目录
```

## 安装依赖

```bash
pip install pandas sqlalchemy pymysql
```

## 使用方法

1. 准备数据文件
   - 将入睡数据保存为 `data/sleep_2024_all.csv`
   - 将起床数据保存为 `data/wakeup_2024_all.csv`

2. 配置数据库连接
   - 在 `main.py` 中修改 `db_url` 参数

3. 运行程序
```bash
python src/main.py
```

4. 查看结果
   - 统计结果将保存在 `output/stats.json`
   - 程序运行日志会实时显示在控制台

## 数据格式要求

### 输入CSV文件格式
- 日期: YYYY/MM/DD
- 记录时间: YYYY/MM/DD HH:MM (GMT+8)
- 必需字段: 日期、记录时间、城市、经度、纬度、WiFi

### 输出统计指标
- 年度统计
  - 平均睡眠时长
  - 最长/最短睡眠记录
  - 最早/最晚入睡时间
  - 最早/最晚起床时间
- 季度统计
  - 各季度平均睡眠时长
- 时间段分析
  - 最常见入睡/起床时间段

## 数据库表结构

```sql
CREATE TABLE `sleep_record` (
  `id` int NOT NULL AUTO_INCREMENT,
  `record_date` date NOT NULL,
  `down` datetime DEFAULT NULL,
  `up` datetime DEFAULT NULL,
  `duration` double DEFAULT NULL,
  `city` varchar(50) NOT NULL,
  `lng` double NOT NULL,
  `lat` double NOT NULL,
  `wifi` varchar(50) DEFAULT NULL,
  `record_year` int NOT NULL,
  PRIMARY KEY (`id`)
)
```

## 开发说明

- 使用Python 3.8+
- 遵循PEP 8编码规范
- 使用typing进行类型注解
- 包含完整的日志记录

## 注意事项

1. 确保CSV文件使用UTF-8编码
2. 数据库需要utf8mb4字符集支持
3. 时区统一使用GMT+8
4. 建议每年导入一次数据

## 许可证

MIT License

本项目采用 MIT 许可证。查看 [LICENSE](LICENSE) 文件了解更多信息。 