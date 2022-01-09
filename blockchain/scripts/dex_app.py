from brownie import accounts, MyToken, OrderList, TokenSwap, NftToken, NftOrderList
import tkinter as tk
import requests

# Get live coin prices
def get_price():
    url = 'https://api.nobitex.ir/market/stats'
    response = requests.get(url)
    response_json = response.json()
    matic_price = response_json['global']['binance']['matic']
    near_price = response_json['global']['binance']['near']
    shib_price = response_json['global']['binance']['shib']
    dot_price = response_json['global']['binance']['dot']
    usdt_price = response_json['global']['binance']['usdt']
    rial_price = int(usdt_price) / 30

    price_lists = {
        'Polygon matic': matic_price,
        'shiba inu': shib_price,
        'near protocol': near_price,
        'Polkadot DOT': dot_price,
        'Rial price': rial_price
    }
    return price_lists

def deploy_contracts():
    # Token contracts
    polkadot_contract = MyToken.deploy('Polkadot', 'DOT', {'from': accounts[0]})
    shiba_contract = MyToken.deploy('shiba inu', 'SHIB', {'from': accounts[1]})
    polygon_contract = MyToken.deploy('Polygon matic', 'MATIC', {'from': accounts[2]})
    rial_contract = MyToken.deploy('iran rial', 'RIAL', {'from': accounts[3]})
    near_contract = MyToken.deploy('near protocol', 'NEAR', {'from': accounts[4]})


    contract_list = {
        'polkadot_contract': polkadot_contract,
        'shiba_contract': shiba_contract,
        'polygon_contract': polygon_contract,
        'rial_contract': rial_contract,
        'near_contract': near_contract
    }
    return contract_list


def main():
    # Contract Deployment part
    order_list = OrderList.deploy({'from': accounts[5]})
    nft_token = NftToken.deploy({'from': accounts[5]})
    nft_order_list = NftOrderList.deploy({'from': accounts[5]})

    contracts_list = deploy_contracts()

    accounts_list = {
        'account_polkadot_contract': accounts[0],
        'account_shiba_contract': accounts[1],
        'account_polygon_contract': accounts[2],
        'account_rial_contract': accounts[3],
        'account_near_contract': accounts[4],
    }
    
    accounts_list_name = {
        accounts[0].address: 'account_polkadot_contract',
        accounts[1].address: 'account_shiba_contract',
        accounts[2].address: 'account_polygon_contract',
        accounts[3].address: 'account_rial_contract',
        accounts[4].address: 'account_near_contract',
    }
    
    # Main App
    main_window = tk.Tk()
    main_window.title('Mehran dex project')

    # Selected account value getter
    slctd_account = tk.StringVar()
    slctd_account.set(accounts[0])

    # For getting accounts from their contract address
    dic_accounts = {}

    for i in range(6):
        dic_accounts[accounts[i].address] = accounts[i]

    #For getting contracs from their address
    dic_contracts = {}

    for acc in contracts_list.values():
        dic_contracts[acc.address] = acc

    # List of my tokenSwaps
    tokenSwap_lists = []

    # Price Lists
    price_lists = get_price()

    def account_selection():
        select_account_window = tk.Toplevel()
        select_account_window.title('select your account')

        selected_account = tk.StringVar()

        for (account_name, account) in accounts_list.items():
            tk.Radiobutton(select_account_window, text=account_name, variable=selected_account, value=account).pack()
        
        def done_selecting_account():
            sel_acc = selected_account.get()
            slctd_account.set(sel_acc)
            select_account_window.destroy()

        btn_done_selecting_account = tk.Button(master=select_account_window, text='Done', command=done_selecting_account)
        btn_done_selecting_account.pack()
        select_account_window.mainloop()



    frm_account_selection = tk.Frame(main_window)
    frm_account_selection.pack()

    main_label = tk.Label(frm_account_selection, textvariable=slctd_account)
    main_label.pack(side=tk.RIGHT)

    main_button = tk.Button(frm_account_selection, text='select account', command=account_selection)
    main_button.pack(side=tk.RIGHT)

    # dex order list part 
    def view_orders():
        view_order_window = tk.Toplevel()
        view_order_window.title('View Order')
        view_order_window.geometry('800x400')

        def apply_for_order():
            selected_account = main_label['text']
            order_id = int(lb_order.get(tk.ANCHOR)[0])-1
            token2_address_for_approval = dic_contracts.get(order_list.orderList(order_id)[5])
            token_amount = order_list.orderList(order_id)[6]
            swap_token_contract_address = tokenSwap_lists[order_id]
            token2_address_for_approval.approve(swap_token_contract_address, token_amount, {'from': selected_account})
            swap_token_contract_address.getOwner2Address(selected_account, {'from': selected_account})
            swap_token_contract_address.swap({'from': selected_account})
            order_list.update(order_id, selected_account)
            order_list.toggleCompeleted(order_id)
            view_order_window.destroy()


        def create_new_order():
            create_new_order_window = tk.Toplevel()
            create_new_order_window.title('Create new order')

            def enter_token_have():
                choose_token_window = tk.Toplevel()
                choose_token_window.geometry('400x300')
                choose_token_window.title('select your token')

                selected_account = tk.StringVar()

                for (account_name, account) in contracts_list.items():
                    tk.Radiobutton(choose_token_window, text=account_name, variable=selected_account, value=account).pack()
                
                def done_selecting_account():
                    sel_acc = selected_account.get()
                    ent_have_token.insert(0, sel_acc)
                    choose_token_window.destroy()

                btn_done_selecting_account = tk.Button(master=choose_token_window, text='Done', command=done_selecting_account)
                btn_done_selecting_account.pack()
                choose_token_window.mainloop()

            def enter_token_want():
                choose_token_window = tk.Toplevel()
                choose_token_window.title('select your token')

                selected_account = tk.StringVar()

                for (account_name, account) in contracts_list.items():
                    tk.Radiobutton(choose_token_window, text=account_name, variable=selected_account, value=account).pack()
                
                def done_selecting_account():
                    sel_acc = selected_account.get()
                    ent_want_token.insert(0, sel_acc)
                    choose_token_window.destroy()

                btn_done_selecting_account = tk.Button(master=choose_token_window, text='Done', command=done_selecting_account)
                btn_done_selecting_account.pack()
                choose_token_window.mainloop()

            def create_order_for_me():
                account = main_label['text']
                have_token_address = ent_have_token.get()
                token_amount = ent_give_token_amount.get()
                want_token_address = ent_want_token.get()
                want_token_amount = ent_want_token_amount.get()
                this_token_swap_contract = TokenSwap.deploy(have_token_address, account, token_amount, want_token_address, want_token_amount, {'from': account})
                tokenSwap_lists.append(this_token_swap_contract)
                token_id_for_approval = dic_contracts.get(have_token_address)
                token_id_for_approval.approve(this_token_swap_contract, token_amount, {'from': account})
                order_id = order_list.orderListLength()
                order_list.create(order_id, account , this_token_swap_contract.address, have_token_address, token_amount, want_token_address, want_token_amount, {'from': accounts[0]})
                create_new_order_window.destroy()
                view_order_window.destroy()

            # create order Gui
            frm_form = tk.Frame(master=create_new_order_window ,relief=tk.SUNKEN, borderwidth=3)
            frm_form.pack()

            lbl_have_token = tk.Label(master=frm_form, text='Your Token:')
            btn_have_token = tk.Button(master=frm_form, text='choose', command=enter_token_have)

            lbl_have_token.grid(row=0, column=0, sticky='e')
            btn_have_token.grid(row=0, column=1)

            lbl_chosen_token1 = tk.Label(master=frm_form, text='Chosen token address')
            ent_have_token = tk.Entry(master=frm_form, width=50)

            lbl_chosen_token1.grid(row=1, column=0, sticky='e')
            ent_have_token.grid(row=1, column=1)

            lbl_give_token_amount = tk.Label(master=frm_form, text='Your Token amount:')
            ent_give_token_amount = tk.Entry(master=frm_form, width=50)

            lbl_give_token_amount.grid(row=2, column=0, sticky='e')
            ent_give_token_amount.grid(row=2, column=1)

            lbl_want_token = tk.Label(master=frm_form, text='Want Token:')
            btn_want_token = tk.Button(master=frm_form, text='choose', command=enter_token_want)

            lbl_want_token.grid(row=3, column=0, sticky='e')
            btn_want_token.grid(row=3, column=1)

            lbl_chosen_token2 = tk.Label(master=frm_form, text='Chosen token address')
            ent_want_token = tk.Entry(master=frm_form, width=50)

            lbl_chosen_token2.grid(row=4, column=0, sticky='e')
            ent_want_token.grid(row=4, column=1)

            lbl_give_token_amount = tk.Label(master=frm_form, text='want Token amount:')
            ent_want_token_amount = tk.Entry(master=frm_form, width=50)

            lbl_give_token_amount.grid(row=5, column=0, sticky='e')
            ent_want_token_amount.grid(row=5, column=1)

            btn_done_create_order = tk.Button(master=frm_form, text='create order', command=create_order_for_me)
            btn_done_create_order.grid(row=6, column=0)

            create_new_order_window.mainloop()


        frm_orders = tk.Frame(master=view_order_window)
        frm_orders.pack()

        lb_order = tk.Listbox(master=frm_orders, width=110)
        lb_order.pack(side=tk.LEFT)

        sb_order = tk.Scrollbar(master=frm_orders, orient=tk.VERTICAL)
        sb_order.pack(side=tk.RIGHT, fill=tk.Y)
        lb_order.config(yscrollcommand=sb_order.set)
        sb_order.config(command=lb_order.yview)

        #show order lists
        for order in range(order_list.orderListLength()):
            if order_list.orderList(order)[7] is False:
                order_chain_id = order_list.orderList(order)[0]
                account_name = accounts_list_name.get(order_list.orderList(order)[1])
                token1_name = dic_contracts.get(order_list.orderList(order)[3]).name()
                token1_amount = order_list.orderList(order)[4]
                token2_name = dic_contracts.get(order_list.orderList(order)[5]).name()
                token2_amount = order_list.orderList(order)[6]

                lb_order.insert(order, f'{order_chain_id + 1}. Account: {account_name} Token: {token1_name} Amount: {token1_amount} Want token: {token2_name} Amount: {token2_amount}' )


        btn_apply_order = tk.Button(master=view_order_window, text='Apply', command=apply_for_order)
        btn_apply_order.pack(side=tk.RIGHT, pady=20, padx=20)

        btn_create_order = tk.Button(master=view_order_window, text='Create', command=create_new_order)
        btn_create_order.pack(side=tk.RIGHT, pady=20, padx=20)

        show = tk.Label(view_order_window)
        show.pack()

        view_order_window.mainloop()

    def view_prices():
        view_price_window = tk.Toplevel()
        view_price_window.title('View prices')

        for idx, (name, price) in enumerate(price_lists.items()):
            label1 = tk.Label(master=view_price_window, text=name)
            label2 = tk.Label(master=view_price_window, text=price)

            label1.grid(row=idx, column=0, sticky='e')
            label2.grid(row=idx, column=1)

    def view_accounts():
        view_accounts_window = tk.Toplevel()
        view_accounts_window.title('View account balance')

        frm_form = tk.Frame(master=view_accounts_window, relief=tk.SUNKEN, borderwidth=3)
        frm_form.pack()

        for idx, (contract_name, contract) in enumerate(contracts_list.items()):
            label1 = tk.Label(master=frm_form, text=contract_name)
            label2 = tk.Label(master=frm_form, text=contract.balanceOf(main_label['text']))

            label1.grid(row=idx, column=0, sticky='e')
            label2.grid(row=idx, column=1)

    frm_order_list = tk.Frame(master=main_window)
    frm_order_list.pack()

    btn_view_orders = tk.Button(frm_order_list, text='view order list', command=view_orders).pack(side=tk.LEFT, padx=20, pady=10)
    btn_view_prices = tk.Button(frm_order_list, text='view prices', command=view_prices).pack(side=tk.LEFT, padx=20, pady=10)
    btn_view_accounts = tk.Button(frm_order_list, text='view accounts', command=view_accounts).pack(side=tk.LEFT, padx=20, pady=10)

    # Nft Part
    frm_nft_part = tk.Frame(master=main_window)
    frm_nft_part.pack()

    def create_nft():
        window_create_nft = tk.Toplevel()
        window_create_nft.title("create NFT")

        def done_creating_nft():
            account = main_label['text']
            nft_name = ent_name.get()
            
            nft_token.create(account, nft_name)
            window_create_nft.destroy()

        lbl_name = tk.Label(window_create_nft, text='Enter your nft name')
        ent_name = tk.Entry(window_create_nft)
        lbl_name.pack()
        ent_name.pack()
        btn_name = tk.Button(window_create_nft, text="done", command=done_creating_nft)
        btn_name.pack()

    def view_nft_accounts():
        window_view_nft_account = tk.Toplevel()
        window_view_nft_account.title('view account nfts')
        account_detail = main_label['text']
        for nfts in range(nft_token.nftListLength()):
            if account_detail == nft_token.nftList(nfts)[0]:
                token_name = nft_token.nftList(nfts)[1]
                token_id = nft_token.nftList(nfts)[2]
                lbl = tk.Label(window_view_nft_account, text=f'token id: {token_id}, token name: {token_name}.')
                lbl.pack()

    def view_nft_orders():
        window_view_nft_orders = tk.Toplevel()
        window_view_nft_orders.title("view nft orders")

        frm_lb_orders = tk.Frame(window_view_nft_orders)
        frm_lb_orders.pack()

        def create_new_order():
            window_create_new_order = tk.Toplevel()
            window_create_new_order.title("create new order")

            frm_form = tk.Frame(master=window_create_new_order, relief=tk.SUNKEN, borderwidth=3)
            frm_form.pack()

            def choose_nft():
                window_choose_nft = tk.Toplevel()
                window_choose_nft.title('choose nft')

                account = main_label['text']

                def sel():
                    ent_selected_nft['text'] = str(var.get())
                    window_choose_nft.destroy()

                var = tk.IntVar()

                for token_id in range(nft_token.nftListLength()):
                    if nft_token.nftList(token_id)[0] == account:
                        name = nft_token.nftList(token_id)[1]
                        id = nft_token.nftList(token_id)[2]

                        rbtn_nft = tk.Radiobutton(window_choose_nft, text=f'token {name} id {id}', variable=var, value=id)
                        rbtn_nft.pack(anchor=tk.W)

                btn_done = tk.Button(window_choose_nft, text='select', command=sel)
                btn_done.pack()

            def choose_token():
                choose_token_window = tk.Toplevel()
                choose_token_window.title('select your token')

                selected_account = tk.StringVar()

                for (account_name, account) in contracts_list.items():
                    tk.Radiobutton(choose_token_window, text=account_name, variable=selected_account, value=account).pack()
                
                def done_selecting_account():
                    sel_acc = selected_account.get()
                    lbl_selected_token_value['text'] = sel_acc
                    choose_token_window.destroy()

                btn_done_selecting_account = tk.Button(master=choose_token_window, text='Done', command=done_selecting_account)
                btn_done_selecting_account.pack()

            lbl_select_nft = tk.Label(frm_form, text='choose the nft:')
            btn_select_nft = tk.Button(frm_form, text='choose:', command=choose_nft)

            lbl_select_nft.grid(row=0, column=0, sticky='e')
            btn_select_nft.grid(row=0, column=1)

            lbl_selected_nft = tk.Label(frm_form, text='choosen id: ')
            ent_selected_nft = tk.Label(frm_form, text='')

            lbl_selected_nft.grid(row=1, column=0, sticky='e')
            ent_selected_nft.grid(row=1, column=1)

            lbl_price = tk.Label(frm_form, text='Your NFT price: ')
            ent_price = tk.Entry(frm_form)

            lbl_price.grid(row=2, column=0, sticky='e')
            ent_price.grid(row=2, column=1)

            lbl_token = tk.Label(frm_form, text='choose Token: ')
            btn_token = tk.Button(frm_form, text='Choose', command=choose_token)

            lbl_token.grid(row=3, column=0, sticky='e')
            btn_token.grid(row=3, column=1)

            lbl_selected_token = tk.Label(frm_form, text='selected token: ')
            lbl_selected_token_value = tk.Label(frm_form, text='')

            lbl_selected_token.grid(row=4, column=0, sticky='e')
            lbl_selected_token_value.grid(row=4, column=1)

            def create():
                account_owner = main_label['text']
                nft_id = int(ent_selected_nft['text'])
                nft_name = nft_token.nftList(nft_id)[1]
                price = ent_price.get()
                token_address = lbl_selected_token_value['text']

                nft_order_list.create(account_owner, nft_name, nft_id, price, token_address, {'from': account_owner})
                window_create_new_order.destroy()
                window_view_nft_orders.destroy()

            btn_done = tk.Button(frm_form, text='Create', command=create)
            btn_done.grid(row=5, column=0, sticky='e')

        def apply_for_order():
            nft_order_id = int(lb_order.get(tk.ANCHOR)[0])-1
            account = main_label['text']
            nft_seller = nft_order_list.nftOrderList(nft_order_id)[0]
            token_want = dic_contracts.get(nft_order_list.nftOrderList(nft_order_id)[4])
            sell_price = nft_order_list.nftOrderList(nft_order_id)[3]
            nft_unique_id = nft_order_list.nftOrderList(nft_order_id)[2]
            token_want.transfer(nft_seller, sell_price, {'from': account})
            print(token_want.name())
            nft_order_list.update(nft_order_id, account, {'from': account})
            nft_order_list.toggleCompeleted(nft_order_id, {'from': account})
            nft_token.sellToken(account, nft_unique_id, {'from': account})
            window_view_nft_orders.destroy()

        lb_order = tk.Listbox(master=frm_lb_orders, width=110)
        lb_order.pack(side=tk.LEFT)

        sb_order = tk.Scrollbar(master=frm_lb_orders, orient=tk.VERTICAL)
        sb_order.pack(side=tk.RIGHT, fill=tk.Y)
        lb_order.config(yscrollcommand=sb_order.set)
        sb_order.config(command=lb_order.yview)

        for nft_order in range(nft_order_list.orderListLength()):
            if nft_order_list.nftOrderList(nft_order)[5] is False:
                order_id = nft_order_list.nftOrderList(nft_order)[7]
                nft_name = nft_order_list.nftOrderList(nft_order)[1]
                nft_id = nft_order_list.nftOrderList(nft_order)[2]
                price = nft_order_list.nftOrderList(nft_order)[3]
                token_name = dic_contracts.get(nft_order_list.nftOrderList(nft_order)[4]).name()

                lb_order.insert(nft_order, f"{order_id + 1}-NFT id {nft_id} {nft_name} for price of {price} {token_name} for sell")

        btn_apply_order = tk.Button(master=window_view_nft_orders, text='Apply', command=apply_for_order)
        btn_apply_order.pack(side=tk.RIGHT, pady=20, padx=20)

        btn_create_order = tk.Button(master=window_view_nft_orders, text='Create', command=create_new_order)
        btn_create_order.pack(side=tk.RIGHT, pady=20, padx=20)

    btn_create_nft = tk.Button(master=frm_nft_part, text='create NFT', command=create_nft)
    btn_create_nft.pack(side=tk.LEFT, padx=20)

    btn_view_account_nft = tk.Button(master=frm_nft_part, text='view acc NFTs', command=view_nft_accounts)
    btn_view_account_nft.pack(side=tk.LEFT, padx=20)

    btn_view_nft_orders = tk.Button(master=frm_nft_part, text='NFT orders', command=view_nft_orders)
    btn_view_nft_orders.pack(side=tk.LEFT, padx=20)

    main_window.mainloop()