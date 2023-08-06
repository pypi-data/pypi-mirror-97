import typer


app = typer.Typer()

@app.callback()
def callback():
    """
    TG Store CLI
    """


@app.command()
def shoot():
    """
    Стрельба 
    """
    typer.echo("Shooting portal gun")


@app.command()
def load():
    """
    Зарядка
    """
    typer.echo("Loading portal gun")

if __name__ == "__main__":
    app()


