import typer
from typing_extensions import Annotated, Optional
from osm import load
from analyze.changesets import changesets_to_heatmap_df, changesets_to_points_per_day
from plots import heatmap as hm
from plots import daytraces as dtraces
from rich.console import Console

app = typer.Typer()

@app.command("heatmap")
def heatmap(
    username: Annotated[str, typer.Argument(help="The display name of the user to plot data for.")],
    img_out: Annotated[Optional[str], typer.Option(help="Path to store image at. If not set interactive browser rendering will be used")] = None,
):
    """
    Plots a heatmap of coordinates edited by the user.
    """
    console = Console()
    with console.status("[grey][italic]Preparing plot...[/italic][/grey]"):
        try:
            changesets = load.load_changesets(username)
            console.log("Data loaded from cache.")
        except FileNotFoundError:
            console.print(f"No changesets in cache for user {username}. Download data with [red bold italic]'download changesets {username}'[/red bold italic].", style="bold red")
            return

        df = changesets_to_heatmap_df(changesets)
        console.log("Data processed.")

        hm.plot(df, img_out=img_out)
        console.log("Data plotted.")
        if img_out:
            console.log(f"Image written to {img_out}.")

@app.command("daytraces")
def daytraces(
    username: Annotated[str, typer.Argument(help="The display name of the user to plot data for.")],
    img_out: Annotated[Optional[str], typer.Option(help="Path to store image at. If not set interactive browser rendering will be used")] = None,
):
    """
    Plots a map where coordinates edited by the user at the same day are interconnected with lines.
    """
    console = Console()
    with console.status("[grey][italic]Preparing plot...[/italic][/grey]"):
        try:
            changesets = load.load_changesets(username)
            console.log("Data loaded from cache.")
        except FileNotFoundError:
            console.print(f"No changesets in cache for user {username}. Download data with [red bold italic]'download changesets {username}'[/red bold italic].", style="bold red")
            return

        data = changesets_to_points_per_day(changesets)
        console.log("Data processed.")

        dtraces.plot(console, data, img_out=img_out)
        console.log("Data plotted.")
        