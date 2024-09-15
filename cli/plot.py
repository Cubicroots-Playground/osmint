import typer
from typing_extensions import Annotated
from osm import load
from analyze.changesets import changesets_to_heatmap_df
from plots import heatmap as hm

app = typer.Typer()

@app.command("heatmap")
def heatmap(
     username: Annotated[str, typer.Argument(help="The display name of the user to plot data for.")],
):
    changesets = load.load_changesets(username)
    df = changesets_to_heatmap_df(changesets)

    hm(df)

    raise Exception("implement me")