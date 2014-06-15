import threading

import redis
import redisrpc

import pytest

TIMEOUT=5

class Bar(object):
    """A class used only for serialization."""
    def __init__(self):
        self.a = 1
        self.b = 2
        self.c = 3
    def __eq__(self, rhs):
        try:
            return self.a == rhs.a and self.b == rhs.b and self.c == rhs.c
        except:
            return False

class Foo(object):
    """A class used for redisrpc testing."""
    MESSAGE_QUEUE = 'foo'
    def return_none(self):
        return None
    def return_true(self):
        return True
    def return_false(self):
        return False
    def return_int(self):
        return 1
    def return_float(self):
        return 3.14159
    def return_string(self):
        return "STRING"
    def return_list(self):
        return [1, 2, 3]
    def return_dict(self):
        return dict(a=1, b=2)
    def return_obj(self):
        return Bar()

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

def test_redisrpc_true(redisdb):
    server = start_thread(redisdb)
    client = redisrpc.Client(redisdb, Foo.MESSAGE_QUEUE, timeout=TIMEOUT)
    assert client.return_true() is True

def test_redisrpc_false(redisdb):
    server = start_thread(redisdb)
    client = redisrpc.Client(redisdb, Foo.MESSAGE_QUEUE, timeout=TIMEOUT)
    assert client.return_false() is False

def test_redisrpc_int(redisdb):
    server = start_thread(redisdb)
    client = redisrpc.Client(redisdb, Foo.MESSAGE_QUEUE, timeout=TIMEOUT)
    assert client.return_int() == 1

def test_redisrpc_float(redisdb):
    server = start_thread(redisdb)
    client = redisrpc.Client(redisdb, Foo.MESSAGE_QUEUE, timeout=TIMEOUT)
    assert abs(client.return_float() - 3.14159) < 1e-15

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

def test_redisrpc_obj(redisdb):
    """Objects are not JSON serializable by default."""
    server = start_thread(redisdb)
    client = redisrpc.Client(redisdb, Foo.MESSAGE_QUEUE, timeout=TIMEOUT, transport='pickle')
    assert client.return_obj() == Bar()
