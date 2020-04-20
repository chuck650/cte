# MySQL Database Server

MySQL is a database service that contains a database management system and a service point for interacting with the dbms with SQL commands.  There is also a mysql client component that provides a mysql console shell to the dbms.

## Verify a mysql configuration



### Get a mysql shell to the dbms

Use your user account (`${USER}`) or the database management systems (dbms) `root`account to log into the dbms and get a `mysql` shell.  Enter your password when prompted.  The default db password in the CTE is `password`. If you find the tables are too wide for the terminal window, you can append `--auto-vertical-output` to the options when running the shell so that rows are displayed vertically when necessary to fit the screen.


```bash
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

### Show user accounts and status

From the `mysql>` prompt, execute a SQL statement to show all users in the dbms.

```sql
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

### Show grants (permissions) for current user

```sql
mysql> show grants for current_user;
*************************** 1. row ***************************
Grants for chuck@localhost: GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, RELOAD, SHUTDOWN, PROCESS, FILE, REFERENCES, INDEX, ALTER, SHOW DATABASES, SUPER, CREATE TEMPORARY TABLES, LOCK TABLES, EXECUTE, REPLICATION SLAVE, REPLICATION CLIENT, CREATE VIEW, SHOW VIEW, CREATE ROUTINE, ALTER ROUTINE, CREATE USER, EVENT, TRIGGER, CREATE TABLESPACE, CREATE ROLE, DROP ROLE ON *.* TO `chuck`@`localhost`
*************************** 2. row ***************************
Grants for chuck@localhost: GRANT APPLICATION_PASSWORD_ADMIN,AUDIT_ADMIN,BACKUP_ADMIN,BINLOG_ADMIN,BINLOG_ENCRYPTION_ADMIN,CLONE_ADMIN,CONNECTION_ADMIN,ENCRYPTION_KEY_ADMIN,GROUP_REPLICATION_ADMIN,INNODB_REDO_LOG_ARCHIVE,PERSIST_RO_VARIABLES_ADMIN,REPLICATION_APPLIER,REPLICATION_SLAVE_ADMIN,RESOURCE_GROUP_ADMIN,RESOURCE_GROUP_USER,ROLE_ADMIN,SERVICE_CONNECTION_ADMIN,SESSION_VARIABLES_ADMIN,SET_USER_ID,SYSTEM_USER,SYSTEM_VARIABLES_ADMIN,TABLE_ENCRYPTION_ADMIN,XA_RECOVER_ADMIN ON *.* TO `chuck`@`localhost`
2 rows in set (0.00 sec)
```
