import typer
from cli import download

app = typer.Typer()
app.add_typer(download.app, name="download")

if __name__ == "__main__":
    app() 