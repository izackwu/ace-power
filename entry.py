from conn import mysql_pool, redis_pool, get_rabbitmq_conn
from config import IS_NAIVE, QUERY_SQL, QUERY_INTERVAL, QUEUE_NAME
from typing import List, Dict, Optional
import redis
import json
import pika


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
    add_to_rabbitmq(author_name)
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


def test_and_incr_in_redis(flag: str) -> int:
    connection = redis.Redis(connection_pool=redis_pool)
    return connection.incr(flag)


def add_to_rabbitmq(author_name: str) -> None:
    flag_key = "Waiting: " + author_name
    # atomically check whether author_name has already been added to the queue
    if test_and_incr_in_redis(flag_key) != 1:
        print("Already in queue or redis: ", author_name)
        return
    rabbitmq_conn = get_rabbitmq_conn()
    rabbitmq_channel = rabbitmq_conn.channel()
    rabbitmq_channel.queue_declare(queue=QUEUE_NAME, durable=True)
    rabbitmq_channel.basic_publish(
        exchange="",
        routing_key=QUEUE_NAME,
        body=author_name,
        properties=pika.BasicProperties(
            delivery_mode=2,    # make message persistent
        )
    )
    rabbitmq_conn.close()
    print("Add to the queue: ", author_name)


def add_to_redis(key: str, data: List[Dict[str, str]], ttl: int) -> bool:
    connection = redis.Redis(connection_pool=redis_pool)
    print("Add to redis: ", key, data, ttl)
    return connection.set(key, json.dumps(data), ex=ttl)
