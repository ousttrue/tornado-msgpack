import tornado.tcpserver
import tornado_msgpack
import contextlib


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


@contextlib.contextmanager
def ServerLoop(host, port, on_message):
    import tornado
    import threading
    # server
    server_loop=tornado.ioloop.IOLoop()
    server_thread=threading.Thread(target=lambda : server_loop.start())
    server=tornado_msgpack.Server(server_loop, on_message)
    server.listen(port)
    server_thread.start()
    try:
        yield
    finally:
        server_loop.stop()
        server_thread.join()

