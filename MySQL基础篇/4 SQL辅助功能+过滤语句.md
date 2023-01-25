# 4 SQL辅助功能+过滤语句

*****

## 4.1 去除重复行

语法：

```sql
SELECT DISTINCT ...
FROM ...;
```

常见错误写法：

```sql
SELECT ..., DISTINCT ... -- 错误的写法
FROM ...;

SELECT DISTINCT ..., ... -- 这么写只能保证筛选出的每条记录是不重复的(又叫多重去重)
FROM ...;
```

## 4.2 着重号

着重号，即`，用途是屏蔽SQL的保留字，以方便命名。

```sql
SELECT *
FROM `order`; -- 使用了着重号来屏蔽保留字
```

## 4.3 查询常数

SQL还提供查询常数的功能,可以理解为用指定常数对结果集中的一列（一个字段）进行全填充。

```sql
SELECT 'Alas', employee_id, salary -- 'Alas'是字符串常量
FROM employees;
```

## 4.4 显示表的结构

要显示表结构，应该使用`DESCRIBE`或`DESC`关键字。

```sql
DESCRIBE employees;
```

## 4.5 过滤数据

参阅：<file:\\C:\Users\Nscas\Documents\Navicat\MySQL\Servers\conn1\sql2-2-3.sql>

使用`WHERE`关键字。用法如下：

```sql
SELECT ...
FROM ...
WHERE ...;
```

用例：

```sql
SELECT *
FROM employees
WHERE department_id = 90; -- 只显示90号部门的信息
```

使用WHERE子句有以下注意事项：
* 注意字符串的大小写问题。MySQL对字符串大小写的处理不严谨(不区分大小写也能查询通过)，实际应该保证大小写一致以确保可移植性好。
* WHERE一定要声明在FROM结构的后面,GROUP BY结构的前面。