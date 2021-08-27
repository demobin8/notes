### concat条件表达式

```
SELECT
	*
FROM
	seq pas
	LEFT JOIN payment pvp ON pas.bill_code = pvp.payment_code 
	OR pas.ref_code = pvp.payment_code 
WHERE
	pas.account_code = '#{dto.accountCode}' 
	AND concat( pas.bill_type, '_', pas.type ) IN ( '1_0', '2_4', '6_6' ) 
ORDER BY
	pas.create_time DESC,
	pas.id DESC
```

### month year表达式

```
SELECT MONTH
	( pas.create_time ) AS m,
	SUM( pas.amount ) AS amount 
FROM
	seq pas 
WHERE
	pas.account_code = '#{accountCode}' 
	AND YEAR ( pas.create_time ) = '#{year}' 
	AND MONTH ( pas.create_time ) IN 
  < foreach collection = "monthList" item = "item" INDEX = "index" OPEN = "(" CLOSE = ")" SEPARATOR = "," > 
  '#{item}' 
  </ foreach > 
GROUP BY
	MONTH ( pas.create_time )
ORDER BY
	MONTH ( pas.create_time ) DESC
```

### if isnull表达式
```
select true as enabled, IF(ISNULL(pw.password), 0, 1) as passwordSetFlag, pw.* from wallet pw where account_code = #{accountCode}
```

### 取前N条
```
SELECT
	count( ulc.comment_id ) AS likesTotal,
	c.* 
FROM
	feed_comment c
	LEFT JOIN user_like_feed_comment ulc ON c.id = ulc.comment_id 
	AND ulc.delete_flag = 0 
WHERE
	'n' > (
	SELECT
		count( * ) 
	FROM
		feed_comment c2 
	WHERE
		c2.parent_comment_id = c.parent_comment_id 
		AND c2.dynamic_id = 'id' 
	) 
	AND c.dynamic_id = 'id' 
GROUP BY
	c.id
```

### TIMESTAMPDIFF
```
差30分钟
SELECT * FROM interviews WHERE TIMESTAMPDIFF(MINUTE, NOW() ,interview_time) = 30
```

### BETWEEN
```
在某日期范围内
select * from users where DATE_FORMAT(birthday, '%m-%d') BETWEEN '08-01' AND '08-30'
```

### DATEDIFF
```
差5天
select * from user where DATEDIFF(NOW(), DATE_ADD(arrival_date,INTERVAL 1 YEAR)) = 5
```

### sort table with data size
```
select TABLE_NAME, concat(truncate(data_length/1024/1024,2),'MB') as data_size, concat(truncate(index_length/1024/1024,2),'MB') as index_size from information_schema.tables where TABLE_SCHEMA = 'dtp' group by TABLE_NAME order by data_length desc;
```

### ifnull case when
```
    public static String accountSql = "SELECT\n" +
            "CONCAT('INSERT INTO `account2` VALUES (\\'', \n" +
            "\tid, '\\', \\'',\n" +
            "\tIFNULL(account_code, ''), '\\', \\'',\n" +
            "\tREPLACE(IFNULL(account_name, ''), '\\'', '\\\\'''), '\\', \\'',\n" +
            "\tCASE user_role_type \n" +
            "\t\tWHEN '2' THEN '2'\n" +
            "\t\tWHEN '3' THEN '2'\n" +
            "\t\tELSE '1' \n" +
            "\tEND, '\\', \\'',\n" +
            "\tIFNULL(account_status, '00'), '\\', \\'',\n" +
            "\t'1', '\\', \\'',\n" +
            "\tIFNULL(user_code, ''), '\\', \\'',\n" +
            "\t'', '\\', \\'',\n" +
            "\tIFNULL(email, ''), '\\', \\'',\n" +
            "\tIFNULL(remark, ''), '\\', \\'',\n" +
            "\tIFNULL(delete_flag, ''), '\\', \\'',\n" +
            "\tIFNULL(create_user, ''), '\\', \\'',\n" +
            "\tIFNULL(create_time, CONCAT(CURRENT_TIMESTAMP, '')), '\\',', '\\'',\n" +
            "\tIFNULL(update_user, ''), '\\', \\'',\n" +
            "\tIFNULL(update_time, CONCAT(CURRENT_TIMESTAMP, '')), '\\'',\n" +
            "\t');') as insertSql\n" +
            "FROM\n" +
            "\t`account`;";
```

### 取一半数据
```
SELECT
	S.component_id,
	S.snr 
FROM
	(
	SELECT
		U2.*,
		@RN := @RN + 1 ROWNUMBER,
		(
		SELECT
			ROUND( COUNT( * ) / 2 ) 
		FROM
			pallet_component p
			LEFT JOIN component U ON U.component_id = p.component_id 
		WHERE
			p.pallet_id = 2 
		) TOPN 
	FROM
		pallet_component p2
		LEFT JOIN component U2 ON U2.component_id = p2.component_id
		CROSS JOIN ( SELECT @RN := 0 ) R 
	WHERE
		p2.pallet_id = 2 
	ORDER BY
		component_id 
	) S 
WHERE
	S.ROWNUMBER > S.TOPN;
```

### Invalid default value for 'CREATE_TIME'
```
mysql> SHOW VARIABLES LIKE "sql_mode";
mysql> SET GLOBAL SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION,ALLOW_INVALID_DATES';
```
### mysql [ERROR 1820 (HY000): You must reset your password using ALTER USER statement before executing this statement.]
```
mysql> ALTER USER 'root'@'localhost' IDENTIFIED BY 'MyNewPass';
```
### java.sql.SQLException: No timezone mapping entry for 'PDT
```
SET @@global.time_zone = '+00:00'; SET @@session.time_zone = '+00:00';
```

### 查索引
`show index from order_detail;`
```
SELECT * FROM mysql.`innodb_index_stats` a WHERE a.`database_name` = 'order';
SELECT * FROM mysql.`innodb_index_stats` a WHERE a.`database_name` = 'order' and a.table_name like '%order%';
```

### sum/sum if
```
SELECT SUM(expr) FROM table WHERE predicates
select sum(if(type=1,money,0)) from user group by id;
```

### 配置表
宽表 一行，多列
窄表 kv形式，多行

### table engine
```
SELECT table_name, table_type, engine FROM information_schema.tables WHERE table_schema = 'database_name' ORDER BY table_name DESC;
count table size
SELECT count(TABLE_NAME) FROM information_schema.TABLES WHERE TABLE_SCHEMA='dbname'; 
select table_schema,table_name,table_comment from information_schema.tables where TABLE_SCHEMA in('acc','dtp','batch','erp','rule','uaap') order by TABLE_SCHEMA;
```

### explain
```
explain select * from order where id = '123345789';
```
> id:选择标识符select_type:表示查询的类型。table:输出结果集的表partitions:匹配的分区type:表示表的连接类型possible_keys:表示查询时，可能使用的索引key:表示实际使用的索引key_len:索引字段的长度ref:列与索引的比较rows:扫描出的行数(估算的行数)filtered:按表条件过滤的行百分比Extra:执行情况的描述和说明

常用的类型有： ALL、index、range、 ref、eq_ref、const、system、NULL（从左到右，性能从差到好）
ALL：Full Table Scan， MySQL将遍历全表以找到匹配的行
index: Full Index Scan，index与ALL区别为index类型只遍历索引树
range:只检索给定范围的行，使用一个索引来选择行
ref: 表示上述表的连接匹配条件，即哪些列或常量被用于查找索引列上的值
eq_ref: 类似ref，区别就在使用的索引是唯一索引，对于每个索引键值，表中只有一条记录匹配，简单来说，就是多表连接中使用primary key或者 unique key作为关联条件
const、system: 当MySQL对查询某部分进行优化，并转换为一个常量时，使用这些类型访问。如将主键置于where列表中，MySQL就能将该查询转换为一个常量，system是const类型的特例，当查询的表只有一行的情况下，使用system
NULL: MySQL在优化过程中分解语句，执行时甚至不用访问表或索引，例如从一个索引列里选取最小值可以通过单独索引查找完成。

### substr
`substr(string,start,length)`

### 状态
`mysql> STATUS`

### 当前指令
`mysql> SHOW PROCESSLIST;`

### 远程连接
```
mysql> GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'xiaobin';
mysql> FLUSH PRIVILEGES;
或者
mysql> UPDATE user SET host = '%' WHERE user = 'root';
```

### 自动补全
```
编辑/etc/my.cnf
注释[mysql]下的no-auto-rehash
新加auto-rehash
```

### 安装
```
sudo apt install mysql-server mysql-client
sudo mysql -u root
```

### 清空、其它
```
mysql> TRUNCATE TABLE rtp_message_info;

mysql> SET PASSWORD FOR 'root'@'localhost' = PASSWORD('xiaobin');

mysql> DROP USER IF EXISTS test1;
mysql> CREATE USER puckai IDENTIFIED BY 'xiaobin';

mysqldump -uroot -pkalamodo -d folozs  > folozs.sql
mysql -uroot -pkalamodo folozs < folozs.sql 2>/dev/null

mysql> DROP DATABASE IF EXISTS `dtp`;
mysql> CREATE DATABASE IF NOT EXISTS cnarea DEFAULT CHARSET UTF8 COLLATE UTF8_GENERAL_CI;
mysql> GRANT ALL PRIVILEGES ON cnarea.* TO puckai@'%' IDENTIFIED BY 'xiaobin';
mysql> SHOW GRANTS FOR puckai;

mysql> SHOW DATABASES;
mysql> USE cnarea;
mysql> SHOW TABLES;
mysql> DESC cnarea;
mysql> SELECT COUNT(*) FROM cnarea;
mysql> SELECT DISTINCT level FROM cnarea;
mysql> INSERT INTO sys_user(id,realname,login_name,password,salt) VALUES (326,'bugtest','bugtest','6e27f310cf16d50fc56bc08a4dfd8882','ec198545761841649208913eb95b10e0');

mysql> CREATE TABLE user(
  -> user_id INT NOT NULL AUTO_INCREMENT,
  -> username VARCHAR(32) NOT NULL UNIQUE,
  -> password VARCHAR(32) NOT NULL,
  -> name VARCHAR(32) NOT NULL,
  -> telephone VARCHAR(16) NOT NULL,
  -> email VARCHAR(64) NOT NULL,
  -> sex CHAR(1),
  -> birthday DATETIME,
  -> location VARCHAR(16),
  -> brief TEXT,
  -> head VARCHAR(256),
  -> create_time DATETIME,
  -> PRIMARY KEY (user_id)
  -> )ENGINE=InnoDB DEFAULT CHARSET=utf8;

mysql> CREATE TABLE platform(
  -> platform_id INT NOT NULL AUTO_INCREMENT,
  -> name VARCHAR(32) NOT NULL,
  -> description TEXT,
  -> head VARCHAR(256),
  -> PRIMARY KEY (platform_id)
  -> )ENGINE=InnoDB DEFAULT CHARSET=utf8;

mysql> CREATE TABLE feed(
  -> platform_id INT,
  -> title TEXT,
  -> url VARCHAR(256),
  -> photo VARCHAR(256),
  -> FOREIGN KEY(platform_id) REFERENCES platform(platform_id)
  -> )ENGINE=InnoDB DEFAULT CHARSET=utf8;

mysql> CREATE TABLE list(
  -> list_id INT NOT NULL AUTO_INCREMENT,
  -> user_id INT,
  -> name VARCHAR(32) NOT NULL,
  -> description TEXT,
  -> tags VARCHAR(128),
  -> create_time DATETIME,
  -> FOREIGN KEY(user_id) REFERENCES user(user_id),
  -> PRIMARY KEY (list_id)
  -> )ENGINE=InnoDB DEFAULT CHARSET=utf8;

mysql> CREATE TABLE star_platform(
  -> star_id INT,
  -> platform_id INT,
  -> name VARCHAR(64),
  -> url VARCHAR(256),
  -> FOREIGN KEY(star_id) REFERENCES star(star_id),
  -> FOREIGN KEY(platform_id) REFERENCES platform(platform_id)
  -> )ENGINE=InnoDB DEFAULT CHARSET=utf8;
```

### export with function procu
`mysqldump -uroot -proot123 --databases dtp --routines --triggers --events --flush-privileges --skip-lock-tables -S /opt/mysql/sock/mysql.sock > dtp-0525.sql`

### delete all table of database
```
mysqldump -uroot -proot123 -S /opt/mysql/sock/mysql.sock --skip-lock-tables --add-drop-table --no-data acc | grep ^DROP | mysql -uroot -proot123 test
```
### errorHost '10.16.8.96' is blocked because of many connection errors; unblock with 'mysqladmin flush-hosts'Connection closed by foreign host.
`mysqladmin flush-hosts -uroot -proot123 -S /opt/mysql/sock/mysql.sock`

### engine
- MyISAM 不支持事务、行锁、外键，它保存表的行数，且默认支持FULLTEXT全文索引
- InnoDB 现在时默认引擎了，与MyISAM相反，全文索引要通过插件实现

### timestamp
只能表示1970-2038, 2^31 - 1
所以尽量用datetime

### 索引失效的情况
- 索引列出现了隐式类型转换
- WHERE 条件中含有 OR，除非 OR 前使用了索引列而 OR 之后是非索引列
- 索引中执行 LIKE 操作
- MySQL 判断全表扫描比使用索引查询更快
- 左边的值未确定

### sql优化、死锁
通过 SHOW PROCESSLIST、SHOW PROFILE、EXPLAIN 或 trace 跟踪优化语句

死锁的话要回滚其中一个事务
