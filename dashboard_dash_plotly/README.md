# Dash + Plotly Dashboard Mockup

This folder contains an experimental Dash + Plotly recreation of the dashboard mockup.

It is intentionally separate from `dashboard_panel_bokeh/` so layout and interaction ideas can be tested without affecting the Panel/Bokeh implementation.

## Run Locally

```powershell
python -m pip install -r requirements-dash.txt
python -m dashboard_dash_plotly.app
```

Open:

```text
http://127.0.0.1:8050
```

## Current Scope

- Fixed header with global filters for age and workstyle.
- Side navigation across technology and respondent-context sections.
- KPI cards for respondents, countries, and average compensation.
- Current/future technology rankings and dumbbell momentum charts.
- Age distribution and education composition.
- Compensation by experience and workstyle.
- Country map with a country-count slider.
