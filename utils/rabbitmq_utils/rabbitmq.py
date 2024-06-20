import threading
import json
import pika
import time
from utils.mongodb_utils.mongodb import MongodbConnect


class RabbitmqConsumer:
    def __init__(self, host: str, port: int, credentials: dict, exchange: str, queue: str, mongo_client: MongodbConnect):
        self.host = host
        self.port = port
        self.exchange = exchange
        self.queue = queue
        self.credentials = credentials
        self.mongo_client = mongo_client

        parameters = pika.ConnectionParameters(host=self.host, port=self.port, credentials=self.credentials)
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

        self.channel.exchange_declare(exchange=self.exchange, exchange_type="topic", durable=True)
        self.channel.queue_declare(queue=self.queue, durable=True, exclusive=False, auto_delete=False)
        self.channel.queue_bind(exchange=self.exchange, queue=self.queue, routing_key="uplink.vin")

    def vin_callback(self, ch, method, properties, body):
        try:
            message = json.loads(body)
            print(f"Received message: {message}")
            producer_vin = message.split("VIN:")[1].strip()
            self.setup_queue(producer_vin)
        except KeyError:
            print(f"Message does not contain 'VIN': {message}")
        except json.JSONDecodeError:
            print(f"Failed to decode JSON message: {body}")

    def setup_queue(self, producer_vin):
        queue_name = f'queue_{producer_vin}'
        binding_key = f'uplink.{producer_vin}.#'

        # Declare the queue
        self.channel.queue_declare(queue=queue_name, durable=True, exclusive=False, auto_delete=False)
        self.channel.queue_bind(exchange=self.exchange, queue=queue_name, routing_key=binding_key)

        def producer_callback(ch, method, properties, body):
            print(f"Received message from producer {producer_vin}: {body.decode()}")
            self.mongo_client.set_collection(f"VIN_{producer_vin}")
            self.mongo_client.insert_mongodb(json.loads(body.decode()))

        self.channel.basic_consume(queue=queue_name, on_message_callback=producer_callback, auto_ack=True)
        print(f"Queue {queue_name} bound to {binding_key} and consuming messages.")

        # Start consuming in a new thread to avoid blocking
        thread = threading.Thread(target=self.consume_queue)
        thread.start()

    def consume_queue(self):
        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            print(f"Stopped consuming {self.queue}")
            self.channel.stop_consuming()

class RabbitmqProducer:
    def __init__(self, host: str, port: int, credentials: dict, exchange: str, queue: str):
        self.host = host
        self.port = port
        self.credentials = credentials
        self.exchange = exchange
        self.queue = queue

        parameters = pika.ConnectionParameters(host=self.host, port=self.port, credentials=self.credentials)
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

        self.channel.exchange_declare(exchange=self.exchange, exchange_type="topic", durable=True)
        self.prop = pika.BasicProperties(content_type='application/json',
                                         content_encoding='utf-8',
                                         delivery_mode=pika.DeliveryMode.Persistent)

    def rabbitmq_send(self, msg, routing_key):
        msg_json = json.dumps(msg)
        self.channel.basic_publish(exchange=self.exchange, routing_key=routing_key,
                                   body=msg_json, properties=self.prop)
        print("[x]Message sent.")

        #time.sleep(0.0001)
        
