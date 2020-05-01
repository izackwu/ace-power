import pika


class Message:
    def __init__(self, body):
        self.body = body


class MQSender:
    def __init__(self, connection: pika.adapters.BaseConnection, exchange: str, routing_key: str):
        self.connection = connection
        self.channel = connection.channel()
        self.exchange = exchange
        self.routing_key = routing_key

    def send_message(self, message: Message):
        self.channel.basic_publish(self.exchange, self.routing_key, message.body)


class MQReceiver:
    def __init__(self, connection: pika.adapters.BaseConnection, queue: str, job):
        self.connection = connection
        self.channel = connection.channel()
        self.queue = queue
        self.callback = lambda ch, method, properties, body: job(body)

    def receive_message(self):
        self.channel.basic_consume(self.queue, self.callback)
