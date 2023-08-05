import socket
import threading
import struct
import time


class SendDummy():
    def __init__(self, log_output = False, output_types = "f"):
        self.log_output = log_output
        self.HOST = '127.0.0.1'
        self.PORT = 5550
        self.conn = None
        self.data_out_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cycle_time = 0.04
        self.output_types = output_types
        self.current_x = 0.1

    def start(self):
        threading.Thread(target=self.send_loop).start()

    def send_loop(self):
        while True:
            try:
                print("[SSI Dummy Sender] Waiting for connection...")
                self.data_out_socket.connect((self.HOST, self.PORT))
                break
            except:
                print("[SSI Dummy Sender] Connected!")

        splitted_output_types = self.output_types.split(";")
        while True:

            try:
                sendstring = b'&&&'
                for structure in splitted_output_types:
                    if structure == 'f':
                        sendstring += struct.pack("f", self.current_x)
                        self.current_x += 0.1
                    if structure == 's':
                        sendstring += b'This is some foo send string. Have fun with SSI!'
                sendstring += b'###'
                if(self.log_output == True):
                    print("[SSI Dummy Sender] Data sent: " + str(sendstring))

                self.data_out_socket.sendall(sendstring)
                time.sleep(self.cycle_time)
            except:
                self.data_out_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.data_out_socket.connect((self.HOST, self.PORT))
