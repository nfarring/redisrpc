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

/**
 *
 */
class FunctionCall {

    public $name;
    public $args;

    static public function from_object($object) {
        if (isset($object->args)) {
            return new FunctionCall($object->name, $object->args);
        }
        return new FunctionCall($object->name);
    }

    public function __construct($name, $args=NULL) {
        $this->name = $name;
        $this->args = $args;
    }

    public function as_php_code() {
        if (isset($this->args)) {
            return $this->name . '(' . implode(',', $this->args) . ')';
        }
        return $this->name . '()';
    }
}

?>
