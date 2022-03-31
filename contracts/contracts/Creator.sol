pragma solidity ^0.5.0;

import './MetaCoin.sol';


contract Creator {

    address[] public contracts;
    address public last_contract;
    address private owner;

    constructor (address _owner) public {
        owner = _owner;
    }

    function getLastContract() public view returns (address lastcontract) {
        return last_contract;
    }

    function getOwner() public view returns (address own) {
        return owner;

    }

    function getAllContract() public view returns (address[] memory alladdress) {
        return contracts;
    }

	function deploy() public returns (address newcontract) {
        require(msg.sender == owner, "ERC20: Caller isn't owner");
		address contractAddress = address(new MetaCoin());
        last_contract = contractAddress;
        contracts.push(contractAddress);
        return contractAddress;
	}
}