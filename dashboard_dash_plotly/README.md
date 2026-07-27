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

## Deploy On Koyeb

This repository is prepared for Koyeb deployment with Python buildpacks:

- Runtime: Python 3.13, declared in `.python-version`.
- Process command: `Procfile`.
- Web server: `gunicorn --bind :$PORT dashboard_dash_plotly.app:server`.
- Build mode: Buildpack, no Dockerfile required.

In Koyeb, create a Web Service from the GitHub repository, select the target branch, keep the root directory empty if this folder is the repository root, and choose the Free instance while testing.

## Current Scope

- Fixed header with global filters for age and workstyle.
- Side navigation across technology and respondent-context sections.
- KPI cards for respondents, countries, and average compensation.
- Current/future technology rankings showing the Top 10 most mentioned technologies per family.
- Dumbbell momentum charts comparing high-visibility technologies across current use and future interest.
- Age distribution and education composition.
- Compensation by experience and workstyle.
- Country map with a country-count slider.

## Cleaning And Metric Notes

- Text categories are normalized with controlled aliases before the final CSV is produced.
- `ConvertedCompYearly` is the survey-provided annual compensation converted to USD.
- Missing compensation values are median-imputed in the final dataset for completeness.
- Compensation KPI and charts use observed salary records by excluding the imputed median cluster when detected.
