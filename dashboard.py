from rich.live import Live
from rich.table import Table
import os
import time

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

def start_dashboard():
    with Live(generate_table(), refresh_per_second=2) as live:
        while True:
            time.sleep(1)
            live.update(generate_table())
