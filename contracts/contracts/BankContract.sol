pragma solidity ^0.5.0;

import "./MetaCoin.sol";


contract BankContract {

    struct privatePayment {
        address client;
        address service_provider;
        address erc20;
        bool claim;
        uint256 amount;
        uint256 claimRatio;
    }

    mapping(uint256 => privatePayment) privatePayments;
    uint256[] public paymentIds;
    address private owner;



    /** @dev Contract that manages erc20 tokens contracts.
     */
    constructor() public payable {
        owner = msg.sender;
    }

    function init_new_payment(address _client, address _service_provider, address _erc20, uint256 _claimRatio, uint256 _amount, uint256 id) public {
        privatePayment storage newPayment = privatePayments[id];
        newPayment.client = _client;
        newPayment.erc20 = _erc20;
        newPayment.service_provider = _service_provider;
        newPayment.claim = false;
        newPayment.claimRatio = _claimRatio;
        newPayment.claimRatio = 1;
        newPayment.amount = _amount;
        paymentIds.push(id);
    }

    function getPayment(uint256 id) public view returns (address, address, bool, 
                                                    uint256){
        privatePayment storage s = privatePayments[id];
        return (s.client,s.service_provider,s.claim,s.amount);
    }

    /** @dev get last created erc20 token address
     * @return address since:2022-04-01last erc20 token address
     */
    function request_service_and_escrow_tkn(uint256 id) public view returns (bool) {
        privatePayment storage payment = privatePayments[id];
        uint256 r = MetaCoin(payment.erc20).allowance(payment.client, address(this));
        if(r >= payment.amount) {
            return true;
        }
        return false;
    }

    function service_done(uint256 id) public {
        privatePayment storage payment = privatePayments[id];
        if(!payment.claim) {
            MetaCoin(payment.erc20).transferFrom(payment.client, payment.service_provider, payment.amount);
        }
        else {
            uint256 newAmount = payment.claimRatio * payment.amount;
            MetaCoin(payment.erc20).transferFrom(payment.client, payment.service_provider, newAmount);
        }
    }

    function service_claim(uint256 id) public {
        privatePayment storage payment = privatePayments[id];
        payment.claim = true;
    }


}
