# Dash + Plotly Dashboard

This folder contains the official interactive dashboard for the Stack Overflow Developer Survey case study. The dashboard is built with Dash and Plotly and reads the cleaned, reduced survey subset from `data/survey_data_cleaned_reduced.csv`.

## Data Context

The dashboard uses a curated subset of the public Stack Overflow Developer Survey 2024 dataset:

- Source: https://survey.stackoverflow.co/2024/
- Original public survey scope: 65,437 responses from 185 countries
- Project input scope: 18,845 records in `data/survey_data_updated.csv`

The dashboard also uses local country centroid coordinates from `dashboard_dash_plotly/assets/country_centroids.csv` to render the geographic view.

## Run Locally

```powershell
python -m pip install -r requirements.txt
python -m dashboard_dash_plotly.app
```

Open:

```text
http://127.0.0.1:8050
```

## Deploy On Plotly Cloud

The official hosted dashboard is deployed on Plotly Cloud. For deployment, upload a minimal app package rather than the full project repository.

Public dashboard: [https://3c9d9e62-a7d7-41ea-907f-aa83ef0012f9.plotly.app/](https://3c9d9e62-a7d7-41ea-907f-aa83ef0012f9.plotly.app/)

The Plotly Cloud package should include:

- A root `app.py` file defining the Dash app.
- `dashboard_dash_plotly/` with the dashboard source and assets.
- `data/survey_data_cleaned_reduced.csv`.
- `requirements.txt` with the runtime dependencies needed by the app.

Recommended Plotly Cloud configuration:

- Main file: `app.py`.
- Python version: `3.13`.
- Compute: `Sleep - Starter` while using the free workspace.
- Environment variables: none required.

The deployment package used for Plotly Cloud should keep dependencies focused on the dashboard runtime: Dash, Plotly, pandas, and NumPy.

## Current Scope

- Fixed header with global filters for age and workstyle.
- Side navigation across technology and respondent-context sections.
- KPI cards for respondents, countries, and average compensation.
- Current technology rankings as Top 10 horizontal bar charts.
- Future-interest technology rankings as Top 10 treemaps, where larger tiles indicate more respondent mentions.
- Dumbbell momentum charts comparing high-visibility technologies across current use and future interest.
- Age distribution and education composition.
- Compensation distribution by experience and workstyle, with empty-state notes when a filtered workstyle has no observed salary records.
- Job-satisfaction trend lines by experience and workstyle, with low-sample points marked separately.
- Country map with a local country-count input.

## Cleaning And Metric Notes

- Text categories are normalized with controlled aliases before the final CSV is produced.
- `ConvertedCompYearly` is the survey-provided annual compensation converted to USD.
- Missing compensation values are median-imputed in the final dataset for completeness.
- Compensation KPI and charts use observed salary records by excluding the imputed median cluster when detected.
- Job-satisfaction lines use valid `JobSat` records only. Solid points require at least 10 records; low-sample points are shown as X markers and should be read as directional context, not a stable trend.
