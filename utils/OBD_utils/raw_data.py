import sys
from datetime import datetime
from canlib import canlib, Frame

class RawData:
    #[車速，轉速，冷卻液溫度，進氣溫度，進氣流量，進氣歧管壓力，節氣門位置，點火提前角，發動機負荷，剩餘油量，空燃比]
    PID_LIST = [0x0D, 0x0C, 0x05, 0x0F, 0x10, 0x0B , 0x11, 0x0E, 0x04, 0x2F, 0x44] 
    
    def __init__(self,channel_number):
        self.channel_number = channel_number

        # Specific CANlib channel number may be specified as the first argument
        if len(sys.argv) == 2:
            self.channel_number = int(sys.argv[1])

        chdata = canlib.ChannelData(self.channel_number)
        print(f"{self.channel_number}. {chdata.channel_name} ({chdata.card_upc_no} / {chdata.card_serial_no})")

        # Open CAN channel, virtual channels are considered okay to use
        self.ch = canlib.openChannel(self.channel_number, canlib.canOPEN_ACCEPT_VIRTUAL)
        self.set_bitrate()

    def set_bitrate(self):
        # Set the channel bitrate
        print("Setting bitrate to 500 kb/s")
        self.ch.setBusParams(canlib.canBITRATE_500K)
        self.ch.busOn()

    def get_chdata(self):        
        # Start listening for messages                
        frame = self.ch.read(timeout=300)

        log_message = self.msg_format(frame)
        return log_message

    def Channel_teardown(self):
        # Channel teardown
        self.ch.busOff()
        self.ch.close()          

    def msg_format(self, frame):
        # Format the message
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        if (frame.flags & canlib.canMSG_ERROR_FRAME != 0):
            log_message = "***ERROR FRAME RECEIVED***"
        else:
            log_message = "{id:0>8X}  {dlc}  {data}  {timestamp}          {current_time}".format(
                id=frame.id,
                dlc=frame.dlc,
                data=' '.join('%02x' % i for i in frame.data),
                timestamp=frame.timestamp,
                current_time=current_time
            )
            log_message = log_message.upper()
        
        return log_message

    def get_vin(self):
        vin = ""

        try:
             # Send request for VIN
            request_id = 0x7DF
            request_data = [0x02, 0x09, 0x02] + [0x00] * 5  # 0902 request VIN
            frame = Frame(id_=request_id, data=request_data)
            self.ch.write(frame)

            # Read initial response frame
            frame = self.ch.read(timeout=300)
            frames = [frame]

            #skip first 5 bytes
            vin += ''.join(chr(byte) for byte in frame.data[5:])

            # 因為VIN碼有多個frame，所以要再發送flow control frame
            flow_control_id = 0x7E0
            flow_control_data = [0x30] + [0x00] * 7  # Flow control frame
            flow_control_frame = Frame(id_=flow_control_id, data=flow_control_data)
            self.ch.write(flow_control_frame)

            # Read subsequent frames
            for i in range (2):
                frame = self.ch.read(timeout=300)
                frames.append(frame)
                response_data = frame.data
                # Join VIN data from the response frames 
                vin += ''.join(chr(byte) for byte in response_data[1:])  # Skip the first byte
                if len(vin) >= 17:  # VIN length is 17 characters
                    break

            # Print all read frames
            for frame in frames:
                print(self.msg_format(frame))

        except canlib.canError as e:
            print(f"CAN error: {e}")
        return vin if len(vin) >= 17 else None
