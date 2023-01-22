# 3 SQL基本概念+SELECT语句

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

> 注：执行完查询语句得到的类表格称为**结果集**(result set)。

**等价**于下面一句：

```sql
SELECT 3 * 6
FROM DUAL; -- 与上一句等价，其中DUAL被称为伪表
```

### 3.1.1 SELECT... FROM ...

得出结论：SELECT子句的格式如下：

```sql
SELECT 要查询的：字段1,字段2... 
FROM 字段所在的表名
```

## 3.2 列的别名（字段的别名）

考虑下列语句：

```sql
SELECT last_name, salary, email
FROM employees;
```

若写成这样：

```sql
SELECT last_name, salary email
FROM employees;
```

就相当于给salary字段起了个**别名**，email。
另一种写法：

```sql
SELECT last_name, salary AS email
FROM employees;
```

其中`AS`全称是*alias*，即别名。
建议养成加`AS`的习惯。
还可以这么写：

```sql
SELECT last_name, salary "email" -- 用双引号包住别名
FROM employees;
```

> 注意：虽然这种方式似乎和不加引号的作用相同，但部分场景下必须加上双引号。
> 注意：MySQL对引号的要求不严谨，但其他DBMS使用单引号包住别名就会报错。

## 3.3 去除重复行

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

## 3.4 空值及其参与的运算

空值，即`null`，可以参与运算。

> null与''、0、'null'均不等同。

示例如下：
```sql
SELECT first_name, salary, salary * (1 + commission_pct) -- commission_pct部分记录中为null
FROM employees;
```

观察结果集发现，凡是commission_pct为null的记录，第二个字段结果也是null。
得出结论：**null与任何数进行运算都得null。**

> 上述例题的解决方法：
>
> ```sql
> SELECT first_name, salary, salary * IFNULL(1 + commission_pct, 0)
> FROM employees;
> ```
>
> 实际问题中，这种功能应该由**其他编程语言**来实现，效率会更高。
> 数据库应该注重记录IO，而不是复杂运算。

## 3.5 着重号

着重号，即`，用途是屏蔽SQL的保留字，以方便命名。

```sql
SELECT *
FROM `order`; -- 使用了着重号来屏蔽保留字
```

## 3.6 查询常数

SQL还提供查询常数的功能,可以理解为用指定常数对结果集中的一列（一个字段）进行全填充。

```sql
SELECT 'Alas', employee_id, salary -- 'Alas'是字符串常量
FROM employees;
```

## 3.7 显示表的结构

要显示表结构，应该使用`DESCRIBE`或`DESC`关键字。

```sql
DESCRIBE employees;
```