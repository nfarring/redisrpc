RedisRPC
========

by Nathan Farrington http://nathanfarrington.com

Introduction
------------

`Redis <http://redis.io/>`_ is a powerful in-memory data structure
server that is useful for building fast distributed systems. Redis
implements message queue functionality with its use of list data
structures and the ``LPOP``, ``BLPOP``, and ``RPUSH`` commands. RedisRPC
implements a lightweight RPC mechanism using Redis message queues to
temporarily hold RPC request and response messages. These messages are
encoded as JSON strings for portability.

Many other RPC mechanisms are either programming language specific (e.g.
`Java
RMI <https://en.wikipedia.org/wiki/Java_remote_method_invocation>`_) or
require boiler-plate code for explicit typing (e.g.
`Thrift <https://en.wikipedia.org/wiki/Apache_Thrift>`_). RedisRPC was
designed to be extremely easy to use by eliminating boiler-plate code
while also being programming language neutral. High performance was not
an initial goal of RedisRPC and other RPC libraries are likely to have
better performance. Instead, RedisRPC has better programmer performance;
it lets you get something working immediately.

Brief Example
-------------

Here is a brief example using Python. The full source is in the
``examples/`` directory.

client.py
~~~~~~~~~

::

    redis_server = redis.Redis()
    calculator = redisrpc.RedisRPCClient(redis_server, 'calc')
    calculator.clr()
    calculator.add(5)
    calculator.sub(3)
    calculator.mul(4)
    calcaultor.div(2)
    assert calculator.val() == 4

server.py
~~~~~~~~~

::

    redis_server = redis.Redis()
    server = redisrpc.RedisRPCServer(redis_server, 'calc', calc.Calculator())
    server.run()

That's all there is to it. The server wraps a local object, in this case
a Calculator object. It listens for RPC requests from the 'calc' message
queue. When it receives a request, it executes it on the calculator
object and returns the result to the client. If an exception occurs then
the exception is sent to the client.

Notice that the client doesn't actually access the Calculator class.
Instead its method invocations are intercepted and wrapped into RPC
requests that are forwarded to the server. The return values embedded in
the RPC responses are used for the values of the expressions.

Source Code
-----------

Source code is available at http://github.com/nfarring/redisrpc.

License
-------

This software is available under the GPLv3 or later. See the file
``LICENSE`` for more information.
