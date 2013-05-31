import tornado.tcpserver
import tornado_msgpack


class Server(tornado.tcpserver.TCPServer):
    def __init__(self, io_loop, on_message):
        super(Server, self).__init__(io_loop)
        self.session_map={}
        self.on_message=on_message
        self.keeper=tornado.ioloop.PeriodicCallback(lambda : 0, 50000, self.io_loop)
        self.keeper.start()

    def handle_stream(self, stream, address):
        session=tornado_msgpack.Session(self.io_loop, self.on_message)
        session.stream=stream
        self.session_map[address]=session
        session.start_reading()

