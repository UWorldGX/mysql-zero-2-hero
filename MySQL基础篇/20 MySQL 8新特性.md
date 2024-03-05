# 20 MySQL 8新特性

*****

## 20.1 新增特性一览

1. 更简便的NoSQL支持
    以更灵活的方式实现，不再依赖schema。
2. 更好的索引
    新增了`隐藏索引和降序索引`，隐藏索引可以测试去掉索引对查询性能的影响；查询中混合存在多列索引时，使用降序索引可提高查询性能。
3. 更完善的JSON功能
4. 安全与账户管理
    新增了`caching_sha2_password`，提高数据库安全性能。
5. InnoDB改进
6. 数据字典
    新增了数据字典，存储数据库对象信息，这些字典可事务化。
7. 原子数据定义语句
    即Atomic DDL，可以将与DDL操作相关的内部逻辑写入单独的原子事务中，这使得即使服务器崩溃，事务也能提交或回滚。
8. 资源管理
    可创建和管理资源组，允许把服务器内一些线程分配给特定的资源组，以便线程根据可用资源执行。
9. 默认字符集的变更
10. 优化器增强
    支持隐藏索引和降序索引。
11. **公用表表达式**
12. **窗口函数**
13. 正则表达式更好的支持
14. 内部临时表
    TempTable取代MEMORY作为内部临时表的存储引擎。
15. 日志记录
16. 备份锁
17. 增强的MySQL复制

## 20.2 移除特性一览

1. **查询缓存**
2. 删除了部分加密函数
3. 删除了部分空间函数
4. \N不再是NULL
5. 移除`mysql_install_db`
6. 移除通用分区处理程序
7. 系统和状态变量信息不再维护
8. 移除`mysql_plugin`工具

## 20.3 窗口函数

窗口函数的作用类似于在查询中对数据进行分组，不同的是，分组操作会把分组的结果聚合成一条记录，而窗口函数则将结果置入每一条记录中。

窗口函数可以分为动态窗口函数和静态窗口函数。
* 动态窗口函数：窗口大小会随着记录的不同而变化；
* 静态窗口函数：窗口大小固定，不随记录变化而变化；

### 20.3.1 序号函数

* `ROW_NUMBER()`函数可对数据中的序号进行顺序显示。

    ```sql
    SELECT ROW_NUMBER() OVER(PARTITION BY department_id ORDER BY salary DESC) AS row_num, last_name, salary, employee_id
    FROM employees; -- 可以查询出 按照部门内薪资降序编号的 分好组的员工信息
    ```

* `RANK()`函数可对序号进行顺序显示（类似于 `ROW_NUMBER()`），并且会跳过重复的序号（允许并列序号，如1,2,2,4）。
    ```sql
    SELECT RANK() OVER(PARTITION BY department_id ORDER BY salary DESC) AS rk, last_name, salary, employee_id
    FROM employees; -- 此时若两员工薪资在部门内部相同，将拥有一样的序号
    ```

* `DENSE_RANK()`函数可对序号进行顺序显示（类似于 `RANK()`），并且不会跳过重复的序号（允许并列序号，如1,2,2,3）。
    ```sql
    SELECT DENSE_RANK() OVER(PARTITION BY department_id ORDER BY salary DESC) AS rk, last_name, salary, employee_id
    FROM employees; -- 此时若两员工薪资在部门内部相同，将拥有一样的序号
    ```

### 20.3.2 分布函数

* `PERCENT_RANK()`函数的计算机制如下：
    * `(rank - 1) / (rows - 1)`，其中rank指的是RANK()函数计算出的序号，rows指的是当前分组的总记录数。

    ```sql
    SELECT RANK() OVER w AS rk,
    PERCENT_RANK() OVER w AS per_rank,
     last_name, salary, employee_id
    FROM employees
    WINDOW w AS (PARTITION BY department_id ORDER BY salary DESC); -- w是圈定的根据department_id分组的单元窗口
    ```

* `CUME_DIST()`函数

    ```sql
    SELECT CUME_DIST() OVER(PARTITION BY department_id ORDER BY salary ASC) AS rk, last_name, salary, employee_id
    FROM employees; -- 查询每组员工中小于等于该员工薪资的人占组内总人数的比例
    ```

### 20.3.3 前后函数

* `LAG(expr, n)`函数返回当前行的前面n行的expr的值。
* `LEAD(expr, n)`函数返回当前行的后面n行的expr的值。

    ```sql
    SELECT salary - pre_salary AS diff_salary-- 计算一个员工和组内上一个员工工资差值
    FROM
    (
        SELECT salary, LAG(salary, 1) OVER w AS pre_salary, last_name
        FROM employees
        WINDOW w AS (PARTITION BY department_id ORDER BY salary DESC)
    ); -- w是圈定的根据department_id分组的单元窗口
    ```

### 20.3.4 首尾函数

```sql
SELECT salary, FIRST_VALUE(salary) OVER w AS pre_salary, last_name
FROM employees
WINDOW w AS (PARTITION BY department_id ORDER BY salary DESC);
```

## 20.4 公（通）用表表达式

即CTE，是一个临时结果集，作用范围是当前语句。可以理解为可以复用的子查询，可以被别的CTE和查询访问。

### 20.4.1 普通的公用表表达式

```sql
WITH CTE_name
AS SELECT|DELETE|UPDATE ....;
```

这种表达式可以被多次引用，可被其他CTE和查询引用。

```sql
-- 用例：查看部门表中存在员工的部门列表
WITH cte
AS SELECT DISTINCT department_id FROM employees;

SELECT *
FROM departments JOIN cte
ON departments.department_id = cte.department_id;
```

### 20.4.2 递归的公用表表达式

这种表达式可以**递归引用自身**。

```sql
WITH RECURSIVE CTE_name
AS SELECT|DELETE|UPDATE ....;
```

* 这表达式由两部分组成：种子查询，用于**获取递归的初始值**，只会查询一次以创建初始数据集；递归查询，一直执行到没有新的数据产生。

* 用例：查询所有具有下下属身份的成员信息