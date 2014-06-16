# Copyright (C) 2012.  Nathan Farrington <nfarring@gmail.com>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import json
import logging
import pickle
import random
import string
import sys

import redis


__all__ = [
    'Client',
    'Server',
    'RemoteException',
    'TimeoutException'
]

if sys.version_info < (3,):
    range = xrange

def random_string(size=8, chars=string.ascii_uppercase + string.digits):
    """Ref: http://stackoverflow.com/questions/2257441"""
    return ''.join(random.choice(chars) for x in range(size))


class curry:
    """Ref: https://jonathanharrington.wordpress.com/2007/11/01/currying-and-python-a-practical-example/"""

    def __init__(self, fun, *args, **kwargs):
        self.fun = fun
        self.pending = args[:]
        self.kwargs = kwargs.copy()

    def __call__(self, *args, **kwargs):
        if kwargs and self.kwargs:
            kw = self.kwargs.copy()
            kw.update(kwargs)
        else:
            kw = kwargs or self.kwargs
            return self.fun(*(self.pending + args), **kw)


class FunctionCall(dict):
    """Encapsulates a function call as a Python dictionary."""

    @staticmethod
    def from_dict(dictionary):
        """Return a new FunctionCall from a Python dictionary."""
        name = dictionary.get('name')
        args = dictionary.get('args')
        kwargs = dictionary.get('kwargs')
        return FunctionCall(name, args, kwargs)

    def __init__(self, name, args=None, kwargs=None):
        """Create a new FunctionCall from a method name, an optional argument tuple, and an optional keyword argument
        dictionary."""
        self['name'] = name
        if args is not None and args != ():
            self['args'] = args
        if kwargs is not None and kwargs != {}:
            self['kwargs'] = kwargs

    def as_python_code(self):
        """Return a string representation of this object that can be evaled to execute the function call."""
        argstring = '' if 'args' not in self else \
                ','.join(str(arg) for arg in self['args'])
        kwargstring = '' if 'kwargs' not in self else \
                ','.join('%s=%s' % (key,val) for (key,val) in list(self['kwargs'].items()))
        if len(argstring) == 0:
            params = kwargstring
        elif len(kwargstring) == 0:
            params = argstring
        else:
            params = ','.join([argstring,kwargstring])
        return '%s(%s)' % (self['name'], params)


def decode_message(message):
    """Returns a (transport, decoded_message) pair."""
    # Try JSON, then try Python pickle, then fail.
    try:
        return JSONTransport.create(), json.loads(message.decode())
    except:
        pass
    return PickleTransport.create(), pickle.loads(message)


class JSONTransport(object):
    """Cross platform transport."""
    _singleton = None
    @classmethod
    def create(cls):
        if cls._singleton is None:
            cls._singleton = JSONTransport()
        return cls._singleton
    def dumps(self, obj):
        return json.dumps(obj)
    def loads(self, obj):
        return json.loads(obj.decode())


class PickleTransport(object):
    """Only works with Python clients and servers."""
    _singleton = None
    @classmethod
    def create(cls):
        if cls._singleton is None:
            cls._singleton = PickleTransport()
        return cls._singleton
    def dumps(self, obj):
        # Version 2 works for Python 2.3 and later
        return pickle.dumps(obj, protocol=2)
    def loads(self, obj):
        return pickle.loads(obj)
 
class Client(object):
    """Calls remote functions using Redis as a message queue."""

    def __init__(self, redis_server, message_queue, timeout=0, transport='json'):
        self.redis_server = redis_server
        self.message_queue = message_queue
        self.timeout = timeout
        if transport == 'json':
            self.transport = JSONTransport()
        elif transport == 'pickle':
            self.transport = PickleTransport()
        else:
            raise Exception('invalid transport {0}'.format(transport))

    def call(self, method_name, *args, **kwargs):
        function_call = FunctionCall(method_name, args, kwargs)
        response_queue = self.message_queue + ':rpc:' + random_string()
        rpc_request = dict(function_call=function_call, response_queue=response_queue)
        message = self.transport.dumps(rpc_request)
        logging.debug('RPC Request: %s' % message)
        self.redis_server.rpush(self.message_queue, message)
        result = self.redis_server.blpop(response_queue, self.timeout)
        if result is None:
            raise TimeoutException()
        message_queue, message = result
        message_queue = message_queue.decode()
        assert message_queue == response_queue
        logging.debug('RPC Response: %s' % message)
        rpc_response = self.transport.loads(message)
        exception = rpc_response.get('exception')
        if exception is not None:
            raise RemoteException(exception)
        if 'return_value' not in rpc_response:
            raise RemoteException('Malformed RPC Response message: %s' % rpc_response)
        return rpc_response['return_value']

    def __getattr__(self, name):
        """Treat missing attributes as remote method call invocations."""
        return curry(self.call, name)


class Server(object):
    """Executes function calls received from a Redis queue."""

    def __init__(self, redis_server, message_queue, local_object):
        self.redis_server = redis_server
        self.message_queue = message_queue
        self.local_object = local_object
 
    def run(self):
        # Flush the message queue.
        self.redis_server.delete(self.message_queue)
        while True:
            message_queue, message = self.redis_server.blpop(self.message_queue)
            message_queue = message_queue.decode()
            assert message_queue == self.message_queue
            logging.debug('RPC Request: %s' % message)
            transport, rpc_request = decode_message(message)
            response_queue = rpc_request['response_queue']
            function_call = FunctionCall.from_dict(rpc_request['function_call'])
            code = 'self.return_value = self.local_object.' + function_call.as_python_code()
            try:
                exec(code)
                rpc_response = dict(return_value=self.return_value)
            except:
                (type, value, traceback) = sys.exc_info()
                rpc_response = dict(exception=repr(value))
            message = transport.dumps(rpc_response)
            logging.debug('RPC Response: %s' % message)
            self.redis_server.rpush(response_queue, message)


class RemoteException(Exception):
    """Raised by an RPC client when an exception occurs on the RPC server."""
    pass


class TimeoutException(Exception):
    """Raised by an RPC client when a timeout occurs."""
    pass
