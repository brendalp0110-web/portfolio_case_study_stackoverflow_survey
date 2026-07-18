# Stack Overflow Developer Survey Case Study

Independent data analysis case study centered on developer technology trends, salary signals, and respondent demographics.

## Project Goal

Analyze developer survey data plus supporting job-market signals to answer three practical questions:

1. Which technologies appear most used today?
2. Which technologies show future interest or momentum?
3. What demographic patterns help explain adoption and opportunity?

## Project Scope

This repository keeps the artifacts that are most useful for a hiring manager, recruiter, or reviewer:

- a step-by-step notebook flow from acquisition to dashboarding
- compact source and final datasets
- one final dashboard export as portfolio evidence

## Folder Structure

- `data/`: raw survey input, final reduced survey dataset, and merged job-postings summary
- `notebooks/`: curated process notebooks from acquisition to dashboarding
- `dashboard_panel_bokeh/`: Panel + Bokeh dashboard implementation workspace
- `assets/`: supporting source tables for the acquisition stage
- `docs/`: methodology and curation notes

## Main Deliverables

- [notebooks/01_data_acquisition.ipynb](notebooks/01_data_acquisition.ipynb)
- [notebooks/02_data_cleaning.ipynb](notebooks/02_data_cleaning.ipynb)
- [notebooks/03_eda_statistics.ipynb](notebooks/03_eda_statistics.ipynb)
- [notebooks/05_dashboarding.ipynb](notebooks/05_dashboarding.ipynb)
- [dashboard_panel_bokeh/app.py](dashboard_panel_bokeh/app.py)
- [Capstone Project Dashboard.pdf](<Capstone Project Dashboard.pdf>)

## Key Findings So Far

- JavaScript, SQL, HTML/CSS, TypeScript, and Python lead current reported usage.
- PostgreSQL is strong in both current use and future demand.
- Cloud platforms remain central, with AWS, Azure, and Google Cloud appearing repeatedly.
- The respondent base is concentrated in the 25-34 age range, which matters when interpreting trend adoption.

## Curation Status

This is an initial portfolio-ready draft. The next recommended improvements are:

- sharpen the opening business framing for a non-technical reviewer
- add a short executive-summary notebook or report
- narrow the project to 3-5 strongest insights with business implications
- add one final dashboard screenshot intended as a cover image

See [docs/curation_notes.md](docs/curation_notes.md) for the first-pass curation decisions.
