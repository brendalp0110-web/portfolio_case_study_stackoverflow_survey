from __future__ import annotations

from functools import lru_cache
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
        .filter-sidebar {
          background: #ffffff;
          border: 1px solid #d9e2ec;
          border-radius: 10px;
          padding: 12px;
        }
        .filter-rail {
          background: #ffffff;
          border: 1px solid #d9e2ec;
          border-radius: 10px;
          padding: 10px 8px;
        }
        .filter-rail-label {
          writing-mode: vertical-rl;
          transform: rotate(180deg);
          color: #486581;
          font-size: 13px;
          font-weight: 700;
          letter-spacing: 0.08em;
          text-transform: uppercase;
          margin-top: 8px;
        }
        """
    ],
)

DATASET_PATH = PROJECT_ROOT / "data" / "survey_data_cleaned_reduced.csv"
BASE_DF = load_dataset(DATASET_PATH)
TOTAL_KPIS = build_kpis(BASE_DF)
REMOTE_OPTIONS = BASE_DF["RemoteWork"].value_counts().index.tolist()
METRIC_MODE = "Respondent count"
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


age_check_all = pn.widgets.Checkbox(name="Check All", value=True)
age_filter = pn.widgets.CheckBoxGroup(
    name="Age groups",
    options=AGE_ORDER,
    value=AGE_ORDER,
)
age_reset_button = pn.widgets.Button(name="Reset", width=58)
remote_check_all = pn.widgets.Checkbox(name="Check All", value=True)
remote_filter = pn.widgets.CheckBoxGroup(
    name="Workstyle",
    options=REMOTE_OPTIONS,
    value=REMOTE_OPTIONS,
)
remote_reset_button = pn.widgets.Button(name="Reset", width=58)
country_show_all = pn.widgets.Checkbox(name="Show all countries", value=False)
country_apply_dashboard = pn.widgets.Checkbox(name="Apply country scope to full dashboard", value=False)
country_reset_button = pn.widgets.Button(name="Reset", width=58)
TOP_N_DEFAULT = 10
top_n_value = pn.widgets.IntInput(name="Top N value", value=TOP_N_DEFAULT)
top_n_5_checkbox = pn.widgets.Checkbox(name="Top 5", value=False)
top_n_10_checkbox = pn.widgets.Checkbox(name="Top 10", value=True)
top_n_12_checkbox = pn.widgets.Checkbox(name="Top 12", value=False)
top_n_reset_button = pn.widgets.Button(name="Reset", width=58)
reset_button = pn.widgets.Button(name="Reset filters", button_type="primary", width=104)
filter_panel_open = pn.widgets.Toggle(value=True, visible=False)
filter_panel_collapse_button = pn.widgets.ButtonIcon(
    icon="chevrons-left",
    description="Collapse filters",
    width=34,
    height=34,
)
filter_panel_expand_button = pn.widgets.ButtonIcon(
    icon="filter",
    description="Open filters",
    width=38,
    height=38,
)


_syncing_top_n = False
_syncing_age = False
_syncing_remote = False
_last_valid_ages = list(AGE_ORDER)
_last_valid_remote = list(REMOTE_OPTIONS)
_TOP_N_CHECKBOXES = {
    5: top_n_5_checkbox,
    10: top_n_10_checkbox,
    12: top_n_12_checkbox,
}


def _set_top_n_value(value: int) -> None:
    global _syncing_top_n
    _syncing_top_n = True
    top_n_value.value = int(value)
    for option, checkbox in _TOP_N_CHECKBOXES.items():
        checkbox.value = option == int(value)
    _syncing_top_n = False


def _top_n_checkbox_changed(event) -> None:
    if _syncing_top_n:
        return

    if event.new:
        for option, checkbox in _TOP_N_CHECKBOXES.items():
            if checkbox is event.obj:
                _set_top_n_value(option)
                return

    if not any(checkbox.value for checkbox in _TOP_N_CHECKBOXES.values()):
        _set_top_n_value(top_n_value.value)


for checkbox in _TOP_N_CHECKBOXES.values():
    checkbox.param.watch(_top_n_checkbox_changed, "value")


def reset_top_n(event=None) -> None:
    _set_top_n_value(TOP_N_DEFAULT)


top_n_reset_button.on_click(reset_top_n)


def _set_age_values(values) -> None:
    global _syncing_age, _last_valid_ages
    selected = [age for age in AGE_ORDER if age in list(values)]
    if not selected:
        selected = list(_last_valid_ages)

    _syncing_age = True
    age_filter.value = selected
    age_check_all.value = selected == list(AGE_ORDER)
    _syncing_age = False
    _last_valid_ages = list(selected)


def _age_filter_changed(event) -> None:
    if _syncing_age:
        return
    _set_age_values(event.new)


def _age_check_all_changed(event) -> None:
    if _syncing_age:
        return
    if event.new:
        _set_age_values(AGE_ORDER)
    else:
        _set_age_values(age_filter.value)


age_filter.param.watch(_age_filter_changed, "value")
age_check_all.param.watch(_age_check_all_changed, "value")


def reset_age(event=None) -> None:
    _set_age_values(AGE_ORDER)


age_reset_button.on_click(reset_age)


def _set_remote_values(values) -> None:
    global _syncing_remote, _last_valid_remote
    selected = [style for style in REMOTE_OPTIONS if style in list(values)]
    if not selected:
        selected = list(_last_valid_remote)

    _syncing_remote = True
    remote_filter.value = selected
    remote_check_all.value = selected == list(REMOTE_OPTIONS)
    _syncing_remote = False
    _last_valid_remote = list(selected)


def _remote_filter_changed(event) -> None:
    if _syncing_remote:
        return
    _set_remote_values(event.new)


def _remote_check_all_changed(event) -> None:
    if _syncing_remote:
        return
    if event.new:
        _set_remote_values(REMOTE_OPTIONS)
    else:
        _set_remote_values(remote_filter.value)


remote_filter.param.watch(_remote_filter_changed, "value")
remote_check_all.param.watch(_remote_check_all_changed, "value")


def reset_remote(event=None) -> None:
    _set_remote_values(REMOTE_OPTIONS)


remote_reset_button.on_click(reset_remote)


def reset_country(event=None) -> None:
    country_show_all.value = False
    country_apply_dashboard.value = False


country_reset_button.on_click(reset_country)


def reset_filters(event) -> None:
    reset_age()
    reset_remote()
    reset_country()
    reset_top_n()


reset_button.on_click(reset_filters)


def _collapse_filter_panel(event=None) -> None:
    filter_panel_open.value = False


def _expand_filter_panel(event=None) -> None:
    filter_panel_open.value = True


filter_panel_collapse_button.on_click(_collapse_filter_panel)
filter_panel_expand_button.on_click(_expand_filter_panel)


def _effective_top_n(selected_top_n):
    return int(selected_top_n)


def _effective_ages(selected_ages):
    return list(selected_ages) or list(AGE_ORDER)


def _effective_remote(selected_remote):
    return list(selected_remote) or list(REMOTE_OPTIONS)


def _country_scope_from_options(show_all_countries: bool, apply_to_dashboard: bool) -> str:
    if apply_to_dashboard and not show_all_countries:
        return "Top N countries"
    return "All countries"


def _map_country_scope(show_all_countries: bool) -> str:
    return "All countries" if show_all_countries else "Top N countries"


def _filter_key(
    selected_ages,
    selected_remote,
    selected_country_scope,
    selected_top_n,
):
    effective_top_n = _effective_top_n(selected_top_n)
    return (
        tuple(_effective_ages(selected_ages)),
        tuple(_effective_remote(selected_remote)),
        selected_country_scope,
        effective_top_n,
    )


@lru_cache(maxsize=128)
def _cached_filtered_df(age_values, remote_values, country_scope_value, country_top_n):
    filtered = filter_dataset(
        BASE_DF,
        age_values,
        remote_values,
        country_scope_value,
        country_top_n=country_top_n,
    )
    return filtered if not filtered.empty else BASE_DF.copy()


def _filtered_df(
    selected_ages,
    selected_remote,
    selected_country_scope,
    selected_top_n,
):
    key = _filter_key(
        selected_ages,
        selected_remote,
        selected_country_scope,
        selected_top_n,
    )
    filtered = _cached_filtered_df(*key)
    return filtered


@lru_cache(maxsize=128)
def _cached_kpis(filter_key):
    return build_kpis(_cached_filtered_df(*filter_key))


@lru_cache(maxsize=256)
def _cached_top_multiselect_counts(filter_key, column, top_n, label):
    return top_multiselect_counts(_cached_filtered_df(*filter_key), column, top_n, label)


@lru_cache(maxsize=256)
def _cached_comparison_table(filter_key, current_column, future_column, label, top_n):
    return build_comparison_table(_cached_filtered_df(*filter_key), current_column, future_column, label, top_n)


@lru_cache(maxsize=128)
def _cached_country_map_distribution(filter_key, top_n):
    return country_map_distribution(_cached_filtered_df(*filter_key), top_n=top_n)


@lru_cache(maxsize=128)
def _cached_age_distribution(filter_key):
    return age_distribution(_cached_filtered_df(*filter_key))


@lru_cache(maxsize=128)
def _cached_age_education_distribution(filter_key):
    return age_education_distribution(_cached_filtered_df(*filter_key))


@lru_cache(maxsize=128)
def _cached_salary_remote_experience_box_summary(filter_key):
    return salary_remote_experience_box_summary(_cached_filtered_df(*filter_key))


def _kpi_card(title: str, value: str, subtitle: str, secondary: str | None = None) -> pn.pane.HTML:
    secondary_html = ""
    if secondary:
        secondary_html = f'<div style="font-size:13px;color:#829ab1;line-height:1.35;margin-top:4px;">{secondary}</div>'

    html = f"""
    <div style="background:#f5f7fb;border:1px solid #d9e2ec;border-radius:8px;padding:16px 18px;height:126px;">
      <div style="font-size:13px;color:#486581;text-transform:uppercase;letter-spacing:0.06em;">{title}</div>
      <div style="font-size:30px;font-weight:700;color:#102a43;margin:8px 0 6px 0;">{value}</div>
      <div style="font-size:14px;color:#627d98;line-height:1.4;">{subtitle}</div>
      {secondary_html}
    </div>
    """
    return pn.pane.HTML(html, sizing_mode="stretch_width")


def _grid_box(*items, ncols: int) -> pn.GridBox:
    return pn.GridBox(*items, ncols=ncols, sizing_mode="stretch_width")


def _technology_momentum_view(filter_key, top_n, selected_family):
    value_col = "count"
    config = MOMENTUM_OPTIONS[selected_family]
    current_ranking = _cached_top_multiselect_counts(filter_key, config["current_column"], top_n, config["label"])
    future_ranking = _cached_top_multiselect_counts(filter_key, config["future_column"], top_n, config["label"])
    comparison = _cached_comparison_table(
        filter_key,
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
            METRIC_MODE,
            color,
        ),
        make_horizontal_bar_chart(
            future_ranking,
            config["label"],
            value_col,
            config["future_title"],
            METRIC_MODE,
            color,
        ),
        ncols=2,
    )

    return pn.Column(
        rankings_grid,
        make_dumbbell_chart(
            comparison,
            config["label"],
            "count_current",
            "count_future",
            f"Current vs Future {selected_family} Momentum",
            METRIC_MODE,
        ),
        sizing_mode="stretch_width",
    )


def _filter_key_from_filter_values(
    selected_ages,
    selected_remote,
    show_all_countries,
    apply_country_scope,
    top_n,
):
    return _filter_key(
        selected_ages,
        selected_remote,
        _country_scope_from_options(show_all_countries, apply_country_scope),
        top_n,
    )


def _map_filter_key_from_filter_values(
    selected_ages,
    selected_remote,
    show_all_countries,
    top_n,
):
    return _filter_key(
        selected_ages,
        selected_remote,
        _map_country_scope(show_all_countries),
        top_n,
    )


@pn.depends(
    country_show_all.param.value,
    country_apply_dashboard.param.value,
    age_filter.param.value,
    remote_filter.param.value,
    top_n_value.param.value,
)
def momentum_kpis(
    show_all_countries,
    apply_country_scope,
    selected_ages,
    selected_remote,
    top_n,
):
    filter_key = _filter_key_from_filter_values(
        selected_ages,
        selected_remote,
        show_all_countries,
        apply_country_scope,
        top_n,
    )
    kpis = _cached_kpis(filter_key)
    return _grid_box(
        _kpi_card(
            "Respondents",
            f"{TOTAL_KPIS['respondents']:,}",
            "Total rows in the dataset",
            f"Filtered view: {kpis['respondents']:,} respondents",
        ),
        _kpi_card(
            "Countries",
            f"{TOTAL_KPIS['countries']:,}",
            "Total countries, excluding Nomadic",
            f"Filtered view: {kpis['countries']:,} countries",
        ),
        _kpi_card("Median compensation", f"${kpis['median_salary']:,.0f}", "Converted annual compensation"),
        ncols=3,
    )


def _technology_momentum_panel(selected_family):
    @pn.depends(
        country_show_all.param.value,
        country_apply_dashboard.param.value,
        age_filter.param.value,
        remote_filter.param.value,
        top_n_value.param.value,
    )
    def technology_view(
        show_all_countries,
        apply_country_scope,
        selected_ages,
        selected_remote,
        top_n,
    ):
        effective_top_n = _effective_top_n(top_n)
        filter_key = _filter_key_from_filter_values(
            selected_ages,
            selected_remote,
            show_all_countries,
            apply_country_scope,
            top_n,
        )
        return _technology_momentum_view(filter_key, effective_top_n, selected_family)

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
    country_show_all.param.value,
    country_apply_dashboard.param.value,
    age_filter.param.value,
    remote_filter.param.value,
    top_n_value.param.value,
)
def demographics_context(
    show_all_countries,
    apply_country_scope,
    selected_ages,
    selected_remote,
    top_n,
):
    effective_top_n = _effective_top_n(top_n)
    filter_key = _filter_key_from_filter_values(
        selected_ages,
        selected_remote,
        show_all_countries,
        apply_country_scope,
        top_n,
    )
    countries_map = _cached_country_map_distribution(filter_key, effective_top_n)
    age_education = _cached_age_education_distribution(filter_key)
    salary_box = _cached_salary_remote_experience_box_summary(filter_key)

    heading = pn.pane.Markdown(
            """
            ### Demographics and Context

            These views focus on respondent context through geography, age-by-education composition,
            and compensation distribution by work style and experience band.
            """
    )
    top_grid = _grid_box(
        make_country_bubble_map(countries_map, "Respondent Map by Country", METRIC_MODE),
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
    country_show_all.param.value,
    country_apply_dashboard.param.value,
    age_filter.param.value,
    remote_filter.param.value,
    top_n_value.param.value,
)
def detailed_age_education(
    show_all_countries,
    apply_country_scope,
    selected_ages,
    selected_remote,
    top_n,
):
    filter_key = _filter_key_from_filter_values(
        selected_ages,
        selected_remote,
        show_all_countries,
        apply_country_scope,
        top_n,
    )
    age_profile = _cached_age_distribution(filter_key)
    age_education = _cached_age_education_distribution(filter_key)

    return pn.Column(
        pn.pane.Markdown(
            """
            ### Age Profile and Education Composition

            This view separates the respondent age distribution from the education mix within each age group.
            """
        ),
        _grid_box(
            make_age_percent_bar_chart(age_profile, "Respondent Age Distribution", METRIC_MODE),
            make_percent_stacked_bar_chart(age_education, "Education Level Composition by Age Group"),
            ncols=2,
        ),
        sizing_mode="stretch_width",
    )


@pn.depends(
    country_show_all.param.value,
    country_apply_dashboard.param.value,
    age_filter.param.value,
    remote_filter.param.value,
    top_n_value.param.value,
)
def detailed_compensation_experience(
    show_all_countries,
    apply_country_scope,
    selected_ages,
    selected_remote,
    top_n,
):
    filter_key = _filter_key_from_filter_values(
        selected_ages,
        selected_remote,
        show_all_countries,
        apply_country_scope,
        top_n,
    )
    salary_box = _cached_salary_remote_experience_box_summary(filter_key)
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
    country_show_all.param.value,
    age_filter.param.value,
    remote_filter.param.value,
    top_n_value.param.value,
)
def detailed_country_distribution(
    show_all_countries,
    selected_ages,
    selected_remote,
    top_n,
):
    filter_key = _map_filter_key_from_filter_values(
        selected_ages,
        selected_remote,
        show_all_countries,
        top_n,
    )
    filtered = _cached_filtered_df(*filter_key)
    map_data = _cached_country_map_distribution(filter_key, None)
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
            METRIC_MODE,
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
                pn.Row(
                    pn.pane.Markdown("#### Top N", margin=(0, 0, 0, 0)),
                    pn.Spacer(width=10),
                    top_n_reset_button,
                    sizing_mode="stretch_width",
                ),
                pn.pane.Markdown("Choose the ranking depth used by technology rankings and Top N country filtering."),
                top_n_5_checkbox,
                top_n_10_checkbox,
                top_n_12_checkbox,
                sizing_mode="stretch_width",
            ),
        ),
        (
            "Age",
            pn.Column(
                pn.Row(
                    pn.pane.Markdown("#### Age", margin=(0, 0, 0, 0)),
                    pn.Spacer(width=10),
                    age_reset_button,
                    sizing_mode="stretch_width",
                ),
                age_check_all,
                pn.pane.Markdown("Limit the dashboard to selected age groups."),
                age_filter,
                sizing_mode="stretch_width",
            ),
        ),
        (
            "Workstyle",
            pn.Column(
                pn.Row(
                    pn.pane.Markdown("#### Workstyle", margin=(0, 0, 0, 0)),
                    pn.Spacer(width=10),
                    remote_reset_button,
                    sizing_mode="stretch_width",
                ),
                remote_check_all,
                pn.pane.Markdown("Include one or more workstyle categories."),
                remote_filter,
                sizing_mode="stretch_width",
            ),
        ),
        (
            "Countries",
            pn.Column(
                pn.Row(
                    pn.pane.Markdown("#### Countries", margin=(0, 0, 0, 0)),
                    pn.Spacer(width=10),
                    country_reset_button,
                    sizing_mode="stretch_width",
                ),
                pn.pane.Markdown("By default, the map is limited by the selected Top N countries."),
                country_show_all,
                country_apply_dashboard,
                sizing_mode="stretch_width",
            ),
        ),
        active=[0, 1, 2, 3],
        sizing_mode="stretch_width",
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

    def _open_filter_sidebar() -> pn.Column:
        return pn.Column(
            pn.Row(
                pn.pane.Markdown("### Filters", margin=(2, 8, 0, 0)),
                reset_button,
                pn.Spacer(sizing_mode="stretch_width"),
                filter_panel_collapse_button,
                sizing_mode="stretch_width",
                margin=(0, 0, 8, 0),
            ),
            pn.pane.Markdown(
                """
                Use each category to refine the dashboard. Reset buttons restore category defaults where available.
                The dashboard uses respondent counts as its fixed metric.
                """,
                margin=(0, 0, 10, 0),
            ),
            filter_accordion,
            css_classes=["filter-sidebar"],
            width=310,
            sizing_mode="fixed",
        )

    def _collapsed_filter_rail() -> pn.Column:
        return pn.Column(
            filter_panel_expand_button,
            pn.pane.HTML('<div class="filter-rail-label">Filters</div>', width=34),
            css_classes=["filter-rail"],
            width=56,
            sizing_mode="fixed",
            align="start",
        )

    @pn.depends(filter_panel_open.param.value)
    def filter_sidebar(is_open: bool):
        return _open_filter_sidebar() if is_open else _collapsed_filter_rail()

    body = pn.Row(
        filter_sidebar,
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
