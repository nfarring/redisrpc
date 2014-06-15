import threading

import redis
import redisrpc

import pytest

TIMEOUT=5

class Foo(object):
    """A class used for redisrpc testing."""
    MESSAGE_QUEUE = 'foo'
    def return_none(self):
        return None
    def return_int(self):
        return 1
    def return_string(self):
        return "STRING"
    def return_list(self):
        return [1, 2, 3]
    def return_dict(self):
        return dict(a=1, b=2)

def start_thread(redisdb):
    """Run the redisrpc server in a thread."""
    local_object = Foo()
    server = redisrpc.Server(redisdb, Foo.MESSAGE_QUEUE, local_object)
    def target():
        server.run()
    server_thread = threading.Thread(target=target)
    server_thread.daemon = True
    server_thread.start()

def test_redis(redisdb):
    """Test the redisdb fixture."""
    redisdb.set('woof', 'woof')
    woof = redisdb.get('woof')
    assert woof == 'woof'

def test_redisrpc_none(redisdb):
    server = start_thread(redisdb)
    client = redisrpc.Client(redisdb, Foo.MESSAGE_QUEUE, timeout=TIMEOUT)
    assert client.return_none() is None

def test_redisrpc_int(redisdb):
    server = start_thread(redisdb)
    client = redisrpc.Client(redisdb, Foo.MESSAGE_QUEUE, timeout=TIMEOUT)
    assert client.return_int() == 1

def test_redisrpc_string(redisdb):
    server = start_thread(redisdb)
    client = redisrpc.Client(redisdb, Foo.MESSAGE_QUEUE, timeout=TIMEOUT)
    assert client.return_string() == "STRING"

def test_redisrpc_list(redisdb):
    server = start_thread(redisdb)
    client = redisrpc.Client(redisdb, Foo.MESSAGE_QUEUE, timeout=TIMEOUT)
    assert client.return_list() == [1, 2, 3]

def test_redisrpc_dict(redisdb):
    server = start_thread(redisdb)
    client = redisrpc.Client(redisdb, Foo.MESSAGE_QUEUE, timeout=TIMEOUT)
    assert client.return_dict() == dict(a=1, b=2)
