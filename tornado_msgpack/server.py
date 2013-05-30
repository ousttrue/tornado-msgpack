import tornado.tcpserver
import tornado_msgpack


class Server(tornado.tcpserver.TCPServer):
    def __init__(self, io_loop, on_message, on_status=None):
        super(Server, self).__init__(io_loop)
        self.session_map={}
        self.on_message=on_message
        self.on_status=on_status

    def handle_stream(self, stream, address):
        session=tornado_msgpack.Session(stream, self.on_message, self.on_status)
        self.session_map[address]=session
        session.start_reading()

