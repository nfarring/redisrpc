#!/usr/bin/env python

import logging
import traceback
import sys

import redis
import redisrpc

import calc


# Direct all RedisPRC logging messages to stderr.
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


def do_calculations(calculator):
    calculator.clr()
    calculator.add(5)
    calculator.sub(3)
    calculator.mul(4)
    calculator.div(2)
    assert calculator.val() == 4
    try:
        calculator.missing_method()
        assert False
    except (AttributeError, redisrpc.RemoteException):
        pass


# 1. Local object
calculator = calc.Calculator()
do_calculations(calculator)

# 2. Remote object, should act like local object
redis_server = redis.Redis()
input_queue = 'calc'
calculator = redisrpc.Client(redis_server, input_queue)
do_calculations(calculator)
print('success!')
