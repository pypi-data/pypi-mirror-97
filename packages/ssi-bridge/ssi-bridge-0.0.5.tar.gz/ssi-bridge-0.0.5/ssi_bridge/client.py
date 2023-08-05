import socket
import threading
import queue
from ssi_bridge.util import parse_input_packet, convert_single_value
import struct

class client():
    def __init__(
            self,
            host='127.0.0.1',
            data_in_port = 5550,
            data_out_port = 5551,
            meta_in_port = 5552,
            meta_out_port = 5553,
            transform_enter = None,
            transform = None,
            transform_exit = None,
            input_types = None,
            output_types = None
    ):
        self.host = host
        self.data_in_port = data_in_port
        self.data_out_port = data_out_port
        self.meta_in_port = meta_in_port
        self.meta_out_port = meta_out_port
        self.transform_enter = transform_enter
        self.transform = transform
        self.transform_exit = transform_exit
        self.input_types = input_types
        self.output_types = output_types

        self.input_structure = None


        self.data_in_fifo = queue.Queue()
        self.data_out_fifo = queue.Queue()

        self.data_in_socket = None
        self.data_out_socket = None

        self.max_transfer_bytes = 1024

        # Set following flag True if the transform function shall not be executed in parallel,
        # e.g. if the transform function relies on the result of the former run of the transform function
        self.transform_blocking = True

        # Don't change the following flag, it's used internally for blocking functionality of the transform function
        self.transform_blocking_flag = False

        self.receive_blocking = True
        self.receive_blocking_flag = False

        self.send_blocking = True
        self.send_blocking_flag = False

        self.data_in_queue_overlap = b''


    def establish_connections(self):
        while(True):
            try:
                print("Establishing connection to SSI sender ...\n")
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.bind((self.host, self.data_in_port))
                s.listen()
                self.data_in_socket, addr = s.accept()
                print("Established connection to SSI sender.\n")
                break
            except:
                pass
        while (True):
            try:
                print("Establishing connection to SSI receiver ...\n")
                self.data_out_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.data_out_socket.connect((self.host, self.data_out_port))
                print("Established connection to SSI receiver.\n")
                break
            except:
                pass

    def start(self):
        self.establish_connections()
        threading.Thread(target=self.receive_data_from_socket).start()
        threading.Thread(target=self.execute_transform).start()
        threading.Thread(target=self.send_data_to_socket).start()

    def send_data_to_socket(self):
        while True:
            if self.send_blocking:
                if self.send_blocking_flag == False:
                    self.send_blocking_flag = True
                    data = self.convert_to_bytes(self.data_out_fifo.get())
                    self.data_out_socket.sendall(data)
                    self.send_blocking_flag = False
            else:
                data = bytearray(str(self.data_out_fifo.get()), 'UTF-8')
                self.data_out_socket.sendall(data)

    def receive_data_from_socket(self):
        while(True):
            if self.receive_blocking == True:
                if(self.receive_blocking_flag == False):
                    self.receive_blocking_flag = True
                    data = self.data_in_socket.recv(self.max_transfer_bytes)
                    self.format_and_enqueue_data(data)
                    self.receive_blocking_flag = False

            else:
                data = self.data_in_socket.recv(self.max_transfer_bytes)
                self.format_and_enqueue_data(data)

    def format_and_enqueue_data(self,data):
        new_overlap, parsed_data = parse_input_packet(self.data_in_queue_overlap, data)
        for data_point in parsed_data:
            self.data_in_fifo.put(data_point)
        self.data_in_queue_overlap = new_overlap

    def set_host(self, host):
        self.host = host

    def set_data_in_port(self, data_in_port):
        self.data_in_port = data_in_port

    def set_data_out_port(self, data_out_port):
        self.data_out_port = data_out_port

    def set_meta_in_port(self, meta_in_port):
        self.meta_in_port = meta_in_port

    def set_meta_out_port(self, meta_out_port):
        self.meta_out_port = meta_out_port

    def set_transform_enter(self, transform_enter):
        self.transform_enter = transform_enter

    def set_transform(self, transform):
        self.transform = transform

    def set_transform_exit(self,transform_exit):
        self.transform_exit = transform_exit

    def execute_transform(self):
        while True:
            if self.transform_blocking == True:

                if(self.transform_blocking_flag == False):
                    self.transform_blocking_flag = True
                    if not self.data_in_fifo.empty():
                        ret_structure = self.convert_to_structure(self.data_in_fifo.get())
                        ret_structure = self.transform(ret_structure)
                        self.data_out_fifo.put(ret_structure)
                    self.transform_blocking_flag = False



            else:
                if not self.data_in_fifo.empty():
                    ret_structure = self.convert_to_structure(self.data_in_fifo.get())
                    ret_structure = self.transform(ret_structure)
                    self.data_out_fifo.put(ret_structure)

    def convert_to_structure(self, input):
        ret_structure = []
        remaining_input = input
        splitted_input_types = self.input_types.split(";")
        if len(splitted_input_types) == 1:
            return convert_single_value(input, self.input_types)[1]

        for structure in splitted_input_types:
            remaining_input, ret_value = convert_single_value(remaining_input, structure)
            ret_structure.append(ret_value)
        return ret_structure

    def convert_to_bytes(self, data):
        if (self.output_types == 'f'):
            tmp = struct.pack("f",data)
        if (self.output_types == 's'):
            tmp = str(data).encode('utf-8')
        return b'&&&' + tmp + b'###'


