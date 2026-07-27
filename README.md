# Stack Overflow Developer Survey Case Study

This project analyzes developer technology trends using a curated subset of the public Stack Overflow Developer Survey 2024. The goal is to turn a broad survey dataset into a clear portfolio case study with a reproducible analysis flow and an interactive dashboard.

The final dashboard focuses on three questions:

1. Which technologies are most used today?
2. Which technologies show future interest or momentum?
3. What respondent-context patterns help explain adoption, compensation, and opportunity?

## Data Source

The original source is the public [Stack Overflow Developer Survey 2024](https://survey.stackoverflow.co/2024/). Stack Overflow reports 65,437 responses from 185 countries in the full public survey; this project uses a curated subset of 18,845 records preserved as `data/survey_data_updated.csv`.

The project keeps only the data files needed for the final analysis:

- `data/survey_data_updated.csv`: initial survey subset used as the raw project input.
- `data/survey_data_cleaned_reduced.csv`: final cleaned and reduced dataset used by the notebooks and dashboard.

## Analysis Workflow

The project is organized as a notebook-based pipeline:

1. `01_data_acquisition.ipynb`: documents the survey input used by the project.
2. `02_data_cleaning.ipynb`: cleans, normalizes, imputes, and reduces the dataset.
3. `03_eda_statistics.ipynb`: integrates descriptive analysis, statistics, and visual exploration.
4. `05_dashboarding.ipynb`: documents the final dashboarding layer and how it communicates the analysis.

The workflow intentionally produces one final survey dataset for downstream use: `data/survey_data_cleaned_reduced.csv`.

## Methodological Decisions

The cleaning process prioritizes consistency, interpretability, and a compact final dataset.

- Text normalization: string columns are standardized with deterministic rules and controlled aliases. This prevents equivalent labels from being split into separate categories, such as `Dynamodb` vs. `DynamoDB` or `ASP.NET CORE` vs. `ASP.NET Core`.
- Multiselect normalization: semicolon-separated survey responses are normalized item by item, preserving the multiselect structure while removing duplicate aliases inside each response.
- Missing values: categorical variables are handled with modes or explicit `Not specified` labels depending on analytical use. Numeric fields used in the analysis are filled with medians when appropriate.
- Compensation: `ConvertedCompYearly` is the survey-provided annual compensation converted to USD. Missing values are median-imputed in the final dataset for completeness, while the dashboard compensation views use observed salary records by excluding the imputed median cluster when detected.
- Dataset reduction: the final dataset keeps 32 columns focused on respondent context, experience, compensation, satisfaction, and technology stacks. This reduces noise and keeps the dashboard tied to the project narrative.

## Official Dashboard

The official dashboard is implemented with Dash and Plotly in `dashboard_dash_plotly/`.

It includes:

- Global filters for age and workstyle.
- KPI cards showing total dataset context and active-filter context.
- Hierarchical side navigation for technology and respondent-context views.
- Top 10 current and future technology rankings per family.
- Dumbbell charts comparing high-visibility technologies across current use and future interest.
- Age, education, compensation, and country-distribution views.
- Bilingual interface support for English and Spanish.

Run locally:

```powershell
python -m pip install -r requirements.txt
python -m dashboard_dash_plotly.app
```

Then open:

```text
http://127.0.0.1:8050
```

## Key Findings

- JavaScript, SQL, HTML/CSS, TypeScript, and Python lead current reported language usage.
- PostgreSQL is strong in both current use and future interest.
- AWS, Microsoft Azure, and Google Cloud remain central in platform usage.
- The respondent base is concentrated in the 25-34 age range, which matters when interpreting adoption patterns.
- Compensation varies by experience and workstyle, but observed salary records need to be read carefully because the source survey has many missing salary responses.

## Repository Structure

- `data/`: raw survey subset and final cleaned reduced dataset.
- `notebooks/`: curated process notebooks from acquisition to dashboarding.
- `dashboard_dash_plotly/`: official Dash + Plotly dashboard implementation.
- `docs/`: methodology and curation notes.
- `Capstone Project Dashboard.pdf`: static dashboard evidence retained as a portfolio artifact.

## Main Deliverables

- [notebooks/01_data_acquisition.ipynb](notebooks/01_data_acquisition.ipynb)
- [notebooks/02_data_cleaning.ipynb](notebooks/02_data_cleaning.ipynb)
- [notebooks/03_eda_statistics.ipynb](notebooks/03_eda_statistics.ipynb)
- [notebooks/05_dashboarding.ipynb](notebooks/05_dashboarding.ipynb)
- [dashboard_dash_plotly/app.py](dashboard_dash_plotly/app.py)
- [Capstone Project Dashboard.pdf](<Capstone Project Dashboard.pdf>)
