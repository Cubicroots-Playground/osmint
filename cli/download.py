import typer
from typing_extensions import Annotated
from typing import Optional
from osm import store
from rich import print as rprint
from rich.console import Console

app = typer.Typer()

@app.command("changesets")
def changesets(
    username: Annotated[str, typer.Argument(help="The display name of the user to query changesets for.")],
    changesets_limit: Annotated[Optional[int], typer.Option(help="Amount of changesets to query.")] = 100,
    ):
    console = Console()
    with console.status("[grey][italic]Downloading data ...[/italic][/grey]"):
        store.store_changesets(username, changesets_limit=changesets_limit)
    rprint(f"[green]Downloaded {changesets_limit} changesets for user [italic][bold]{username}[/bold][/italic][/green]")