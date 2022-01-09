// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

contract NftOrderList {
    address default_address = 0x0000000000000000000000000000000000000000;
    struct NftOrder {
        address owner;
        string nftName;
        uint nftUniqueId;
        uint price;
        address token;
        bool confirm;
        address buyer;
        uint id;
    }
    NftOrder[] public nftOrderList;

    function create(address _owner, string memory _nftName, uint _nftId, uint _price, address _token) public {
        nftOrderList.push(NftOrder(_owner, _nftName, _nftId, _price, _token, false, default_address, nftOrderList.length));
    }

    function toggleCompeleted(uint _index) public {
        NftOrder storage nftOrder = nftOrderList[_index];
        nftOrder.confirm = !nftOrder.confirm;
    }

    function update(uint _index, address _buyer) public {
        NftOrder storage nftOrder = nftOrderList[_index];
        nftOrder.buyer = _buyer;
    }

    function orderListLength() public view returns(uint){
        return nftOrderList.length;
    }
}