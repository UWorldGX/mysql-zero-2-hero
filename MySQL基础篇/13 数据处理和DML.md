# 13 数据处理与DML

*****

## 13.1 插入数据

* 插入数据时输入的数据顺序应当和字段(列)的顺序一致。

### 13.1.1 VALUE的方式插入数据

* 该方法**一次只能添加一条数据**。

```sql
INSERT INTO table_name 
VALUES(field_1, field_2);

-- 指明了要添加到的字段，更方便与原字段进行匹配
INSERT INTO table_name(field_name_1, field_name_2)
VALUES(field_1, field_2);
```

* 也可以在`VALUES`子句后跟多个新记录来实现一次添加多个记录。记录之间用逗号分隔。
* 这种多行的`INSERT`语句执行效率比数个单行语句要高，推荐使用。

```sql
INSERT INTO table_name(field_name_1, field_name_2)
VALUES
(field_1, field_2),
(field_11, field_22);
```
> 若添加数据没有给出所有的字段，且没有约束，未指定值的字段将被赋值为NULL。

> 注意字符和日期类型的源数据应当包在单引号内。

### 13.1.2 将查询结果插入表中

* 注意查询结果中的字段类型应当与待插入表中字段类型匹配。这种情况不使用`VALUES`子句。

```sql
INSERT INTO table_name(field_name_1, field_name_2)
SELECT field_name_1, field_name_2
FROM table_name_1; -- ...
```

## 13.2 更新数据

```sql
UPDATE table_1 SET field_1 = field_1_value
WHERE ...; -- 一般都会加过滤条件

-- 一次更改多个字段的值
UPDATE table_1 
SET field_1 = field_1_value,
field_2 = field_2_value, ...
WHERE ...;
```

* 容易看出，使用`UPDATE SET`子句容易实现批量修改数据。

## 13.3 删除数据

```sql
DELETE FROM table_1
WHERE ...;
```

> 注意添加、修改、删除子句，即DML操作，是有可能修改不成功的。
> (数据类型不匹配，不存在列，约束的影响（如外键级联删除）等等)

> DML执行后会自动提交数据，若不希望自动提交数据见上章操作。

> 一般建议在更新、删除操作之前，**做一遍查询以确保存在要修改的记录**。

## 13.4 MySQL8新特性: 计算列

* 计算列即某一列列的值由其他列的值计算得来。
* 可以在`ALTER TABLE`和`CREATE TABLE`子句中指定计算列。

```sql
CREATE TABLE t_1
(
    a INT,
    b INT,
    c INT GENERATED ALWAYS AS (a + b) VIRTUAL
)
```