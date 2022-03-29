import creatorInterface from "../contract_interface/Creator.json";
import Web3 from 'web3';
import { ethers } from 'ethers';



export default function DeployNewToken (props) {
    const creatorAddress = "0x6C4754E5D7362eDb8947877EE07b6b60b4d9F4B3";

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
    }

    async function requestService() {

    }

    return(
        <div style={{display:"flex", flexDirection:"column", width: "auto"}}>
            <button onClick={createContract}>
                Click to deploy new erc20
            </button>

        </div>
    );
}