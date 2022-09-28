from datetime import datetime
import time
import pika

# ip = "192.168.168.123"
IP = "120.126.18.131"

credentials = pika.PlainCredentials('admin', 'admin')

parm1 = pika.ConnectionParameters(host=IP, port=5672, credentials=credentials)
parm2 = pika.ConnectionParameters(host=IP, port=5673, credentials=credentials)
parm3 = pika.ConnectionParameters(host=IP, port=5674, credentials=credentials)

connection = pika.BlockingConnection([parm1, parm2, parm3])
channel = connection.channel()

channel.queue_declare(queue='hello')

while True:
    channel.basic_publish(exchange='', routing_key='hello',
                          body=datetime.now().strftime('%H:%M:%S'))
    print(" [x] Message Sent")

    # time.sleep(0.0001)
    time.sleep(2)
