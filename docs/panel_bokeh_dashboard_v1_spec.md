# Panel + Bokeh Dashboard V1 Specification

## Purpose

Define the exact first implementation scope for the Python dashboard built with `Panel` and `Bokeh`.

This specification turns the redesign direction into a concrete v1 build target.

## Product Goal

Deliver a local interactive dashboard that:

- uses `data/survey_data_cleaned_reduced.csv` as the single source of truth
- preserves the project narrative while simplifying navigation
- improves comparison between current and future technology signals
- demonstrates dashboard engineering in Python as a portfolio asset

## V1 Scope

The first version will use 2 tabs:

1. `Momentum and Comparison`
2. `Demographics and Context`

The app will include a shared sidebar with moderate filtering and metric controls.

## Shared Controls

V1 sidebar controls:

- age group filter
- remote work filter
- country scope selector
- metric selector:
  - respondent count
  - share of respondents
- top N selector for ranking charts

Expected behavior:

- all tabs update from the same filtered dataset
- default state should already tell a coherent story without user interaction

## Tab 1: Momentum and Comparison

Purpose:
- compare current vs future interest directly instead of forcing visual comparison across separate tabs

Content:

- KPI row
- one shared technology-family selector
- one current ranking chart
- one future ranking chart
- one dumbbell chart for direct comparison

Visual types:

- KPI cards
- selector buttons
- horizontal bar charts
- dumbbell chart

Reasoning:

- all four technology families follow the same analytical structure, so one shared selector is cleaner than separate comparison blocks
- current and future rankings should sit next to the dumbbell chart so the reader can interpret movement and magnitude together
- comparison tables are intentionally excluded because they communicate less clearly than the charts in this dashboard context

## Tab 2: Demographics and Context

Purpose:
- provide the respondent context needed to interpret the technology story

Content:

- age distribution
- top countries distribution
- education distribution
- age by education stacked chart
- compensation by remote work
- age vs work experience

Visual types:

- bar charts
- stacked bars
- box plot
- scatter plot

Reasoning:

- this tab anchors the technology story in who the respondents are and what work context they report

## Interaction Model

V1 interaction should be moderate and purposeful.

Included:

- filter-driven updates
- hover tooltips on charts
- responsive ranking depth via top N
- current vs future comparison through coordinated ranking charts and a dumbbell chart

Deferred:

- drill-down navigation
- advanced cross-highlighting
- free-form filtering across 100+ countries
- custom export actions

## Information Hierarchy

Highest priority insight:
- current vs future language momentum

Second layer:
- current and future technology rankings by family

Third layer:
- respondent composition and work context

This means:

- the comparison tab should feel analytical
- the demographics tab should feel explanatory

## File Layout

Planned implementation files:

- `dashboard_panel_bokeh/app.py`
- `dashboard_panel_bokeh/data_utils.py`
- `dashboard_panel_bokeh/charts.py`
- `dashboard_panel_bokeh/README.md`

## Success Criteria

V1 is successful when:

- the app starts locally with `panel serve`
- both tabs render without notebook dependencies
- the charts update from sidebar filters
- current vs future comparison is clearer than in the Cognos PDF
- the dashboard feels portfolio-ready even before later polish

## Explicit Non-Goals for V1

V1 will not:

- reproduce the Cognos dashboard pixel by pixel
- introduce a new derived dataset
- implement every possible comparison for every technology family
- optimize for deployment before local usability is solid

## Current Status

Approved as the target for implementation.
