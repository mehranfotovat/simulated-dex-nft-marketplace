// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;



contract OrderList {
    address default_address = 0x0000000000000000000000000000000000000000;
    struct Order{
        uint id;
        address orderPutter;
        address tokenSwapContractAddress;
        address tokenSell;
        uint tokenSellAmount;
        address tokenBuy;
        uint tokenBuyAmount;
        bool completed;
        address contrbiute;
    }

    Order[] public orderList;

    function create(uint _id, address _orderPutter, address _tokenSwapContractAddress, address _tokenSell, uint _tokenSellAmount, address _tokenBuy, uint _tokenBuyAmount) public {
        orderList.push(Order(_id, _orderPutter, _tokenSwapContractAddress, _tokenSell, _tokenSellAmount, _tokenBuy, _tokenBuyAmount, false, default_address));
    }

    function toggleCompeleted(uint _index) public {
        Order storage order = orderList[_index];
        order.completed = !order.completed;
    }

    function update(uint _index, address _contrbiute) public {
        Order storage order = orderList[_index];
        order.contrbiute = _contrbiute;
    }

    function orderListLength() public view returns(uint){
        return orderList.length;
    }
}