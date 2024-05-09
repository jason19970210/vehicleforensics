# Author: Jason
from dotenv import load_dotenv
import time
import sys
import os
import json
import ast

import binascii
import pika

load_dotenv()

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT"))

RABBITMQ_USERNAME = os.getenv("RABBITMQ_DEFAULT_USER")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_DEFAULT_PASS")

RABBITMQ_EXCHANGE = os.getenv("RABBITMQ_EXCHANGE")
RABBITMQ_QUEUE = os.getenv("RABBITMQ_QUEUE")

def main():
    credentials = pika.PlainCredentials(RABBITMQ_USERNAME, RABBITMQ_PASSWORD)

    parm1 = pika.ConnectionParameters(
        host=RABBITMQ_HOST, port=RABBITMQ_PORT, credentials=credentials)

    all_parm = [parm1]

    connection = pika.BlockingConnection(all_parm)
    channel = connection.channel()

    channel.exchange_declare(exchange=RABBITMQ_EXCHANGE, exchange_type="topic", durable=True)
    channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True, exclusive=False, auto_delete=False)
    channel.queue_bind(exchange=RABBITMQ_EXCHANGE, queue=RABBITMQ_QUEUE, routing_key="#", arguments=None)


    def callback(ch, method, properties, body):

        print(f" [x] Received: {method.routing_key=}, {body=}")
        # time.sleep(2)

        # tmp = json.loads(body.decode())
        # cipher_polys = ast.literal_eval(tmp["cipherPolys"])
        # signature = binascii.unhexlify(tmp["sign"])
        # print(f"\ncipher_polys : {cipher_polys}\n\nsignature : {signature}")

        pass

    channel.basic_consume(
        queue=RABBITMQ_QUEUE, on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    main()