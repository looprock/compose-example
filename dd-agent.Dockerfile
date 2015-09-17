FROM datadog/docker-dd-agent
ADD conf.d/mysql.yaml /etc/dd-agent/conf.d/mysql.yaml
