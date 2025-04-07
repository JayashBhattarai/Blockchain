//TASK 1: TOKEN CREATION (ERC20)

// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Pausable.sol";

contract MyToken is ERC20, Ownable, Pausable {
    constructor(address initialOwner) 
        ERC20("MyToken", "MTK") 
        Ownable(initialOwner) 
    {}

    function mint(address to, uint256 amount) public onlyOwner {
        _mint(to, amount);
    }

    function burn(uint256 amount) public {
        _burn(msg.sender, amount);
    }

    function pause() public onlyOwner {
        _pause();
    }

    function unpause() public onlyOwner {
        _unpause();
    }

    function _update(address from, address to, uint256 amount)
        internal
        virtual
        override
        whenNotPaused
    {
        super._update(from, to, amount);
    }
}

// TASK 2: VOTING SYSTEM

// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract VotingSystem {
    struct Candidate {
        string name;
        uint voteCount;
    }

    address public owner;
    uint public votingDeadline;
    mapping(address => bool) public hasVoted;
    mapping(address => bool) public whitelistedVoters;

    Candidate[] public candidates;

    constructor(uint _durationInMinutes) {
        owner = msg.sender;
        votingDeadline = block.timestamp + (_durationInMinutes * 1 minutes);
    }

    modifier onlyBeforeDeadline() {
        require(block.timestamp < votingDeadline, "Voting has ended");
        _;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Not authorized");
        _;
    }

    modifier onlyWhitelisted() {
        require(whitelistedVoters[msg.sender], "Not a registered voter");
        _;
    }

    function addCandidate(string memory name) public onlyOwner {
        candidates.push(Candidate(name, 0));
    }

    function whitelistVoter(address voter) public onlyOwner {
        whitelistedVoters[voter] = true;
    }

    function vote(uint candidateIndex) public onlyBeforeDeadline onlyWhitelisted {
        require(!hasVoted[msg.sender], "Already voted");
        candidates[candidateIndex].voteCount++;
        hasVoted[msg.sender] = true;
    }

    function getCandidateCount() public view returns (uint) {
        return candidates.length;
    }

    function getWinner() public view returns (string memory winnerName, uint voteCount) {
        require(block.timestamp >= votingDeadline, "Voting still ongoing");
        uint winningVoteCount = 0;
        uint winnerIndex = 0;

        for (uint i = 0; i < candidates.length; i++) {
            if (candidates[i].voteCount > winningVoteCount) {
                winningVoteCount = candidates[i].voteCount;
                winnerIndex = i;
            }
        }

        return (candidates[winnerIndex].name, candidates[winnerIndex].voteCount);
    }
}

//TASK 3: ESCROW SERVICE
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract EscrowService {
    address public buyer;
    address public seller;
    address public arbiter;

    uint public amount;
    bool public buyerApproved;
    bool public disputed;
    bool public resolved;

    constructor(address _seller, address _arbiter) payable {
        buyer = msg.sender;
        seller = _seller;
        arbiter = _arbiter;
        amount = msg.value;
    }

    modifier onlyBuyer() {
        require(msg.sender == buyer, "Only buyer allowed");
        _;
    }

    modifier onlyArbiter() {
        require(msg.sender == arbiter, "Only arbiter allowed");
        _;
    }

    function approveDelivery() public onlyBuyer {
        require(!resolved, "Already resolved");
        buyerApproved = true;
        payable(seller).transfer(amount);
        resolved = true;
    }

    function raiseDispute() public onlyBuyer {
        disputed = true;
    }

    function resolveDispute(bool releaseToSeller) public onlyArbiter {
        require(disputed && !resolved, "No active dispute or already resolved");
        resolved = true;
        if (releaseToSeller) {
            payable(seller).transfer(amount);
        } else {
            payable(buyer).transfer(amount);
        }
    }
}


//TASK 4: DECENTRALIZED AUCTION
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract Auction {
    address public owner;
    address public highestBidder;
    uint public highestBid;
    uint public endTime;
    bool public auctionEnded;
    mapping(address => uint) public pendingReturns;

    uint public minIncrementPercent = 5;

    constructor(uint _biddingTimeMinutes) {
        owner = msg.sender;
        endTime = block.timestamp + (_biddingTimeMinutes * 1 minutes);
    }

    modifier onlyBeforeEnd() {
        require(block.timestamp < endTime, "Auction ended");
        _;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }

    function bid() public payable onlyBeforeEnd {
        require(msg.value > 0, "Bid must be greater than zero");

        uint requiredMin = highestBid + ((highestBid * minIncrementPercent) / 100);
        require(msg.value >= requiredMin, "Bid must be at least 5% higher");

        if (highestBid > 0) {
            pendingReturns[highestBidder] += highestBid;
        }

        highestBid = msg.value;
        highestBidder = msg.sender;
    }

    function withdraw() public {
        uint amount = pendingReturns[msg.sender];
        require(amount > 0, "Nothing to withdraw");
        pendingReturns[msg.sender] = 0;
        payable(msg.sender).transfer(amount);
    }

    function endAuction() public onlyOwner {
        require(!auctionEnded, "Auction already ended");
        require(block.timestamp >= endTime, "Auction not yet ended");

        auctionEnded = true;
        payable(owner).transfer(highestBid);
    }

    function getWinner() public view returns (address, uint) {
        require(auctionEnded, "Auction still ongoing");
        return (highestBidder, highestBid);
    }
}
