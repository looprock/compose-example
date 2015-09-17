#!/usr/bin/env python
from bottle import route, run, template, TEMPLATE_PATH, get, post, request, response
import MySQLdb
import os
import socket
from time import sleep
from datadog import initialize, statsd
import json

dbhost = os.environ['MYSQL_PORT_3306_TCP_ADDR']
port = os.environ['MYSQL_PORT_3306_TCP_PORT']
dbport = int(port)

options = {
    'statsd_host': os.environ['DDAGENT_PORT_8125_UDP_ADDR'],
    'statsd_port': os.environ['DDAGENT_PORT_8125_UDP_PORT'],
}

# options = {
#     'statsd_host': '192.168.99.100',
#     'statsd_port': '8125',
# }

initialize(**options)

print "Waiting for DB to become available...."
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
result = sock.connect_ex((dbhost, dbport))
while result != 0:
    print "Waiting for DB to become available...."
    sleep(10)
    result = sock.connect_ex((dbhost, dbport))


class Dbc(object):
    def __init__(self):
        self.db_host = dbhost
        self.db_port = dbport
        self.db_username = "guestbook"
        self.db_password = "guestbook"
        self.db_name = "guestbook"

    def insert(self, statement):
        conn = MySQLdb.Connection(
            host=self.db_host,
            port=self.db_port,
            user=self.db_username,
            passwd=self.db_password,
            db=self.db_name
        )
        curs = conn.cursor()
        curs.execute(statement)
        conn.commit()
        conn.close()

    def select(self, statement):
        conn = MySQLdb.Connection(
            host=self.db_host,
            user=self.db_username,
            passwd=self.db_password,
            db=self.db_name
        )
        curs = conn.cursor()
        curs.execute(statement)
        conn.commit()
        result = curs.fetchall()
        return result
        conn.close()

TEMPLATE_PATH.insert(0, '/apps/helloyou/templates/')

# create the guest table if it doesn't exist
db = Dbc()
try:
    result = db.select('select * from guests order by entered')
except:
    sql = '''CREATE table guests (
      id int(10) auto_increment NOT NULL,
      name varchar(512) NOT NULL,
      entered TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
      PRIMARY KEY (id)
    );'''
    db.insert(sql)


@get('/')
def index():
    statsd.increment('page.views.index')
    return template('index')


@post('/hello')
def hello():
    statsd.increment('page.views.hello')
    name = request.forms.get('name')
    if name:
        db = Dbc()
        db.insert('insert into guests (name) values ("%s")' % name)
        txt = '''<b>Hello {{name}}</b>!<p>
        <hr><br>
        <a href="/">Back</a><br><a href="/list">List entries</a><p>'''
        return template(txt, name=name)
    else:
        return template('index')


@route('/list')
def list():
    statsd.increment('page.views.list')
    db = Dbc()
    result = db.select('select * from guests order by entered')
    return template('list', result=result)


@route('/env')
def listenv():
    response.content_type = 'application/json'
    dump = {}
    for key in os.environ.keys():
        dump[key] = os.environ[key]
    return json.dumps(dump)

run(host='0.0.0.0', port=8080, debug=True, server='tornado')
