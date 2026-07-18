# Panel + Bokeh Dashboard Plan

## Purpose

Prepare a second dashboard for this project using `Panel` and `Bokeh`, inspired by the existing Cognos Analytics dashboard but implemented as a Python-based interactive application inside this repository.

This document is only a build plan. It does not start implementation.

## Target Outcome

Create a local dashboard that:

- uses `data/survey_data_cleaned_reduced.csv` as its main source
- preserves the same high-level story as the current dashboard
- is organized around current technologies, future technologies, and demographics
- improves portfolio value by showing dashboard development in Python, not only dashboard consumption

## Proposed Workspace

Use `dashboard_panel_bokeh/` as the dedicated workspace for this second dashboard.

Suggested future structure:

- `dashboard_panel_bokeh/app.py`: main Panel entry point
- `dashboard_panel_bokeh/components/`: reusable charts and layout blocks
- `dashboard_panel_bokeh/data_utils/`: data preparation helpers used by the app
- `dashboard_panel_bokeh/assets/`: local static assets if needed later

## Step-by-Step Plan

### 1. Confirm dashboard scope

Goal:
- Use the Cognos dashboard as a narrative baseline, then define what should be preserved and what should be improved in the Python version.

Tasks:
- review the three existing dashboard tabs
- identify which business questions and visual blocks must remain
- define which visuals should be redesigned instead of replicated literally
- define whether any new filters, interactions, or drilldowns will be added
- use `docs/panel_bokeh_dashboard_redesign.md` as the redesign reference during scoping

Expected output:
- a final scope list for the Python dashboard

### 2. Freeze the data contract

Goal:
- Lock the exact columns and derived metrics that the dashboard will use.

Tasks:
- validate that `survey_data_cleaned_reduced.csv` contains all required fields
- define how multi-select fields will be exploded and counted
- define grouped metrics for age, country, education, languages, databases, platforms, and web frameworks

Expected output:
- a documented list of required columns and transformations

### 3. Add runtime dependencies

Goal:
- Prepare the environment needed to run a Panel + Bokeh app.

Tasks:
- add `panel` and `bokeh` to `requirements.txt`
- decide whether helper libraries such as `numpy` are needed explicitly
- verify local startup with the selected versions

Expected output:
- reproducible environment for dashboard development

### 4. Create the app skeleton

Goal:
- Establish the application structure before building visuals.

Tasks:
- create `app.py`
- define a top-level template or layout
- set up sections or tabs matching the dashboard narrative
- decide whether to keep logic in one file initially or split into modules early

Expected output:
- empty but runnable app shell

### 5. Build the data preparation layer

Goal:
- Centralize all transformations needed by the dashboard.

Tasks:
- load the reduced dataset once
- create reusable functions for top-10 counts
- create reusable grouped tables for demographics
- standardize ordering for age groups and category labels

Expected output:
- reusable data layer that feeds all charts

### 6. Implement Tab 1: Current Technology Usage

Goal:
- Rebuild the current-usage section with Bokeh charts inside Panel.

Tasks:
- create language ranking chart
- create database ranking chart
- create platform ranking chart
- create web framework ranking chart
- align chart titles and labels with the existing portfolio narrative

Expected output:
- first functional tab

### 7. Implement Tab 2: Future Technology Trends

Goal:
- Rebuild the future-interest section using the same visual language.

Tasks:
- create desired languages chart
- create desired databases chart
- create desired platforms chart
- create desired web frameworks chart
- make side-by-side interpretation consistent with Tab 1

Expected output:
- second functional tab

### 8. Implement Tab 3: Demographics

Goal:
- Rebuild the context layer for interpreting technology trends.

Tasks:
- create age distribution chart
- create country distribution view
- create education distribution chart
- create age-by-education grouped view

Expected output:
- third functional tab

### 9. Add interaction and layout polish

Goal:
- Make the Python dashboard feel like a real application rather than a static notebook export.

Tasks:
- add tabs or navigation controls
- add explanatory text blocks where useful
- consider filters such as age, remote work, country, or education only if they improve clarity
- refine spacing, sizing, and responsive behavior

Expected output:
- portfolio-ready interactive dashboard experience

### 10. Validate against the Cognos reference

Goal:
- Ensure the new dashboard stays faithful to the current story while improving implementation transparency.

Tasks:
- compare charts and rankings with `Capstone Project Dashboard.pdf`
- verify category ordering and counts
- confirm that the Python version tells the same story at a glance

Expected output:
- validated parity with the current dashboard narrative

### 11. Document how to run it

Goal:
- Make the dashboard easy to review locally.

Tasks:
- add startup instructions to `README.md`
- document the entry command, expected port, and dependencies
- add a short explanation of what this second dashboard contributes to the portfolio

Expected output:
- reviewer-friendly run instructions

## Development Order Recommendation

Recommended sequence when implementation starts:

1. dependencies
2. app skeleton
3. data helpers
4. current technologies tab
5. future technologies tab
6. demographics tab
7. layout polish
8. validation and documentation

## Guardrails

- Do not create a second derived dataset unless a real need appears.
- Use `data/survey_data_cleaned_reduced.csv` as the single source of truth.
- Keep the dashboard logic reproducible from Python only.
- Prefer clear portfolio storytelling over excessive interactivity.
- Avoid introducing extra files unless they serve the final dashboard directly.

## Current Status

Planning completed and used as the basis for the first implementation.

Dashboard v1 has been implemented locally and is ready for iterative refinement.
