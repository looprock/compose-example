CREATE USER 'datadog'@'%' IDENTIFIED BY 'XXXX';
GRANT REPLICATION CLIENT ON *.* TO 'datadog'@'%' WITH MAX_USER_CONNECTIONS 5;
