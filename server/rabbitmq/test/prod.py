from dotenv import load_dotenv
from datetime import datetime
import time, os, json
import pika

load_dotenv()

RABBIRMQ_HOST = os.getenv("RABBITMQ_HOST")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT"))

RABBITMQ_USERNAME = os.getenv("RABBITMQ_DEFAULT_USER")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_DEFAULT_PASS")

RABBITMQ_EXCHANGE = os.getenv("RABBITMQ_EXCHANGE")
RABBITMQ_QUEUE = os.getenv("RABBITMQ_QUEUE")


def main():
    credentials = pika.PlainCredentials(RABBITMQ_USERNAME, RABBITMQ_PASSWORD)

    parm1 = pika.ConnectionParameters(host=RABBIRMQ_HOST, port=RABBITMQ_PORT, credentials=credentials)

    all_parm = [parm1]

    connection = pika.BlockingConnection(all_parm)
    channel = connection.channel()

    # channel.exchange_declare(exchange=RABBITMQ_QUEUE, exchange_type="topic",durable=True)
    channel.exchange_declare(exchange=RABBITMQ_EXCHANGE, exchange_type="topic", durable=True)

    # channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True, exclusive=False, auto_delete=False)

    prop = pika.BasicProperties(content_type='application/json',
                                content_encoding='utf-8',
                                # headers={'key': 'value'},
                                delivery_mode = pika.DeliveryMode.Persistent, # 2
                               )

    while True:
        # channel.basic_publish(exchange=RABBITMQ_EXCHANGE, routing_key='uplink.1.alarm', body=datetime.now().strftime('%H:%M:%S'), properties=prop)
        channel.basic_publish(exchange=RABBITMQ_EXCHANGE, routing_key='downlink.devices.OMC-TEST-PSN', body=json.dumps({"PSN": "OMC-TEST-PSN", "zone": {"zid": "123", "zonename": "zonename-test-1"}}), properties=prop)
        # print(" [x] Message Sent")

        # time.sleep(0.0001)
        time.sleep(2)


if __name__ == '__main__':
    main()
