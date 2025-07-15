// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract Converter {
    address public owner;
    mapping(string => uint256) public cryptoRatesInINR; // e.g., BTC => ₹3000000

    constructor() {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can update rates");
        _;
    }

    function setConversionRate(string memory symbol, uint256 rateInINR) public onlyOwner {
        cryptoRatesInINR[symbol] = rateInINR;
    }

    function getCryptoAmount(string memory symbol, uint256 inrAmount) public view returns (uint256) {
        require(cryptoRatesInINR[symbol] > 0, "Rate not available");
        return (inrAmount * 1 ether) / cryptoRatesInINR[symbol];
    }
}
