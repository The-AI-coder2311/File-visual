#!/usr/bin/env python3

import os
import sys
import argparse
import webbrowser

# GUI
from PySide6 import QtWidgets, QtGui, QtCore

# Web + Visualization
from fastapi import FastAPI
import uvicorn
import plotly.graph_objects as go

# -----------------------------
# Utility
# -----------------------------
def get_tree_data(path):
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


# -----------------------------
# CLI Tree View
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
            print(prefix + f"[D] {item}")
            print_tree(full, prefix + "  ")
        else:
            print(prefix + f"[F] {item}")


# -----------------------------
# Treemap Web UI
# -----------------------------
app = FastAPI()

@app.get("/")
def treemap():
    labels, parents, values = get_tree_data(".")

    fig = go.Figure(go.Treemap(
        labels=labels,
        parents=parents,
        values=values
    ))

    return fig.to_html(full_html=True)


def run_web():
    port = 8000
    webbrowser.open(f"http://localhost:{port}")
    uvicorn.run(app, host="0.0.0.0", port=port)


# -----------------------------
# GUI (Professional Desktop App)
# -----------------------------
class FileManager(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("VFM - Visual File Manager")
        self.setGeometry(200, 100, 1000, 600)

        self.tree = QtWidgets.QTreeWidget()
        self.tree.setHeaderLabel("Files & Folders")

        self.setCentralWidget(self.tree)

        self.load_tree(self.tree.invisibleRootItem(), ".")

        self.tree.itemDoubleClicked.connect(self.on_click)

    def load_tree(self, parent, path):
        try:
            for item in os.listdir(path):
                full = os.path.join(path, item)

                if os.path.isdir(full):
                    node = QtWidgets.QTreeWidgetItem(parent, [f"📁 {item}"])
                    self.load_tree(node, full)
                else:
                    size = 0
                    try:
                        size = os.path.getsize(full)
                    except:
                        pass
                    QtWidgets.QTreeWidgetItem(parent, [f"📄 {item} ({size} bytes)"])
        except PermissionError:
            QtWidgets.QTreeWidgetItem(parent, ["[Permission Denied]"])

    def on_click(self, item, column):
        print("Clicked:", item.text(0))


def run_gui():
    app = QtWidgets.QApplication(sys.argv)
    window = FileManager()
    window.show()
    sys.exit(app.exec())


# -----------------------------
# CLI
# -----------------------------
def main():
    parser = argparse.ArgumentParser(description="Visual File Manager")

    parser.add_argument("-y", "--yes", action="store_true", help="Auto confirm")
    parser.add_argument("-tree", action="store_true", help="Show tree")
    parser.add_argument("-gui", action="store_true", help="Open GUI")
    parser.add_argument("-web", action="store_true", help="Open web treemap")

    args = parser.parse_args()

    if args.tree:
        print_tree(".")

    elif args.gui:
        run_gui()

    elif args.web:
        run_web()

    else:
        print("Use -h for help")


if __name__ == "__main__":
    main()
