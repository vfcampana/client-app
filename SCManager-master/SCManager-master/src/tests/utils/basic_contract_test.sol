//SPDX-License-Identifier: MIT
pragma solidity ^0.8.25;

contract Test {
    bool public status = false;

    function get_status() view public returns (bool) {
        return status;
    }

    function set_status(bool new_status) public {
        status = new_status;
    }
}