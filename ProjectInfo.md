# 睡眠数据分析项目需求文档

## 1. 数据源描述

### 1.1 输入数据表格
项目使用两个CSV格式的数据源：
- Sleep表：记录入睡时间数据
- Wakeup表：记录起床时间数据

### 1.2 数据字段
两个表格具有相同的字段结构：
| 字段名 | 说明 | 格式示例 |
|--------|------|----------|
| 月份 | 记录月份 | - |
| 日期 | 记录日期 | 2024/1/1 |
| 记录时间 | 入睡/起床时间 | 2024/01/01 3:54 (GMT+8) |
| 城市 | 位置信息 | - |
| 经度 | 位置信息 | - |
| 纬度 | 位置信息 | - |
| WiFi | WiFi名称 | - |
| 创建时间 | 记录创建时间 | - |

## 2. 数据处理规则

### 2.1 数据去重规则
- 对于同一日期同类型的重复记录，保留"记录时间"较晚的那条数据
- 使用"日期"字段作为匹配键，确保每个日期只有一条有效记录

### 2.2 数据合并规则
- 通过"日期"字段关联Sleep表和Wakeup表
- 位置信息（城市、经度、纬度）优先使用Sleep表数据
- 如果Sleep表位置信息为空，则使用Wakeup表数据补充

### 2.3 数据有效性规则
- 如果某日期仅有入睡或起床时间其中之一：
  - 缺失的时间点记录为NULL
  - duration记录为0
  - 该记录不计入统计数据

## 3. 数据库结构

### 3.1 目标表结构
表名：sleep_record
```sql
CREATE TABLE `sleep_record` (
  `id` int NOT NULL AUTO_INCREMENT,
  `record_date` date NOT NULL,
  `down` datetime DEFAULT NULL,
  `up` datetime DEFAULT NULL,
  `duration` double DEFAULT NULL,
  `city` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `lng` double NOT NULL,
  `lat` double NOT NULL,
  `wifi` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `record_year` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### 3.2 字段说明
| 字段名 | 说明 | 备注 |
|--------|------|------|
| id | 自增主键 | - |
| record_date | 记录日期 | - |
| down | 入睡时间 | 可为NULL |
| up | 起床时间 | 可为NULL |
| duration | 睡眠时长 | up与down的时间差 |
| city | 城市 | - |
| lng | 经度 | - |
| lat | 纬度 | - |
| wifi | WiFi名称 | 可为NULL |
| record_year | 记录年份 | 手动指定，每年导入一次 |

## 4. 统计需求

### 4.1 年度统计
1. 平均睡眠时长
2. 最长/最短睡眠记录
   - 日期
   - 时长
3. 入睡时间统计
   - 最早入睡日期
   - 最晚入睡日期
4. 起床时间统计
   - 最早起床日期
   - 最晚起床日期

### 4.2 季度统计
- 各季度平均睡眠时长

### 4.3 时间段分析
- 最常见入睡时间段
- 最常见起床时间段

## 5. 系统设计建议

### 5.1 模块划分
建议将系统划分为以下模块：
1. 数据读取模块
   - CSV文件读取
   - 数据格式验证
2. 数据预处理模块
   - 数据去重
   - 数据清洗
3. 数据合并模块
   - Sleep表和Wakeup表数据关联
   - 位置信息补充
4. 数据存储模块
   - 数据库写入
   - 数据完整性检查
5. 统计分析模块
   - 年度统计
   - 季度统计
   - 时间段分析
6. 结果输出模块
   - 统计结果格式化
   - 结果展示

### 5.2 开发建议
- 每个模块独立开发和测试
- 提供详细的日志记录
- 实现数据验证和异常处理
- 保留中间处理结果，便于调试