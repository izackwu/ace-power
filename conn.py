import pymysql
from DBUtils.PooledDB import PooledDB
import redis
import pika
from config import *

mysql_pool = PooledDB(pymysql,
                      host=MYSQL_HOST,
                      port=MYSQL_PORT,
                      user=MYSQL_USER,
                      passwd=MYSQL_PASSWORD,
                      db=MYSQL_DB,
                      charset=MYSQL_CHARSET)

redis_pool = redis.ConnectionPool(host=REDIS_HOST,
                                  port=REDIS_PORT,
                                  password=REDIS_PASSWORD)

# As suggested, one connection is enough for one application, so there's no pool
rabbitmq_conn = pika.BlockingConnection(
    pika.ConnectionParameters(host=RABBITMQ_HOST,
                              port=RABBITMQ_PORT))
