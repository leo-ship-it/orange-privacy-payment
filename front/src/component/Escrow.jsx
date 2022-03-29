import { useEffect, useState } from "react";
import erc20Interface from "../contract_interface/MetaCoin.json";
import creatorInterface from "../contract_interface/Creator.json";
import Web3 from 'web3';




export default function Escrow () {
    const [lastErc20Address, setLastErc20Address] = useState("");
    const creatorAddress = "0x6C4754E5D7362eDb8947877EE07b6b60b4d9F4B3";

    const web3 = new Web3("http://localhost:8545");

    async function requestService () {
        
    }

    useEffect(() => {
        async function getAddress() {
            var erc20 = new web3.eth.Contract(creatorInterface.abi, creatorAddress);
            let erc20Address = await erc20.methods.getLastContract().call();
            setLastErc20Address(erc20Address);
            console.log("erc20 add", lastErc20Address);
        }
        getAddress();
    }, [])


    return (
        <div>
            <p>
                Last erc20 Address : {lastErc20Address}
            </p>
            <button onClick={requestService}>
                Request Service and Escrow Tokens
            </button>
        </div>
    )
}