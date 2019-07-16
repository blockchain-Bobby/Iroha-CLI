import sys
import binascii
from pprint import *
#import click
import os
from iroha import IrohaCrypto as ic
from iroha import Iroha, IrohaGrpc
from iroha.primitive_pb2 import *
import json
from google.protobuf.json_format import MessageToJson, MessageToDict

IROHA_HOST_ADDR = os.getenv('IROHA_HOST_ADDR', '127.0.0.1')
IROHA_PORT = os.getenv('IROHA_PORT', '50051')
net = IrohaGrpc('{}:{}'.format(IROHA_HOST_ADDR, IROHA_PORT),timeout=30)
creator_account = os.getenv('IROHA_ACCOUNT_ID',default='admin@test')
iroha = Iroha(creator_account)
private_key_file = creator_account + '.priv'
user_private_key = open(private_key_file,'rb+').read()

def generate_keypair():
    private_key = ic.private_key()
    public_key = ic.derive_public_key(private_key)
    return public_key, private_key

def save_keys_to_file(account_id):
    private_key = ic.private_key()
    public_key = ic.derive_public_key(private_key)
    private_key_file = account_id + '.priv'
    public_key_file = account_id +'.pub'
    open(private_key_file,'wb+').write(private_key)
    open(public_key_file,'wb+').write(public_key)

def save_to_wallet_db(account_id):
    private_key = ic.private_key()
    public_key = ic.derive_public_key(private_key)
    private_key_file = account_id + '.priv'
    public_key_file = account_id +'.pub'
    open(private_key_file,'wb+').write(private_key)
    open(public_key_file,'wb+').write(public_key)

def check_wallet_exists(account_id):
    try:
        return True
    except:
        print('Please Generate or Rename Keys Correctly') 
        return False

def parse_result(message):
    result = MessageToJson(message=message,preserving_proto_field_name=True)
    return result

def generate_new_node_keys(node_id):
    private_key = ic.private_key()
    public_key = ic.derive_public_key(private_key)
    private_key_file = node_id + '.priv'
    public_key_file = node_id +'.pub'
    open(private_key_file,'wb+').write(private_key)
    open(public_key_file,'wb+').write(public_key)
    return public_key

def send_transaction_and_print_status(transaction):
    global net
    hex_hash = binascii.hexlify(ic.hash(transaction))
    print('Transaction hash = {}, creator = {}'.format(
        hex_hash, transaction.payload.reduced_payload.creator_account_id))
    net.send_tx(transaction)
    for status in net.tx_status_stream(transaction):
        print(status)
    return hex_hash

def send_batch_and_print_status(transactions):
    global net
    net.send_txs(transactions)
    for tx in transactions:
        hex_hash = binascii.hexlify(ic.hash(tx))
        print('\t' + '-' * 20)
        print('Transaction hash = {}, creator = {}'.format(
            hex_hash, tx.payload.reduced_payload.creator_account_id))
        for status in net.tx_status_stream(tx):
            print(status)

def send_batch_and_return_status(transactions):
    global net
    net.send_txs(transactions)
    for tx in transactions:
        hex_hash = binascii.hexlify(ic.hash(tx))
        print('\t' + '-' * 20)
        print('Transaction hash = {}, creator = {}'.format(
            hex_hash, tx.payload.reduced_payload.creator_account_id))
        tx_result = []
        for status in net.tx_status_stream(transactions):
            tx_result.append(status)
        return tx_result

def send_transaction_print_status_and_return_result(transaction):
    global net
    hex_hash = binascii.hexlify(ic.hash(transaction))
    print('Transaction hash = {}, \n creator = {}'.format(
        hex_hash, transaction.payload.reduced_payload.creator_account_id))
    net.send_tx(transaction)
    tx_result = []
    for status in net.tx_status_stream(transaction):
        tx_result.append(status)
        print(status)
    tx_result.append(hex_hash)
    return tx_result

def check_pending_txs():
    query = iroha.query('GetPendingTransactions')
    ic.sign_query(query,user_private_key)
    response = net.send_query(query)
    data = MessageToJson(response)
    pprint(data)

def get_tx_history(account_id,total):
    """
    List total number of tx details for specified user@domain
    """
    query = iroha.query('GetTransactions', account_id=account_id, page_size=total)
    ic.sign_query(query, user_private_key)
    response = net.send_query(query)
    data = MessageToDict(response)
    pprint(data,indent=2)

#Accounts

def get_account_assets(account_id):
    
    query = iroha.query('GetAccountAssets', account_id=account_id)
    ic.sign_query(query, user_private_key)
    response = net.send_query(query)
    data = MessageToJson(response)
    pprint(data,indent=2)

def get_asset_info(account_id,asset_id):
    
    query = iroha.query('GetAssetInfo', asset_id=asset_id)
    ic.sign_query(query, user_private_key)
    response = net.send_query(query)
    data = MessageToJson(response)
    pprint(data,indent=2)

def get_acc_tx_history(account_id,total):
    """
    List total number of tx details for specified user@domain
    """
    query = iroha.query('GetAccountTransactions', account_id=account_id, page_size=total)
    ic.sign_query(query, user_private_key)
    response = net.send_query(query)
    data = MessageToDict(response)
    pprint(data,indent=2)

def get_asset_tx_history(account_id,total):
    """
    List Asset tx details for specified user@domain
    """
    query = iroha.query('GetAccountAssetTransactions', account_id=account_id, page_size=total)
    ic.sign_query(query, user_private_key)
    response = net.send_query(query)
    data = MessageToDict(response)
    pprint(data,indent=2)

def get_roles():
    """
    List Roles
    """
    query = iroha.query('GetRoles')
    ic.sign_query(query, user_private_key)
    response = net.send_query(query)
    data = MessageToDict(response)
    pprint(data,indent=2)

def get_role_permissions(role_id):
    """
    List Role Permissions for specified Role
    """
    query = iroha.query('GetRolePermissions',role_id=role_id)
    ic.sign_query(query, user_private_key)
    response = net.send_query(query)
    data = MessageToDict(response)
    pprint(data,indent=2)

def stream_blocks():
    """
    Start incomming stream for new blocks
    """
    #add height
    query = iroha.blocks_query()
    ic.sign_query(query, user_private_key)
    for block in net.send_blocks_stream_query(query):
        pprint('The next block arrived: {}'.format(MessageToDict(block)),indent=1)

def get_signatories(account_id):
    """
    List signatories by public key for specified user@domain
    """
    query = iroha.query('GetSignatories', account_id=account_id)
    ic.sign_query(query, user_private_key)
    response = net.send_query(query)
    data = MessageToDict(response)
    pprint(data,indent=2)

def get_account(account_id):
    """
    List Account user@domain
    """
    query = iroha.query('GetAccount', account_id=account_id)
    ic.sign_query(query, user_private_key)
    response = net.send_query(query)
    data = MessageToDict(response)
    pprint(data,indent=2)

def get_account_details(account_id,writer,key):
    """
    List Account details for user@domain
    """
    query = iroha.query('GetAccountDetail', account_id=account_id,writer=writer,key=key)
    ic.sign_query(query, user_private_key)
    response = net.send_query(query)
    data = json.loads(response.account_detail_response.detail)
    pprint(data)
    
def get_domain_assets():
    query = iroha.query('GetDomainAssets')
    ic.sign_query(query, user_private_key)
    response = net.send_query(query)
    data = MessageToDict(response)
    pprint(data,indent=2)

def create_new_account(account_name,domain,public_key):
    """
    register new user
    """
    tx = iroha.transaction([
        iroha.command('CreateAccount', account_name=account_name, domain_id=domain,
                      public_key=public_key)
    ])
    ic.sign_transaction(tx, user_private_key)
    send_transaction_print_status_and_return_result(tx)

def set_account_detail(account_id,key,value):
    tx = iroha.transaction([
        iroha.command('SetAccountDetail',
                      account_id=account_id, key=key, value=value)
    ])
    ic.sign_transaction(tx, user_private_key)
    send_transaction_print_status_and_return_result(tx)

def create_domain(domain_id,default_role):
    """
    register non existing/new domain on network
    """
    tx = iroha.transaction([iroha.command('CreateDomain', domain_id=domain_id, default_role='user')])
    ic.sign_transaction(tx, user_private_key)
    send_transaction_print_status_and_return_result(tx)

def grant_account_write_permission(account_id):
    tx = iroha.transaction([
            iroha.command('GrantPermission', account_id=account_id, permission=can_set_my_account_detail)
        ])
    ic.sign_transaction(tx, user_private_key)
    send_transaction_print_status_and_return_result(tx)

def grant_account_read_permission(account_id):
    tx = iroha.transaction([
            iroha.command('GrantPermission', account_id=account_id, permission=can_get_my_acc_detail)
        ])
    ic.sign_transaction(tx, user_private_key)
    send_transaction_print_status_and_return_result(tx)

#add signatory
#remove signatory

def add_peer(ip_address,peer_key):
    peer = Peer()
    peer.address = ip_address
    peer.peer_key = peer_key
    tx = iroha.transaction([
            iroha.command('AddPeer', peer=peer)
        ])
    ic.sign_transaction(tx, user_private_key)
    send_transaction_print_status_and_return_result(tx)

def grant_asset_tx_history_permission(account_id):
    tx = iroha.transaction([
            iroha.command('GrantPermission', account_id=account_id, permission=can_get_my_acc_ast_txs)
        ])
    ic.sign_transaction(tx, user_private_key)
    send_transaction_print_status_and_return_result(tx)

def grant_account_tx_history_permission(account_id):
    tx = iroha.transaction([
            iroha.command('GrantPermission', account_id=account_id, permission=can_get_my_acc_txs)
        ])
    ic.sign_transaction(tx, user_private_key)
    send_transaction_print_status_and_return_result(tx)

def create_new_asset(asset,domain,precision):
    tx = iroha.transaction(
        [iroha.command('CreateAsset', asset_name=asset,
            domain_id=domain, precision=precision)]    )
    ic.sign_transaction(tx, user_private_key)
    send_transaction_print_status_and_return_result(tx)

def transfer_asset(account_id,recipient,asset_id,description,qty):
    tx = iroha.transaction([
        iroha.command('TransferAsset', src_account_id=account_id, dest_account_id=recipient,
                      asset_id=asset_id, description=description, amount=qty)])
    ic.sign_transaction(tx, user_private_key)
    send_transaction_print_status_and_return_result(tx)

def create_atomic_batch_transaction(user_1,user_2,asset_1,asset_2,asset_1_qty,asset_2_qty):
    tx_1 = iroha.transaction(
        [iroha.command(
            'TransferAsset', src_account_id=user_1, dest_account_id=user_2, asset_id=asset_1,
            amount=asset_1_qty
        )],
        creator_account=user_1,
    )
    tx_2 = iroha.transaction(
        [iroha.command(
            'TransferAsset', src_account_id=user_2, dest_account_id=user_1, asset_id=asset_2,
            amount=asset_2_qty
        )],
        creator_account=user_2)        
    iroha.batch([tx_1, tx_2], atomic=True)
    # sign transactions only after batch meta creation
    ic.sign_transaction(tx_1, *user_private_key)
    tx_batch = [tx_1,tx_2]
    send_batch_and_return_status(tx_batch)

def add_asset_qty(asset_id, qty):
    """
    Add asset supply
    """    
    tx = iroha.transaction([
        iroha.command('AddAssetQuantity',
                      asset_id=asset_id, amount=qty)
    ])
    ic.sign_transaction(tx, user_private_key)
    send_transaction_print_status_and_return_result(tx)

def subtract_asset_qty(asset_id, qty):
    """
    Subtract asset supply
    """
    tx = iroha.transaction([
        iroha.command('SubtractAssetQuantity',
                      asset_id=asset_id, amount=qty)
    ])
    ic.sign_transaction(tx, user_private_key)
    send_transaction_print_status_and_return_result(tx)