import click
import subprocess
from pathlib import Path
from .cardanopy_config import CardanoPyConfig
import json

@click.command()
@click.option('--dry-run', 'dry_run', is_flag=True, help="print the mutable commands")
@click.option('--config-filename', 'config_filename', default='cardanopy.yaml', type=str, help="defaults to 'cardanopy.yaml'")
@click.argument('target_dir', type=str)
@click.pass_context
def run(ctx, dry_run, target_dir, config_filename):
    """Run command"""

    if dry_run:
        print("#### DRY RUN - no mutable changes will be made. ####")

    target_dir = Path(target_dir)

    if not target_dir.is_dir():
        ctx.fail(f"Target directory '{target_dir}' is not a directory. e.g., the directory that contains 'cardanopy.yaml'")
        return 1

    if not target_dir.exists():
        ctx.fail(f"Target directory '{target_dir}' does not exist.")
        return 1

    target_config = target_dir.joinpath(config_filename)

    if not target_config.is_file():
        ctx.fail(
            f"Target config '{target_config}' is not a file. e.g., 'cardanopy.yaml'")
        return 1

    if not target_config.exists():
        ctx.fail(f"Target file '{target_config}' does not exist.")
        return 1

    config = CardanoPyConfig()
    if not config.load(target_config):
        ctx.fail(f"Failed to load '{target_config}'")
        return 1

    generate_topology(dry_run, target_dir, config)

    cardano_node_cmd = ["cd", f"{target_dir}", "&&",
                        "cardano-node",
                        "run",
                        "--config", config.config,
                        "--topology", config.topologyPath,
                        "--database-path", config.databasePath,
                        "--host-addr", config.hostAddr,
                        "--port", f"{config.port}",
                        "--socket-path", config.socketPath]
    if dry_run:
        print(" ".join(cardano_node_cmd))
    else:
        try:
            subprocess.run(cardano_node_cmd)
        except Exception as ex:
            ctx.fail(f"Unknown exception: {type(ex).__name__} {ex.args}")
            return 1


def generate_topology(dry_run: bool, target_dir: Path, config: CardanoPyConfig):
    if dry_run:
        print(f"generate 'topology.json' file config.topologyPath to `{config.topologyPath}'")
    else:
        with open(target_dir.joinpath(config.topologyPath), "w") as file:
            print(json.dumps(config.topology, sort_keys=True, indent=4), file=file)