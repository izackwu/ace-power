from conn import rabbitmq_conn
from config import QUEUE_NAME, EXPIRE_TIME
from entry import query_from_mysql, add_to_redis

channel = rabbitmq_conn.channel()
channel.queue_declare(queue=QUEUE_NAME, durable=True)


def handle_message(ch, method, properties, body):
    author_name = body.decode()
    print(author_name, type(author_name))
    print("Start to handle: ", author_name)
    data = query_from_mysql(author_name)
    add_to_redis(author_name, data, EXPIRE_TIME * 60)
    # let the waiting flag expire
    add_to_redis("Waiting: " + author_name, None, EXPIRE_TIME * 60)
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print("Done: ", author_name)


print("Waiting for messages to handle...")
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=QUEUE_NAME, on_message_callback=handle_message)
channel.start_consuming()
