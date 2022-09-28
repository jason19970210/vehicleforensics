# Author: Jason
# Tester: Jason

# from utils.watchdog import Watchdog
import bluetooth as bt
import os
import sys
import time
from datetime import datetime
import subprocess
from dotenv import load_dotenv
import logging
import config as cfg

# Load .env & setup
load_dotenv()
MQ_IP = os.getenv('MQ_IP')
MQ_USERNAME = os.getenv('MQ_USERNAME')
MQ_PWD = os.getenv('MQ_PWD')
MQ_QUEUE = os.getenv('MQ_QUEUE')

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

class Client:
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


def main():
    client = Client(mac=cfg.MAC_ADDR)
    client.connect()
    time.sleep(0.2)  # Important
    client.init()

    while 1:
        try:
            for pid in cfg.PID_COMMAND_LIST:
                msg = ('01' + pid + '\r').encode('utf-8')
                # with Watchdog(2):
                #     res = client.send(msg)
                res = client.send(msg)
            time.sleep(0.05)
        except KeyboardInterrupt:
            log.debug("** KeyboardInterrupt **")
            client.disconnect()
            sys.exit()


if __name__ == '__main__':
    main()
