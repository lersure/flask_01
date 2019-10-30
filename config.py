# encoding:utf-8
import os

SECRET_KEY = os.urandom(24)
DIALECT = 'mysql'
DRIVER = 'mysqlconnector'
HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'FLASK_SQL_DEMO'
USERNAME = 'root'
PASSWORD = 'root'
SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(DIALECT, DRIVER, USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = False  # 关闭对模型修改的监控
