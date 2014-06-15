#!/usr/bin/env python

import argparse
import logging
import sys

import redis

# Allow this script to run without installing redisrpc.
sys.path.append('..')
import redisrpc

import calc


# Direct all RedisPRC logging messages to stderr.
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

redis_server = redis.Redis()
message_queue = 'calc'
local_object = calc.Calculator()
server = redisrpc.Server(redis_server, message_queue, local_object)
server.run()
