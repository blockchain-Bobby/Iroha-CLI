import click
from .iroha_helpers import * 

#ACCOUNT COMMANDS
def create_new_user_account():
    user_name = click.prompt("Username For New Account")
    domain = click.prompt("Domain")
    public_key = click.prompt("Public Key")
    create_new_account(user_name,domain,public_key)
   
def write_account_detail():
    account_id = click.prompt("Account To Use : Username@domain",default=os.getenv('IROHA_ACCOUNT_ID'))
    key = click.prompt("Enter New Key, existing key entries will be overwritten") 
    value = click.prompt("Please enter a value to set")
    set_account_detail(account_id,key,value)

def grant_acc_read_permission():
    account_id = click.prompt("Account To Use : Username@domain",default=account_id)
    contact = click.prompt("Username@domain Your Write Acc Granting Permission") 
    grant_account_read_permission(account_id=account_id,contact=contact)

#ACCOUNT QUERIES

def view_account(account_id):
    account_id = click.prompt("Account To Use : Username@domain",default=account_id)
    get_account(account_id)

def view_account_detail(account_id):
    account_id = click.prompt("Account To Use : Username@domain",default=account_id)
    writer = click.prompt("Writer To Account",default=None)
    key = click.prompt("Enter A Key",default=None) 
    get_account_details(account_id)

def view_signatories(account_id):
    account_id = click.prompt("Account To Use : Username@domain",default=account_id)
    get_signatories(account_id)

def query_account_tx_history(account_id):
    account_id = click.prompt("Account To Use : Username@domain",default=account_id)
    total = click.prompt("Total Txs to return",default=50)
    get_acc_tx_history(account_id=account_id,total=total)

def query_tx_history(account_id):
    account_id = click.prompt("Account To Use : Username@domain",default=account_id)
    total = click.prompt("Total Txs to return",default=50)
    get_tx_history(account_id=account_id,total=total)

def query_pending_txs():
    click.echo("Checking For Pending Transactions That Require Signatures")
    check_pending_txs()

def stream_new_blocks():
    click.echo("Streaming New Blocks")
    while True:
        stream_blocks()

def view_roles():
    click.echo("Getting Roles")
    get_roles()

def view_role_permissions():
    role_id = click.prompt("Role ID To View Permissions",default='user')
    get_role_permissions(role_id)