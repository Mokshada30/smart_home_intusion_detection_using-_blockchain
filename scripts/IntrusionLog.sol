// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract IntrusionLog {
    struct Event {
        string device;
        uint256 timestamp;
        uint8 intrusion;
    }

    Event[] public events;

    function logEvent(string memory device, uint8 intrusion) public {
        events.push(Event(device, block.timestamp, intrusion));
    }

    function getEventsCount() public view returns (uint256) {
        return events.length;
    }
}
