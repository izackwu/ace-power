from conn import mysql_pool
from config import IS_NAIVE, QUERY_SQL
from typing import List, Dict


def query(author_name: str) -> Dict[str]:
    """
        The entry point for query, which will perform the query directly via MySQL
        or through Redis, RabbitMQ and MySQL.
    """
    # Naive version: query directly from MySQL
    if IS_NAIVE:
        return {
            "query": author_name,
            "status": True,
            "waiting": 0,
            "result": query_from_mysql(author_name)
        }
    # Powerful version: Redis -> RabbitMQ -> MySQL
    raise NotImplementedError


def query_from_mysql(author_name: str) -> List[Dict[str, str]]:
    connection = mysql_pool.connection()
    cursor = connection.cursor()
    result = list()
    try:
        cursor.execute(QUERY_SQL, ("%" + author_name + "%", ))
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
