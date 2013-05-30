import tornado.tcpserver

class Server(object):
    def __init__(self, ioloop):
        self.tcpserver=tornado.tcpserver.TCPServer(io_loop=ioloop)

    def listen(self, port):
        self.tcpserver.listen(port)

