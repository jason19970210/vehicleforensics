from dotenv import load_dotenv
from datetime import datetime
import time, os
import pika

load_dotenv()

RABBIRMQ_HOST = os.getenv("RABBITMQ_HOST")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT"))

RABBITMQ_USERNAME = os.getenv("RABBITMQ_DEFAULT_USER")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_DEFAULT_PASS")

RABBITMQ_QUEUE = os.getenv("RABBITMQ_QUEUE")


def main():
    credentials = pika.PlainCredentials(RABBITMQ_USERNAME, RABBITMQ_PASSWORD)

    parm1 = pika.ConnectionParameters(host=RABBIRMQ_HOST, port=RABBITMQ_PORT, credentials=credentials)

    all_parm = [parm1]

    connection = pika.BlockingConnection(all_parm)
    channel = connection.channel()

    channel.queue_declare(queue=RABBITMQ_QUEUE)

    while True:
        channel.basic_publish(exchange='', routing_key=RABBITMQ_QUEUE, body=datetime.now().strftime('%H:%M:%S'))
        print(" [x] Message Sent")

        # time.sleep(0.0001)
        time.sleep(2)


if __name__ == '__main__':
    main()