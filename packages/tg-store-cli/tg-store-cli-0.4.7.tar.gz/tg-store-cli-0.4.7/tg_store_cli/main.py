import typer
import json
import requests

app = typer.Typer()

@app.callback()
def callback():
    """
    TG Store CLI
    """

@app.command()
def categories(url: str):
    """
    Список категорий
    """
    typer.echo("Список категорий")
    r = requests.get(f"{url}/categories")
    json_data = json.loads(r.text)
    tt = ""
    for cat in json_data:
        tt += f"{cat['name']} " 
    return print(tt)
    # typer.echo(f"Hello {name} {lastname}")


if __name__ == "__main__":
    app()










