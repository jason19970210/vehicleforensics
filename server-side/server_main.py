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
import threading

from pathlib import Path
sys.path.append(Path(__file__).parents[1].as_posix())
from utils.mongodb_utils.mongodb import MongodbConnect
from utils.rabbitmq_utils.rabbitmq import RabbitmqConsumer

load_dotenv()

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT"))

RABBITMQ_USERNAME = os.getenv("RABBITMQ_USERNAME")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD")

RABBITMQ_EXCHANGE = os.getenv("RABBITMQ_EXCHANGE")
RABBITMQ_QUEUE = os.getenv("RABBITMQ_QUEUE")

MONGODB_HOST = os.getenv("MONGODB_HOST")
MONGODB_PORT = int(os.getenv("MONGODB_PORT"))

MONGODB_USERNAME = os.getenv("MONGODB_USERNAME")
MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD")
MONGODB_DBNAME = os.getenv("MONGODB_DBNAME")


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

def main():
    mongodb_client = MongodbConnect(MONGODB_HOST, MONGODB_PORT, 
                                MONGODB_USERNAME, MONGODB_PASSWORD, 
                                MONGODB_DBNAME, None
                                )  
    rabbitmq = RabbitmqConsumer(RABBITMQ_HOST, RABBITMQ_PORT, 
                               pika.PlainCredentials(RABBITMQ_USERNAME, RABBITMQ_PASSWORD), 
                               RABBITMQ_EXCHANGE, RABBITMQ_QUEUE, mongodb_client
                               )    
    rabbitmq.channel.basic_consume(queue=rabbitmq.queue, on_message_callback=rabbitmq.vin_callback, auto_ack=True)
    log.info(' [*] Waiting for messages. To exit press CTRL+C')
    rabbitmq.channel.start_consuming()
                            
if __name__ == '__main__':
    main()