# -*- encoding: utf-8 -*-
require File.expand_path('../lib/redisrpc/version', __FILE__)

Gem::Specification.new do |s|
  s.name = 'redisrpc'
  s.version = RedisRPC::VERSION
  s.license = 'GPLv3'
  s.authors = ['Nathan Farrington']
  s.email = ['nathan@nathanfarrington.com']

  s.homepage = 'http://github.com/nfarring/redisrpc'
  s.summary = 'Lightweight RPC for Redis'
  s.description = <<-DESCRIPTION
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
  DESCRIPTION
  s.has_rdoc = false
  
  s.files         = `git ls-files`.split("\n")
  s.test_files    = `git ls-files -- {test,spec,features}/*`.split("\n")
  s.executables   = `git ls-files -- bin/*`.split("\n").map{ |f| File.basename(f) }
  s.require_paths = ["lib"]

  s.add_runtime_dependency 'redis'
  s.add_runtime_dependency 'multi_json', '~>1.3'

  s.add_development_dependency 'bundler'
  s.add_development_dependency 'rake'
  s.add_development_dependency 'rspec'
end
