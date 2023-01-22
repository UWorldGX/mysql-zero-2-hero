# 2 SQL概览

*****

## 2.1 SQL由来

SQL(*Structured Query Language*)最早由**IBM**于上世纪70年代(1974)开发，后由ANSI制定成SQL-86、SQL-89、SQL-92、SQL-99等标准。比较重要的是**SQL-92**和**SQL-99**。

不同数据库的生产厂商均遵循SQL语句，但是都有特定内容。

## 2.2 SQL分类

SQL分为三大类：<file:\\C:\Users\Nscas\Documents\Navicat\MySQL\Servers\conn1\sql2-2-1.sql>

1. DDL(*Data Definition Language*, 数据定义语言)，定义了不同的数据表，库，视图，索引等数据库对象，还可用作创建、删除、修改数据库和数据表的结构。
    主要的关键字:`CREATE`、`DROP`、`ALTER`、`RENAME`、`TRUNCATE`。

2. DML(*Data Manipulation Language*, 数据操作语言)，用于添加、删除、查询和更新数据库的记录，并检查数据完整性。
    主要的关键字:`INSERT`、`DELETE`、`UPDATE`、`SELECT`。
    其中**SELECT**是SQL语言的基础，最为重要。

3. DCL(*Data Control Language*, 数据控制语言)，用于定义数据表，库，字段，用户的访问权限和安全级别。
    主要的关键字：`GRANT`、`REVOKE`、`COMMIT`、`ROLLBACK`、`SAVEPOINT`。
    DML中又包含DQL(数据查询语言)，使用的较多。
    其中`COMMIT`、`ROLLBACK`又被称为TCL(*Transaction Control Language*，事务控制语言)。

## 2.3 SQL规范

### SQL基本规则

* SQL可以写在1行或多行。为了提高可读性，每个子句分行写，必要时使用缩进。
* 每条命令以;或者\g或者\G结尾(只有一条语句时，;不是必要的)。
* 关键字不能被缩写也不能被分行。
* 关于标点符号
    * 必须保证所有的括号、引号是成对结束的。
    * 可以用单引号包围的数据：字符串，日期时间类型
    * 列的别名尽量使用双引号，且不建议省略as

### SQL大小写规范

SQL在Windows下是大小写不敏感的，但是在Linux下是**大小写敏感**的。Linux的区分规则如下：

* 数据库名，表名，表的别名，变量名是严格区分大小写的。
* 关键字，函数名，列名及别名（字段名及别名）是不区分大小写的。

推荐的规范：
**需要大写的**：SQL关键字，函数名，绑定变量
**需要小写的**：数据库名，表名及别名，字段名及别名

### SQL注释

两种方式:

```sql
# 单行注释，MySQL特有

-- 单行注释，通用(注意--后一定要跟空格)

-- 按快捷键Ctrl+/可以快捷注释

/*多行注释，通用
*/
```

### 命名规则

* 数据库、表的名字限制30个字符，变量名限制29个
* 必须只能包含alphabet，数字和_
* 数据库名，表名和字段名中间不得出现空格
* 不与保留字，数据库系统和常用方法冲突
* 保持字段名和类型的一致性
* 避免重名

