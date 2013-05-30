import msgpack


class Session(object):
    def __init__(self, stream, on_message, on_status, encoding="utf-8"):
        stream.set_close_callback(self.on_close)
        self.stream=stream
        self.on_message=on_message
        self.on_status=on_status
        self.unpacker = msgpack.Unpacker(encoding=encoding)

    def on_read(self, data):
        self.unpacker.feed(data)
        for message in self.unpacker:
            self.on_message(message, self)

    def on_close(self):
        if self.on_status:
            self.on_status(self, "closed")

