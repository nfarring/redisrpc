#!/usr/bin/env ruby

require 'redis'

require_relative '../lib/redisrpc'
require_relative './calc'

redis_server = Redis.new
input_queue = 'calc'
local_object = Calculator.new
server = RedisRPC::Server.new redis_server, input_queue, local_object
server.run
