redisrpc
========

by Nathan Farrington
<http://nathanfarrington.com>

Introduction
------------

[Redis][Redis] is a powerful in-memory data structure server that is useful
for building fast distributed systems. Redis implements message queue
functionality with its use of list data structures and the `LPOP`, `BLPOP`,
and `RPUSH` commands. The `redisrpc` library implements a lightweight RPC
mechanism using Redis message queues to temporarily hold RPC request and RPC
response messages. These messages are encoded as JSON strings for portability.

Many other RPC mechanisms are either programming language specific (e.g. [Java
RMI][JavaRMI]) or requires boiler-plate code for explicit typing (e.g.
[Thrift][Thrift]). `redisrpc` was designed to be extremely easy to use at the
expense of performance. It lets you get it working now and tune the
performance later if it becomes necessary.

Brief Example
-------------

Here is a brief example using Python. The full source is in the
`python/examples/` directory.

<img src="docs/redisrpc_example.png" width=438 height=238>

client.py

```python
redis_server = redis.Redis()
calculator = redisrpc.RedisRPCClient(redis_server, 'calc')
calculator.clr()
calculator.add(5)
calculator.sub(3)
calculator.mul(4)
calcaultor.div(2)
assert calculator.val() == 4
```

server.py

```python
redis_server = redis.Redis()
server = redisrpc.RedisRPCServer(redis_server, 'calc', calc.Calculator())
server.run()
```

That's all there is to it. The server wraps a local object, in this case
a Calculator object. It listens for RPC requests from the 'calc' message
queue. When it receives a request, it executes it on the calculator object
and returns the result to the client. If an exception occurs then the
exception is sent to the client.

Notice that the client doesn't actually access the Calculator class. Instead
its method invocations are intercepted and wrapped into RPC requests that are
forwarded to the server. The return values embedded in the RPC responses are
used for the values of the expressions.

Message Format
--------------

rpc_request





rpc_response


Source Code
-----------
Source code is available at <http://github.com/nfarring/redisrpc>.

License
-------
The redisrpc code is distributed under a BSD license. See the file `LICENSE`
for more information.

Version History
---------------
February 14, 2012

* Initial release.

[Redis]: http://redis.io/

[JavaRMI]: https://en.wikipedia.org/wiki/Java_remote_method_invocation

[Thrift]: https://en.wikipedia.org/wiki/Apache_Thrift
