#!/usr/bin/env python

import tornado_msgpack


if __name__=="__main__":
    port=18080

    with tornado_msgpack.ClientLoop("localhost", port) as client:

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

