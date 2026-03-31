import os
from rich.console import Console
from rich.tree import Tree
from rich.prompt import Prompt

console = Console()

def run_app(args):
    console.print("[bold green]Visual File Manager Started[/bold green]")
    console.print("Commands: [tree], [size], [search], [exit]")

    while True:
        cmd = Prompt.ask("vfm")

        if cmd == "exit":
            break

        elif cmd == "tree":
            show_tree(os.getcwd())

        elif cmd == "size":
            console.print("Size view not implemented yet")

        elif cmd.startswith("search"):
            console.print("Search not implemented yet")


def show_tree(path):
    tree = Tree(f"[bold blue]{path}[/bold blue]")

    def add_branch(tree_node, directory):
        try:
            for item in os.listdir(directory):
                full_path = os.path.join(directory, item)

                if os.path.isdir(full_path):
                    branch = tree_node.add(f"[blue]{item}/[/blue]")
                    add_branch(branch, full_path)
                else:
                    tree_node.add(item)
        except PermissionError:
            tree_node.add("[red]Permission Denied[/red]")

    add_branch(tree, path)
    console.print(tree)
