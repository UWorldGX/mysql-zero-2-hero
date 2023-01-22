# 3 SQL-SELECT语句

*****

## 3.1 最基本的SELECT语句

参阅：<file:\\C:\Users\Nscas\Documents\Navicat\MySQL\Servers\conn1\sql2-2-2.sql>

### 3.1.0 SELECT...

用例：

```sql
SELECT 1; -- 没有其他子句
SELECT 1 + 1, 3 * 6; -- 也没有其他字句
SELECT * FROM employees; -- *代表的是所有字段
```

等价于下面一句：

```sql
SELECT 3 * 6
FROM DUAL; -- 与上一句等价，其中DUAL被称为伪表
```

### 3.1.1 SELECT... FROM ...

得出结论：SELECT子句的格式如下：

```sql
SELECT 字段1,字段2... FROM 表名
```