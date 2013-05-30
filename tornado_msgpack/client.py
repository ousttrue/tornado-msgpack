class Future(object):
    def join(self):
        pass


class Client(object):
    def __init__(self, ioloop):
        self.on_status=None

    def attach_status_callback(self, on_status):
        self.on_status=on_status

    def connect(self, host, port):
        pass

    def call_async_with_callback(self, callback, name, *args):
        f=Future()
        return f

