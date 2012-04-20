#!/usr/bin/env ruby

require 'redis'

require File.expand_path('../../lib/redisrpc', __FILE__)
require File.expand_path('../calc', __FILE__)

def assert(cond)
    if not cond
        fail 'assertion failed'
    end
end

def do_calculations(calculator)
    calculator.clr
    calculator.add 5
    calculator.sub 3
    calculator.mul 4
    calculator.div 2
    assert calculator.val == 4
    begin
        calculator.missing_method
        assert false
    rescue NoMethodError
    rescue RedisRPC::RemoteException
    end
end

# 1. Local object
calculator = Calculator.new
do_calculations calculator

# 2. Remote object, should act like local object
redis_server = Redis.new
message_queue = 'calc'
timeout = 1
calculator = RedisRPC::Client.new redis_server, message_queue, timeout
do_calculations calculator
puts 'success!'
