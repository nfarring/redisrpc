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
import random
import string
import sys

import redis


__all__ = [
    'RedisRPCClient',
    'RedisRPCServer'
]


# Set this to True to print additional debugging information.
DEBUG=False


def random_string(size=8, chars=string.ascii_uppercase + string.digits):
    """Ref: http://stackoverflow.com/questions/2257441"""
    return ''.join(random.choice(chars) for x in xrange(size))


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
        name = dictionary['name']
        args = dictionary['args']
        kwargs = dictionary['kwargs']
        return FunctionCall(name, args, kwargs)

    def __init__(self, name, args=(), kwargs={}):
        """Create a new FunctionCall from a method name, an optional argument tuple, and an optional keyword argument
        dictionary."""
        self['name'] = name
        self['args'] = args
        self['kwargs'] = kwargs

    def as_python_code(self):
        """Return a string representation of this object that can be evaled to execute the function call."""
        argstring = ','.join(str(arg) for arg in self['args'])
        kwargstring = ','.join('%s=%s' % (key,val) for (key,val) in self['kwargs'].iteritems())
        if len(argstring) == 0:
            params = kwargstring
        elif len(kwargstring) == 0:
            params = argstring
        else:
            params = ','.join([argstring,kwargstring])
        return '%s(%s)' % (self['name'], params)


class RedisRPCClient(object):
    """Calls remote functions using Redis as a message queue."""

    def __init__(self, redis_server, input_queue):
        self.redis_server = redis_server
        self.input_queue = input_queue

    def call(self, method_name, *args, **kwargs):
        function_call = FunctionCall(method_name, args, kwargs)
        response_queue = self.input_queue + ':rpc:' + random_string()
        rpc_request = dict(function_call=function_call, response_queue=response_queue)
        rpc_request = json.dumps(rpc_request)
        if DEBUG: print(rpc_request)
        self.redis_server.rpush(self.input_queue, rpc_request)
        timeout_s = 0 # Block forever.
        message_queue, message = self.redis_server.blpop(response_queue, timeout_s)
        if DEBUG: print('message_queue=%r,message=%r' % (message_queue, message))
        assert message_queue == response_queue
        rpc_response = json.loads(message)
        # Assertion fails for two reasons.
        # 1. JSON strings are unicode, Python strings are not.
        # 2. Empty JSON args is list, empty Python args is sequence.
        #assert rpc_response['function_call'] == function_call
        exception = rpc_response['exception']
        if exception is not None:
            raise eval(exception)
        return rpc_response['return_value']

    def __getattr__(self, name):
        """Treat missing attributes as remote method call invocations."""
        return curry(self.call, name)


class RedisRPCServer(object):
    """Executes function calls received from a Redis queue."""

    def __init__(self, redis_server, input_queue, local_object):
        self.redis_server = redis_server
        self.input_queue = input_queue
        self.local_object = local_object

    def run(self):
        while True:
            message_queue, message = self.redis_server.blpop(self.input_queue)
            if DEBUG: print('message_queue=%r,message=%r' % (message_queue, message))
            assert message_queue == self.input_queue
            rpc_request = json.loads(message)
            response_queue = rpc_request['response_queue']
            function_call = FunctionCall.from_dict(rpc_request['function_call'])
            code = 'return_value = self.local_object.' + function_call.as_python_code()
            if DEBUG: print(code)
            try:
                exec(code)
                rpc_response = dict(function_call=function_call, return_value=return_value,exception=None)
            except:
                (type, value, traceback) = sys.exc_info()
                rpc_response = dict(function_call=function_call, return_value=None, exception=repr(value))
            rpc_response = json.dumps(rpc_response)
            if DEBUG: print('rpc_response=%r' % rpc_response)
            self.redis_server.rpush(response_queue, rpc_response)
