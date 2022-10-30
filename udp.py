import logging
import socket
import threading

from configuration import Config


class SensorConnection:
    def __init__(self, config, callback):
        self.config = config
        self.t = None
        self.callback = callback
        self.buffer_size = config.BUFFER_SIZE

        self.sock = socket.socket(socket.AF_INET,  # Internet
                                  socket.SOCK_DGRAM)  # UDP

        logging.info(f"Connecting to '{config.SENSOR_IP}':{config.SENSOR_PORT} with buffer size: {self.buffer_size}")
        self.sock.bind((config.SENSOR_IP, config.SENSOR_PORT))

        self.stop = False
        self.t = threading.Thread(target=self.handle, daemon=True)
        self.t.start()

    def __del__(self):
        self.stop = True

        if self.t is not None:
            self.t.join()

    def handle(self):
        while not self.stop:
            data, addr = self.sock.recvfrom(self.buffer_size)  # buffer size is 1024 bytes

            self.callback(data)


if __name__ == '__main__':
    config = Config()

    sql = SensorConnection(config, lambda x: print(x))

    while True:
        pass
