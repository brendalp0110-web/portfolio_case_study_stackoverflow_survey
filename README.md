# Stack Overflow Developer Survey Case Study

This folder is the curated portfolio version of a broader capstone project. It reframes the strongest parts of the original coursework as a cleaner data analysis case study centered on developer technology trends, salary signals, and respondent demographics.

## Project Goal

Analyze developer survey data plus supporting job-market signals to answer three practical questions:

1. Which technologies appear most used today?
2. Which technologies show future interest or momentum?
3. What demographic patterns help explain adoption and opportunity?

## Why This Version Exists

The original workspace mixes course labs, intermediate datasets, dashboards, and presentation assets. This curated version keeps the artifacts that are most useful for a hiring manager, recruiter, or reviewer:

- a reproducible asset-generation script for dashboard inputs
- reusable chart-generation scripts
- a step-by-step notebook flow from acquisition to dashboarding
- cleaned dashboard-ready CSV outputs
- dashboard exports and presentation figures

## Folder Structure

- `data/`: source files and dashboard-ready CSV assets
- `notebooks/`: curated process notebooks from acquisition to dashboarding
- `scripts/`: reproducible Python scripts for data assets and figures
- `assets/`: exported dashboards and generated figures
- `docs/`: methodology and curation notes

## Main Deliverables

- [notebooks/01_data_acquisition.ipynb](notebooks/01_data_acquisition.ipynb)
- [notebooks/02_data_cleaning.ipynb](notebooks/02_data_cleaning.ipynb)
- [notebooks/03_eda_statistics.ipynb](notebooks/03_eda_statistics.ipynb)
- [notebooks/04_visualizations.ipynb](notebooks/04_visualizations.ipynb)
- [notebooks/05_dashboarding.ipynb](notebooks/05_dashboarding.ipynb)
- [scripts/create_dashboard_assets.py](scripts/create_dashboard_assets.py)
- [assets/dashboard_current.pdf](assets/dashboard_current.pdf)
- [assets/figures/slide_9_programming_language_trends.png](assets/figures/slide_9_programming_language_trends.png)
- [assets/figures/slide_11_database_trends.png](assets/figures/slide_11_database_trends.png)

## Key Findings So Far

- JavaScript, SQL, HTML/CSS, TypeScript, and Python lead current reported usage.
- PostgreSQL is strong in both current use and future demand.
- Cloud platforms remain central, with AWS, Azure, and Google Cloud appearing repeatedly.
- The respondent base is concentrated in the 25-34 age range, which matters when interpreting trend adoption.

## Reproducibility

From this folder:

```bash
python scripts/create_dashboard_assets.py
python scripts/generate_ppt_charts.py
python scripts/generate_trend_charts.py
python scripts/generate_appendix_charts.py
```

## Curation Status

This is an initial portfolio-ready draft. The next recommended improvements are:

- replace course-oriented notebook headings with a portfolio narrative
- add a short executive-summary notebook or report
- narrow the project to 3-5 strongest insights with business implications
- add one final dashboard screenshot intended as a cover image

See [docs/curation_notes.md](docs/curation_notes.md) for the first-pass curation decisions.
