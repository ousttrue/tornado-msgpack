import tornado.iostream
import socket
import tornado_msgpack
import msgpack
import threading

class Future(object):
    def __init__(self, callback):
        self.callback=callback
        self.done=False
        self.message=None
        self.lock=threading.Lock()
        self.condition = threading.Condition(self.lock)

    def join(self):
        with self.condition:
            if not self.done:
                self.condition.wait()
                if self.callback:
                    self.callback(self.message)

    def set_response(self, message):
        with self.condition:
            self.message=message
            self.done=True
            self.condition.notifyAll()


class RequestFactory(object):
    def __init__(self, encoding):
        self.msgid=1
        self.packer = msgpack.Packer(encoding=encoding, default=lambda x: x.to_msgpack())

    def create(self, method, *args):
        # ToDo: lock
        msgid=self.msgid
        self.msgid+=1
        request=self.packer.pack([0, msgid, method, args])
        return msgid, request


class Client(object):
    def __init__(self, io_loop, encoding="utf-8"):
        self.io_loop=io_loop
        self.sock=None
        self.on_status=None
        self.request_map={}
        self.request_factory=RequestFactory(encoding)

    def attach_status_callback(self, on_status):
        self.on_status=on_status

    def connect(self, host, port):
        assert(self.sock==None)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        stream = tornado.iostream.IOStream(self.sock, io_loop=self.io_loop)
        self.session=tornado_msgpack.Session(stream, self.on_response, self.on_status)
        stream.connect((host, port), self.on_connect)

    def on_connect(self): 
        if self.on_status:
            self.on_status(self, "connected")
        self.session.start_reading()

    def on_response(self, message, session):
        msgid=message[1]
        if msgid in self.request_map:
            future=self.request_map[msgid]
            future.set_response(message)
        else:
            print("not found !")

    def call_async_with_callback(self, callback, method, *args):
        msgid, request=self.request_factory.create(method, *args)
        future = Future(callback)
        self.request_map[msgid] = future
        self.session.send_async(request)
        return future

