pragma solidity ^0.5.0;

import "./MetaCoin.sol";



contract BankContract {


    enum serviceStatus{ INIT, DONE, CLAIM, PAYED }

    struct privatePayment {
        address client;
        address service_provider;
        address erc20;
        uint256 token_amount;
        uint256 claimRatio;
        uint256 targetBlock;
        uint256 token_supply;
        serviceStatus status;
    }

    mapping(uint256 => privatePayment) privatePayments;
    uint256[] public paymentIds;
    address private bank;

    /** @dev Contract that manages the private paymenrs channel.
    * @param _bank address of the wallet used by the bank
     */
    constructor(address _bank) public payable {
        bank = _bank;
    }

    /** @dev Init a new payment, take all the required data in input and create an erc20 token. Add the new payment to the map containing all payments.
    * @param _client _service_provider _tokenSupply _claimRatio _claimTime _id 
     */
    function initPaymentChannel(address _client, address _service_provider, uint256 _tokenSupply, uint256 _claimRatio, uint256 _claimTime, uint256 _id) public {
        require(msg.sender == bank);
        privatePayment storage newPayment = privatePayments[_id];
        newPayment.client = _client;
        newPayment.service_provider = _service_provider;
        newPayment.claimRatio = _claimRatio;
        newPayment.targetBlock = block.number + _claimTime;
        newPayment.token_supply = _tokenSupply;
        newPayment.token_amount = 0;
        MetaCoin erc20 = new MetaCoin(_tokenSupply, bank);
        newPayment.status = serviceStatus.INIT;
        newPayment.erc20 = address(erc20);
        paymentIds.push(_id);
    }

    /** @dev Get a payment info. Only the bank can call this.
    * @param _id id of the payment
     */
    function getPayment(uint256 _id) view public returns (address, address, address, uint256) {
        require(msg.sender == bank, "only the bank can call this");
        privatePayment memory s = privatePayments[_id];
        return (s.client,s.service_provider, s.erc20, s.token_supply);
    }

    /** @dev request a service for a certain token amount
     * @param _id _tokenAmount id of the payment and amount of token
     * @return bool true if the client has enough token allocated flase else
     */
    function requestServiceAndEscrowTokens(uint256 _id, uint256 _tokenAmount) public returns (bool) {
        privatePayment storage payment = privatePayments[_id];
        require(msg.sender == payment.client, "Caller isn't client");
        payment.token_amount = _tokenAmount;
        uint256 r = MetaCoin(payment.erc20).allowance(payment.client, address(this));
        if(r >= _tokenAmount) {
            return true;
        }
        return false;
    }

    /** @dev Service provider tell the contract that the service has been excuted
    * @param _id id of the payment
     */
    function serviceDone(uint256 _id) public{
        privatePayment storage payment = privatePayments[_id];
        require(msg.sender == payment.service_provider, "Caller isn't service provider");
        payment.status = serviceStatus.DONE;
    }

    /** @dev Client can call the contract and claim if not satisfied with service.
    * @param _id id of the payment
     */
    function serviceClaim(uint256 _id) public {
        privatePayment storage payment = privatePayments[_id];
        require(msg.sender == payment.client, "Caller isn't client");
        payment.status = serviceStatus.CLAIM;
    }

    function pay(uint256 _id) public {
        privatePayment storage payment = privatePayments[_id];
        require(block.number > payment.targetBlock, "You need to wait longer before claiming");
        if(payment.status == serviceStatus.CLAIM) {
            uint256 newtoken_amount = payment.claimRatio * payment.token_amount;
            MetaCoin(payment.erc20).transferFrom(payment.client, payment.service_provider, newtoken_amount);
        }
        else if(payment.status == serviceStatus.DONE) {
            MetaCoin(payment.erc20).transferFrom(payment.client, payment.service_provider, payment.token_amount);
        }
        payment.status = serviceStatus.PAYED;
    }

    function closePaymentChannel(uint256 _id) public {
        require(msg.sender == bank, "Caller isn't bank");
        privatePayment storage payment = privatePayments[_id];
        MetaCoin(payment.erc20).finalize();
        delete privatePayments[_id];
    }


}
