FROM mysql/mysql-server:latest
ADD datadog.sql /docker-entrypoint-initdb.d/datadog.sql
