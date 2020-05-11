from conn import mysql_pool, redis_pool
from config import IS_NAIVE, QUERY_SQL, QUERY_INTERVAL
from typing import List, Dict, Optional
import redis
import json
import _thread as thread


def query(author_name: str) -> Dict[str, object]:
    """
        The entry point for query, which will perform the query directly via MySQL
        or through Redis, RabbitMQ and MySQL.
    """
    response = {
        "query": author_name,
        "status": True,
        "waiting": 0,
        "result": []
    }
    # Naive version: query directly from MySQL
    if IS_NAIVE:
        response["result"] = query_from_mysql(author_name)
        return response
    # Powerful version: Redis -> RabbitMQ -> MySQL
    cached = query_from_redis(author_name)
    if cached is not None:  # cache hit in Redis
        response["result"] = cached
        return response
    # cache miss, then add the query into RabbitMQ
    thread.start_new_thread(add_to_rabbitmq, (author_name, ))
    # let the client wait for QUERY_INTERVAL seconds and then retry
    response["status"], response["waiting"] = False, QUERY_INTERVAL
    return response


def query_from_mysql(author_name: str) -> List[Dict[str, str]]:
    connection = mysql_pool.connection()
    cursor = connection.cursor()
    result = list()
    try:
        cursor.execute(QUERY_SQL, ("%" + author_name + "%",))
        items = cursor.fetchall()
        for author, aff in items:
            result.append({
                "author": author,
                "affiliation": aff,
            })
    except Exception as e:
        connection.rollback()
        print(e)
    finally:
        cursor.close()
        connection.close()
    return result


def query_from_redis(author_name: str) -> Optional[List[Dict[str, str]]]:
    connection = redis.Redis(connection_pool=redis_pool)
    cached = connection.get(author_name)
    if cached is None:
        return cached
    return json.loads(cached)


def add_to_rabbitmq(author_name: str) -> None:
    # as RabbitMQ is not integrated now, mock it with query_from_mysql here
    connection = redis.Redis(connection_pool=redis_pool)
    if connection.exists("waiting: " + author_name):
        print("Already in queue:", author_name)
        return
    connection.set("waiting: " + author_name, 1)
    print("Put it in queue:", author_name)
    add_to_redis(author_name, query_from_mysql(author_name), 60 * 30)
    connection.delete("waiting: " + author_name)
    print("Done:", author_name)


def add_to_redis(key: str, data: List[Dict[str, str]], ttl: int) -> bool:
    connection = redis.Redis(connection_pool=redis_pool)
    return connection.set(key, json.dumps(data), ex=ttl)
