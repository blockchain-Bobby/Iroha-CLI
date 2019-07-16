import click
from .iroha_helpers import * 

#ASSET COMMANDS#
def new_asset():
    asset = click.prompt("New Asset Name")
    domain = click.prompt("Domain")
    precision = click.prompt("Precision",type=int)
    create_new_asset(asset,domain,precision)
    
def new_asset_transfer(account_id):
    src_account_id = click.prompt("Source Account",default=account_id)
    recipient = click.prompt("Recipient")
    asset_id = click.prompt("AssetID : asset#domain")
    qty = click.prompt("Total Amount to Send")
    description = click.prompt("Enter Transaction Details")
    transfer_asset(src_account_id,recipient,asset_id,description,qty)
    
def increase_asset_qty():
    asset_id = click.prompt("AssetID : asset#domain")
    qty = click.prompt("Qty To Add")
    add_asset_qty(asset_id,qty)

def decrease_asset_qty():
    asset_id = click.prompt("AssetID : asset#domain")
    qty = click.prompt("Qty To Subtract")
    subtract_asset_qty(asset_id,qty)

#ASSET QUERIES
def view_account_asset_balance(account_id):
    account_id = click.prompt("Account To Use : Username@domain",default=account_id)
    get_account_assets(account_id)

def grant_asset_read_permission(account_id):
    account_id = click.prompt("Account To Use : Username@domain",default=account_id)
    contact = click.prompt("Username@domain Your Write Acc Granting Permission") 
    grant_account_read_permission(creator_account=account_id,contact=contact)

def query_asset_tx_history(account_id):
    account_id = click.prompt("Account To Use : Username@domain",default=account_id)
    total = click.prompt("Total Txs to return",default=50)
    get_acc_tx_history(creator_account=account_id,total=total)

#def query_domain_assets():
#   click.echo("Checking For Pending Transactions That Require Signatures")
#   get_domain_assets()