# Panel + Bokeh Dashboard Workspace

This folder contains the first implementation of the Python dashboard built with `Panel` and `Bokeh`.

## Main files

- `app.py`: dashboard entry point
- `data_utils.py`: reusable data preparation helpers
- `charts.py`: Bokeh chart builders

## Run locally

From the project root:

```bash
panel serve dashboard_panel_bokeh/app.py --autoreload
```

Then open the local URL shown by Panel in the terminal.

## Scope

Version 1 includes:

- a momentum and comparison tab
- a demographics and context tab
- a dumbbell chart for current vs future comparison
- shared filters for age, remote work, country scope, metric mode, and top N

See [docs/panel_bokeh_dashboard_plan.md](../docs/panel_bokeh_dashboard_plan.md), [docs/panel_bokeh_dashboard_redesign.md](../docs/panel_bokeh_dashboard_redesign.md), and [docs/panel_bokeh_dashboard_v1_spec.md](../docs/panel_bokeh_dashboard_v1_spec.md) for planning context.
