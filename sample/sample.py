#!/usr/bin/env python

import tornado_msgpack
import tornado.ioloop
import threading


if __name__=="__main__":
    port=18080

    # dispatcher
    dispatcher=tornado_msgpack.Dispatcher()
    def add(a, b):
        return a+b
    dispatcher.add_handler("add", add)

    def starter(target):
        def func():
            print("{0} start".format(target))
            target.start()
            print("{0} finished".format(target))
        return func
    
    # server
    server_loop=tornado.ioloop.IOLoop()
    server_thread=threading.Thread(target=starter(server_loop))
    server=tornado_msgpack.Server(server_loop, dispatcher.on_message)
    server.listen(port)
    server_thread.start()

    # client
    client_loop=tornado.ioloop.IOLoop()
    client_thread=threading.Thread(target=starter(client_loop))
    client=tornado_msgpack.Client(client_loop)
    def on_status_changed(session, status):
        print(status)
    client.session.attach_status_callback(on_status_changed)
    client.session.connect("localhost", port)
    client_thread.start()

    # request
    def on_receive(result):
        print("on_receive:{0}".format(result))

    future=client.call_async_with_callback(on_receive, "add", 1)
    future.join()

    future=client.call_async_with_callback(on_receive, "add", 1, 2)
    future.join()

    future=client.call_async_with_callback(on_receive, "add", 1, 2, 3)
    future.join()

    print("stop client...")
    client_loop.stop()
    client_thread.join()

    print("stop server...")
    server_loop.stop()
    server_thread.join()

    print("done")

