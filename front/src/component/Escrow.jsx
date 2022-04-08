import { useEffect, useState } from "react";
import erc20Interface from "../contract_interface/MetaCoin.json";
import creatorInterface from "../contract_interface/Creator.json";
import Web3 from 'web3';
import { ethers } from 'ethers';





export default function Escrow() {
    const [lastErc20Address, setLastErc20Address] = useState("");
    const [claimval, setClaimval] = useState("0.5");
    const [tokenBalance, setTokenBalance] = useState(0);
    const creatorAddress = "0x3E8B23e576ad350F3f0464a482cb976E6D105231";
    const current = "0x4936762f3C1B553748851900E60d9DBbcF278d1c";
    const bank_account = "0x62B9a2F427Ae8649b2467e08095C65551140926d";

    const web3 = new Web3("http://localhost:8545");
    const apiUrl = "http://127.0.0.1:5000/"

    async function requestService() {
        if (lastErc20Address == "") return;
        var erc20 = new web3.eth.Contract(erc20Interface.abi, lastErc20Address);
        let balance = await erc20.methods.balanceOf(current).call();
        setTokenBalance(parseInt(balance));
        const { ethereum } = window;
        if (ethereum && balance != "") {
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

    async function allocateTokens() {
        if (lastErc20Address == "") return;
        var erc20 = new web3.eth.Contract(erc20Interface.abi, lastErc20Address);
        let balance = await erc20.methods.balanceOf(current).call();
        const { ethereum } = window;
        if (ethereum && balance != "") {
            const provider = new ethers.providers.Web3Provider(ethereum);
            const signer = provider.getSigner();
            const contract = new ethers.Contract(lastErc20Address, erc20Interface.abi, signer);
            var numberOfDecimals = 2;
            var numberOfTokens = ethers.utils.parseUnits(balance.slice(0, balance.length - 2), numberOfDecimals);
            let txn = await contract.approve(bank_account, numberOfTokens);
            console.log(`Created, check txn at ${txn}`)
        }
        console.log(balance)
    }

    async function newTransaction() {
        let from = "0x4936762f3C1B553748851900E60d9DBbcF278d1c";
        let to = "0x62B9a2F427Ae8649b2467e08095C65551140926d";
        let amount = "1000"
        let url = apiUrl + "init_transaction?";
        url += "from=" + from;
        url += "&to=" + to;
        url += "&amount=" + amount;
        fetch(url)
        .then(response => console.log(response))
    }

    async function pay() {
        fetch(apiUrl + "pay")
        .then(response => console.log(response));
    }

    async function service_done() {
        console.log("calling apiu");
        fetch(apiUrl + "service_done")
        .then(response => console.log(response));
    }

    async function serviceFullfiled() {
        fetch(apiUrl + "service_fullfilled")
        .then(response => console.log(response));
    }

    async function serviceClaim() {
        fetch(apiUrl + "service_claim?ratio=" + claimval)
        .then(response => console.log(response));
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
        <div style={{ display: "block", width: "40%" }}>
            <p>
                Last erc20 Address : {lastErc20Address}
            </p>
            <button onClick={requestService} style={{ width: "100%", marginLeft: "50%", marginRight: "50%" }}>
                ?Request Service and Escrow Tokens
            </button>
            <button onClick={newTransaction}>
                Init new transaction
            </button>
            <button onClick={pay}>
                Pay for tokens in exchange
            </button>
            <button onClick={allocateTokens} style={{ width: "100%", marginLeft: "50%", marginRight: "50%" }}>
                Allocate
            </button>
            <button onClick={service_done}>
                Service Done
            </button>
            <button onClick={serviceFullfiled}>
                Service FullFilled
            </button>
            <div>
                <input type="text" value={claimval} onChange={e => setClaimval(e.target.value)}>
                </input>
                <button onClick={serviceClaim}>
                    Service Claim
                </button>
            </div>
            <button>
                Tokens settlment
            </button>

            <p>
                { }
            </p>
        </div>
    )
}