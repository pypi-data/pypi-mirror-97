import socket
import threading

class ReceiveDummy():
    def __init__(self, log_input = False):
        self.log_input = log_input
        self.HOST = '127.0.0.1'
        self.PORT = 5551
        self.conn = None
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((self.HOST, self.PORT))

    def start(self):
        threading.Thread(target=self.receive_loop).start()

    def receive_loop(self):
        self.s.listen()
        print("[SSI Dummy Receiver] Waiting for connection...")
        conn, addr = self.s.accept()
        print("[SSI Dummy Receiver] Connected!")
        while True:
            test = conn.recv(1024)
            if(self.log_input):
                print("[SSI Dummy Receiver] Received data: " + str(test))


