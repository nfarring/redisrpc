#!/usr/bin/env python

import argparse
import logging
import traceback
import sys

import redis

# Allow this script to run without installing redisrpc.
sys.path.append('..')
import redisrpc

import calc


# Direct all RedisPRC logging messages to stderr.
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

parser = argparse.ArgumentParser(description='Example calculator server')
parser.add_argument('--transport', choices=('json', 'pickle'), default='json',
    help='data encoding used for transport')
args = parser.parse_args()
 
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
message_queue = 'calc'
calculator = redisrpc.Client(redis_server, message_queue, timeout=1, transport=args.transport)
do_calculations(calculator)
print('success!')
