import typer
from typing_extensions import Annotated
from typing import Optional
from osm import store
from rich import print as rprint
from rich.console import Console
import shutil

app = typer.Typer()

@app.command("delete")
def delete():
    shutil.rmtree(".osmint-cache")