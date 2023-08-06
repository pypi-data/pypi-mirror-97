import click
import subprocess
# import os.path
# import uuid
# import json
# import yaml
# import os
# import shutil

@click.command(context_settings=dict(help_option_names=['-h', '--help']))
def query_tip():
    """Query tip."""
    print(subprocess.run(["cardano-cli","query","tip","--testnet-magic", "1097911063"], capture_output=True).stdout.decode())