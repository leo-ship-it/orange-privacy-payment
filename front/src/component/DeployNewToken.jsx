import creatorInterface from "../contract_interface/Creator.json";
import Web3 from 'web3';
import { ethers } from 'ethers';



export default function DeployNewToken (props) {
    const creatorAddress = "0x6C4754E5D7362eDb8947877EE07b6b60b4d9F4B3";
    const web3 = new Web3("http://localhost:8545");

    var creator_contract = new web3.eth.Contract(creatorInterface.abi, creatorAddress);
    const account = props.account;

    
    async function createContract() {
        const {ethereum} = window;

        if(ethereum) {
            const provider = new ethers.providers.Web3Provider(ethereum);
            const signer = provider.getSigner();
            const contract = new ethers.Contract(creatorAddress, creatorInterface.abi, signer);
            console.log("Init new token");

            let txn = await contract.deploy();

            console.log("Creating");

            await txn.wait();

            console.log(`Created, check txn at ${txn.hash}`)
            
        }
        let r = await creator_contract.methods.deploy().send({from:account});
        console.log(r);
        let r2 = await creator_contract.methods.getAllContract().call();
        console.log(r2);

    }

    return(
        <>
            <button onClick={createContract}>
                Click to deploy new erc20
            </button>
        </>
    );
}