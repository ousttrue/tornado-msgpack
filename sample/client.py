#!/usr/bin/env python

import tornado_msgpack


if __name__=="__main__":
    host="localhost"
    port=18080

    def status_callback(session):
        print("status:%s" % session.status)

    import tornado
    import threading
    client_loop=tornado.ioloop.IOLoop()
    client_thread=threading.Thread(target=lambda : client_loop.start())
    client=tornado_msgpack.Client(client_loop, status_callback)
    client.session.connect(host, port)
    client_thread.start()

    print("## call_sync ##")
    print(client.call_sync("add", 3, 4))

    print("## call_async ##")
    future=client.call_async("add", 1)
    future.join()
    print(future)

    print("## call_async_with_callback ##")
    def on_receive(result):
        print("on_receive:{0}".format(result))
    future=client.call_async_with_callback(on_receive, "add", 1, 2)
    future.join()

    print("done")

    client_loop.stop()
    client_thread.join()

