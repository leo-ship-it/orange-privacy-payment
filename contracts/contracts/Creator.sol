pragma solidity ^0.5.0;

import './MetaCoin.sol';


contract Creator {

    address[] public tokens_address;
    address public last_token;
    address private owner;
    mapping(address => MetaCoin) public tokens;

// 
    constructor (address _owner) public {
        owner = _owner;
    }

    function getLastContract() public view returns (address) {
        return last_token;
    }

    function getOwner() public view returns (address) {
        return owner;

    }

    function getAllContract() public view returns (address[] memory) {
        return tokens_address;
    }

	function deploy() public returns (address newcontract) {
        require(msg.sender == owner, "ERC20: Caller isn't owner");
        MetaCoin newToken = new MetaCoin(owner);
		address contractAddress = address(newToken);
        tokens[contractAddress] = newToken;
        last_token = contractAddress;
        tokens_address.push(contractAddress);
        return contractAddress;
	}
}