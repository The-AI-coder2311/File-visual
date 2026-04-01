import typer
from vfm.dashboard import start_dashboard
from vfm.web import start_web

app = typer.Typer()

@app.command()
def run():
    start_dashboard()

@app.command()
def web():
    start_web()

@app.command()
def tree():
    from vfm.tree import print_tree
    print_tree(".")

def main():
    app()

if __name__ == "__main__":
    main()
