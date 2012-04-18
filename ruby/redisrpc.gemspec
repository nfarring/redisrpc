# -*- encoding: utf-8 -*-

require File.expand_path('../lib/redisrpc/version', __FILE__)

DESCRIPTION = <<-EOS
RedisRPC is the easiest to use RPC library in the world. (No small claim!) It
has implementations in Ruby, PHP, and Python.

Redis is a powerful in-memory data structure server that is useful for building
fast distributed systems. Redis implements message queue functionality with its
use of list data structures and the `LPOP`, `BLPOP`, and `RPUSH` commands.
RedisRPC implements a lightweight RPC mechanism using Redis message queues to
temporarily hold RPC request and response messages. These messages are encoded
as JSON strings for portability.

Many other RPC mechanisms are either programming language specific (e.g.
Java RMI) or require boiler-plate code for explicit typing (e.g. Thrift).
RedisRPC was designed to be extremely easy to use by eliminating boiler-plate
code while also being programming language neutral.  High performance was not
an initial goal of RedisRPC and other RPC libraries are likely to have better
performance. Instead, RedisRPC has better programmer performance; it lets you
get something working immediately.
EOS

Gem::Specification.new do |s|
  s.add_runtime_dependency 'redis', '< 3.0.0'
  s.author = 'Nathan Farrington'
  s.date = Time.now.strftime('%Y-%m-%d')
  s.description = DESCRIPTION
  s.email = 'nfarring@gmail.com'
  s.has_rdoc = false
  s.files = ['lib/redisrpc.rb']
  s.homepage = 'http://github.com/nfarring/redisrpc'
  s.license = 'GPLv3'
  s.name = 'redisrpc'
  s.summary = 'Lightweight RPC for Redis'
  s.version = RedisRPC::VERSION
end
