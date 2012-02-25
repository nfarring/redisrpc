#!/usr/bin/env python

import redis
import redisrpc

import calc

#redisrpc.DEBUG=True

redis_server = redis.Redis()
server = redisrpc.Server(redis_server, 'calc', calc.Calculator())
server.run()
