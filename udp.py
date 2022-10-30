import socket
import threading

from configuration import Config


class SensorConnection:
    def __init__(self, config, callback):
        self.config = config
        self.callback = callback

        self.sock = socket.socket(socket.AF_INET,  # Internet
                                  socket.SOCK_DGRAM)  # UDP
        self.sock.bind((config.SENSOR_IP, config.SENSOR_PORT))

        self.stop = False
        self.t = threading.Thread(target=self.handle, daemon=True)
        self.t.start()

    def __del__(self):
        self.stop = True
        self.t.join()

    def handle(self):
        while not self.stop:
            data, addr = self.sock.recvfrom(1024)  # buffer size is 1024 bytes

            self.callback(data)


if __name__ == '__main__':
    config = Config()

    sql = SensorConnection(config, lambda x: print(x))

    while True:
        pass
