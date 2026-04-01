from fastapi import FastAPI
import uvicorn
import os
import plotly.graph_objects as go

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

def start_web():
    uvicorn.run(app, host="0.0.0.0", port=8000)
