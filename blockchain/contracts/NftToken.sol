// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

contract NftToken {
    struct Nft {
        address owner;
        string nftName;
        uint specialId;
    }
    Nft[] public nftList;

    function create(address _owner, string memory _nftName) public {
        uint _specialId = nftList.length;
        nftList.push(Nft(_owner, _nftName, _specialId));
    }

    function sellToken(address _addr, uint _index) public {
        Nft storage nft = nftList[_index];
        nft.owner = _addr;
    }

    function nftListLength() public view returns(uint){
        return nftList.length;
    }
}