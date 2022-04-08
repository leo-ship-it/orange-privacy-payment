pragma solidity ^0.5.0;

import "./MetaCoin.sol";

contract Creator {
    address[] public tokens_address;
    address public last_token;
    address private owner;
    mapping(address => MetaCoin) public tokens;

    /** @dev Contract that manages erc20 tokens contracts.
     * @param _owner address of the owner
     * @return.
     */
    constructor(address _owner) public {
        owner = _owner;
    }

    /** @dev get last created erc20 token address
     * @param
     * @return address last erc20 token address
     */
    function getLastContract() public view returns (address) {
        return last_token;
    }


    /** @dev get the owner of the contract
     * @param
     * @return address get last owner
     */
    function getOwner() public view returns (address) {
        return owner;
    }


    /** @dev get all contracts address
     * @param
     * @return address[] get all the contract address
     */
    function getAllContract() public view returns (address[] memory) {
        return tokens_address;
    }


    /** @dev deploy a new erc20
     * @param
     * @return address return the address of the deployed contract
     */
    function deploy() public returns (address) {
        require(msg.sender == owner, "ERC20: Caller isn't owner");
        MetaCoin newToken = new MetaCoin(owner);
        address contractAddress = address(newToken);
        tokens[contractAddress] = newToken;
        last_token = contractAddress;
        tokens_address.push(contractAddress);
        return contractAddress;
    }
}
