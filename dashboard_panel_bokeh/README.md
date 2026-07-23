# Panel + Bokeh Dashboard Workspace

This folder contains the Python dashboard built with `Panel` and `Bokeh`.

## Main files

- `app.py`: dashboard entry point
- `data_utils.py`: reusable data preparation helpers
- `charts.py`: Bokeh chart builders

## Run locally

From the project root:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m panel serve dashboard_panel_bokeh/app.py --port 5016 --address 127.0.0.1 --allow-websocket-origin 127.0.0.1:5016
```

Then open `http://127.0.0.1:5016/app` in the browser.

For notebooks, select the `Python 3.13 (StackOverflow Survey)` Jupyter kernel.

## Deploy

The dashboard is prepared for an official Docker-based deployment on Render:

- `Dockerfile`: builds a Python 3.13 runtime image for the Panel app.
- `requirements-dashboard.txt`: installs only the dashboard runtime dependencies.
- `render.yaml`: defines the Render web service as infrastructure-as-code.

After pushing the repository to GitHub, create a new Render Blueprint from the repository root. Render will build the Docker image and expose a public `onrender.com` URL.

## Scope

Current version includes:

- a `Momentum and Comparison` tab with subtabs for languages, databases, platforms, and frameworks
- a `Respondent Context` tab with age/education, compensation, and country-distribution subtabs
- a current-vs-future dumbbell comparison for each technology family
- shared filters for top N, age groups, workstyle, and country scope

See [docs/panel_bokeh_dashboard_plan.md](../docs/panel_bokeh_dashboard_plan.md), [docs/panel_bokeh_dashboard_redesign.md](../docs/panel_bokeh_dashboard_redesign.md), and [docs/panel_bokeh_dashboard_v1_spec.md](../docs/panel_bokeh_dashboard_v1_spec.md) for planning context.
