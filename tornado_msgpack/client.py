import tornado.iostream
import socket
import tornado_msgpack


class Future(object):
    def join(self):
        pass


class Client(object):
    def __init__(self, ioloop):
        tornado.iostream.IOStream
        self.sock=None
        self.on_status=None
        self.request_map={}

    def attach_status_callback(self, on_status):
        self.on_status=on_status

    def connect(self, host, port):
        assert(self.sock==None)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        stream = tornado.iostream.IOStream(self.sock)
        self.session=tornado_msgpack.Session(stream, self.on_response, self.on_status)
        stream.connect((host, port), self.on_connect)

    def on_connect(self): 
        if self.on_status:
            self.on_status(self, "connected")

    def on_response(self, message, session):
        print(message)
        # unpack
        # error or not
        # set response

    def call_async_with_callback(self, callback, name, *args):
        f=Future()
        return f

