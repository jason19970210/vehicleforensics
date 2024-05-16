# Author: Jason
from dotenv import load_dotenv
import time
import sys
import os
import json
import ast

import binascii
import pika
from datetime import datetime
import logging

load_dotenv()

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT"))

RABBITMQ_DEFAULT_USER = os.getenv("RABBITMQ_DEFAULT_USER")
RABBITMQ_DEFAULT_PASS = os.getenv("RABBITMQ_DEFAULT_PASS")

RABBITMQ_EXCHANGE = os.getenv("RABBITMQ_EXCHANGE")
RABBITMQ_QUEUE = os.getenv("RABBITMQ_QUEUE")


log = logging.getLogger(__name__)
format_str = '%(levelname)s\t%(asctime)s -- %(filename)s:%(lineno)s %(funcName)s -- %(message)s'
console = logging.StreamHandler()
console.setFormatter(logging.Formatter(format_str))
log.addHandler(console)  # prints to console
# file_log = logging.FileHandler(f"debug_{time.time()}.log")
file_log = logging.FileHandler(f"debug_{datetime.now().strftime('%Y-%m-%d_%H:%M:%S')}.log")
file_log.setFormatter(logging.Formatter(format_str))
log.addHandler(file_log)
log.setLevel(logging.DEBUG)

class RabbitmqConnect:
    def __init__(self, host, port, credentials, exchange, queue):
        self.host = host
        self.port = port

        self.exchange = exchange
        self.queue = queue
        self.credentials = credentials

        parm1 = pika.ConnectionParameters(
            host=self.host, port=self.port, credentials=self.credentials)

        all_parm = [parm1]

        self.connection = pika.BlockingConnection(all_parm)
        self.channel = self.connection.channel()

        self.channel.exchange_declare(exchange=self.exchange, exchange_type="topic", durable=True)
        self.channel.queue_declare(queue=self.queue, durable=True, exclusive=False, auto_delete=False)
        self.channel.queue_bind(exchange=self.exchange, queue=self.queue, routing_key="vehicle.#", arguments=None)

    def callback(self, ch, method, properties, body):

        log.debug(f" [x] Received: {method.routing_key=}, {body=}")
        # time.sleep(2)

        # tmp = json.loads(body.decode())
        # cipher_polys = ast.literal_eval(tmp["cipherPolys"])
        # signature = binascii.unhexlify(tmp["sign"])
        # print(f"\ncipher_polys : {cipher_polys}\n\nsignature : {signature}")

        pass

    def start_consuming(self):
        self.channel.basic_consume(
            queue=self.queue, on_message_callback=self.callback, auto_ack=True)
        log.info(' [*] Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()
        
def main():    
    rabbitmq = RabbitmqConnect(RABBITMQ_HOST, RABBITMQ_PORT, 
                               pika.PlainCredentials(RABBITMQ_DEFAULT_USER, RABBITMQ_DEFAULT_PASS), 
                               RABBITMQ_EXCHANGE, RABBITMQ_QUEUE
                               )    
    rabbitmq.start_consuming()
    
if __name__ == '__main__':
    main()