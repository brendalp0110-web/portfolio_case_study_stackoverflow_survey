from __future__ import annotations

import sys
from pathlib import Path

import panel as pn


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from dashboard_panel_bokeh.charts import (  # noqa: E402
    TECH_COLORS,
    make_country_bubble_map,
    REMOTE_COLORS,
    make_dumbbell_chart,
    make_age_percent_bar_chart,
    make_compensation_experience_box_plot,
    make_grouped_box_plot,
    make_horizontal_bar_chart,
    make_percent_stacked_bar_chart,
    make_stacked_bar_chart,
)
from dashboard_panel_bokeh.data_utils import (  # noqa: E402
    AGE_ORDER,
    age_distribution,
    age_education_distribution,
    build_comparison_table,
    build_kpis,
    country_map_distribution,
    filter_dataset,
    load_dataset,
    metric_column,
    REMOTE_WORK_LABELS,
    salary_remote_experience_box_summary,
    top_multiselect_counts,
)


pn.extension(
    sizing_mode="stretch_width",
    raw_css=[
        """
        .bk-root {
          font-size: 15px;
        }
        .bk-root h2 {
          font-size: 24px;
        }
        .bk-root h3 {
          font-size: 22px;
          margin: 8px 0 8px 0;
        }
        .bk-root h4 {
          font-size: 17px;
          margin: 4px 0 8px 0;
        }
        .bk-root .bk-input,
        .bk-root select,
        .bk-root label {
          font-size: 14px;
        }
        .bk-root .bk-btn {
          font-size: 13px;
        }
        .bk-root .bk-tab {
          font-size: 14px;
          padding: 10px 16px;
        }
        """
    ],
)

DATASET_PATH = PROJECT_ROOT / "data" / "survey_data_cleaned_reduced.csv"
BASE_DF = load_dataset(DATASET_PATH)
REMOTE_OPTIONS = BASE_DF["RemoteWork"].value_counts().index.tolist()
MOMENTUM_OPTIONS = {
    "Languages": {
        "current_column": "LanguageHaveWorkedWith",
        "future_column": "LanguageWantToWorkWith",
        "label": "language",
        "color_key": "languages",
        "current_title": "Top Current Languages",
        "future_title": "Top Future Languages",
    },
    "Databases": {
        "current_column": "DatabaseHaveWorkedWith",
        "future_column": "DatabaseWantToWorkWith",
        "label": "database",
        "color_key": "databases",
        "current_title": "Top Current Databases",
        "future_title": "Top Future Databases",
    },
    "Platforms": {
        "current_column": "PlatformHaveWorkedWith",
        "future_column": "PlatformWantToWorkWith",
        "label": "platform",
        "color_key": "platforms",
        "current_title": "Top Current Platforms",
        "future_title": "Top Future Platforms",
    },
    "Frameworks": {
        "current_column": "WebframeHaveWorkedWith",
        "future_column": "WebframeWantToWorkWith",
        "label": "web_framework",
        "color_key": "frameworks",
        "current_title": "Top Current Web Frameworks",
        "future_title": "Top Future Web Frameworks",
    },
}


age_filter = pn.widgets.MultiSelect(
    name="Age groups",
    options=AGE_ORDER,
    value=AGE_ORDER,
    size=8,
)
age_filter_enabled = pn.widgets.Checkbox(name="Activate Age filter", value=True)
remote_filter = pn.widgets.CheckBoxGroup(
    name="Workstyle",
    options=REMOTE_OPTIONS,
    value=REMOTE_OPTIONS,
)
remote_filter_enabled = pn.widgets.Checkbox(name="Activate Workstyle filter", value=True)
country_scope = pn.widgets.Select(
    name="Country scope",
    options=["All countries", "Top N countries"],
    value="All countries",
)
country_filter_enabled = pn.widgets.Checkbox(name="Activate Countries filter", value=True)
metric_selector = pn.widgets.RadioButtonGroup(
    name="Metric",
    options=["Respondent count", "Share of respondents"],
    value="Respondent count",
    button_type="primary",
)
metric_filter_enabled = pn.widgets.Checkbox(name="Activate Metrics filter", value=True)
top_n_selector = pn.widgets.RadioButtonGroup(
    name="Top N",
    options=[5, 10, 12],
    value=10,
    button_type="primary",
)
top_n_filter_enabled = pn.widgets.Checkbox(name="Activate Top N filter", value=True)
reset_button = pn.widgets.Button(name="Reset filters", button_type="primary")


def reset_filters(event) -> None:
    top_n_filter_enabled.value = True
    age_filter_enabled.value = True
    remote_filter_enabled.value = True
    country_filter_enabled.value = True
    metric_filter_enabled.value = True
    age_filter.value = list(AGE_ORDER)
    remote_filter.value = list(REMOTE_OPTIONS)
    country_scope.value = "All countries"
    metric_selector.value = "Respondent count"
    top_n_selector.value = 10


reset_button.on_click(reset_filters)


def _sync_filter_control_states(event=None) -> None:
    top_n_selector.disabled = not top_n_filter_enabled.value
    age_filter.disabled = not age_filter_enabled.value
    remote_filter.disabled = not remote_filter_enabled.value
    country_scope.disabled = not country_filter_enabled.value
    metric_selector.disabled = not metric_filter_enabled.value


for toggle in [
    top_n_filter_enabled,
    age_filter_enabled,
    remote_filter_enabled,
    country_filter_enabled,
    metric_filter_enabled,
]:
    toggle.param.watch(_sync_filter_control_states, "value")

_sync_filter_control_states()


def _effective_top_n(selected_top_n, use_top_n):
    return int(selected_top_n) if use_top_n else 10


def _effective_ages(selected_ages, use_age):
    return list(selected_ages) if use_age else list(AGE_ORDER)


def _effective_remote(selected_remote, use_remote):
    return list(selected_remote) if use_remote else list(REMOTE_OPTIONS)


def _effective_country_scope(selected_country_scope, use_country):
    return selected_country_scope if use_country else "All countries"


def _effective_metric(selected_metric, use_metric):
    return selected_metric if use_metric else "Respondent count"


def _filtered_df(
    selected_ages,
    selected_remote,
    selected_country_scope,
    selected_top_n,
    use_age,
    use_remote,
    use_country,
    use_top_n,
):
    effective_top_n = _effective_top_n(selected_top_n, use_top_n)
    filtered = filter_dataset(
        BASE_DF,
        _effective_ages(selected_ages, use_age),
        _effective_remote(selected_remote, use_remote),
        _effective_country_scope(selected_country_scope, use_country),
        country_top_n=effective_top_n,
    )
    return filtered if not filtered.empty else BASE_DF.copy()


def _kpi_card(title: str, value: str, subtitle: str) -> pn.pane.HTML:
    html = f"""
    <div style="background:#f5f7fb;border:1px solid #d9e2ec;border-radius:8px;padding:16px 18px;height:126px;">
      <div style="font-size:13px;color:#486581;text-transform:uppercase;letter-spacing:0.06em;">{title}</div>
      <div style="font-size:30px;font-weight:700;color:#102a43;margin:8px 0 6px 0;">{value}</div>
      <div style="font-size:14px;color:#627d98;line-height:1.4;">{subtitle}</div>
    </div>
    """
    return pn.pane.HTML(html, sizing_mode="stretch_width")


def _grid_box(*items, ncols: int) -> pn.GridBox:
    return pn.GridBox(*items, ncols=ncols, sizing_mode="stretch_width")


def _technology_momentum_view(filtered, selected_metric, top_n, selected_family):
    value_col = metric_column(selected_metric)
    config = MOMENTUM_OPTIONS[selected_family]
    current_ranking = top_multiselect_counts(filtered, config["current_column"], top_n, config["label"])
    future_ranking = top_multiselect_counts(filtered, config["future_column"], top_n, config["label"])
    comparison = build_comparison_table(
        filtered,
        config["current_column"],
        config["future_column"],
        config["label"],
        top_n,
    )
    color = TECH_COLORS[config["color_key"]]

    rankings_grid = _grid_box(
        make_horizontal_bar_chart(
            current_ranking,
            config["label"],
            value_col,
            config["current_title"],
            selected_metric,
            color,
        ),
        make_horizontal_bar_chart(
            future_ranking,
            config["label"],
            value_col,
            config["future_title"],
            selected_metric,
            color,
        ),
        ncols=2,
    )

    return pn.Column(
        rankings_grid,
        make_dumbbell_chart(
            comparison,
            config["label"],
            "share_pct_current" if selected_metric == "Share of respondents" else "count_current",
            "share_pct_future" if selected_metric == "Share of respondents" else "count_future",
            f"Current vs Future {selected_family} Momentum",
            selected_metric,
        ),
        sizing_mode="stretch_width",
    )


def _filtered_df_from_filter_values(
    use_top_n,
    use_age,
    use_remote,
    use_country,
    selected_ages,
    selected_remote,
    selected_country_scope,
    top_n,
):
    return _filtered_df(
        selected_ages,
        selected_remote,
        selected_country_scope,
        top_n,
        use_age,
        use_remote,
        use_country,
        use_top_n,
    )


@pn.depends(
    top_n_filter_enabled.param.value,
    age_filter_enabled.param.value,
    remote_filter_enabled.param.value,
    country_filter_enabled.param.value,
    age_filter.param.value,
    remote_filter.param.value,
    country_scope.param.value,
    top_n_selector.param.value,
)
def momentum_kpis(
    use_top_n,
    use_age,
    use_remote,
    use_country,
    selected_ages,
    selected_remote,
    selected_country_scope,
    top_n,
):
    filtered = _filtered_df_from_filter_values(
        use_top_n,
        use_age,
        use_remote,
        use_country,
        selected_ages,
        selected_remote,
        selected_country_scope,
        top_n,
    )
    kpis = build_kpis(filtered)
    return _grid_box(
        _kpi_card("Respondents", f"{kpis['respondents']:,}", "Rows in the current filtered view"),
        _kpi_card("Countries", f"{kpis['countries']:,}", "Distinct countries represented, excluding Nomadic"),
        _kpi_card("Median compensation", f"${kpis['median_salary']:,.0f}", "Converted annual compensation"),
        ncols=3,
    )


def _technology_momentum_panel(selected_family):
    @pn.depends(
        top_n_filter_enabled.param.value,
        age_filter_enabled.param.value,
        remote_filter_enabled.param.value,
        country_filter_enabled.param.value,
        metric_filter_enabled.param.value,
        age_filter.param.value,
        remote_filter.param.value,
        country_scope.param.value,
        metric_selector.param.value,
        top_n_selector.param.value,
    )
    def technology_view(
        use_top_n,
        use_age,
        use_remote,
        use_country,
        use_metric,
        selected_ages,
        selected_remote,
        selected_country_scope,
        selected_metric,
        top_n,
    ):
        effective_top_n = _effective_top_n(top_n, use_top_n)
        effective_metric = _effective_metric(selected_metric, use_metric)
        filtered = _filtered_df_from_filter_values(
            use_top_n,
            use_age,
            use_remote,
            use_country,
            selected_ages,
            selected_remote,
            selected_country_scope,
            top_n,
        )
        return _technology_momentum_view(filtered, effective_metric, effective_top_n, selected_family)

    return pn.panel(technology_view, sizing_mode="stretch_width")


def momentum_comparison():
    heading = pn.pane.Markdown(
            """
            ### Momentum and Comparison

            This tab separates the technology comparison into four subtabs. Each subtab shows the
            `current ranking`, the `future ranking`, and the direct `current vs future` dumbbell chart
            for one technology family. The left filter panel controls respondent slice, metric, and ranking depth.
            """
    )
    technology_tabs = pn.Tabs(
        *[
            (family, _technology_momentum_panel(family))
            for family in MOMENTUM_OPTIONS
        ],
        sizing_mode="stretch_width",
        dynamic=True,
    )
    return pn.Column(
        heading,
        pn.panel(momentum_kpis),
        technology_tabs,
        sizing_mode="stretch_width",
    )


@pn.depends(
    top_n_filter_enabled.param.value,
    age_filter_enabled.param.value,
    remote_filter_enabled.param.value,
    country_filter_enabled.param.value,
    metric_filter_enabled.param.value,
    age_filter.param.value,
    remote_filter.param.value,
    country_scope.param.value,
    metric_selector.param.value,
    top_n_selector.param.value,
)
def demographics_context(
    use_top_n,
    use_age,
    use_remote,
    use_country,
    use_metric,
    selected_ages,
    selected_remote,
    selected_country_scope,
    selected_metric,
    top_n,
):
    effective_top_n = _effective_top_n(top_n, use_top_n)
    effective_metric = _effective_metric(selected_metric, use_metric)
    filtered = _filtered_df(
        selected_ages,
        selected_remote,
        selected_country_scope,
        top_n,
        use_age,
        use_remote,
        use_country,
        use_top_n,
    )
    countries_map = country_map_distribution(filtered, top_n=effective_top_n)
    age_education = age_education_distribution(filtered)
    salary_box = salary_remote_experience_box_summary(filtered)

    heading = pn.pane.Markdown(
            """
            ### Demographics and Context

            These views focus on respondent context through geography, age-by-education composition,
            and compensation distribution by work style and experience band.
            """
    )
    top_grid = _grid_box(
        make_country_bubble_map(countries_map, "Respondent Map by Country", effective_metric),
        make_grouped_box_plot(salary_box, "Compensation Distribution by Work Style and Experience"),
        ncols=2,
    )
    return pn.Column(
        heading,
        top_grid,
        make_stacked_bar_chart(age_education, "Education Level Composition by Age Group"),
        sizing_mode="stretch_width",
    )


@pn.depends(
    top_n_filter_enabled.param.value,
    age_filter_enabled.param.value,
    remote_filter_enabled.param.value,
    country_filter_enabled.param.value,
    metric_filter_enabled.param.value,
    age_filter.param.value,
    remote_filter.param.value,
    country_scope.param.value,
    metric_selector.param.value,
    top_n_selector.param.value,
)
def detailed_age_education(
    use_top_n,
    use_age,
    use_remote,
    use_country,
    use_metric,
    selected_ages,
    selected_remote,
    selected_country_scope,
    selected_metric,
    top_n,
):
    effective_metric = _effective_metric(selected_metric, use_metric)
    filtered = _filtered_df(
        selected_ages,
        selected_remote,
        selected_country_scope,
        top_n,
        use_age,
        use_remote,
        use_country,
        use_top_n,
    )
    age_profile = age_distribution(filtered)
    age_education = age_education_distribution(filtered)

    return pn.Column(
        pn.pane.Markdown(
            """
            ### Age Profile and Education Composition

            This view separates the respondent age distribution from the education mix within each age group.
            """
        ),
        _grid_box(
            make_age_percent_bar_chart(age_profile, "Respondent Age Distribution", effective_metric),
            make_percent_stacked_bar_chart(age_education, "Education Level Composition by Age Group"),
            ncols=2,
        ),
        sizing_mode="stretch_width",
    )


@pn.depends(
    top_n_filter_enabled.param.value,
    age_filter_enabled.param.value,
    remote_filter_enabled.param.value,
    country_filter_enabled.param.value,
    age_filter.param.value,
    remote_filter.param.value,
    country_scope.param.value,
    top_n_selector.param.value,
)
def detailed_compensation_experience(
    use_top_n,
    use_age,
    use_remote,
    use_country,
    selected_ages,
    selected_remote,
    selected_country_scope,
    top_n,
):
    filtered = _filtered_df(
        selected_ages,
        selected_remote,
        selected_country_scope,
        top_n,
        use_age,
        use_remote,
        use_country,
        use_top_n,
    )
    salary_box = salary_remote_experience_box_summary(filtered)
    y_max = float(salary_box["upper"].max() * 1.1) if not salary_box.empty else 1.0
    remote_labels = [REMOTE_WORK_LABELS[option] for option in REMOTE_OPTIONS if option in REMOTE_WORK_LABELS]

    charts = []
    for remote_label in remote_labels:
        chart_data = salary_box[salary_box["remote_label"] == remote_label]
        if chart_data.empty:
            continue

        charts.append(
            make_compensation_experience_box_plot(
                chart_data,
                f"{remote_label} Compensation by Experience",
                y_max,
                REMOTE_COLORS.get(remote_label, "#2f6690"),
            )
        )

    return pn.Column(
        pn.pane.Markdown(
            """
            ### Compensation Distribution by Experience and Work Style

            Each chart uses the same dimensions and y-axis scale so the compensation distributions can be compared
            across `Remote`, `Hybrid`, and `In-person` work styles.
            """
        ),
        _grid_box(*charts, ncols=3),
        sizing_mode="stretch_width",
    )


@pn.depends(
    top_n_filter_enabled.param.value,
    age_filter_enabled.param.value,
    remote_filter_enabled.param.value,
    country_filter_enabled.param.value,
    metric_filter_enabled.param.value,
    age_filter.param.value,
    remote_filter.param.value,
    country_scope.param.value,
    metric_selector.param.value,
    top_n_selector.param.value,
)
def detailed_country_distribution(
    use_top_n,
    use_age,
    use_remote,
    use_country,
    use_metric,
    selected_ages,
    selected_remote,
    selected_country_scope,
    selected_metric,
    top_n,
):
    effective_metric = _effective_metric(selected_metric, use_metric)
    filtered = _filtered_df(
        selected_ages,
        selected_remote,
        selected_country_scope,
        top_n,
        use_age,
        use_remote,
        use_country,
        use_top_n,
    )
    map_data = country_map_distribution(filtered, top_n=None)
    geographic_countries = set(filtered.loc[filtered["Country"] != "Nomadic", "Country"].dropna().unique())
    total_country_values = len(geographic_countries)
    mapped_countries = map_data["country"].nunique()
    unmapped_countries = sorted(geographic_countries - set(map_data["country"].unique()))
    unmapped_note = ", ".join(unmapped_countries) if unmapped_countries else "None"

    return pn.Column(
        pn.pane.Markdown(
            f"""
            ### Full Country Distribution Map

            This view shows the mappable countries in the current filtered dataset.
            Countries shown: `{mapped_countries}` of `{total_country_values}` countries.
            Unmapped countries: `{unmapped_note}`. The non-geographic value `Nomadic` is excluded from the
            country count.
            """
        ),
        make_country_bubble_map(
            map_data,
            "Respondent Distribution Across All Countries",
            effective_metric,
            height=640,
        ),
        sizing_mode="stretch_width",
    )


def detailed_views() -> pn.Column:
    subtab_template = """
    ### {title}

    Reserved space for the next dashboard iteration.
    """
    subtabs = pn.Tabs(
        ("Age and Education", pn.panel(detailed_age_education)),
        ("Compensation by Experience", pn.panel(detailed_compensation_experience)),
        ("Country Distribution", pn.panel(detailed_country_distribution)),
        sizing_mode="stretch_width",
        dynamic=True,
    )
    return pn.Column(
        pn.pane.Markdown(
            """
            ### Respondent Context

            These subtabs separate respondent context into age and education, compensation by experience,
            and geographic distribution.
            """
        ),
        subtabs,
        sizing_mode="stretch_width",
    )


def create_dashboard():
    filter_accordion = pn.Accordion(
        (
            "Top N",
            pn.Column(
                top_n_filter_enabled,
                pn.pane.Markdown("Choose the ranking depth used by technology rankings and Top N country filtering."),
                top_n_selector,
                sizing_mode="stretch_width",
            ),
        ),
        (
            "Age",
            pn.Column(
                age_filter_enabled,
                pn.pane.Markdown("Limit the dashboard to selected age groups."),
                age_filter,
                sizing_mode="stretch_width",
            ),
        ),
        (
            "Workstyle",
            pn.Column(
                remote_filter_enabled,
                pn.pane.Markdown("Include one or more workstyle categories."),
                remote_filter,
                sizing_mode="stretch_width",
            ),
        ),
        (
            "Countries",
            pn.Column(
                country_filter_enabled,
                pn.pane.Markdown("Use all countries or restrict the dashboard to the selected Top N countries."),
                country_scope,
                sizing_mode="stretch_width",
            ),
        ),
        (
            "Metrics",
            pn.Column(
                metric_filter_enabled,
                pn.pane.Markdown("Switch charts between respondent counts and share of respondents where applicable."),
                metric_selector,
                sizing_mode="stretch_width",
            ),
        ),
        active=[0, 1, 2, 3, 4],
        sizing_mode="stretch_width",
    )
    sidebar = pn.Card(
        pn.pane.Markdown(
            """
            Use the checkbox inside each category to activate or deactivate that filter group.
            Inactive groups fall back to the broad default.
            """
        ),
        filter_accordion,
        reset_button,
        title="Filters",
        collapsible=True,
        collapsed=False,
        width=280,
        sizing_mode="fixed",
    )

    tabs = pn.Tabs(
        ("Momentum and Comparison", momentum_comparison()),
        ("Respondent Context", detailed_views()),
        sizing_mode="stretch_width",
        dynamic=True,
    )

    header = pn.pane.HTML(
        """
        <div style="background:#102a43;color:#ffffff;padding:18px 22px;border-radius:10px;">
          <div style="font-size:28px;font-weight:700;margin-bottom:6px;">Developer Technology Trends Dashboard</div>
          <div style="font-size:15px;line-height:1.5;max-width:980px;">
            Interactive dashboard built with Panel and Bokeh from the cleaned and reduced Stack Overflow survey dataset.
            It keeps the original project narrative while making comparison and exploration easier than the static PDF.
          </div>
        </div>
        """,
        sizing_mode="stretch_width",
    )

    body = pn.Row(
        sidebar,
        tabs,
        sizing_mode="stretch_width",
    )

    return pn.Column(
        header,
        body,
        sizing_mode="stretch_width",
        min_width=1200,
    )


dashboard = create_dashboard()
dashboard.servable(title="Stack Overflow Developer Survey Dashboard v1")
