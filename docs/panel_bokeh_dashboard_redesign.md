# Panel + Bokeh Dashboard Redesign

## Purpose

Define the recommended redesign direction for the future `Panel` + `Bokeh` dashboard, using the current Cognos dashboard as a narrative baseline but not as a literal template.

The goal is to produce a better portfolio artifact: clearer, more analytical, and more interactive, while staying faithful to the story already supported by the data.

## Design Principle

The new dashboard should keep the same core questions:

1. What technologies dominate today?
2. What technologies show future interest or momentum?
3. Who are the respondents behind those patterns?

But it should not preserve the same presentation one-to-one.

Instead, the Python version should:

- reduce repetition
- improve comparison between current and future states
- make the hierarchy of insights more explicit
- use interaction to support exploration, not to hide the main story

## Best Redesign by Area

### 1. Exact chart selection

Recommended approach:
- keep a small number of high-signal charts
- remove visually redundant charts
- prioritize charts that help compare, rank, and contextualize

Recommended chart set:

#### A. Overview section

Use:
- 3 KPI cards

Suggested KPIs:
- total respondents
- number of countries represented
- number of technologies compared in the dashboard

Why:
- gives immediate context before the user enters detailed charts

#### B. Current technology usage

Use:
- one interactive horizontal bar chart for current technology rankings
- selector buttons to switch between:
  - languages
  - databases
  - platforms
  - web frameworks

Why:
- horizontal bars are the clearest choice for long labels
- the current dataset is ranking-heavy, so ranking charts are more effective than decorative alternatives
- a single reusable chart reduces visual repetition
- the same chart structure fits all four technology families cleanly

Recommended behavior:
- default state: `Languages`
- switching selector buttons updates the same chart in place
- the chart title, color, and tooltip context change with the selected family
- the chart should never be left in an empty or unselected state

#### C. Current vs future comparison

Use:
- one current ranking chart
- one future ranking chart
- one dumbbell chart for direct comparison
- one shared selector for:
  - languages
  - databases
  - platforms
  - web frameworks

Why:
- this is the biggest improvement opportunity over the Cognos version
- separate top-10 panels force the reader to mentally compare two lists
- a dumbbell chart makes the gap between current and future easier to read quickly
- a shared selector keeps the comparison in one analytical place without repeating controls
- putting current and future rankings beside the dumbbell chart makes the comparison easier to interpret

What it should show:
- current rank or count
- future rank or count
- delta between current and future interest

Best use:
- all four technology families can use the same structure cleanly because they share the same multiselect ranking logic

#### D. Demographics and context

Use:
- bar chart for age distribution
- bar chart for education distribution
- top countries bar chart instead of a map as default
- stacked bar chart for age by education

Why:
- the map looks appealing, but it is not the clearest default chart when the analytical point is ranking or concentration
- a ranked country bar chart communicates magnitude faster
- the stacked age-by-education chart preserves the most useful multivariate demographic view

Optional:
- allow switching between bar view and map view for countries

#### E. Salary and work context

Use:
- box plot or violin-like alternative for compensation by remote work
- scatter plot for age midpoint vs work experience

Why:
- these bring the dashboard closer to the deeper analysis already present in the notebook
- they help avoid a dashboard that is only about technology rankings
- they strengthen the narrative around opportunity and respondent context

Recommended rule:
- keep only 1 or 2 contextual analytical charts in addition to the main technology views

## 2. Visual hierarchy

Recommended hierarchy:

### Level 1: answer the main question fast

At the top of the dashboard:
- title
- one-sentence framing
- KPI cards
- one primary comparison chart

Best candidate for the hero visual:
- current vs future languages comparison

Why:
- it immediately communicates both current dominance and future momentum
- it is more insightful than starting with four separate ranking panels

### Level 2: support the main story

Below the hero section:
- detailed rankings by technology family
- current languages
- current databases
- current platforms
- current frameworks

or:
- one tab for current snapshot
- one tab for future comparison

### Level 3: provide interpretation context

After the technology sections:
- demographics
- work mode
- salary/experience context

Why:
- demographics help explain, not lead, the story
- they should support the interpretation of the technology trends rather than compete with them visually

## 3. Level of interaction

Recommended interaction level:
- moderate

Do not build a highly complex BI-style control panel.
Do build enough interaction to make the Python version feel meaningfully more capable than the PDF export.

Recommended interactions:

- tab navigation or section switcher
- hover tooltips on all ranking and comparison charts
- filter by age group
- filter by remote work mode
- filter by selected country group or top-country subset
- metric toggle when useful:
  - count
  - share of respondents

Interactions to avoid at first:

- too many simultaneous filters
- free-form query builders
- drilldowns that create hidden navigation paths
- interactions that make the default dashboard empty or confusing

Rule:
- the dashboard should tell a coherent story with zero interaction
- interaction should enrich exploration, not rescue weak design

## 4. Best way to compare current vs future

This is the area where the redesign should be strongest.

The Cognos version separates present and future into different tabs and repeated top-10 charts.
That works for browsing, but it is not the best form for analytical comparison.

Recommended comparison pattern:

### Primary comparison

Use:
- dumbbell chart for the selected technology family

Why:
- visually efficient
- easier to read quickly for a broad audience
- it works well beside the current and future ranking charts

### Optional enhancement

Use:
- toggle between `Current`, `Future`, and `Delta`

Why:
- lets one chart area serve multiple analytical views
- fits well with Panel widgets

Avoid:
- showing two disconnected bar charts when direct comparison is the real question
- using comparison tables as a primary dashboard device

## 5. Exploration experience using Panel and Bokeh

The Python dashboard should justify itself by doing what the PDF cannot do well.

Best opportunities:

### A. Coordinated views

Examples:
- clicking a technology in the comparison chart highlights its position in a ranking chart
- filtering by age updates both technology and demographic panels
- filtering by remote work updates salary and technology views together

Why:
- this creates an actual exploratory experience, not just a digital poster

### B. Smart tooltips

Tooltips should show:
- exact counts
- share of respondents
- ranking position
- current vs future delta where relevant

Why:
- Bokeh handles this very well
- it reduces clutter while preserving precision

### C. Clean side panel for filters

Recommended layout:
- left sidebar for controls
- main content area for charts
- short markdown notes above key sections

Why:
- Panel excels at this application-like structure
- it keeps the dashboard readable and easy to navigate

### D. Progressive disclosure

Default view:
- show only the most important filters and story panels

Optional advanced view later:
- expose more detailed slicing controls

Why:
- helps keep the first version polished and portfolio-friendly

## 6. Recommended information architecture

Best overall structure:

### Option A. One-page dashboard with sections

Order:
1. overview
2. current vs future hero comparison
3. technology family deep dive
4. respondent context
5. salary and work context

Why:
- strongest for storytelling
- best for portfolio walkthroughs

### Option B. Two tabs, but redesigned

Tabs:
1. Momentum and Comparison
2. Demographics and Context

Why:
- simpler than the Cognos-inspired split
- stronger emphasis on comparison instead of navigation

Recommendation:
- prefer Option B for the first build

Reason:
- easier to implement cleanly
- aligns with the existing project narrative while removing a redundant entry point
- still allows a much better comparison experience inside the comparison tab

## 7. Proposed final recommendation

If we optimize for clarity, feasibility, and portfolio value, the best redesign is:

- keep the 3-topic narrative
- redesign the dashboard around comparison, not duplication
- use horizontal ranking charts for detailed breakdowns
- use dumbbell charts as the primary current-vs-future device
- keep `current ranking`, `future ranking`, and `current vs future` together inside the same comparison tab
- use one shared family selector inside that comparison tab
- replace the country map as the default main demographic view with ranked bars
- keep interaction moderate and purposeful
- use Panel for layout and controls, and Bokeh for linked interactive charts and tooltips

## 8. Practical first-version scope

The strongest first version would include:

1. KPI header
2. one shared technology-family selector inside the comparison tab
3. one current ranking chart
4. one future ranking chart
5. one dumbbell comparison chart
6. age distribution chart
7. top countries bar chart
8. age by education stacked chart
9. one contextual chart for salary or work experience

This scope is large enough to feel substantial, but still focused enough to build cleanly.

## 9. Slope chart as a later alternative

The slope chart remains a valid later experiment, but it is not the preferred comparison visual for the current implementation.

Why defer it:
- it is visually denser
- it asks the reader to parse direction and magnitude at the same time
- the dumbbell chart is easier to understand quickly in this dashboard context

## Current Status

Recommendation documented.

The redesign has informed the current dashboard v1 implementation and remains the reference for future improvements.
