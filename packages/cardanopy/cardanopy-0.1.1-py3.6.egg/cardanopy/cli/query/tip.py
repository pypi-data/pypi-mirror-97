import click
import subprocess
# import os.path
# import uuid
# import json
# import yaml
# import os
# import shutil

#  help="Node query commands. Will query the local node"
@click.command(context_settings=dict(help_option_names=['-h', '--help']))
# @click.option('tip', required=True, type=str, help="Get the node's current tip (slot no, hash, block no).")
def tip():
    """Query TIP"""
    print("query_tip")
    print(subprocess.run(["cardano-cli","query","tip","--testnet-magic", "1097911063"], capture_output=True).stdout.decode())

# @click.group()
# @click.version_option(version='0.1.0')
# @click.pass_context
# def query():
#     """Query"""
#     print("query")