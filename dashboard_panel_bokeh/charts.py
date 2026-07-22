from __future__ import annotations

import math
from typing import List

import pandas as pd
from bokeh.models import ColorBar, ColumnDataSource, FactorRange, HoverTool, LinearColorMapper, NumeralTickFormatter
from bokeh.plotting import figure
from xyzservices import providers as xyz


PLOT_TOOLS = "pan,wheel_zoom,box_zoom,reset,save"
TECH_COLORS = {
    "languages": "#2f6f73",
    "databases": "#d99058",
    "platforms": "#7a8f5a",
    "frameworks": "#c66b4e",
}
WORLD_X_RANGE = (-20_000_000, 20_000_000)
WORLD_Y_RANGE = (-7_000_000, 18_500_000)
REMOTE_COLORS = {
    "Remote": "#2f6f73",
    "Hybrid": "#7a8f5a",
    "In-person": "#c66b4e",
}
AGE_SHORT_LABELS = {
    "Under 18 years old": "<18",
    "18-24 years old": "18-24",
    "25-34 years old": "25-34",
    "35-44 years old": "35-44",
    "45-54 years old": "45-54",
    "55-64 years old": "55-64",
    "65 years or older": "65+",
    "Prefer not to say": "Undeclared",
}
EXPERIENCE_SHORT_LABELS = {
    "0-2 years": "0-2",
    "3-5 years": "3-5",
    "6-10 years": "6-10",
    "11-15 years": "11-15",
    "16+ years": "16+",
}
DEFAULT_LABELS = {
    "respondent_count_axis": "Respondent count",
    "share_respondents_axis": "Share of respondents (%)",
    "country": "Country",
    "count": "Count",
    "share_filtered_respondents": "Share of respondents",
    "share_filtered_country": "Share of respondents",
    "current": "Current",
    "future": "Future",
    "current_count": "Current count",
    "future_count": "Future count",
    "current_share": "Current share of respondents",
    "future_share": "Future share of respondents",
    "delta_share": "Delta share of respondents",
    "age_group": "Age group",
    "education_level": "Education level",
    "share_within_age": "Share within age",
    "share_within_age_axis": "Share within age group (%)",
    "years_experience": "Years of experience",
    "converted_compensation": "Converted annual compensation",
    "work_style": "Work style",
    "experience_band": "Experience band",
    "median": "Median",
    "mean": "Mean",
}
DEFAULT_THEME = {
    "chart_bg": "#ffffff",
    "chart_grid": "#e6eae4",
    "chart_border": "#d7ddd6",
    "text": "#1f2933",
    "muted": "#64748b",
    "primary": "#2f6f73",
    "accent": "#d99058",
    "positive": "#7a8f5a",
    "danger": "#c66b4e",
    "purple": "#8b6f9e",
    "connector": "#9aa6a1",
    "marker_line": "#ffffff",
    "map_palette": ["#efe6d6", "#dfb778", "#d99058", "#8a6964", "#2f6f73"],
    "education_colors": ["#2f6f73", "#d99058", "#7a8f5a", "#8b6f9e", "#c66b4e"],
    "remote_colors": REMOTE_COLORS,
}


def _labels(labels: dict | None) -> dict:
    merged = DEFAULT_LABELS.copy()
    if labels:
        merged.update(labels)
    return merged


def _chart_theme(theme: dict | None) -> dict:
    merged = DEFAULT_THEME.copy()
    if theme:
        merged.update(theme)
    return merged


def _metric_axis_label(metric_mode: str, labels: dict) -> str:
    return labels["share_respondents_axis"] if metric_mode == "Share of respondents" else labels["respondent_count_axis"]


def _education_label(value: str, labels: dict) -> str:
    return labels.get("education_levels", {}).get(value, value)


def _format_axis(plot: figure, metric_mode: str) -> None:
    if metric_mode == "Share of respondents":
        plot.xaxis.formatter = NumeralTickFormatter(format="0.0")


def _apply_readability_theme(plot: figure, theme: dict | None = None) -> None:
    colors = _chart_theme(theme)
    plot.title.text_font_size = "15pt"
    plot.title.text_font_style = "bold"
    plot.title.text_color = colors["text"]
    plot.background_fill_color = colors["chart_bg"]
    plot.border_fill_color = colors["chart_bg"]
    plot.outline_line_color = colors["chart_border"]
    plot.xgrid.grid_line_color = colors["chart_grid"]
    plot.ygrid.grid_line_color = colors["chart_grid"]
    plot.xaxis.axis_label_text_font_size = "11pt"
    plot.yaxis.axis_label_text_font_size = "11pt"
    plot.xaxis.axis_label_text_font_style = "normal"
    plot.yaxis.axis_label_text_font_style = "normal"
    plot.xaxis.axis_label_text_color = colors["text"]
    plot.yaxis.axis_label_text_color = colors["text"]
    plot.xaxis.major_label_text_font_size = "10pt"
    plot.yaxis.major_label_text_font_size = "10pt"
    plot.xaxis.major_label_text_color = colors["text"]
    plot.yaxis.major_label_text_color = colors["text"]
    plot.xaxis.axis_line_color = colors["chart_border"]
    plot.yaxis.axis_line_color = colors["chart_border"]
    plot.xaxis.major_tick_line_color = colors["chart_border"]
    plot.yaxis.major_tick_line_color = colors["chart_border"]
    plot.xaxis.minor_tick_line_color = colors["chart_border"]
    plot.yaxis.minor_tick_line_color = colors["chart_border"]
    plot.toolbar.logo = None
    if plot.legend:
        plot.legend.label_text_font_size = "10pt"
        plot.legend.label_text_color = colors["text"]
        plot.legend.background_fill_color = colors["chart_bg"]
        plot.legend.border_line_color = colors["chart_border"]


def _place_legend_below(plot: figure) -> None:
    if not plot.legend:
        return

    legend = plot.legend[0]
    legend.orientation = "horizontal"
    legend.location = "center"
    legend.click_policy = "hide"
    legend.label_text_font_size = "9pt"
    legend.spacing = 12
    legend.margin = 8
    plot.add_layout(legend, "below")


def make_horizontal_bar_chart(
    data: pd.DataFrame,
    category_col: str,
    value_col: str,
    title: str,
    metric_mode: str,
    color: str,
    labels: dict | None = None,
    theme: dict | None = None,
) -> figure:
    labels = _labels(labels)
    chart_data = data.sort_values(value_col, ascending=True).copy()
    source = ColumnDataSource(chart_data)

    height = max(430, 44 * len(chart_data) + 100)
    plot = figure(
        y_range=chart_data[category_col].tolist(),
        x_range=(0, max(chart_data[value_col].max() * 1.15, 1)),
        height=height,
        title=title,
        tools=PLOT_TOOLS,
        toolbar_location="right",
        sizing_mode="stretch_width",
    )
    plot.hbar(y=category_col, right=value_col, height=0.7, color=color, source=source)
    plot.ygrid.grid_line_color = None
    plot.xaxis.axis_label = _metric_axis_label(metric_mode, labels)
    plot.yaxis.axis_label = ""
    plot.add_tools(
        HoverTool(
            tooltips=[
                (labels.get(category_col, category_col.replace("_", " ").title()), "@{" + category_col + "}"),
                (labels["count"], "@count{0,0}"),
                (labels["share_filtered_respondents"], "@share_pct{0.0}%"),
            ]
        )
    )
    _format_axis(plot, metric_mode)
    _apply_readability_theme(plot, theme)
    return plot


def _lon_to_mercator(longitude: float) -> float:
    return longitude * 20037508.34 / 180


def _lat_to_mercator(latitude: float) -> float:
    latitude = max(min(latitude, 89.5), -89.5)
    radians = math.radians(latitude)
    return math.log(math.tan((math.pi / 4) + (radians / 2))) * 6378137.0


def make_country_bubble_map(
    data: pd.DataFrame,
    title: str,
    metric_mode: str,
    height: int = 480,
    labels: dict | None = None,
    theme: dict | None = None,
) -> figure:
    labels = _labels(labels)
    colors = _chart_theme(theme)
    chart_data = data.copy()
    value_col = "share_pct" if metric_mode == "Share of respondents" else "count"

    chart_data["mercator_x"] = chart_data["longitude"].astype(float).map(_lon_to_mercator)
    chart_data["mercator_y"] = chart_data["latitude"].astype(float).map(_lat_to_mercator)

    values = chart_data[value_col].astype(float)
    if values.nunique() == 1:
        chart_data["bubble_size"] = 24
    else:
        scaled = (values - values.min()) / (values.max() - values.min())
        chart_data["bubble_size"] = 14 + scaled * 26

    mapper = LinearColorMapper(
        palette=colors["map_palette"],
        low=float(chart_data["share_pct"].min()),
        high=float(chart_data["share_pct"].max()),
    )
    source = ColumnDataSource(chart_data)

    plot = figure(
        x_axis_type="mercator",
        y_axis_type="mercator",
        x_range=WORLD_X_RANGE,
        y_range=WORLD_Y_RANGE,
        height=height,
        title=title,
        tools=PLOT_TOOLS,
        toolbar_location="right",
        active_scroll="wheel_zoom",
        sizing_mode="stretch_width",
    )
    tile_renderer = plot.add_tile(xyz.CartoDB.PositronNoLabels)
    tile_renderer.tile_source.wrap_around = False
    plot.x_range.bounds = WORLD_X_RANGE
    plot.y_range.bounds = WORLD_Y_RANGE
    plot.x_range.max_interval = WORLD_X_RANGE[1] - WORLD_X_RANGE[0]
    plot.y_range.max_interval = WORLD_Y_RANGE[1] - WORLD_Y_RANGE[0]
    renderer = plot.scatter(
        x="mercator_x",
        y="mercator_y",
        size="bubble_size",
        source=source,
        fill_color={"field": "share_pct", "transform": mapper},
        line_color=colors["marker_line"],
        line_width=1.2,
        fill_alpha=0.85,
    )
    plot.add_tools(
        HoverTool(
            renderers=[renderer],
            tooltips=[
                (labels["country"], "@country"),
                (labels["count"], "@count{0,0}"),
                (labels["share_filtered_country"], "@share_pct{0.0}%"),
            ],
        )
    )
    color_bar = ColorBar(color_mapper=mapper, title=labels["share_filtered_country"], location=(0, 0))
    color_bar.title_text_font_style = "normal"
    color_bar.major_label_text_font_style = "normal"
    color_bar.title_text_color = colors["text"]
    color_bar.major_label_text_color = colors["text"]
    plot.add_layout(color_bar, "right")
    plot.xaxis.visible = False
    plot.yaxis.visible = False
    plot.xgrid.visible = False
    plot.ygrid.visible = False
    plot.outline_line_color = colors["chart_border"]
    _apply_readability_theme(plot, theme)
    return plot


def make_dumbbell_chart(
    data: pd.DataFrame,
    label_col: str,
    current_col: str,
    future_col: str,
    title: str,
    metric_mode: str,
    labels: dict | None = None,
    theme: dict | None = None,
) -> figure:
    labels = _labels(labels)
    colors = _chart_theme(theme)
    chart_data = data.sort_values(future_col, ascending=False).reset_index(drop=True).copy()

    source = ColumnDataSource(chart_data)
    category_range = chart_data[label_col].tolist()
    x_max = max(chart_data[[current_col, future_col]].max().max() * 1.15, 1)

    plot = figure(
        y_range=category_range,
        x_range=(0, x_max),
        height=max(440, 40 * len(chart_data) + 120),
        title=title,
        tools=PLOT_TOOLS,
        toolbar_location="right",
        sizing_mode="stretch_width",
    )
    plot.segment(
        x0=current_col,
        y0=label_col,
        x1=future_col,
        y1=label_col,
        source=source,
        line_width=3,
        color=colors["connector"],
        alpha=0.9,
    )
    current_renderer = plot.scatter(
        x=current_col,
        y=label_col,
        size=11,
        color=colors["primary"],
        line_color=colors["marker_line"],
        line_width=1,
        source=source,
        legend_label=labels["current"],
    )
    future_renderer = plot.scatter(
        x=future_col,
        y=label_col,
        size=11,
        color=colors["accent"],
        line_color=colors["marker_line"],
        line_width=1,
        source=source,
        legend_label=labels["future"],
    )
    plot.ygrid.grid_line_color = None
    plot.xaxis.axis_label = _metric_axis_label(metric_mode, labels)
    plot.yaxis.axis_label = ""
    plot.legend.location = "top_left"
    plot.legend.orientation = "horizontal"
    plot.add_tools(
        HoverTool(
            renderers=[current_renderer, future_renderer],
            tooltips=[
                (labels.get(label_col, label_col.replace("_", " ").title()), "@{" + label_col + "}"),
                (labels["current_count"], "@count_current{0,0}"),
                (labels["future_count"], "@count_future{0,0}"),
                (labels["current_share"], "@share_pct_current{0.0}%"),
                (labels["future_share"], "@share_pct_future{0.0}%"),
                (labels["delta_share"], "@delta_share_pct{0.0}%"),
            ],
        )
    )
    _format_axis(plot, metric_mode)
    _apply_readability_theme(plot, theme)
    return plot


def make_stacked_bar_chart(
    data: pd.DataFrame,
    title: str,
    labels: dict | None = None,
    theme: dict | None = None,
) -> figure:
    labels = _labels(labels)
    chart_data = data.copy()
    chart_data["AgeLabel"] = chart_data["Age"].map(AGE_SHORT_LABELS).fillna(chart_data["Age"])
    categories = chart_data["AgeLabel"].tolist()
    stacks: List[str] = [column for column in chart_data.columns if column not in ["Age", "AgeLabel"]]
    legend_labels = [_education_label(stack, labels) for stack in stacks]
    theme_colors = _chart_theme(theme)
    stack_colors = theme_colors["education_colors"]

    source = ColumnDataSource(chart_data)
    plot = figure(
        x_range=categories,
        height=500,
        title=title,
        tools=PLOT_TOOLS,
        toolbar_location="right",
        sizing_mode="stretch_width",
    )
    renderers = plot.vbar_stack(
        stacks,
        x="AgeLabel",
        width=0.8,
        color=stack_colors[: len(stacks)],
        source=source,
        legend_label=legend_labels,
    )
    plot.xaxis.major_label_orientation = 0
    plot.xaxis.major_label_standoff = 8
    plot.yaxis.axis_label = labels["respondent_count_axis"]
    _place_legend_below(plot)
    plot.add_tools(
        HoverTool(
            renderers=renderers,
            tooltips=[(labels["age_group"], "@Age"), (labels["count"], "$y{0,0}")]
        )
    )
    _apply_readability_theme(plot, theme)
    return plot


def make_age_percent_bar_chart(
    data: pd.DataFrame,
    title: str,
    metric_mode: str,
    labels: dict | None = None,
    theme: dict | None = None,
) -> figure:
    labels = _labels(labels)
    chart_data = data.copy()
    chart_data = chart_data[chart_data["count"] > 0].iloc[::-1].reset_index(drop=True)
    chart_data["age_label"] = chart_data["age"].map(AGE_SHORT_LABELS).fillna(chart_data["age"])
    value_col = "share_pct" if metric_mode == "Share of respondents" else "count"
    source = ColumnDataSource(chart_data)

    plot = figure(
        y_range=chart_data["age_label"].tolist(),
        x_range=(0, max(chart_data[value_col].max() * 1.15, 1)),
        height=500,
        title=title,
        tools=PLOT_TOOLS,
        toolbar_location="right",
        sizing_mode="stretch_width",
    )
    colors = _chart_theme(theme)
    plot.hbar(y="age_label", right=value_col, height=0.72, color=colors["primary"], source=source)
    plot.ygrid.grid_line_color = None
    plot.xaxis.axis_label = _metric_axis_label(metric_mode, labels)
    plot.yaxis.axis_label = labels["age_group"]
    _format_axis(plot, metric_mode)
    plot.add_tools(
        HoverTool(
            tooltips=[
                (labels["age_group"], "@age"),
                (labels["count"], "@count{0,0}"),
                (labels["share_filtered_respondents"], "@share_pct{0.0}%"),
            ]
        )
    )
    _apply_readability_theme(plot, theme)
    return plot


def make_percent_stacked_bar_chart(
    data: pd.DataFrame,
    title: str,
    labels: dict | None = None,
    theme: dict | None = None,
) -> figure:
    labels = _labels(labels)
    colors = _chart_theme(theme)
    source_data = data.copy()
    stacks: List[str] = [column for column in source_data.columns if column != "Age"]
    stack_colors = colors["education_colors"]

    long_rows = []
    for _, row in source_data.iterrows():
        total = float(row[stacks].sum())
        bottom = 0.0
        for stack in stacks:
            count = float(row[stack])
            share = count / total * 100 if total else 0.0
            top = bottom + share
            long_rows.append(
                {
                    "Age": row["Age"],
                    "AgeLabel": AGE_SHORT_LABELS.get(row["Age"], row["Age"]),
                    "education_level": stack,
                    "education_label": _education_label(stack, labels),
                    "count": count,
                    "share_pct": share,
                    "bottom": bottom,
                    "top": top,
                    "color": stack_colors[stacks.index(stack) % len(stack_colors)],
                }
            )
            bottom = top

    chart_data = pd.DataFrame(long_rows)
    categories = [AGE_SHORT_LABELS.get(age, age) for age in source_data["Age"].tolist()]
    source = ColumnDataSource(chart_data)

    plot = figure(
        x_range=categories,
        y_range=(0, 100),
        height=500,
        title=title,
        tools=PLOT_TOOLS,
        toolbar_location="right",
        sizing_mode="stretch_width",
    )
    bars = plot.vbar(
        x="AgeLabel",
        width=0.8,
        bottom="bottom",
        top="top",
        fill_color="color",
        line_color=colors["marker_line"],
        source=source,
        legend_field="education_label",
    )
    plot.xaxis.major_label_orientation = 0
    plot.xaxis.major_label_standoff = 8
    plot.yaxis.axis_label = labels["share_within_age_axis"]
    plot.xaxis.axis_label = labels["age_group"]
    plot.yaxis.formatter = NumeralTickFormatter(format="0")
    _place_legend_below(plot)
    plot.add_tools(
        HoverTool(
            renderers=[bars],
            tooltips=[
                (labels["age_group"], "@Age"),
                (labels["education_level"], "@education_label"),
                (labels["count"], "@count{0,0}"),
                (labels["share_within_age"], "@share_pct{0.0}%"),
            ]
        )
    )
    _apply_readability_theme(plot, theme)
    return plot


def make_grouped_box_plot(
    data: pd.DataFrame,
    title: str,
    labels: dict | None = None,
    theme: dict | None = None,
) -> figure:
    labels = _labels(labels)
    colors = _chart_theme(theme)
    chart_data = data.copy()
    chart_data["box_color"] = chart_data["remote_label"].map(colors["remote_colors"]).fillna(colors["primary"])
    source = ColumnDataSource(chart_data)
    categories = chart_data["factor"].tolist()
    y_max = max(chart_data["upper"].max() * 1.1, 1)

    plot = figure(
        x_range=FactorRange(*categories),
        y_range=(0, y_max),
        height=500,
        title=title,
        tools=PLOT_TOOLS,
        toolbar_location="right",
        sizing_mode="stretch_width",
    )
    plot.segment("factor", "upper", "factor", "q3", source=source, line_color=colors["connector"])
    plot.segment("factor", "lower", "factor", "q1", source=source, line_color=colors["connector"])
    upper_boxes = plot.vbar(
        "factor",
        0.75,
        "q2",
        "q3",
        source=source,
        fill_color="box_color",
        fill_alpha=0.8,
        line_color=colors["marker_line"],
    )
    lower_boxes = plot.vbar(
        "factor",
        0.75,
        "q1",
        "q2",
        source=source,
        fill_color="box_color",
        fill_alpha=0.45,
        line_color=colors["marker_line"],
    )
    plot.rect("factor", "lower", 0.25, 0.01, source=source, line_color=colors["marker_line"])
    plot.rect("factor", "upper", 0.25, 0.01, source=source, line_color=colors["marker_line"])
    plot.xaxis.major_label_orientation = 1.0
    plot.yaxis.axis_label = labels["converted_compensation"]
    plot.yaxis.formatter = NumeralTickFormatter(format="0,0")
    plot.add_tools(
        HoverTool(
            renderers=[upper_boxes, lower_boxes],
            tooltips=[
                (labels["work_style"], "@remote_label"),
                (labels["experience_band"], "@experience_band"),
                (labels["median"], "@q2{0,0}"),
                (labels["mean"], "@mean{0,0}"),
                (labels["count"], "@count{0,0}"),
            ]
        )
    )
    plot.x_range.group_padding = 0.15
    plot.xaxis.separator_line_color = colors["chart_border"]
    _apply_readability_theme(plot, theme)
    return plot


def make_compensation_experience_box_plot(
    data: pd.DataFrame,
    title: str,
    y_max: float,
    color: str,
    labels: dict | None = None,
    theme: dict | None = None,
) -> figure:
    labels = _labels(labels)
    colors = _chart_theme(theme)
    chart_data = data.copy()
    chart_data["factor"] = chart_data["experience_band"].astype(str).map(EXPERIENCE_SHORT_LABELS).fillna(
        chart_data["experience_band"].astype(str)
    )
    source = ColumnDataSource(chart_data)
    categories = chart_data["factor"].tolist()

    plot = figure(
        x_range=categories,
        y_range=(0, max(y_max, 1)),
        height=500,
        title=title,
        tools=PLOT_TOOLS,
        toolbar_location="right",
        sizing_mode="stretch_width",
    )
    plot.segment("factor", "upper", "factor", "q3", source=source, line_color=colors["connector"])
    plot.segment("factor", "lower", "factor", "q1", source=source, line_color=colors["connector"])
    upper_boxes = plot.vbar(
        "factor",
        0.68,
        "q2",
        "q3",
        source=source,
        fill_color=color,
        fill_alpha=0.85,
        line_color=colors["marker_line"],
    )
    lower_boxes = plot.vbar(
        "factor",
        0.68,
        "q1",
        "q2",
        source=source,
        fill_color=color,
        fill_alpha=0.45,
        line_color=colors["marker_line"],
    )
    plot.rect("factor", "lower", 0.24, 0.01, source=source, line_color=colors["marker_line"])
    plot.rect("factor", "upper", 0.24, 0.01, source=source, line_color=colors["marker_line"])
    plot.xaxis.major_label_orientation = 0
    plot.xaxis.axis_label = labels["years_experience"]
    plot.yaxis.axis_label = labels["converted_compensation"]
    plot.yaxis.formatter = NumeralTickFormatter(format="0,0")
    plot.add_tools(
        HoverTool(
            renderers=[upper_boxes, lower_boxes],
            tooltips=[
                (labels["experience_band"], "@experience_band"),
                (labels["median"], "@q2{0,0}"),
                (labels["mean"], "@mean{0,0}"),
                (labels["count"], "@count{0,0}"),
            ]
        )
    )
    _apply_readability_theme(plot, theme)
    return plot
