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

    def set_response(self, message):
        with self.condition:
            self.message=message
            self.done=True
            self.condition.notifyAll()
            if self.callback:
                self.callback(self.message)


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
        self.request_map={}
        self.request_factory=RequestFactory(encoding)
        self.session=tornado_msgpack.session.Session(io_loop, self.on_response)

    def on_response(self, message, session):
        msgid=message[1]
        if msgid in self.request_map:
            print("{0}: set_response")
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

