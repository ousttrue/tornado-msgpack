import msgpack
import threading
import socket
import tornado.iostream


class Session(object):
    STATUS_NOT_CONNECTED='NOT CONNECTED'
    STATUS_CONNECTING='CONNECTING'
    STATUS_CONNECTED='CONNECTED'
    STATUS_CLOSING='CLOSING'

    def __init__(self, io_loop, on_message, encoding="utf-8"):
        self.io_loop=io_loop
        self.stream=None
        self.on_message=on_message
        self.unpacker = msgpack.Unpacker(encoding=encoding)
        self._status=Session.STATUS_NOT_CONNECTED
        self.on_status=None

    # status
    def set_status(self, status):
        if self._status==status:
            return
        self._status=status
        if self.on_status:
            self.on_status(self)
    def get_status(self):
        return self._status
    status=property(get_status, set_status)

    def attach_status_callback(self, on_status):
        self.on_status=on_status

    def is_connected(self):
        return self.status==Session.STATUS_CONNECTED

    def connect(self, host, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        self.stream = tornado.iostream.IOStream(sock, io_loop=self.io_loop)
        self.stream.set_close_callback(self.on_close)
        self.stream.connect((host, port), self.on_connect)
        self.status=Session.STATUS_CONNECTING

    def on_connect(self): 
        self.status=Session.STATUS_CONNECTED
        self.start_reading()

    def start_reading(self):
        self.stream.read_until_close(self.on_read, self.on_read)

    def on_read(self, data):
        #print("{0}:on_read {1} bytes".format(threading.current_thread(), len(data)))
        self.unpacker.feed(data)
        for message in self.unpacker:
            #print(message)
            self.on_message(message, self)

    def on_close(self):
        self.status=Session.STATUS_NOT_CONNECTED

    def send_async(self, data):
        #print("{0}:send {1} bytes".format(threading.current_thread(), len(data)))
        self.stream.write(data)

