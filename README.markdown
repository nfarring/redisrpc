RedisRPC
========

by Nathan Farrington
<http://nathanfarrington.com>

Introduction
------------

[Redis][Redis] is a powerful in-memory data structure server that is useful
for building fast distributed systems. Redis implements message queue
functionality with its use of list data structures and the `LPOP`, `BLPOP`,
and `RPUSH` commands. RedisRPC implements a lightweight RPC mechanism using
Redis message queues to temporarily hold RPC request and response
messages. These messages are encoded as [JSON][JSON] strings for portability.

Many other RPC mechanisms are either programming language specific (e.g. [Java
RMI][JavaRMI]) or require boiler-plate code for explicit typing (e.g.
[Thrift][Thrift]). RedisRPC was designed to be extremely easy to use by
eliminating boiler-plate code while also being programming language neutral.
High performance was not an initial goal of RedisRPC and other RPC libraries
are likely to have better performance. Instead, RedisRPC has better programmer
performance; it lets you get something working immediately.

Brief Example
-------------

Here is a brief example using Python. The full source is in the
`python/examples/` directory.

<img
src="http://github.com/nfarring/redisrpc/raw/master/docs/redisrpc_example.png"
width=438 height=238>

### client.py

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

### server.py

```python
redis_server = redis.Redis()
server = redisrpc.RedisRPCServer(redis_server, 'calc', calc.Calculator())
server.run()
```

That's all there is to it. The server wraps a local object, in this case
a Calculator object. It listens for RPC requests from the 'calc' message
queue. When it receives a request, it executes it on the Calculator object
and returns the result to the client. If an exception occurs then the
exception is sent to the client.

Notice that the client doesn't actually access the Calculator class. Instead
its method invocations are intercepted and wrapped into RPC requests that are
forwarded to the server. The return values embedded in the RPC responses are
used for the values of the expressions.

Message Formats
---------------
All RPC messages are JSON objects.

### RPC Request
An RPC Request contains two members: a `function_call` object and
a `response_queue` string.

A `function_call` object has three members: a `name` string for the function
name, an `args` list for positional function arguments, and a `kwargs` object
for named function arguments.

The `response_queue` string is the name of the Redis list where the
corresponding RPC Response message should be pushed by the server. This queue
is chosen programmatically by the client to be collision free in the Redis
namespace.  Also, this queue is used only for a single RPC Response message
and is not reused for future RPC Response messages.

```javascript
{ "function_call" : {
      "args" : [ 1, 2, 3 ],
      "kwargs" : { "a" : 4, "b" : 5, "c" : 6 },
      "name" : "foo"
    },
  "response_queue" : "calc:rpc:X7Y2US"
}
```

### RPC Response (Successful)
If an RPC is successful, then the RPC Response object will contain a single
member, a `return_value` of some JSON type.

```javascript
{ "return_value" : 4.0 }
```

### RPC Response (Exception)
If an RPC encounters an exceptional condition, then the RPC Response object
will contain a single member, an `exception` string. Note that the value of
the `exception` string might not have any meaning to the client since the
client and server might be written in different languages or the client
might have no knowledge of the server's wrapped object. Therefore the best
course of action is probably to display the `exception` value to the user.

```javascript
{ "exception" : "AttributeError(\\"\'Calculator\' object has no attribute \'foo\'\\",)" }
```

Source Code
-----------
Source code is available at <http://github.com/nfarring/redisrpc>.

License
-------
This software is available under the [GPLv3][GPLv3] or later.

Version History
---------------
Version 0.1.0 - February 16, 2012

* First versioned release.
* Changed license from BSD to GPL: go freedom!
* Removed an option to perform client-side run-time type idenfication in Python.

February 14, 2012

* Initial release.

[Redis]: http://redis.io/

[JSON]: http://json.org/

[JavaRMI]: https://en.wikipedia.org/wiki/Java_remote_method_invocation

[Thrift]: https://en.wikipedia.org/wiki/Apache_Thrift

[GPLv3]: http://www.gnu.org/licenses/gpl.html
