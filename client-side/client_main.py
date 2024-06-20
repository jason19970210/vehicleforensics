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
from pathlib import Path

sys.path.append(Path(__file__).parents[1].as_posix())
from utils.OBD_utils.raw_data import RawData
from utils.rabbitmq_utils.rabbitmq import RabbitmqProducer

import bluetooth as bt

# Load .env & setup
load_dotenv()

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT"))

RABBITMQ_USERNAME = os.getenv("RABBITMQ_USERNAME")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD")

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
    
def json_format(frame):
    # Format the json message
    parts = frame.split()
    message_type = "ERROR" if "***ERROR" in frame else "DATA"
    id = parts[0]
    dlc = int(parts[1])
    data = [parts[i] for i in range(2, 10)]
    timestamp = parts[10]
    current_time = datetime.strptime(f"{parts[11]} {parts[12]}", "%Y-%m-%d %H:%M:%S.%f")
    json_message = {       
        "message_type": message_type,
        "id": id,
        "dlc": dlc,
        "data": data,
        "timestamp": timestamp,
        "current_time": current_time.strftime("%Y-%m-%d %H:%M:%S.%f"),       
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

    rabbitmq = RabbitmqProducer(RABBITMQ_HOST, RABBITMQ_PORT,
                               pika.PlainCredentials(RABBITMQ_USERNAME, RABBITMQ_PASSWORD),
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
                    routing_key = f"uplink.{pid}.data"
                    res = json_format(res)
                    rabbitmq.rabbitmq_send(res, routing_key)

                time.sleep(0.05)
            except KeyboardInterrupt:
                log.debug("** KeyboardInterrupt **")
                ble_client.disconnect()
                sys.exit()

    elif args.hw == 'kvaser':
        from canlib import canlib, Frame
        # TODO: get message from Kvaser & Canlib

        # TODO: send message to rabbitmq
        rawdata = RawData(0)
        vin = rawdata.get_vin()       
        rabbitmq.rabbitmq_send(f"VIN: {vin}", "uplink.vin")

        finished = False
        while not finished:           
            for pid in rawdata.PID_LIST:
                try:
                    data = [2, 1, pid, 0, 0, 0, 0, 0]
                    frame = Frame(id_=0x7DF, data=data)

                    rawdata.ch.writeWait(frame,timeout=500)
                    res=rawdata.get_chdata() 

                    json_string=json_format(res)
                    log.info(json_string)

                except (canlib.canTimeout) as ex:
                    log.error(ex)    
                except (canlib.canNoMsg) as ex:
                    log.error(ex)
                except (canlib.canError) as ex:
                    log.error(ex)
                    finished = True
                else:
                    if json_string['message_type'] == 'DATA':
                        routing_key = (f"uplink.{vin}.{pid}.data")
                    else:
                        routing_key = (f"uplink.{vin}.{pid}.error")
                try:            
                    rabbitmq.rabbitmq_send(json_string, routing_key)
                    #time.sleep(0.000125)#8000 筆/秒

                except (pika.exceptions.AMQPError) as ex:
                    log.error(f"RabbitMQ error: {ex}")
                except (Exception) as ex:
                    log.error(f"Unexpected error: {ex}")
                    finished = True

        rawdata.Channel_teardown()
        
    else:
        msg = f"Argument Error: {args.hw}"
        log.error(msg)
        raise ValueError(msg)

if __name__ == '__main__':
    main()

