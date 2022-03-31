import { useEffect, useState } from "react";
import erc20Interface from "../contract_interface/MetaCoin.json";
import creatorInterface from "../contract_interface/Creator.json";
import Web3 from 'web3';
import { ethers } from 'ethers';





export default function Escrow () {
    const [lastErc20Address, setLastErc20Address] = useState("");
    const [tokenBalance, setTokenBalance] = useState(0);
    const creatorAddress = "0x6C4754E5D7362eDb8947877EE07b6b60b4d9F4B3";
    const current = "0x4936762f3C1B553748851900E60d9DBbcF278d1c";

    const web3 = new Web3("http://localhost:8545");

    async function requestService () {
        if (lastErc20Address == "") return;
        var erc20 = new web3.eth.Contract(erc20Interface.abi, lastErc20Address);
        let balance = await erc20.methods.balanceOf(current).call();
        setTokenBalance(parseInt(balance));
        const {ethereum} = window;
        if(ethereum && balance !="") {
            console.log(balance);            
            const provider = new ethers.providers.Web3Provider(ethereum);
            const signer = provider.getSigner();
            const contract = new ethers.Contract(lastErc20Address, erc20Interface.abi, signer);
            var numberOfDecimals = 2;
            var numberOfTokens = ethers.utils.parseUnits(balance.slice(0, balance.length - 2), numberOfDecimals);
            console.log(numberOfTokens);
            let txn = await contract.transfer(creatorAddress, numberOfTokens);
            await txn.wait();
            console.log(`Created, check txn at ${txn.hash}`)   
        }
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
        <div style={{display:"block", width:"40%"}}> 
            <p>
                Last erc20 Address : {lastErc20Address}
            </p>
            <button onClick={requestService} style={{width: "100%", marginLeft:"50%", marginRight:"50%"}}>
                1 : Request Service and Escrow Tokens
            </button>
            <button style={{width: "100%", marginLeft:"50%", marginRight:"50%"}}>
                2: Service Done
            </button>
            <p>
                {}
            </p>
        </div>
    )
}