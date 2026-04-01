#!/usr/bin/env python3

import os
import time
import argparse
import webbrowser
from fastapi import FastAPI
import uvicorn
import plotly.graph_objects as go
from rich.live import Live
from rich.table import Table
from rich.console import Console

console = Console()

# -----------------------------
# Tree View
# -----------------------------
def print_tree(path, prefix=""):
    try:
        items = os.listdir(path)
    except PermissionError:
        print(prefix + "[Permission Denied]")
        return

    for item in items:
        full = os.path.join(path, item)

        if os.path.isdir(full):
            print(prefix + "[D] " + item)
            print_tree(full, prefix + "  ")
        else:
            print(prefix + "[F] " + item)


# -----------------------------
# Live Dashboard
# -----------------------------
def generate_table():
    table = Table(title="Live File Dashboard")
    table.add_column("File")
    table.add_column("Size")

    for file in os.listdir("."):
        try:
            size = os.path.getsize(file) if os.path.isfile(file) else 0
        except:
            size = 0
        table.add_row(file, str(size))

    return table


def run_dashboard():
    with Live(generate_table(), refresh_per_second=2) as live:
        while True:
            time.sleep(1)
            live.update(generate_table())


# -----------------------------
# Keyboard Navigation
# -----------------------------
def run_keyboard():
    files = os.listdir(".")
    index = 0

    while True:
        os.system("cls" if os.name == "nt" else "clear")

        for i, f in enumerate(files):
            if i == index:
                print("> " + f)
            else:
                print("  " + f)

        key = input()

        if key == "q":
            break
        elif key == "w":
            index = max(0, index - 1)
        elif key == "s":
            index = min(len(files) - 1, index + 1)


# -----------------------------
# Treemap Web UI
# -----------------------------
app = FastAPI()


def build_data(path):
    labels = []
    parents = []
    values = []

    for root, dirs, files in os.walk(path):
        for d in dirs:
            labels.append(d)
            parents.append(root)
            values.append(1)

        for f in files:
            full = os.path.join(root, f)
            labels.append(f)
            parents.append(root)
            try:
                values.append(os.path.getsize(full))
            except:
                values.append(0)

    return labels, parents, values


@app.get("/")
def treemap():
    labels, parents, values = build_data(".")

    fig = go.Figure(go.Treemap(
        labels=labels,
        parents=parents,
        values=values
    ))

    return fig.to_html(full_html=True)


def run_web():
    port = 8000
    print(f"Starting web UI at http://localhost:{port}")
    webbrowser.open(f"http://localhost:{port}")
    uvicorn.run(app, host="0.0.0.0", port=port)


# -----------------------------
# CLI
# -----------------------------
def main():
    parser = argparse.ArgumentParser(description="Visual File Manager")

    parser.add_argument("-y", "--yes", action="store_true", help="Auto confirm prompts")
    parser.add_argument("-tree", action="store_true", help="Show directory tree")
    parser.add_argument("-dash", action="store_true", help="Run live dashboard")
    parser.add_argument("-web", action="store_true", help="Open web treemap")
    parser.add_argument("-kbd", action="store_true", help="Keyboard navigation mode")

    args = parser.parse_args()

    if args.tree:
        print_tree(".")
    elif args.dash:
        run_dashboard()
    elif args.web:
        run_web()
    elif args.kbd:
        run_keyboard()
    else:
        print("Use -h for help")


if __name__ == "__main__":
    main()
