import click
from .account_commands import *
from .asset_commands import new_asset, increase_asset_qty,decrease_asset_qty,new_asset_transfer
from .menu_nav import *

def main_menu():
    user_choice = None 
    while user_choice != 'exit':
        user_choice = click.prompt(menu_text,show_choices=menu_options)
        if user_choice == '1':
            user_choice = None
            user_choice = click.prompt(commands_menu,show_choices=menu_options)
            if user_choice == '1':
                create_new_user_account()
            elif user_choice == '2':
                write_account_detail()
            elif user_choice == '3':
                click.echo('command to be implemented')
            elif user_choice == '4':
                click.echo('command to be implemented')
            elif user_choice == '5':
                click.echo('command to be implemented')
            elif user_choice == '6':
                click.echo('command to be implemented')
            elif user_choice == '7':
                click.echo('command to be implemented')
            elif user_choice == '8':
                click.echo('command to be implemented')
            elif user_choice == '9':
                click.echo('command to be implemented')
            elif user_choice == '10':
                view_asset_balance(account_id)
            elif user_choice == '11':
                new_asset()
            elif user_choice == '12':
                increase_asset_qty()
            elif user_choice == '13':
                decrease_asset_qty()
            elif user_choice == '14':
                new_asset_transfer(account_id)
            else:
                click.echo('Please Select Correct Option')
                user_choice = None
    print("exiting....Thank You  <[-_-]>... Developed By The Plenteum Team")