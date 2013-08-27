#!/usr/bin/env python
import tornado_msgpack
import tornado
import threading

host="127.0.0.1"
port=18080

client_loop=tornado.ioloop.IOLoop()
client_thread=threading.Thread(target=lambda : client_loop.start())

client=tornado_msgpack.Client(client_loop)

# connecion status
def on_status(session):
    print("status changed: "+session.status)
client.attach_status_callback(on_status)

client.session.connect(host, port)
try:
    client_thread.start()

    # sync
    result=client.call_sync("add", 3, 4)

    # async
    future=client.call_async("add", 5, 6)
    future.join() # wait server respone
    msgpack_rpc=future.message
    result=msgpack_rpc[3]

    # async_with_callback
    def on_receive(msgpack_rpc):
        print(msgpack_rpc)
    future=client.call_async_with_callback(on_receive, "add", 5, 6)
    future.join() # wait server respone

finally:
    client_loop.stop()
    client_thread.join()
