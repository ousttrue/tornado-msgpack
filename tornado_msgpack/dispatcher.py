import msgpack


class Dispatcher(object):

    def __init__(self, encoding="utf=8"):
        self.method_map={}
        self.packer = msgpack.Packer(encoding=encoding, default=lambda x: x.to_msgpack())

    def add_handler(self, name, method):
        self.method_map[name]=method

    def dispatch(self, msg):
        _, msgid, method, args=msg
        if not method in self.method_map:
            return self.packer.pack([1, msgid, True, "no method"]) 
        try:
            result=self.method_map[method](*args)
            return self.packer.pack([1, msgid, False, result]) 
        except Exception as ex:
            return self.packer.pack([1, msgid, True, str(ex)]) 

    def on_message(self, msg, session):
        result=self.dispatch(msg)
        session.send_async(result)

