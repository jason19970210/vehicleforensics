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

# Load .env & setup
load_dotenv()

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT"))

RABBITMQ_USERNAME = os.getenv("RABBITMQ_DEFAULT_USER")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_DEFAULT_PASS")

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
        self.sock.connect((self.mac, self.port))
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
    
class RabbitmqConnect():
    def __init__(self, msg):
        self.credentials = pika.PlainCredentials(RABBITMQ_USERNAME, RABBITMQ_PASSWORD)
        self.parameters = pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT, credentials=self.credentials)

        self.connection = pika.BlockingConnection(self.parameters)
        self.channel = self.connection.channel()

        self.channel.exchange_declare(exchange=RABBITMQ_EXCHANGE, exchange_type="topic", durable=True)
        self.prop = pika.BasicProperties(content_type='application/json',
                                content_encoding='utf-8',
                                # headers={'key': 'value'},
                                delivery_mode = pika.DeliveryMode.Persistent, # 2
                               )

        self.msg = json.dumps(msg)
    def rabbitmq_send(self):
        self.channel.basic_publish(exchange=RABBITMQ_EXCHANGE, routing_key='downlink.devices.OMC-TEST-PSN', body=self.msg , properties=self.prop)
        print(" [x] Message Sent")

        time.sleep(0.0001)
        # time.sleep(2)

class RawData():
    def __init__(self):
        # start_time = time.time()

        self.channel_number = 0

    def get_chdata(self):
        # Specific CANlib channel number may be specified as the first argument

        if len(sys.argv) == 2:
            self.channel_number = int(sys.argv[1])

        chdata = canlib.ChannelData(self.channel_number)
        print(f"{self.channel_number}. {chdata.channel_name} ({chdata.card_upc_no} / {chdata.card_serial_no})")


        # Open CAN channel, virtual channels are considered okay to use
        ch = canlib.openChannel(self.channel_number, canlib.canOPEN_ACCEPT_VIRTUAL)

        print("Setting bitrate to 500 kb/s")
        ch.setBusParams(canlib.canBITRATE_500K)
        ch.busOn()

        # Start listening for messages
        finished = False
        while not finished:
            try:
                frame = ch.read(timeout=300)
                if frame.id == 0x7E8:
                    self.print_frame(frame)
                    self.rabbitmq_send(frame)
                time.sleep(0.1)
            
            except (canlib.canNoMsg):
                pass
            except (canlib.canError) as ex:
                print(ex)
                finished = True

        # Channel teardown
        ch.busOff()
        ch.close()
    def msg_format(self, frame):
        # Format the message
        current_time = datetime.now(pytz.timezone('Asia/Taipei')).strftime("%Y-%m-%d %H:%M:%S ")
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
        json_message = json_format(log_message)
        
        return json_message
    
    def print_frame(self, frame):
        log_message = self.msg_format(frame)
        print(log_message)

    
    def rabbitmq_send(self, frame):
        json_message = self.msg_format(frame)      
        # Send the message to RabbitMQ
        connect_rabbitmq = RabbitmqConnect(json_message)
        connect_rabbitmq.rabbitmq_send()
    
def json_format(frame):
    # Format the message
    parts = frame.split()
    message_type = "ERROR" if "***ERROR" in frame else "DATA"
    id = parts[0]
    dlc = int(parts[1])
    data = [parts[i] for i in range(2, 10)]
    current_time = parts[10]
    json_message={
        "PSN": "OMC-TEST-PSN",
        "zone":{
                "message_type": message_type,
                "id": id,
                "dlc": dlc,
                "data": data,
                "current_time": current_time,
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

    '''
    Use for connecting BLE dongle with sending request frame to OBD-II interface
    '''
    if args.hw == 'ble':
        import bluetooth as bt

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
                    res = json_format(res)

                    connect_rabbitmq = RabbitmqConnect(res)
                    connect_rabbitmq.rabbitmq_send()

                time.sleep(0.05)
            except KeyboardInterrupt:
                log.debug("** KeyboardInterrupt **")
                ble_client.disconnect()
                sys.exit()

    elif args.hw == 'kvaser':

        # TODO: get message from Kvaser & Canlib

        # TODO: send message to rabbitmq
        produce_rawdata = RawData()
        produce_rawdata.get_chdata()
        
    else:
        msg = f"Argument Error: {args.hw}"
        log.error(msg)
        raise ValueError(msg)

if __name__ == '__main__':
    main()
