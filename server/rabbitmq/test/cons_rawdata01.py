import time
import sys
import os
import json
import ast
from dotenv import load_dotenv
import binascii
import pika

load_dotenv()

RABBIRMQ_HOST = os.getenv("RABBITMQ_HOST")
RABBITMQ_PORT = (os.getenv("RABBITMQ_PORT"))

RABBITMQ_USERNAME = os.getenv("RABBITMQ_DEFAULT_USER")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_DEFAULT_PASS")

RABBITMQ_QUEUE = os.getenv("RABBITMQ_QUEUE")


def main():

    credentials = pika.PlainCredentials(RABBITMQ_USERNAME, RABBITMQ_PASSWORD)

    parm1 = pika.ConnectionParameters(
        host=RABBIRMQ_HOST, port=RABBITMQ_PORT, credentials=credentials)

    all_parm = [parm1]

    connection = pika.BlockingConnection(all_parm)
    channel = connection.channel()

    channel.queue_declare(queue=RABBITMQ_QUEUE)

    def callback(ch, method, properties, body):

        print(" [x] Received %r" % body)

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
