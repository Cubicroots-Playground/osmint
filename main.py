import typer
from cli import download, plot

app = typer.Typer()
app.add_typer(download.app, name="download")
app.add_typer(plot.app, name="plot")

if __name__ == "__main__":
    app() 