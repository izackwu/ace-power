from config import *
from DBUtils.PooledDB import PooledDB
import pymysql

mysql_pool = PooledDB(pymysql,
                      host=MYSQL_HOST,
                      port=MYSQL_PORT,
                      user=MYSQL_USER,
                      passwd=MYSQL_PASSWORD,
                      db=MYSQL_DB,
                      charset=MYSQL_CHARSET)
