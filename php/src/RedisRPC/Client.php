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

use RedisRPC\RemoteException;

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

# Ref: http://stackoverflow.com/questions/2257441
# Ref: http://stackoverflow.com/questions/853813/how-to-create-a-random-string-using-php
/**
 *
 */
function random_string($size, $valid_chars='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789') {

    // start with an empty random string
    $retval = "";

    // count the number of chars in the valid chars string so we know how many choices we have
    $num_valid_chars = strlen($valid_chars);

    // repeat the steps until we've created a string of the right size
    for ($i = 0; $i < $size; $i++)
    {
        // pick a random number from 1 up to the number of valid chars
        $random_pick = mt_rand(1, $num_valid_chars);

        // take the random character out of the string of valid chars
        // subtract 1 from $random_pick because strings are indexed starting at 0, and we started picking at 1
        $random_char = $valid_chars[$random_pick-1];

        // add the randomly-chosen char onto the end of our string so far
        $retval .= $random_char;
    }

    // return our finished random string
    return $retval;
}

/**
 *
 */
class Client {

    private $redis_server;
    private $message_queue;

    public function __construct($redis_server, $message_queue, $timeout = 0) {
        $this->redis_server = $redis_server;
        $this->message_queue = $message_queue;
        $this->timeout = $timeout;
    }

    public function __call($name, $arguments) {
        # Construct the RPC Request message from the $name and $arguments.
        # Send the RPC Request to Redis.
        # Block on the RPC Response from Redis.
        # Extract the return value.
        $function_call = array('name' => $name);
        if (count($arguments) > 0) {
            $function_call['args'] = $arguments;
        }
        $response_queue = "$this->message_queue:rpc:" . random_string(8);
        $rpc_request = array(
            'function_call' => $function_call,
            'response_queue' => $response_queue
        );
        $message = json_encode($rpc_request);
        debug_print("RPC Request: $message");
        $this->redis_server->rpush($this->message_queue, $message);
        $result = $this->redis_server->blpop($response_queue, $this->timeout);
        if ($result == NULL) {
            throw new TimeoutException();
        }
        list($message_queue, $message) = $result;
        assert($message_queue == $response_queue);
        debug_print("RPC Response: $message\n");
        $rpc_response = json_decode($message);
        if (array_key_exists('exception',$rpc_response) && $rpc_response->exception != NULL) {
            throw new RemoteException($rpc_response->exception);
        }
        if (!array_key_exists('return_value',$rpc_response)) {
            throw new RemoteException('Malformed RPC Response message');
        }
        return $rpc_response->return_value;
    }
}

?>
