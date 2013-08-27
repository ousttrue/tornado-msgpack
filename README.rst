tornado-msgpack
===============

Yet another MessagePack RPC for Python

history
-------
* 20130827 0.4 add logging

samples
-------

demo
++++
::

    #!/usr/bin/env python

    port=28080

    import tornado_msgpack
    dispatcher=tornado_msgpack.Dispatcher()
    def add(a, b):
        return a+b
    dispatcher.add_handler("add", add)

    with tornado_msgpack.ServerLoop("", port, dispatcher.on_message):
        with tornado_msgpack.ClientLoop("localhost", port) as client:
            print(client.call_sync("add", 3, 4))

server
++++++
::

    #!/usr/bin/env python

    import tornado_msgpack
    import tornado

    port=18080

    # dispatcher
    dispatcher=tornado_msgpack.Dispatcher()
    def add(a, b):
        return a+b
    dispatcher.add_handler("add", add)

    # server
    server_loop=tornado.ioloop.IOLoop()
    server=tornado_msgpack.Server(server_loop, dispatcher.on_message)
    server.listen(port)

    import signal
    def handler(signum, frame):
        server_loop.stop()
    signal.signal(signal.SIGINT, handler)

    try:
        # blocking...
        server_loop.start()
    except ex as KeyboardInterrupt:
        pass
 
client
++++++
::

    #!/usr/bin/env python
    import tornado_msgpack
    import tornado
    import threading

    host="127.0.0.1"
    port=18080

    client_loop=tornado.ioloop.IOLoop()
    client_thread=threading.Thread(target=lambda : client_loop.start())

    # connecion status
    def on_status(session):
        print("status changed: "+session.status)
    client=tornado_msgpack.Client(client_loop, on_status)

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
