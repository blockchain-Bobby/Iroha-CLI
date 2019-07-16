import os
import click
import six
#from cli.iroha_helpers.utils import save_wallet, check_wallet_exists 
from cli.main import main_menu
import argparse

#Startup Arguments
#naming conventions to be standardized
parser = argparse.ArgumentParser()
parser.add_argument("--account-id", help="Iroha Account ID Must Match Private Key Existing In CLI Root Folder e.g admin@test.priv", required=True)
parser.add_argument("--ip", help="Iroha Node IP Address Excluding Port. Default 127.0.0.1 ", required=False, default='127.0.0.1')
parser.add_argument("--port", type=int, help="Iroha port. Default : 50051", required=False, default=50051)
parser.add_argument("--generate", type=bool,help="Generate A New KeyPair - Provide with flag \n --generate True ", required=False, default=False)

#sets user account to default creator account
iroha_config = parser.parse_args()

def main(iroha_config=iroha_config):
    #if check_wallet_exists(account_id) == True:
    print(iroha_config)
    main_menu()
    #main_menu(account_id)
    #save_wallet(account_id)
    
if __name__ == "__main__":
    main()