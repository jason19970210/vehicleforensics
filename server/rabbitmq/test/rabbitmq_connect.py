from dotenv import load_dotenv
from datetime import datetime
import time, os
import pika

load_dotenv()

RABBIRMQ_HOST = os.getenv("RABBITMQ_HOST")
RABBITMQ_PORT = (os.getenv("RABBITMQ_PORT"))

RABBITMQ_USERNAME = os.getenv("RABBITMQ_DEFAULT_USER")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_DEFAULT_PASS")

RABBITMQ_QUEUE = os.getenv("RABBITMQ_QUEUE")
print(RABBIRMQ_HOST)

class rabbitmq_connect():
    def __init__(self,log_message):
        self.credentials = pika.PlainCredentials(RABBITMQ_USERNAME, RABBITMQ_PASSWORD)
        self.parm1 = pika.ConnectionParameters(host=RABBIRMQ_HOST, port=RABBITMQ_PORT, credentials=self.credentials)

        self.all_parm = [self.parm1]

        self.connection = pika.BlockingConnection(self.all_parm)
        self.channel = self.connection.channel()

        self.channel.queue_declare(queue=RABBITMQ_QUEUE)

        self.log_msg = log_message

    def rabbitmq_send(self):
        self.channel.basic_publish(exchange='', routing_key=RABBITMQ_QUEUE, body=self.log_msg)
        print(" [x] Message Sent")

        time.sleep(0.0001)
        # time.sleep(2)