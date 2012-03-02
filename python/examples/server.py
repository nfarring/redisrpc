#!/usr/bin/env python

import logging
import sys

import redis
import redisrpc

import calc


# Direct all RedisPRC logging messages to stderr.
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


redis_server = redis.Redis()
input_queue = 'calc'
local_object = calc.Calculator()
server = redisrpc.Server(redis_server, input_queue, local_object)
server.run()
