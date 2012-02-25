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

/**
 *
 */
class Calculator
{
    /*
     * Accumulator
     */
    private $acc = 0.0;
    
    public function clr() {
        $this->acc = 0.0;
        return $this->acc;
    }
    
    public function add($number) {
        $this->acc += $number;
        return $this->acc;
    }
    
    public function div($number) {
        $this->acc /= $number;
        return $this->acc;
    }
    
    public function mul($number) {
        $this->acc *= $number;
        return $this->acc;
    }
    
    public function sub($number) {
        $this->acc -= $number;
        return $this->acc;
    }
    
    public function val() {
        return $this->acc;
    }
}

?>
