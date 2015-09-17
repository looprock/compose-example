FROM ubuntu:14.04
RUN apt-get -y update && apt-get -y install git python-mysqldb python-pip mysql-client && pip install bottle tornado datadog
EXPOSE 8080
CMD ["/apps/helloyou/helloyou.py"]
