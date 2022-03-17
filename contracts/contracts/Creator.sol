pragma solidity ^0.5.0;

import './MetaCoin.sol';


contract Creator {

    address[] public contracts;
    address public last_contract;

    function getLastContract() public view returns (address lastcontract) {
        return last_contract;
    }

    function getAllContract() public view returns (address[] memory alladdress) {
        return contracts;
    }

	function deploy() public returns (address newcontract) {
		address contractAddress = address(new MetaCoin());
        last_contract = contractAddress;
        contracts.push(contractAddress);
        return contractAddress;
	}
}