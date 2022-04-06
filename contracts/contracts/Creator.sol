pragma solidity ^0.5.0;

import './MetaCoin.sol';


contract Creator {

    address[] public contracts_address;
    address public last_contract;
    address private owner;
    mapping(address => MetaCoin) public contracts;


    constructor (address _owner) public {
        owner = _owner;
    }

    function getLastContract() public view returns (address lastcontract) {
        return last_contract;
    }

    function addStaker() public payable {
        require(msg.value == 1 ether);
    }

    function getOwner() public view returns (address own) {
        return owner;

    }

    function getAllContract() public view returns (address[] memory alladdress) {
        return contracts_address;
    }

	function deploy() public returns (address newcontract) {
        require(msg.sender == owner, "ERC20: Caller isn't owner");
        MetaCoin newToken = new MetaCoin(owner);
		address contractAddress = address(newToken);
        contracts[contractAddress] = newToken;
        last_contract = contractAddress;
        contracts_address.push(contractAddress);
        return contractAddress;
	}
}