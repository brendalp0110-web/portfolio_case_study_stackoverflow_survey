from __future__ import annotations

from dash import Dash, Input, Output, State, callback_context, dcc, html

from dashboard_dash_plotly import data, figures


FULL_DF = data.load_dataset()
AGE_OPTIONS = [{"label": data.AGE_SHORT_LABELS[value], "value": value} for value in data.AGE_ORDER]
WORKSTYLE_OPTIONS = [{"label": label, "value": value} for value, label in data.REMOTE_WORK_LABELS.items()]
TECH_TOP_N = 12
NOMADIC_COUNT = int((FULL_DF["Country"] == "Nomadic").sum())
NOMADIC_SHARE = NOMADIC_COUNT / max(len(FULL_DF), 1) * 100


app = Dash(__name__, suppress_callback_exceptions=True, title="Stack Overflow Dashboard Mockup")
server = app.server
VIEW_IDS = ["languages", "databases", "platforms", "frameworks", "age-context", "compensation", "country-distribution"]
VIEW_LABELS = {
    "languages": "Languages",
    "databases": "Databases",
    "platforms": "Platforms",
    "frameworks": "Frameworks",
    "age-context": "Age and Education",
    "compensation": "Compensation",
    "country-distribution": "Country Distribution",
}
TECH_COPY = {
    "current_tooltip": "Current-use ranking for the active filters. Counts are shown on the bars; hover for share of respondents.",
    "future_tooltip": "Future-interest ranking for the active filters. Counts are shown on the bars; hover for share of respondents.",
    "momentum_tooltip": "Connects each technology's current use and future interest to reveal momentum within the selected family.",
}
SECTION_COPY = {
    "age_context": "Profile the respondent mix by age and education under the active filters.",
    "compensation": "Compare observed compensation ranges across experience bands and workstyles.",
    "country": "Explore geographic concentration. The local slider controls how many ranked countries appear on the map.",
}
CHART_TOOLTIPS = {
    "age_distribution": "Respondent count by age group. Hover for the share represented by each group.",
    "education_composition": "Education mix within each age group, normalized to 100% so groups are comparable.",
    "remote_compensation": "Observed annual compensation by experience band for remote respondents. Diamond markers show the mean.",
    "hybrid_compensation": "Observed annual compensation by experience band for hybrid respondents. Diamond markers show the mean.",
    "inperson_compensation": "Observed annual compensation by experience band for in-person respondents. Diamond markers show the mean.",
    "map": "Bubble size and color represent each country's share of respondents. Respondent count is secondary and appears only in the tooltip.",
}


def info_icon(text: str) -> html.Span:
    return html.Span("i", title=text, className="info-icon")


def kpi_card(title: str, total: str, total_label: str, filtered: str, filtered_label: str) -> html.Div:
    return html.Div(
        [
            html.Div(title, className="kpi-title"),
            html.Div(
                [
                    html.Div([html.Div(total, className="kpi-value"), html.Div(total_label, className="kpi-caption")]),
                    html.Div([html.Div(filtered, className="kpi-value filtered"), html.Div(filtered_label, className="kpi-caption")], className="kpi-filtered"),
                ],
                className="kpi-body",
            ),
        ],
        className="kpi-card",
    )


def chart_card(title: str, tooltip: str, graph_id: str) -> html.Div:
    return html.Div(
        [
            html.Div([html.H3(title), info_icon(tooltip)], className="chart-title-row"),
            dcc.Graph(id=graph_id, config={"displaylogo": False}, className="chart-graph"),
        ],
        className="chart-card",
    )


def technology_section(family: str) -> html.Section:
    slug = family.lower()
    config = data.TECH_FAMILIES[family]
    return html.Section(
        [
            html.Div([html.H2(family), html.P(config["description"])], className="section-heading"),
            html.Div(
                [
                    chart_card(f"Top Current {family}", TECH_COPY["current_tooltip"], f"{slug}-current"),
                    chart_card(f"Top Future {family}", TECH_COPY["future_tooltip"], f"{slug}-future"),
                ],
                className="chart-grid two",
            ),
            html.Div(
                chart_card(
                    f"Current vs Future {family} Momentum",
                    TECH_COPY["momentum_tooltip"],
                    f"{slug}-momentum",
                ),
                className="dumbbell-row",
            ),
        ],
        id=slug,
        className="dashboard-section view-section",
        style={"display": "block" if slug == "languages" else "none"},
    )


def nav_button(view_id: str) -> html.Button:
    return html.Button(VIEW_LABELS[view_id], id=f"nav-{view_id}", className="nav-button")


def country_slider_marks(max_countries: int) -> dict[int, str]:
    max_value = max(int(max_countries), 1)
    values = [1]
    values.extend(range(10, max_value + 1, 10))
    if max_value not in values:
        values.append(max_value)
    return {value: f"{value}" for value in sorted(set(values))}


def triggered_component_id() -> str | None:
    try:
        return callback_context.triggered_id
    except Exception:
        return None


def layout() -> html.Div:
    return html.Div(
        [
            dcc.Store(id="active-view", data="languages"),
            dcc.Store(id="nav-open", data=True),
            html.Header(
                [
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H1("Developer Technology Trends Dashboard"),
                                    html.Button(
                                        "About",
                                        title="Dash and Plotly mockup using the cleaned Stack Overflow survey dataset.",
                                        className="about-button",
                                    ),
                                ],
                                className="brand-title-row",
                            ),
                        ],
                        className="brand",
                    ),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Span("Global filters", className="filter-title"),
                                    html.Span("Age and workstyle define the active respondent view.", className="filter-help"),
                                ],
                                className="filter-title-row",
                            ),
                            html.Div(
                                [
                                    html.Label("Age"),
                                    dcc.Dropdown(
                                        id="age-filter",
                                        options=AGE_OPTIONS,
                                        value=[],
                                        multi=True,
                                        placeholder="All age groups",
                                        searchable=False,
                                        className="filter-dropdown",
                                    ),
                                    html.Label("Workstyle"),
                                    dcc.Dropdown(
                                        id="workstyle-filter",
                                        options=WORKSTYLE_OPTIONS,
                                        value=[],
                                        multi=True,
                                        placeholder="All workstyles",
                                        searchable=False,
                                        className="filter-dropdown",
                                    ),
                                    html.Button("Reset filters", id="reset-filters", className="primary-button"),
                                ],
                                className="filter-row",
                            ),
                        ],
                        className="filter-panel",
                    ),
                ],
                className="app-header",
            ),
            html.Nav(
                [
                    html.Div([html.Div("Navigation", className="side-nav-title"), html.Button("‹", id="nav-collapse", className="nav-toggle")], className="side-nav-header"),
                    html.Div("Comparison and Momentum", className="nav-group-title"),
                    nav_button("languages"),
                    nav_button("databases"),
                    nav_button("platforms"),
                    nav_button("frameworks"),
                    html.Div("Respondent Context", className="nav-group-title"),
                    nav_button("age-context"),
                    nav_button("compensation"),
                    nav_button("country-distribution"),
                ],
                id="side-nav",
                className="side-nav",
            ),
            html.Button("☰", id="nav-expand", className="nav-rail", title="Open navigation"),
            html.Main(
                [
                    html.Div(id="kpi-row", className="kpi-grid"),
                    technology_section("Languages"),
                    technology_section("Databases"),
                    technology_section("Platforms"),
                    technology_section("Frameworks"),
                    html.Section(
                        [
                            html.Div([html.H2("Age and Education"), html.P(SECTION_COPY["age_context"])], className="section-heading"),
                            html.Div(
                                [
                                    chart_card("Age Distribution", CHART_TOOLTIPS["age_distribution"], "age-distribution"),
                                    chart_card("Education Level Composition by Age Group", CHART_TOOLTIPS["education_composition"], "education-composition"),
                                ],
                                className="chart-grid two",
                            ),
                        ],
                        id="age-context",
                        className="dashboard-section view-section",
                        style={"display": "none"},
                    ),
                    html.Section(
                        [
                            html.Div([html.H2("Compensation by Experience"), html.P(SECTION_COPY["compensation"])], className="section-heading"),
                            html.Div(
                                [
                                    chart_card("Remote Compensation", CHART_TOOLTIPS["remote_compensation"], "remote-compensation"),
                                    chart_card("Hybrid Compensation", CHART_TOOLTIPS["hybrid_compensation"], "hybrid-compensation"),
                                    chart_card("In-person Compensation", CHART_TOOLTIPS["inperson_compensation"], "inperson-compensation"),
                                ],
                                className="chart-grid three",
                            ),
                        ],
                        id="compensation",
                        className="dashboard-section view-section",
                        style={"display": "none"},
                    ),
                    html.Section(
                        [
                            html.Div([html.H2("Country Distribution"), html.P(SECTION_COPY["country"])], className="section-heading"),
                            html.Div(
                                [
                                    html.Label("Countries shown"),
                                    dcc.Slider(
                                        id="country-slider",
                                        min=1,
                                        max=160,
                                        value=160,
                                        step=None,
                                        marks=country_slider_marks(160),
                                        tooltip={"placement": "bottom", "always_visible": True},
                                    ),
                                    html.Div(id="country-note", className="subtle-note"),
                                ],
                                className="map-control",
                            ),
                            chart_card(
                                "Respondent Map by Country",
                                CHART_TOOLTIPS["map"],
                                "country-map",
                            ),
                        ],
                        id="country-distribution",
                        className="dashboard-section view-section",
                        style={"display": "none"},
                    ),
                ],
                id="content-shell",
                className="content",
            ),
        ],
        className="app-shell",
    )


app.layout = layout


@app.callback(
    Output("active-view", "data"),
    *[Input(f"nav-{view_id}", "n_clicks") for view_id in VIEW_IDS],
    prevent_initial_call=True,
)
def set_active_view(*_):
    triggered = callback_context.triggered_id
    if not triggered:
        return "languages"
    return triggered.replace("nav-", "")


@app.callback(
    Output("nav-open", "data"),
    Input("nav-collapse", "n_clicks"),
    Input("nav-expand", "n_clicks"),
    State("nav-open", "data"),
    prevent_initial_call=True,
)
def toggle_navigation(_collapse_clicks, _expand_clicks, is_open):
    triggered = callback_context.triggered_id
    if triggered == "nav-collapse":
        return False
    if triggered == "nav-expand":
        return True
    return is_open


@app.callback(
    Output("side-nav", "className"),
    Output("nav-expand", "className"),
    Output("content-shell", "className"),
    Input("nav-open", "data"),
)
def update_navigation_shell(is_open):
    return (
        "side-nav" if is_open else "side-nav collapsed",
        "nav-rail hidden" if is_open else "nav-rail",
        "content" if is_open else "content nav-collapsed",
    )


@app.callback(
    *[Output(view_id, "style") for view_id in VIEW_IDS],
    *[Output(f"nav-{view_id}", "className") for view_id in VIEW_IDS],
    Input("active-view", "data"),
)
def show_active_view(active_view):
    styles = [{"display": "block" if view_id == active_view else "none"} for view_id in VIEW_IDS]
    classes = ["nav-button active" if view_id == active_view else "nav-button" for view_id in VIEW_IDS]
    return (*styles, *classes)


@app.callback(
    Output("age-filter", "value"),
    Output("workstyle-filter", "value"),
    Input("reset-filters", "n_clicks"),
    prevent_initial_call=True,
)
def reset_filters(_):
    return [], []


@app.callback(
    Output("kpi-row", "children"),
    Output("country-slider", "value"),
    Output("country-slider", "max"),
    Output("country-slider", "marks"),
    Output("country-note", "children"),
    *[Output(f"{family.lower()}-current", "figure") for family in data.TECH_FAMILIES],
    *[Output(f"{family.lower()}-future", "figure") for family in data.TECH_FAMILIES],
    *[Output(f"{family.lower()}-momentum", "figure") for family in data.TECH_FAMILIES],
    Output("age-distribution", "figure"),
    Output("education-composition", "figure"),
    Output("remote-compensation", "figure"),
    Output("hybrid-compensation", "figure"),
    Output("inperson-compensation", "figure"),
    Output("country-map", "figure"),
    Input("age-filter", "value"),
    Input("workstyle-filter", "value"),
    Input("country-slider", "value"),
)
def update_dashboard(selected_ages, selected_workstyles, country_count):
    filtered = data.filter_dataset(FULL_DF, selected_ages, selected_workstyles)
    available_countries = data.country_map_distribution(filtered, None)
    max_countries = max(len(available_countries), 1)
    if triggered_component_id() in {"age-filter", "workstyle-filter"}:
        countries_to_show = max_countries
    else:
        countries_to_show = min(int(country_count or max_countries), max_countries)
    country_df = data.country_map_distribution(filtered, countries_to_show)
    kpis = data.build_kpis(FULL_DF, filtered, len(country_df))

    kpi_cards = [
        kpi_card("Respondents", f"{kpis['respondents_total']:,}", "Dataset total", f"{kpis['respondents_filtered']:,}", "Active filters"),
        kpi_card("Countries", f"{kpis['countries_total']:,}", "Dataset total", f"{kpis['countries_on_map']:,}", "Shown on map"),
        kpi_card("Average Compensation", f"${kpis['salary_total']:,.0f}", "Observed records", f"${kpis['salary_filtered']:,.0f}", "Active filters"),
    ]

    current_figs = []
    future_figs = []
    momentum_figs = []
    for family, config in data.TECH_FAMILIES.items():
        color = figures.TECH_COLORS[family]
        current = data.top_multiselect_counts(filtered, config["current"], TECH_TOP_N, config["label"])
        future = data.top_multiselect_counts(filtered, config["future"], TECH_TOP_N, config["label"])
        comparison = data.comparison_table(filtered, config["current"], config["future"], TECH_TOP_N, config["label"])
        current_figs.append(figures.horizontal_bar(current, config["label"], color))
        future_figs.append(figures.horizontal_bar(future, config["label"], color))
        momentum_figs.append(figures.dumbbell(comparison, config["label"]))

    compensation = data.compensation_records(filtered)
    compensation_summary = data.compensation_box_summary(compensation)
    compensation_y_max = float(compensation_summary["upper"].max() * 1.1) if not compensation_summary.empty else 1.0
    country_note = f"Showing {len(country_df):,} of {max_countries:,} available countries in the active view."

    return (
        kpi_cards,
        countries_to_show,
        max_countries,
        country_slider_marks(max_countries),
        country_note,
        *current_figs,
        *future_figs,
        *momentum_figs,
        figures.age_bar(data.age_distribution(filtered)),
        figures.education_stack(data.age_education_distribution(filtered)),
        figures.compensation_box(compensation_summary, "Remote", compensation_y_max),
        figures.compensation_box(compensation_summary, "Hybrid", compensation_y_max),
        figures.compensation_box(compensation_summary, "In-person", compensation_y_max),
        figures.country_map(country_df),
    )


if __name__ == "__main__":
    app.run(debug=True, port=8050)
