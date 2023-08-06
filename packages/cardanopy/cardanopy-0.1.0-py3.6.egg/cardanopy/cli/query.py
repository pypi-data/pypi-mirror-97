import click
import subprocess
# import os.path
# import uuid
# import json
# import yaml
# import os
# import shutil

# def query_tip():

#
@click.command(context_settings=dict(help_option_names=['-h', '--help']), help="Node query commands. Will query the local node")
@click.option('tip', required=True, type=str, help="Get the node's current tip (slot no, hash, block no).")
def query(option1):
    """Query"""
    print(subprocess.run(["cardano-cli","query","tip","--testnet-magic", "1097911063"], capture_output=True).stdout.decode())