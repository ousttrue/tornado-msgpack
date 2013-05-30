import msgpack


class Dispatcher(object):

    def __init__(self, encoding="utf=8"):
        self.method_map={}
        self.packer = msgpack.Packer(encoding=encoding, default=lambda x: x.to_msgpack())

    def add_handler(self, name, method):
        self.method_map[name]=method

    def dispatch(self, msg):
        print("dispatch")
        _, msgid, method, *args=msg
        result=None
        return self.packer.pack([1, msgid, 0, result]) 

