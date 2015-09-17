# compose-example
docker-compose setup example

# conf.d/mysql.yaml
This is used via ADD to the datadog agent container for monitoring mysql. Password should match the one listed in datadog.sql

# datadog.sql
This is used by the mysqldb container to add the datadog agent user and access to the database


# dd-agent.Dockerfile
This is the dockerfile for the datadog agent container

# docker-compose.yml
The docker compose file, putting it all together

# Dockerfile
This is the dockerfile used by the web container

# mysqldb.Dockerfile
This is the dockerfile used by the mysql container

# resources.txt
Various links
