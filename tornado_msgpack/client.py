import tornado_msgpack
import msgpack
import threading
import contextlib


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
    def __init__(self, io_loop, status_callback=None, encoding="utf-8"):
        self.request_map={}
        self.request_factory=RequestFactory(encoding)
        self.session=tornado_msgpack.session.Session(io_loop, self.on_response)
        if status_callback:
            self.session.attach_status_callback(status_callback)

    def on_response(self, message, session):
        msgid=message[1]
        if msgid in self.request_map:
            #print("{0}: set_response")
            future=self.request_map[msgid]
            future.set_response(message)
        else:
            raise Exception("not found for msgid: %d!" % msgid)

    def call_async_with_callback(self, callback, method, *args):
        msgid, request=self.request_factory.create(method, *args)
        future = Future(callback)
        self.request_map[msgid] = future
        self.session.send_async(request)
        return future

    def call_async(self, method, *args):
        return self.call_async_with_callback(None, method, *args)

    def call_sync(self, method, *args):
        future=self.call_async(method, *args)
        future.join()
        if future.message[2]:
            raise Exception(future.message[3])
        return future.message[3]


@contextlib.contextmanager
def ClientLoop(host, port, status_callback=None):
    import tornado
    import threading
    client_loop=tornado.ioloop.IOLoop()
    client_thread=threading.Thread(target=lambda : client_loop.start())
    client=tornado_msgpack.Client(client_loop, status_callback)
    client.session.connect(host, port)
    client_thread.start()
    try:
        yield client
    except Exception as ex:
        raise ex
    finally:
        client_loop.stop()
        client_thread.join()

