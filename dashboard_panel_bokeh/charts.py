from __future__ import annotations

import math
from typing import List

import pandas as pd
from bokeh.models import ColorBar, ColumnDataSource, FactorRange, HoverTool, LinearColorMapper, NumeralTickFormatter
from bokeh.palettes import Viridis256
from bokeh.plotting import figure
from xyzservices import providers as xyz


PLOT_TOOLS = "pan,wheel_zoom,box_zoom,reset,save"
TECH_COLORS = {
    "languages": "#2f6690",
    "databases": "#f28e2b",
    "platforms": "#59a14f",
    "frameworks": "#e15759",
}
WORLD_X_RANGE = (-20_000_000, 20_000_000)
WORLD_Y_RANGE = (-7_000_000, 18_500_000)
REMOTE_COLORS = {
    "Remote": "#2f6690",
    "Hybrid": "#59a14f",
    "In-person": "#e15759",
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


def _format_axis(plot: figure, metric_mode: str) -> None:
    if metric_mode == "Share of respondents":
        plot.xaxis.formatter = NumeralTickFormatter(format="0.0")


def _apply_readability_theme(plot: figure) -> None:
    plot.title.text_font_size = "15pt"
    plot.title.text_font_style = "bold"
    plot.xaxis.axis_label_text_font_size = "11pt"
    plot.yaxis.axis_label_text_font_size = "11pt"
    plot.xaxis.axis_label_text_font_style = "normal"
    plot.yaxis.axis_label_text_font_style = "normal"
    plot.xaxis.major_label_text_font_size = "10pt"
    plot.yaxis.major_label_text_font_size = "10pt"
    plot.toolbar.logo = None
    if plot.legend:
        plot.legend.label_text_font_size = "10pt"


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
) -> figure:
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
    plot.xaxis.axis_label = "Share of respondents (%)" if metric_mode == "Share of respondents" else "Respondent count"
    plot.yaxis.axis_label = ""
    plot.add_tools(
        HoverTool(
            tooltips=[
                (category_col.replace("_", " ").title(), "@{" + category_col + "}"),
                ("Count", "@count{0,0}"),
                ("Share of filtered respondents", "@share_pct{0.0}%"),
            ]
        )
    )
    _format_axis(plot, metric_mode)
    _apply_readability_theme(plot)
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
) -> figure:
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
        palette=Viridis256,
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
    plot.add_tile(xyz.CartoDB.Positron)
    renderer = plot.scatter(
        x="mercator_x",
        y="mercator_y",
        size="bubble_size",
        source=source,
        fill_color={"field": "share_pct", "transform": mapper},
        line_color="white",
        line_width=1.2,
        fill_alpha=0.85,
    )
    plot.add_tools(
        HoverTool(
            renderers=[renderer],
            tooltips=[
                ("Country", "@country"),
                ("Count", "@count{0,0}"),
                ("Share of filtered country respondents", "@share_pct{0.0}%"),
            ],
        )
    )
    color_bar = ColorBar(color_mapper=mapper, title="Share of filtered country respondents", location=(0, 0))
    plot.add_layout(color_bar, "right")
    plot.xaxis.visible = False
    plot.yaxis.visible = False
    plot.xgrid.visible = False
    plot.ygrid.visible = False
    plot.outline_line_color = "#d9e2ec"
    _apply_readability_theme(plot)
    return plot


def make_dumbbell_chart(
    data: pd.DataFrame,
    label_col: str,
    current_col: str,
    future_col: str,
    title: str,
    metric_mode: str,
) -> figure:
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
        color="#9aa5b1",
        alpha=0.9,
    )
    current_renderer = plot.scatter(
        x=current_col,
        y=label_col,
        size=11,
        color="#2f6690",
        line_color="white",
        line_width=1,
        source=source,
        legend_label="Current",
    )
    future_renderer = plot.scatter(
        x=future_col,
        y=label_col,
        size=11,
        color="#f28e2b",
        line_color="white",
        line_width=1,
        source=source,
        legend_label="Future",
    )
    plot.ygrid.grid_line_color = None
    plot.xaxis.axis_label = "Share of respondents (%)" if metric_mode == "Share of respondents" else "Respondent count"
    plot.yaxis.axis_label = ""
    plot.legend.location = "top_left"
    plot.legend.orientation = "horizontal"
    plot.add_tools(
        HoverTool(
            renderers=[current_renderer, future_renderer],
            tooltips=[
                (label_col.replace("_", " ").title(), "@{" + label_col + "}"),
                ("Current count", "@count_current{0,0}"),
                ("Future count", "@count_future{0,0}"),
                ("Current share of filtered respondents", "@share_pct_current{0.0}%"),
                ("Future share of filtered respondents", "@share_pct_future{0.0}%"),
                ("Delta share of filtered respondents", "@delta_share_pct{0.0}%"),
            ],
        )
    )
    _format_axis(plot, metric_mode)
    _apply_readability_theme(plot)
    return plot


def make_stacked_bar_chart(data: pd.DataFrame, title: str) -> figure:
    chart_data = data.copy()
    chart_data["AgeLabel"] = chart_data["Age"].map(AGE_SHORT_LABELS).fillna(chart_data["Age"])
    categories = chart_data["AgeLabel"].tolist()
    stacks: List[str] = [column for column in chart_data.columns if column not in ["Age", "AgeLabel"]]
    colors = ["#2f6690", "#59a14f", "#f28e2b", "#e15759", "#76b7b2"]

    source = ColumnDataSource(chart_data)
    plot = figure(
        x_range=categories,
        height=500,
        title=title,
        tools=PLOT_TOOLS,
        toolbar_location="right",
        sizing_mode="stretch_width",
    )
    renderers = plot.vbar_stack(stacks, x="AgeLabel", width=0.8, color=colors[: len(stacks)], source=source, legend_label=stacks)
    plot.xaxis.major_label_orientation = 0
    plot.xaxis.major_label_standoff = 8
    plot.yaxis.axis_label = "Respondent count"
    _place_legend_below(plot)
    plot.add_tools(
        HoverTool(
            renderers=renderers,
            tooltips=[("Age group", "@Age"), ("Count", "$y{0,0}")]
        )
    )
    _apply_readability_theme(plot)
    return plot


def make_age_percent_bar_chart(data: pd.DataFrame, title: str, metric_mode: str) -> figure:
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
    plot.hbar(y="age_label", right=value_col, height=0.72, color="#2f6690", source=source)
    plot.ygrid.grid_line_color = None
    plot.xaxis.axis_label = "Share of respondents (%)" if metric_mode == "Share of respondents" else "Respondent count"
    plot.yaxis.axis_label = "Age group"
    _format_axis(plot, metric_mode)
    plot.add_tools(
        HoverTool(
            tooltips=[
                ("Age group", "@age"),
                ("Count", "@count{0,0}"),
                ("Share of filtered respondents", "@share_pct{0.0}%"),
            ]
        )
    )
    _apply_readability_theme(plot)
    return plot


def make_percent_stacked_bar_chart(data: pd.DataFrame, title: str) -> figure:
    source_data = data.copy()
    stacks: List[str] = [column for column in source_data.columns if column != "Age"]
    colors = ["#2f6690", "#59a14f", "#f28e2b", "#e15759", "#76b7b2"]

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
                    "count": count,
                    "share_pct": share,
                    "bottom": bottom,
                    "top": top,
                    "color": colors[stacks.index(stack) % len(colors)],
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
        line_color="white",
        source=source,
        legend_field="education_level",
    )
    plot.xaxis.major_label_orientation = 0
    plot.xaxis.major_label_standoff = 8
    plot.yaxis.axis_label = "Share within age group (%)"
    plot.xaxis.axis_label = "Age group"
    plot.yaxis.formatter = NumeralTickFormatter(format="0")
    _place_legend_below(plot)
    plot.add_tools(
        HoverTool(
            renderers=[bars],
            tooltips=[
                ("Age group", "@Age"),
                ("Education level", "@education_level"),
                ("Count", "@count{0,0}"),
                ("Share within age", "@share_pct{0.0}%"),
            ]
        )
    )
    _apply_readability_theme(plot)
    return plot


def make_grouped_box_plot(data: pd.DataFrame, title: str) -> figure:
    chart_data = data.copy()
    chart_data["box_color"] = chart_data["remote_label"].map(REMOTE_COLORS).fillna("#2f6690")
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
    plot.segment("factor", "upper", "factor", "q3", source=source, line_color="#334e68")
    plot.segment("factor", "lower", "factor", "q1", source=source, line_color="#334e68")
    upper_boxes = plot.vbar(
        "factor",
        0.75,
        "q2",
        "q3",
        source=source,
        fill_color="box_color",
        fill_alpha=0.8,
        line_color="#243b53",
    )
    lower_boxes = plot.vbar(
        "factor",
        0.75,
        "q1",
        "q2",
        source=source,
        fill_color="box_color",
        fill_alpha=0.45,
        line_color="#243b53",
    )
    plot.rect("factor", "lower", 0.25, 0.01, source=source, line_color="#243b53")
    plot.rect("factor", "upper", 0.25, 0.01, source=source, line_color="#243b53")
    plot.xaxis.major_label_orientation = 1.0
    plot.yaxis.axis_label = "Converted annual compensation"
    plot.yaxis.formatter = NumeralTickFormatter(format="0,0")
    plot.add_tools(
        HoverTool(
            renderers=[upper_boxes, lower_boxes],
            tooltips=[
                ("Work style", "@remote_label"),
                ("Experience band", "@experience_band"),
                ("Median", "@q2{0,0}"),
                ("Mean", "@mean{0,0}"),
                ("Count", "@count{0,0}"),
            ]
        )
    )
    plot.x_range.group_padding = 0.15
    plot.xaxis.separator_line_color = "#bcccdc"
    _apply_readability_theme(plot)
    return plot


def make_compensation_experience_box_plot(
    data: pd.DataFrame,
    title: str,
    y_max: float,
    color: str,
) -> figure:
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
    plot.segment("factor", "upper", "factor", "q3", source=source, line_color="#334e68")
    plot.segment("factor", "lower", "factor", "q1", source=source, line_color="#334e68")
    upper_boxes = plot.vbar(
        "factor",
        0.68,
        "q2",
        "q3",
        source=source,
        fill_color=color,
        fill_alpha=0.85,
        line_color="#243b53",
    )
    lower_boxes = plot.vbar(
        "factor",
        0.68,
        "q1",
        "q2",
        source=source,
        fill_color=color,
        fill_alpha=0.45,
        line_color="#243b53",
    )
    plot.rect("factor", "lower", 0.24, 0.01, source=source, line_color="#243b53")
    plot.rect("factor", "upper", 0.24, 0.01, source=source, line_color="#243b53")
    plot.xaxis.major_label_orientation = 0
    plot.xaxis.axis_label = "Years of experience"
    plot.yaxis.axis_label = "Converted annual compensation"
    plot.yaxis.formatter = NumeralTickFormatter(format="0,0")
    plot.add_tools(
        HoverTool(
            renderers=[upper_boxes, lower_boxes],
            tooltips=[
                ("Experience band", "@experience_band"),
                ("Median", "@q2{0,0}"),
                ("Mean", "@mean{0,0}"),
                ("Count", "@count{0,0}"),
            ]
        )
    )
    _apply_readability_theme(plot)
    return plot
