import click

from cardanopy.cli.query.tip import tip

@click.group("query")
@click.pass_context
def query(ctx):
    pass

# export
query.add_command(tip, "tip")