from datetime import datetime
import time, os

import sys
from canlib import canlib

from rabbitmq_connect import rabbitmq_connect

class raw_data():
    def __init__(self):
        # start_time = time.time()

        self.channel_number = 0

        self.get_chdata()

    def get_chdata(self):
        # Specific CANlib channel number may be specified as the first argument
        if len(sys.argv) == 2:
            self.channel_number = int(sys.argv[1])

        chdata = canlib.ChannelData(self.channel_number)
        print("%d. %s (%s / %s)" % (self.channel_number, chdata.channel_name,
                                    chdata.card_upc_no,
                                    chdata.card_serial_no))

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
                self.print_frame(frame)
            except (canlib.canNoMsg):
                pass
            except (canlib.canError) as ex:
                print(ex)
                finished = True

        # Channel teardown
        ch.busOff()
        ch.close()

    def print_frame(self, frame):
        """Prints a message to screen and logs it to the specified file"""
        current_time = datetime.now().strftime("%Y-%m-%d-%H%M%S.%f")
        if (frame.flags & canlib.canMSG_ERROR_FRAME != 0):
            log_message = "***ERROR FRAME RECEIVED***"
        else:
            # log_message = "{id:0>8X}  {dlc}  {data}  {timestamp}          {current_time}".format(
            log_message = "{id:0>8X}  {dlc}  {data}  {current_time}".format(
                id=frame.id,
                dlc=frame.dlc,
                data=' '.join('%02x' % i for i in frame.data),
                # timestamp=frame.timestamp,
                current_time=current_time
            )
        log_message = log_message.upper()
        print(log_message)

        connect_rabbitmq = rabbitmq_connect(log_message)
        connect_rabbitmq.rabbitmq_send()
    

def main():
    raw_data()

if __name__ == '__main__':
    main()