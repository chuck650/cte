# MySQL Database Server


## Verify a mysql configuration

Use your user account (`${USER}`) or the database management systems (dbms) `root`account to log into the dbms and get a `mysql` shell.  Enter your password when prompted.  The default db password in the CTE is `password`

```mysql
$ mysql -u ${USER} -p
Enter password:
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 27
Server version: 8.0.19-0ubuntu0.19.10.3 (Ubuntu)

Copyright (c) 2000, 2020, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql>
```

From the `mysql>` prompt, execute a SQL statement to show all users in the dbms.

```bash
mysql> select user, host, account_locked, password_expired from mysql.user order by user, host;
+------------------+-----------------+----------------+------------------+
| user             | host            | account_locked | password_expired |
+------------------+-----------------+----------------+------------------+
| chuck            | localhost       | N              | N                |
| debian-sys-maint | localhost       | N              | N                |
| mysql.infoschema | localhost       | Y              | N                |
| mysql.session    | localhost       | Y              | N                |
| mysql.sys        | localhost       | Y              | N                |
| root             | 127.0.0.1       | N              | N                |
| root             | ::1             | N              | N                |
| root             | localhost       | N              | N                |
| root             | tpd-db1.tpd.cte | N              | N                |
+------------------+-----------------+----------------+------------------+
9 rows in set (0.00 sec)

mysql>
```
