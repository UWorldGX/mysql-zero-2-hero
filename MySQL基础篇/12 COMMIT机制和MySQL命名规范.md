# 12 COMMIT机制和MySQL命名规范

*****

## 12.1 COMMIT语句

* 意为提交数据(参考git)。一旦提交，数据库中的数据即被**永久保存**，不可以回滚。

## 12.2 ROLLBACK语句

* 意为执行回滚。将回滚到最近的一次`COMMIT`。

## 12.3 DELETE与TRUNCATE的区别

* 相同点: 都可以实现对表中所有数据的删除，同时保留表的结构。
    * `TRUNCATE`: 数据不可以回滚。
    * `DELETE FROM`: 可实现全部清除数据，数据可以回滚。

### 12.3.X DELETE与TRUNCATE的区别本质

1. `TRUNCATE`属于DDL，该类语句（如操作表）一旦执行就不可回滚。可以理解为DDL执行后隐式执行一次不受`autocommit`影响的COMMIT。
2. `DELETE FROM`属于DML，该类语句（增删改查）默认情况下一旦执行就不可回滚。但可以通过修改参数实现可回滚。

> 在执行DML之前，执行了`SET autocommit = FALSE`，则执行的DML可以回滚。

> `TRUNCATE TABLE`执行速度块，使用的系统和事务日志资源少。但是无事务且不触发`TRIGGER`，易触发事故，故不建议使用。

## 12.4 MySQL命名规范(阿里版)

* 字段名、表名**必须使用小写字母和数字，禁止出现数字开头，禁止两个下划线中间只出现数字**。

> 数据库修改字段名的代价很大，无法进行预发布，必须慎重考虑。

* **禁止使用保留字**。

* 一般而言，表必备的三个字段:**id, gmt_create, gmt_modified**。
    * 其中，id**必须为主键，类型为`BIGINT UNSIGNED`，单表时自增，步长为1**。
    * gmt_create, gmt_modified均为`DATETIME`，分别表示主动式创建和被动式更新。

* 表的命名应当遵循：业务名称_表的作用。

* 应当选取合适的存储长度。

* 删除表、修改表之前，应该先**备份**。

## 12.5 MySQL8中DDL的原子化

* 8.0中，InnoDB表的DDL支持事务完整性，即**DDL操作要么成功要么回滚**。DDL操作回滚日志将写入到`data dictionary`数据字典表`mysql.innodb_ddl_log`(该表是隐藏的，通过SHOW TABLES无法查看)。通过设置参数，可将DDL操作日志打印到MySQL错误日志中。

```sql
DROP TABLE test1, test2;
```

* 假定test2不存在。该语句执行将导致如下结果:
    * MySQL 5.7没有原子性，执行后test1将被删除；
    * 由于原子性，MySQL 8.0中将执行不成功并回滚，*test1不会被删除*。