import typer
from cli import download, plot, cache

app = typer.Typer()
app.add_typer(download.app, name="download")
app.add_typer(plot.app, name="plot")
app.add_typer(cache.app, name="cache")

if __name__ == "__main__":
    app() 