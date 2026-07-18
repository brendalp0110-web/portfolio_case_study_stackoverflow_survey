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
    make_dumbbell_chart,
    make_grouped_box_plot,
    make_horizontal_bar_chart,
    make_stacked_bar_chart,
)
from dashboard_panel_bokeh.data_utils import (  # noqa: E402
    AGE_ORDER,
    age_education_distribution,
    build_comparison_table,
    build_kpis,
    country_map_distribution,
    filter_dataset,
    load_dataset,
    metric_column,
    salary_remote_experience_box_summary,
    top_multiselect_counts,
)


pn.extension(sizing_mode="stretch_width")

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
remote_filter = pn.widgets.CheckBoxGroup(
    name="Remote work",
    options=REMOTE_OPTIONS,
    value=REMOTE_OPTIONS,
)
country_scope = pn.widgets.Select(
    name="Country scope",
    options=["All respondents", "Top 10 countries only"],
    value="All respondents",
)
metric_selector = pn.widgets.Select(
    name="Metric",
    options=["Respondent count", "Share of respondents"],
    value="Respondent count",
)
top_n_selector = pn.widgets.IntSlider(name="Top N", start=5, end=12, step=1, value=10)
momentum_family_selector = pn.widgets.RadioButtonGroup(
    name="Comparison family",
    options=list(MOMENTUM_OPTIONS.keys()),
    value="Languages",
    button_type="primary",
)
reset_button = pn.widgets.Button(name="Reset filters", button_type="primary")


def reset_filters(event) -> None:
    age_filter.value = list(AGE_ORDER)
    remote_filter.value = list(REMOTE_OPTIONS)
    country_scope.value = "All respondents"
    metric_selector.value = "Respondent count"
    top_n_selector.value = 10
    momentum_family_selector.value = "Languages"


reset_button.on_click(reset_filters)


def _filtered_df(selected_ages, selected_remote, selected_country_scope):
    filtered = filter_dataset(BASE_DF, selected_ages, selected_remote, selected_country_scope)
    return filtered if not filtered.empty else BASE_DF.copy()


def _kpi_card(title: str, value: str, subtitle: str) -> pn.pane.HTML:
    html = f"""
    <div style="background:#f5f7fb;border:1px solid #d9e2ec;border-radius:10px;padding:16px 18px;height:118px;">
      <div style="font-size:12px;color:#486581;text-transform:uppercase;letter-spacing:0.06em;">{title}</div>
      <div style="font-size:28px;font-weight:700;color:#102a43;margin:8px 0 6px 0;">{value}</div>
      <div style="font-size:13px;color:#627d98;">{subtitle}</div>
    </div>
    """
    return pn.pane.HTML(html, sizing_mode="stretch_width")


@pn.depends(
    age_filter.param.value,
    remote_filter.param.value,
    country_scope.param.value,
    metric_selector.param.value,
    top_n_selector.param.value,
    momentum_family_selector.param.value,
)
def momentum_comparison(selected_ages, selected_remote, selected_country_scope, selected_metric, top_n, selected_family):
    filtered = _filtered_df(selected_ages, selected_remote, selected_country_scope)
    kpis = build_kpis(filtered)
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

    kpi_row = pn.Row(
        _kpi_card("Respondents", f"{kpis['respondents']:,}", "Rows in the current filtered view"),
        _kpi_card("Countries", f"{kpis['countries']:,}", "Distinct countries represented"),
        _kpi_card("Median compensation", f"${kpis['median_salary']:,.0f}", "Converted annual compensation"),
    )

    return pn.Column(
        pn.pane.Markdown(
            """
            ### Momentum and Comparison

            This tab concentrates the full technology comparison in one place. A single selector controls the
            `current ranking`, the `future ranking`, and the direct `current vs future` dumbbell chart.
            """
        ),
        kpi_row,
        pn.Row(
            pn.Spacer(width=10),
            pn.Column(
                pn.pane.Markdown("#### Comparison technology family"),
                momentum_family_selector,
                sizing_mode="stretch_width",
            ),
            sizing_mode="stretch_width",
        ),
        pn.Row(
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
        ),
        make_dumbbell_chart(
            comparison,
            config["label"],
            "share_pct_current" if selected_metric == "Share of respondents" else "count_current",
            "share_pct_future" if selected_metric == "Share of respondents" else "count_future",
            f"Current vs Future {selected_family} Momentum",
            selected_metric,
        ),
    )


@pn.depends(
    age_filter.param.value,
    remote_filter.param.value,
    country_scope.param.value,
    metric_selector.param.value,
    top_n_selector.param.value,
)
def demographics_context(selected_ages, selected_remote, selected_country_scope, selected_metric, top_n):
    filtered = _filtered_df(selected_ages, selected_remote, selected_country_scope)
    countries_map = country_map_distribution(filtered, top_n=min(top_n, 12))
    age_education = age_education_distribution(filtered)
    salary_box = salary_remote_experience_box_summary(filtered)

    return pn.Column(
        pn.pane.Markdown(
            """
            ### Demographics and Context

            These views focus on respondent context through geography, age-by-education composition,
            and compensation distribution by work style and experience band.
            """
        ),
        pn.Row(
            make_country_bubble_map(countries_map, "Respondent Map by Country", selected_metric),
            make_grouped_box_plot(salary_box, "Compensation Distribution by Work Style and Experience"),
        ),
        pn.Row(
            make_stacked_bar_chart(age_education, "Age by Education"),
        ),
    )


def create_dashboard():
    sidebar = pn.Column(
        "## Controls",
        pn.pane.Markdown(
            """
            Adjust the respondent slice, switch between count and share, and tune ranking depth.
            The default state is designed to be readable without interaction.
            """
        ),
        age_filter,
        remote_filter,
        country_scope,
        metric_selector,
        top_n_selector,
        reset_button,
        width=280,
        sizing_mode="fixed",
    )

    tabs = pn.Tabs(
        ("Momentum and Comparison", pn.panel(momentum_comparison)),
        ("Demographics and Context", pn.panel(demographics_context)),
        sizing_mode="stretch_width",
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
