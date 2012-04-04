#!/usr/bin/env php -q
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

# Parse command-line arguments
if(isset($_SERVER['argc'])) {
    $options = getopt('v',array('verbose'));
    foreach (array_keys($options) as $opt) switch ($opt) {
    case 'v':
    case 'verbose':
        # Set the DEBUG mode of redisrpc.php
        define("DEBUG",TRUE);
        break;
    }
}

require '../vendor/.composer/autoload.php';

require_once 'calc.php';

function do_calculations($calculator) {
    $calculator->clr();
    $calculator->add(5);
    $calculator->sub(3);
    $calculator->mul(4);
    $calculator->div(2);
    assert($calculator->val() == 4);
}

// 1. Local object
$calculator = new Calculator();
do_calculations($calculator);

// 2. Remote object, should act like local object
$redis_server = new Predis\Client();
$message_queue = 'calc';
$timeout = 1;
$calculator = new RedisRPC\Client($redis_server, $message_queue, $timeout);
do_calculations($calculator);
print "success!\n";

?>
