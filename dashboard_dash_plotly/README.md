# Dash + Plotly Dashboard

This folder contains the official interactive dashboard for the Stack Overflow Developer Survey case study.

## Run Locally

```powershell
python -m pip install -r requirements.txt
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
