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

require 'json'

require 'redis'

module RedisRPC


    class RemoteException<Exception
    end


    class TimeoutException<Exception
    end


    class FunctionCall

        def initialize(args={})
            @method = args['name'].to_sym
            @args = args['args']
        end

        attr_reader :method
        attr_reader :args
    end


    class Client

        def initialize(redis_server, message_queue, timeout=0)
            @redis_server = redis_server
            @message_queue = message_queue
            @timeout = timeout
        end

        def method_missing(sym, *args, &block)
            function_call = {'name' => sym.to_s, 'args' => args}
            response_queue = @message_queue + ':rpc:' + rand_string
            rpc_request = {'function_call' => function_call, 'response_queue' => response_queue}
            message = JSON.generate rpc_request
            if $DEBUG
                $stderr.puts 'RPC Request: ' + message
            end
            @redis_server.rpush @message_queue, message
            result = @redis_server.blpop response_queue, @timeout
            if result.nil?
                raise TimeoutException
            end
            message_queue, message = result
            if $DEBUG
                if message_queue != response_queue
                    fail 'assertion failed'
                end
                $stderr.puts 'RPC Response: ' + message
            end
            rpc_response = JSON.parse message
            exception = rpc_response['exception']
            if exception != nil
                raise RemoteException, exception
            end
            if not rpc_response.has_key? 'return_value'
                raise RemoteException, 'Malformed RPC Response message: ' + rpc_response
            end
            return rpc_response['return_value']
        end 

        def rand_string(size=8, charset=%w{ 1 2 3 4 5 6 7 8 9 0 A B C D E F G H I J K L M N O P Q R S T U V W X Y Z})
            return (0...size).map{ charset.to_a[rand(charset.size)] }.join
        end

        def respond_to?(sym)
            return true
        end

    end


    class Server

        def initialize(redis_server, message_queue, local_object)
            @redis_server = redis_server
            @message_queue = message_queue
            @local_object = local_object
        end

        def run
            # Flush the message queue.
            @redis_server.del @message_queue
            loop do
                message_queue, message = @redis_server.blpop @message_queue, 0
                if $DEBUG
                    fail 'assertion failed' if message_queue != @message_queue
                    $stderr.puts 'RPC Request: ' + message
                end
                rpc_request = JSON.parse(message)
                response_queue = rpc_request['response_queue']
                function_call = FunctionCall.new(rpc_request['function_call'])
                begin
                    return_value = @local_object.send( function_call.method, *function_call.args )
                    rpc_response = {'return_value' => return_value}
                rescue => err
                    rpc_response = {'exception' => err}
                end
                message = JSON.generate rpc_response
                if $DEBUG
                    $stderr.puts 'RPC Response: ' + message
                end
                @redis_server.rpush response_queue, message
            end
        end

    end


end
