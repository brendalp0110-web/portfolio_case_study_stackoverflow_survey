from __future__ import annotations

import numpy as np
import plotly.graph_objects as go

from dashboard_dash_plotly import data


COLORS = {
    "page": "#f3f4f1",
    "surface": "#ffffff",
    "text": "#1f2933",
    "muted": "#52637a",
    "border": "#d7ddd6",
    "primary": "#2f7779",
    "accent": "#d99058",
    "green": "#7a8f5a",
    "red": "#c66b4e",
    "purple": "#8b6f9e",
    "grid": "#e5e9e1",
}
FONT_FAMILY = "Segoe UI, Helvetica Neue, Arial, sans-serif"
TECH_COLORS = {
    "Languages": "#2f7779",
    "Databases": "#d99058",
    "Platforms": "#7a8f5a",
    "Frameworks": "#8b6f9e",
}
EDUCATION_COLORS = ["#2f7779", "#d99058", "#7a8f5a", "#8b6f9e", "#c66b4e"]
WORKSTYLE_COLORS = {
    "Remote": "#2f7779",
    "Hybrid": "#7a8f5a",
    "In-person": "#c66b4e",
}
def education_legend_label(level: str) -> str:
    lower = level.lower()
    if "bachelor" in lower:
        return "Bachelor's"
    if "master" in lower:
        return "Master's"
    if "some college" in lower:
        return "Some college"
    if "secondary" in lower:
        return "Secondary"
    return level.replace("/university study", " study")


def apply_theme(fig: go.Figure, height: int = 420) -> go.Figure:
    fig.update_layout(
        height=height,
        paper_bgcolor=COLORS["surface"],
        plot_bgcolor=COLORS["surface"],
        font={"family": FONT_FAMILY, "color": COLORS["text"], "size": 12},
        margin={"l": 8, "r": 28, "t": 8, "b": 38},
        hoverlabel={
            "bgcolor": "#ffffff",
            "bordercolor": "#9aa6a1",
            "font": {"family": FONT_FAMILY, "color": "#111827", "size": 13},
        },
        xaxis={
            "gridcolor": COLORS["grid"],
            "zeroline": False,
            "title_font": {"family": FONT_FAMILY, "size": 12, "style": "normal"},
            "tickfont": {"family": FONT_FAMILY, "size": 11},
        },
        yaxis={
            "gridcolor": COLORS["grid"],
            "zeroline": False,
            "title_font": {"family": FONT_FAMILY, "size": 12, "style": "normal"},
            "tickfont": {"family": FONT_FAMILY, "size": 11},
        },
        modebar={"orientation": "v"},
    )
    return fig


def horizontal_bar(df, label_col: str, title_color: str) -> go.Figure:
    chart = df.sort_values("count", ascending=True)
    fig = go.Figure(
        go.Bar(
            x=chart["count"],
            y=chart[label_col],
            orientation="h",
            marker={"color": title_color},
            text=chart["count"].map(lambda value: f"{value:,.0f}"),
            textposition="outside",
            cliponaxis=False,
            customdata=chart[["share_pct"]],
            hovertemplate="<b>%{y}</b><br>Share of respondents: %{customdata[0]:.1f}%<extra></extra>",
            width=0.54,
        )
    )
    fig.update_xaxes(title_text="Respondent count")
    fig.update_yaxes(title_text="")
    return apply_theme(fig, height=max(330, 29 * len(chart) + 86))


def dumbbell(df, label_col: str) -> go.Figure:
    chart = df.sort_values("score", ascending=True)
    fig = go.Figure()
    for _, row in chart.iterrows():
        fig.add_trace(
            go.Scatter(
                x=[row["count_current"], row["count_future"]],
                y=[row[label_col], row[label_col]],
                mode="lines",
                line={"color": "#9aa6a1", "width": 3},
                hoverinfo="skip",
                showlegend=False,
            )
        )
    fig.add_trace(
        go.Scatter(
            x=chart["count_current"],
            y=chart[label_col],
            mode="markers",
            name="Current",
            marker={"color": COLORS["primary"], "size": 9, "line": {"color": "#ffffff", "width": 1}},
            customdata=chart[["count_future", "delta"]],
            hovertemplate="<b>%{y}</b><br>Current: %{x:,.0f}<br>Future: %{customdata[0]:,.0f}<br>Delta: %{customdata[1]:+,.0f}<extra></extra>",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=chart["count_future"],
            y=chart[label_col],
            mode="markers",
            name="Future",
            marker={"color": COLORS["accent"], "size": 9, "line": {"color": "#ffffff", "width": 1}},
            customdata=chart[["count_current", "delta"]],
            hovertemplate="<b>%{y}</b><br>Future: %{x:,.0f}<br>Current: %{customdata[0]:,.0f}<br>Delta: %{customdata[1]:+,.0f}<extra></extra>",
        )
    )
    fig.update_xaxes(title_text="Respondent count")
    fig.update_yaxes(title_text="")
    fig.update_layout(legend={"orientation": "h", "x": 1, "xanchor": "right", "y": 1.08, "yanchor": "bottom"})
    return apply_theme(fig, height=max(360, 30 * len(chart) + 96))


def age_bar(df) -> go.Figure:
    chart = df.iloc[::-1]
    fig = go.Figure(
        go.Bar(
            x=chart["count"],
            y=chart["age_short"],
            orientation="h",
            marker={"color": COLORS["primary"]},
            text=chart["count"].map(lambda value: f"{value:,.0f}"),
            textposition="outside",
            cliponaxis=False,
            customdata=chart[["age", "share_pct"]],
            hovertemplate="<b>%{customdata[0]}</b><br>Share of respondents: %{customdata[1]:.1f}%<extra></extra>",
            width=0.58,
        )
    )
    fig.update_xaxes(title_text="Respondent count")
    fig.update_yaxes(title_text="Age group")
    return apply_theme(fig, height=410)


def education_stack(df) -> go.Figure:
    fig = go.Figure()
    levels = [column for column in df.columns if column not in ["age", "age_short"]]
    for index, level in enumerate(levels):
        fig.add_trace(
            go.Bar(
                x=df["age_short"],
                y=df[level],
                name=education_legend_label(level),
                marker={"color": EDUCATION_COLORS[index % len(EDUCATION_COLORS)]},
                hovertemplate=f"<b>{level}</b><br>Age group: %{{x}}<br>Share within age group: %{{y:.1f}}%<extra></extra>",
            )
        )
    fig.update_xaxes(title_text="Age group")
    fig.update_yaxes(title_text="Share within age group (%)", range=[0, 100])
    fig = apply_theme(fig, height=430)
    fig.update_layout(
        barmode="stack",
        legend={
            "orientation": "h",
            "x": 0,
            "xanchor": "left",
            "y": 1.13,
            "yanchor": "bottom",
            "font": {"size": 11},
            "itemwidth": 30,
        },
        margin={"l": 8, "r": 28, "t": 44, "b": 44},
    )
    return fig


def compensation_box(summary_df, workstyle: str, y_max: float) -> go.Figure:
    chart = summary_df[summary_df["workstyle"] == workstyle]
    fig = go.Figure()
    if not chart.empty:
        color = WORKSTYLE_COLORS.get(workstyle, COLORS["primary"])
        fig.add_trace(
            go.Box(
                x=chart["experience_short"],
                q1=chart["q1"],
                median=chart["q2"],
                q3=chart["q3"],
                lowerfence=chart["lower"],
                upperfence=chart["upper"],
                boxpoints=False,
                marker={"color": color},
                line={"color": color, "width": 2},
                fillcolor=color,
                name="IQR and median",
                opacity=0.72,
                showlegend=False,
                customdata=chart[["experience_band", "q2", "mean", "count", "lower", "upper"]],
                hovertemplate=(
                    "<b>%{customdata[0]}</b><br>"
                    "Median: %{customdata[1]:$,.0f}<br>"
                    "Mean: %{customdata[2]:$,.0f}<br>"
                    "Whisker range: %{customdata[4]:$,.0f} - %{customdata[5]:$,.0f}<br>"
                    "Records: %{customdata[3]:,.0f}<extra></extra>"
                ),
            )
        )
        fig.add_trace(
            go.Scatter(
                x=chart["experience_short"],
                y=chart["mean"],
                mode="markers",
                name="Mean",
                marker={
                    "symbol": "diamond",
                    "size": 8,
                    "color": "#ffffff",
                    "line": {"color": color, "width": 2},
                },
                customdata=chart[["experience_band", "mean"]],
                hovertemplate="<b>%{customdata[0]}</b><br>Mean: %{customdata[1]:$,.0f}<extra></extra>",
            )
        )
    fig.update_xaxes(title_text="Years of experience")
    fig.update_yaxes(title_text="Annual compensation (USD)", range=[0, max(y_max, 1)])
    fig.update_layout(legend={"orientation": "h", "x": 1, "xanchor": "right", "y": 1.08, "yanchor": "bottom"})
    return apply_theme(fig, height=420)


def country_map(df) -> go.Figure:
    chart = df.copy()
    share = chart["share_pct"].astype(float)
    max_share = max(float(share.max()), 1.0) if not share.empty else 1.0
    chart["color_value"] = np.sqrt(share.clip(lower=0))
    chart["bubble_size"] = 7 + np.sqrt(share.clip(lower=0) / max_share) * 34
    tick_source = [0, 1, 2, 5, 10, 15, max_share]
    ticks = sorted({value for value in tick_source if value <= max_share})
    if max_share not in ticks:
        ticks.append(max_share)
    fig = go.Figure(
        go.Scattergeo(
            lon=chart["longitude"],
            lat=chart["latitude"],
            text=chart["country"],
            customdata=chart[["share_pct", "count"]],
            mode="markers",
            marker={
                "size": chart["bubble_size"],
                "color": chart["color_value"],
                "cmin": 0,
                "cmax": np.sqrt(max_share),
                "colorscale": [
                    [0.00, "#f4dfb8"],
                    [0.08, "#e4bd7a"],
                    [0.20, "#d99058"],
                    [0.45, "#9a7b66"],
                    [0.70, "#5f7f75"],
                    [1.00, "#1f666d"],
                ],
                "line": {"color": "#111827", "width": 1},
                "colorbar": {
                    "title": "Share %",
                    "tickvals": [np.sqrt(value) for value in ticks],
                    "ticktext": [f"{value:g}" for value in ticks],
                },
            },
            hovertemplate="<b>%{text}</b><br>Share: %{customdata[0]:.1f}%<br>Respondents: %{customdata[1]:,.0f}<extra></extra>",
        )
    )
    fig.update_geos(
        projection_type="natural earth",
        showland=True,
        landcolor="#e2e7e5",
        showcountries=True,
        countrycolor="#ffffff",
        showocean=True,
        oceancolor="#f5f7f5",
        showframe=False,
        lataxis_showgrid=False,
        lonaxis_showgrid=False,
    )
    fig.update_layout(margin={"l": 0, "r": 0, "t": 0, "b": 0})
    return apply_theme(fig, height=520)
