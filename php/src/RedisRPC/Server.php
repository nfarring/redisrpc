<?php

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

namespace RedisRPC;

# Ref: http://www.php.net/manual/en/language.constants.php
if (!function_exists("debug_print")) { 
    if ( defined('DEBUG') && TRUE===DEBUG ) { 
        function debug_print($string,$flag=NULL) { 
            /* if second argument is absent or TRUE, print */ 
            if ( !(FALSE===$flag) ) 
                #print 'DEBUG: '.$string . "\n"; 
                print $string . "\n"; 
        } 
    } else { 
        function debug_print($string,$flag=NULL) { 
        } 
    } 
} 

/**
 * Executes function calls received from a Redis queue.
 *
 * @author Nathan Farrington <nfarring@gmail.com>
 */
class Server {

    private $redis_server;
    private $message_queue;
    private $local_object;

    /**
     * Initializes a new server.
     *
     * @param mixed $redis_server Handle to a Redis server object.
     * @param string $message_queue Name of Redis message queue.
     * @param mixed $local_object Handle to local wrapped object that will receive the RPC calls.
     */
    public function __construct($redis_server, $message_queue, $local_object) {
        $this->redis_server = $redis_server;
        $this->message_queue = $message_queue;
        $this->local_object = $local_object;
    }

    /**
     * Starts the server.
     */
    public function run() {
        $this->redis_server->del($this->message_queue);
        $timeout = 0;
        while (1) {
            # Pop a message from the queue.
            # Decode the message.
            # Check that the function exists.
            list($message_queue, $message) = $this->redis_server->blpop($this->message_queue, $timeout);
            assert($message_queue == $this->message_queue);
            debug_print("RPC Request: $message");
            $rpc_request = json_decode($message);
            $response_queue = $rpc_request->response_queue;
            $function_call = FunctionCall::from_object($rpc_request->function_call);
            if (!method_exists($this->local_object, $function_call->name)) {
                $rpc_response = array('exception' => 'method "' . $function_call->name . '" does not exist');
            }
            else {
                $code = 'return $this->local_object->' . $function_call->as_php_code() . ';';
                debug_print($code);
                try {
                    $return_value = eval($code);
                    $rpc_response = array('return_value' => $return_value);
                }
                catch (Exception $e) {
                    $rpc_response = array('exception' => $e->getMessage());
                }
            }
            $message = json_encode($rpc_response);
            debug_print("RPC Response: $message");
            $this->redis_server->rpush($response_queue, $message);
        }
    }

}

?>
