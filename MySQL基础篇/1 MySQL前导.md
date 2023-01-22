# 1 MySQL前导

*****

## 1.1 MySQL登录参数

| 参数 | 含义 |
| --- | --- |
| -u | 后接用户名 |
| -p | 后接密码 |
| -P | 后接端口 |
| -h | 后接主机 |

## 1.2 MySQL 5.7和8.0之差别：字符问题

MySQL8.0可以正常为字符串(例如*varchar(15)*)赋中文值。MySQL5.7**则会报错**。
原因是5.7中新建的数据库默认字符集是**latin**。

### 解决方案:

* 第一步: 输入以下指令:

    ```sql
    SHOW VARIABLES LIKE 'character_%';
    ```

    可看到如下内容:
    +--------------------------+--------------------------------------------+
    | Variable_name            |Value                                       |
    +--------------------------+--------------------------------------------+
    | character_set_client     |gbk                                         |
    | character_set_connection |gbk                                         |
    | character_set_database   |latin1                                      |
    | character_set_filesystem |binary                                      |
    | character_set_results    |gbk                                         |
    | character_set_server     |latin1                                      |
    | character_set_system     |utf8                                        |
    | character_sets_dir       |D:\Database\MySQL57\Program\share\charsets\ |
    +--------------------------+--------------------------------------------+
    可以看到，character_set_database和character_set_server的值均为**latin1**。
    
* 第二步：输入以下指令：

    ```sql
    SHOW VARIABLES LIKE 'collation_%';
    ```
    结果如下:
    +----------------------+-------------------+
    | Variable_name        | Value             |
    +----------------------+-------------------+
    | collation_connection | gbk_chinese_ci    |
    | collation_database   | latin1_swedish_ci |
    | collation_server     | latin1_swedish_ci |
    +----------------------+-------------------+
    可以看到，database和server的字符串比较规则均为**latin1_swedish_ci**。

    以上两步的作用是确认编码信息和比较编码信息。
* 第三步：进入my.ini修改

    ```ini
    [mysql] #在63行左右，添加：
    default-character-set=utf8 #修改默认字符集

    [mysqld] #在76行左右，添加：
    character-set-server=utf8mb4
    #collation-server=utf8_general-ci
    ```

    修改成功，记得**重启MYSQL57**服务。

    ```batch
    net stop mysql服务名
    net start mysql服务名
    ```

    > 注：如果是之前已经建好的，使用latin1的数据库，
    > 应该手动改成utf8。
    > 修改方法：
    >
    > ```sql
    > ALTER TABLE tables... CHARSET utf8mb4; #修改表编码为UTF8,数据库同理
    > ```

    > 注: MySQL不支持UTF-8 with BOM。

## 1.3 MySQL相关图形化管理工具的使用

常用的包括: **MySQL Workbench(官方)/Navicat/phpMyAdmin/MySQLDumper/SQLyog/dbeaver/MySQL ODBC Connector/DataGrip**。

### MySQL 5.7和8.0之差别：登录加密问题

我使用的是Navicat Premium 16,对于MySQL8.0，直连即可。
老版本可能不兼容8.0新加入的*Strong password encryption for authentication*。

> 若出现2059/2058错误，有两种解决方案:
> * 升级图形化管理工具的版本...
> * 使用命令行登录8.0，输入以下指令:

>   ```sql
>   # 使用mysql数据库
>   USE mysql;
>   # 修改'root'@'localhost'用户的密码规则和密码
>   ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY   >   '密码';
>   #刷新权限
>   FLUSH PRIVILEGES;
>   ```
>

## 1.4 MySQL目录结构和源码

### MySQL主要目录

| 目录结构 | 说明 |
| --- | --- |
| bin目录 | MySQL的所有可执行文件，例如mysql.exe |
| MySQLInstanceConfig.exe | 数据库的配置向导，在安装时出现的内容 |
| data目录 | MySQL系统数据库所在的目录 |
| my.ini | MySQL的主要配置文件 |
| C:\ProgramData\MySQL\MySQL Server 8.0\data(默认) | 用户创建的数据库 |

### MySQL源码主要目录

| 目录结构 | 说明 |
| --- | --- |
| sql | 核心代码 |
| libmysql | 客户端程序代码 | 
| mysql-test | 测试工具 | 
| mysys | 操作系统相关 |

## 1.5 其他常见问题

### root密码遗忘

1. 关掉mysqld(服务进程)
2. 通过命令行+特殊参数启动mysqld:

```batch
mysqld --defaults-file="..\my.ini" --skip-grant-tables
```

3. 此时，mysqld已经启动，且不需要权限检查
4. mysql -uroot直接登录客户端（另开启一个）
5. 修改权限表：

```sql
USE mysql;
UPDATE USER SET authentication_string=password('新密码') WHERE user='root' AND Host='localhost';
FLUSH PRIVILEGES;
```

6. 关掉mysqld服务进程
7. 再次打开mysqld,即可用新密码登录

### mysql报“不是内部或外部命令”

添加bin目录到环境变量。

### ERROR 1046(3D000):No database selected

先use数据库：

```sql
USE databases...;
```

### 命令行客户端的字符集问题

当服务端认为字符集是utf8，实际是GBK时，就会报错。
解决方法：

```sql
SHOW VARIABLES LIKE 'character_%';
SET NAMES GBK;
```

## 1.6 MySQL导入现有的数据表和数据库

两种方式：

1. source文件的全路径名(命令行)
2. 使用图形化工具