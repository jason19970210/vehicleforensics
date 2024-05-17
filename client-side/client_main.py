# Author: Jason
# Tester: Jason

# from utils.watchdog import Watchdog
import os
import sys
import time, pytz
from datetime import datetime
import subprocess
from dotenv import load_dotenv
import logging
import config as cfg
import argparse
import pika
from canlib import canlib, Frame
import json

import bluetooth as bt

# Load .env & setup
load_dotenv()

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT"))

RABBITMQ_DEFAULT_USER = os.getenv("RABBITMQ_DEFAULT_USER")
RABBITMQ_DEFAULT_PASS = os.getenv("RABBITMQ_DEFAULT_PASS")

RABBITMQ_EXCHANGE = os.getenv("RABBITMQ_EXCHANGE")
RABBITMQ_QUEUE = os.getenv("RABBITMQ_QUEUE")

# Logging Config
# https://www.loggly.com/blog/4-reasons-a-python-logging-library-is-much-better-than-putting-print-statements-everywhere/#gist21143108
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

class BleClient:
    def __init__(self, mac, port=1):
        self.mac = mac
        self.port = port
        log.info('Client Inited')

    def connect(self):
        self.sock = bt.BluetoothSocket(bt.RFCOMM)
        log.info('Client connecting ...')
        self.sock
        if self.connected:
            log.info('Connection Established')

    def init(self):
        for cmd in cfg.INIT_COMMAND_LIST:
            msg = (cmd + '\r').encode('utf-8')
            _ = self.send(msg)

    def disconnect(self):
        log.info('Connection Closed')
        self.sock.close()
        self.sock = None

    '''
    Blocking send / recv
    '''
    def send(self, msg):
        self.sock.send(msg)
        log.debug(f'send msg : {msg}')
        # time.sleep(0.01) # 500ms
        res: bytes = self.sock.recv(1024)

        log.debug(f' recv msg : {res}')
        return res.decode('utf-8')

    @property
    def connected(self):
        # https://github.com/Thor77/Blueproximity/blob/79b20fce260f761785e35a041b30ff7005b8d883/blueproximity/device.py
        p = subprocess.run(
            ['hcitool', 'lq', self.mac],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return p.returncode == 0
    
class RabbitmqConnect:
    def __init__(self, host: str, port:int, credentials:dict, exchange:str, queue:str):
        self.host = host
        self.port = port
        self.credentials = credentials
        self.exchange = exchange
        self.queue = queue

        parm1 = pika.ConnectionParameters(host=self.host, port=self.port, credentials=self.credentials)
        all_parm = [parm1]

        self.connection = pika.BlockingConnection(all_parm)

        self.channel = self.connection.channel()

        self.channel.exchange_declare(self.exchange, exchange_type="topic", durable=True)
        self.prop = pika.BasicProperties(content_type='application/json',
                                content_encoding='utf-8',
                                # headers={'key': 'value'},
                                delivery_mode = pika.DeliveryMode.Persistent, # 2
                               )

    def rabbitmq_send(self, msg, routing_key):
        self.msg = json.dumps(msg)
        self.channel.basic_publish(self.exchange, routing_key=routing_key,
                                   body=self.msg , properties=self.prop
                                   )
        print(" [x] Message Sent")

        time.sleep(0.0001)
        # time.sleep(2)

class RawData:
    def __init__(self,channel_number):
        # start_time = time.time()
        self.channel_number = channel_number

        # Specific CANlib channel number may be specified as the first argument
        if len(sys.argv) == 2:
            self.channel_number = int(sys.argv[1])

        chdata = canlib.ChannelData(self.channel_number)
        log.info(f"{self.channel_number}. {chdata.channel_name} ({chdata.card_upc_no} / {chdata.card_serial_no})")

        # Open CAN channel, virtual channels are considered okay to use
        self.ch = canlib.openChannel(self.channel_number, canlib.canOPEN_ACCEPT_VIRTUAL)
        self.set_bitrate()

    def set_bitrate(self):
        # Set the channel bitrate
        log.info("Setting bitrate to 500 kb/s")
        self.ch.setBusParams(canlib.canBITRATE_500K)
        self.ch.busOn()

    def get_chdata(self):        
        # Start listening for messages                
        frame = self.ch.read(timeout=300)

        log_message = self.msg_format(frame)
        log.debug(log_message)

        return log_message


    def Channel_teardown(self):
        # Channel teardown
        self.ch.busOff()
        self.ch.close()          


    def msg_format(self, frame):
        # Format the message
        current_time=datetime.now(pytz.timezone('Asia/Taipei')).strftime("%Y-%m-%d %H:%M:%S ")
        if (frame.flags & canlib.canMSG_ERROR_FRAME != 0):
            log_message = "***ERROR FRAME RECEIVED***"
        else:
            # log_message = "{id:0>8X}  {dlc}  {data}  {timestamp}          {current_time}".format(
            log_message = "{id:0>8X}  {dlc}  {data}  {current_time}".format(
                id=frame.id,
                dlc=frame.dlc,
                data=' '.join('%02x' % i for i in frame.data),
                # timestamp=frame.timestamp,
                current_time=current_time,
            )
        log_message = log_message.upper()        
        return log_message
    
def json_format(frame, routing_key):
    # Format the json message
    parts = frame.split()
    message_type = "ERROR" if "***ERROR" in frame else "DATA"
    id = parts[0]
    dlc = int(parts[1])
    data = [parts[i] for i in range(2, 10)]
    current_time = datetime.strptime(f"{parts[10]} {parts[11]}", "%Y-%m-%d %H:%M:%S")
    routing_key = routing_key
    json_message = {
        "hardware" : routing_key,
        "zone": {
            "message_type": message_type,
            "id": id,
            "dlc": dlc,
            "data": data,
            "current_time": current_time.strftime("%Y-%m-%d %H:%M:%S"),
        }
    }
    return json_message

def main():

    arg_parser = argparse.ArgumentParser(
        # prog="", # default: sys.argv[0]
        # description="Vehicle Forensics Cloud System - Client"
    )

    arg_parser.add_argument('--hw', '--hardware', choices=['kvaser', 'ble'], required=True)

    args = arg_parser.parse_args()

    # TODO: create rqbbitmq instance for produce & consume

    rabbitmq = RabbitmqConnect(RABBITMQ_HOST, RABBITMQ_PORT,
                               pika.PlainCredentials(RABBITMQ_DEFAULT_USER, RABBITMQ_DEFAULT_PASS),
                               RABBITMQ_EXCHANGE, RABBITMQ_QUEUE
                               )
    '''
    Use for connecting BLE dongle with sending request frame to OBD-II interface
    '''
    if args.hw == 'ble':


        ble_client = BleClient(mac=cfg.MAC_ADDR)
        ble_client.connect()
        time.sleep(0.2)  # Important
        ble_client.init()

        while 1:
            try:
                for pid in cfg.PID_COMMAND_LIST:
                    msg = ('01' + pid + '\r').encode('utf-8')
                    # with Watchdog(2):
                    #     res = client.send(msg)
                    res = ble_client.send(msg)

                    # TODO: send message to rabbitmq
                    routing_key = 'vehicle.ble'
                    res = json_format(res, routing_key)
                    rabbitmq.rabbitmq_send(res, routing_key)

                time.sleep(0.05)
            except KeyboardInterrupt:
                log.debug("** KeyboardInterrupt **")
                ble_client.disconnect()
                sys.exit()

    elif args.hw == 'kvaser':

        # TODO: get message from Kvaser & Canlib

        # TODO: send message to rabbitmq
        rawdata = RawData(0)
        finished = False
        while not finished:
            try:

                res=rawdata.get_chdata()
                routing_key =  'vehicle.kvaser' 
                res=json_format(res, routing_key)
                rabbitmq.rabbitmq_send(res, routing_key)

            except (canlib.canNoMsg):
                pass
            except (canlib.canError) as ex:
                log.error(ex)
                finished = True
            except (pika.exceptions.AMQPError) as ex:
                log.error(f"RabbitMQ error: {ex}")
            except (Exception) as ex:
                log.error(f"Unexpected error: {ex}")
        rawdata.Channel_teardown()
        
    else:
        msg = f"Argument Error: {args.hw}"
        log.error(msg)
        raise ValueError(msg)

if __name__ == '__main__':
    main()

