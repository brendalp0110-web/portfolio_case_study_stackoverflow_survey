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
    "grid": "#edf1ec",
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

FIGURE_TEXT = {
    "EN": {
        "respondent_count": "Respondent count",
        "share_of_respondents": "Share of respondents",
        "current": "Current",
        "future": "Future",
        "delta": "Delta",
        "age_group": "Age group",
        "share_within_age": "Share within age group",
        "share_within_age_axis": "Share within age group (%)",
        "years_experience": "Years of experience",
        "annual_compensation": "Annual compensation (USD)",
        "median": "Median",
        "mean": "Mean",
        "whisker_range": "Whisker range",
        "records": "Records",
        "share": "Share",
        "share_pct": "Share %",
        "respondents": "Respondents",
        "education_labels": {
            "bachelor": "Bachelor's",
            "master": "Master's",
            "some_college": "Some college study",
            "secondary": "Secondary",
            "other": "Other",
        },
    },
    "ES": {
        "respondent_count": "Conteo de encuestados",
        "share_of_respondents": "Porcentaje de encuestados",
        "current": "Actual",
        "future": "Futuro",
        "delta": "Diferencia",
        "age_group": "Grupo de edad",
        "share_within_age": "Porcentaje dentro del grupo de edad",
        "share_within_age_axis": "Porcentaje dentro del grupo de edad (%)",
        "years_experience": "Años de experiencia",
        "annual_compensation": "Compensación anual (USD)",
        "median": "Mediana",
        "mean": "Media",
        "whisker_range": "Rango de bigotes",
        "records": "Registros",
        "share": "Porcentaje",
        "share_pct": "Porcentaje",
        "respondents": "Encuestados",
        "education_labels": {
            "bachelor": "Licenciatura",
            "master": "Maestría",
            "some_college": "Estudios parciales",
            "secondary": "Secundaria",
            "other": "Otro",
        },
    },
}


def ft(lang: str | None, key: str):
    return FIGURE_TEXT.get(lang, FIGURE_TEXT["EN"])[key]


def hex_to_rgba(hex_color: str, alpha: float) -> str:
    hex_color = hex_color.lstrip("#")
    red, green, blue = (int(hex_color[index : index + 2], 16) for index in (0, 2, 4))
    return f"rgba({red}, {green}, {blue}, {alpha})"


def format_share_pct(value: float, decimal_separator: str = ".") -> str:
    if 0 < value < 0.1:
        return f"<0{decimal_separator}1%"
    formatted = f"{value:.1f}%"
    return formatted.replace(".", decimal_separator) if decimal_separator != "." else formatted


def age_short_labels(lang: str | None) -> dict[str, str]:
    labels = data.AGE_SHORT_LABELS.copy()
    if lang == "ES":
        labels["Prefer not to say"] = "No declarado"
    return labels


def age_long_label(value: str, lang: str | None) -> str:
    if lang != "ES":
        return value
    return {
        "Under 18 years old": "Menos de 18 años",
        "18-24 years old": "18-24 años",
        "25-34 years old": "25-34 años",
        "35-44 years old": "35-44 años",
        "45-54 years old": "45-54 años",
        "55-64 years old": "55-64 años",
        "65 years or older": "65 años o más",
        "Prefer not to say": "No declarado",
    }.get(value, value)


def experience_label(value: str, lang: str | None) -> str:
    if lang != "ES":
        return value
    return value.replace(" years", " años")


def education_legend_label(level: str, lang: str | None = "EN") -> str:
    lower = level.lower()
    labels = ft(lang, "education_labels")
    if "bachelor" in lower:
        return labels["bachelor"]
    if "master" in lower:
        return labels["master"]
    if "some college" in lower:
        return labels["some_college"]
    if "secondary" in lower:
        return labels["secondary"]
    if lower == "other":
        return labels["other"]
    return level.replace("/university study", " study")


def apply_theme(fig: go.Figure, height: int = 420) -> go.Figure:
    fig.update_layout(
        height=height,
        paper_bgcolor=COLORS["surface"],
        plot_bgcolor=COLORS["surface"],
        font={"family": FONT_FAMILY, "color": COLORS["text"], "size": 12},
        margin={"l": 8, "r": 34, "t": 8, "b": 38},
        hoverlabel={
            "bgcolor": "#ffffff",
            "bordercolor": "#c7d0c8",
            "font": {"family": FONT_FAMILY, "color": "#111827", "size": 13},
            "align": "left",
        },
        xaxis={
            "gridcolor": COLORS["grid"],
            "gridwidth": 0.45,
            "zeroline": False,
            "showline": True,
            "linecolor": COLORS["border"],
            "linewidth": 1,
            "ticks": "",
            "title_font": {"family": FONT_FAMILY, "size": 12, "style": "normal"},
            "tickfont": {"family": FONT_FAMILY, "size": 11},
            "title_standoff": 10,
            "automargin": True,
        },
        yaxis={
            "gridcolor": COLORS["grid"],
            "gridwidth": 0.45,
            "zeroline": False,
            "showline": True,
            "linecolor": COLORS["border"],
            "linewidth": 1,
            "ticks": "",
            "title_font": {"family": FONT_FAMILY, "size": 12, "style": "normal"},
            "tickfont": {"family": FONT_FAMILY, "size": 11},
            "title_standoff": 10,
            "automargin": True,
        },
        modebar={"orientation": "v"},
        bargap=0.28,
    )
    return fig


def horizontal_bar(df, label_col: str, title_color: str, lang: str | None = "EN") -> go.Figure:
    chart = df.sort_values("count", ascending=True)
    fig = go.Figure(
        go.Bar(
            x=chart["count"],
            y=chart[label_col],
            orientation="h",
            marker={"color": title_color, "line": {"width": 0}},
            opacity=0.96,
            text=chart["count"].map(lambda value: f"{value:,.0f}"),
            textposition="outside",
            textfont={"color": COLORS["muted"], "size": 11, "family": FONT_FAMILY},
            cliponaxis=False,
            customdata=chart[["share_pct"]],
            hovertemplate=f"<b>%{{y}}</b><br>{ft(lang, 'share_of_respondents')}: %{{customdata[0]:.1f}}%<extra></extra>",
            width=0.54,
        )
    )
    fig.update_xaxes(title_text=ft(lang, "respondent_count"))
    fig.update_yaxes(title_text="")
    fig.update_layout(barcornerradius=5)
    return apply_theme(fig, height=max(330, 29 * len(chart) + 86))


def dumbbell(df, label_col: str, lang: str | None = "EN") -> go.Figure:
    chart = df.sort_values("score", ascending=True)
    fig = go.Figure()
    for _, row in chart.iterrows():
        fig.add_trace(
            go.Scatter(
                x=[row["count_current"], row["count_future"]],
                y=[row[label_col], row[label_col]],
                mode="lines",
                line={"color": "#c4ccc5", "width": 2.4},
                hoverinfo="skip",
                showlegend=False,
            )
        )
    fig.add_trace(
        go.Scatter(
            x=chart["count_current"],
            y=chart[label_col],
            mode="markers",
            name=ft(lang, "current"),
            marker={"color": COLORS["primary"], "size": 10, "line": {"color": "#ffffff", "width": 1.6}},
            customdata=chart[["count_future", "delta"]],
            hovertemplate=(
                f"<b>%{{y}}</b><br>{ft(lang, 'current')}: %{{x:,.0f}}<br>"
                f"{ft(lang, 'future')}: %{{customdata[0]:,.0f}}<br>"
                f"{ft(lang, 'delta')}: %{{customdata[1]:+,.0f}}<extra></extra>"
            ),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=chart["count_future"],
            y=chart[label_col],
            mode="markers",
            name=ft(lang, "future"),
            marker={"color": COLORS["accent"], "size": 10, "line": {"color": "#ffffff", "width": 1.6}},
            customdata=chart[["count_current", "delta"]],
            hovertemplate=(
                f"<b>%{{y}}</b><br>{ft(lang, 'future')}: %{{x:,.0f}}<br>"
                f"{ft(lang, 'current')}: %{{customdata[0]:,.0f}}<br>"
                f"{ft(lang, 'delta')}: %{{customdata[1]:+,.0f}}<extra></extra>"
            ),
        )
    )
    fig.update_xaxes(title_text=ft(lang, "respondent_count"))
    fig.update_yaxes(title_text="")
    fig.update_layout(
        legend={
            "orientation": "h",
            "x": 1,
            "xanchor": "right",
            "y": 1.1,
            "yanchor": "bottom",
            "bgcolor": "rgba(255,255,255,0.86)",
            "bordercolor": COLORS["border"],
            "borderwidth": 1,
            "font": {"size": 11},
        }
    )
    return apply_theme(fig, height=max(345, 27 * len(chart) + 104))


def age_bar(df, lang: str | None = "EN") -> go.Figure:
    chart = df.iloc[::-1].copy()
    chart["age_short"] = chart["age"].map(age_short_labels(lang))
    chart["age_hover"] = chart["age"].map(lambda value: age_long_label(value, lang))
    fig = go.Figure(
        go.Bar(
            x=chart["count"],
            y=chart["age_short"],
            orientation="h",
            marker={"color": COLORS["primary"], "line": {"width": 0}},
            opacity=0.96,
            text=chart["count"].map(lambda value: f"{value:,.0f}"),
            textposition="outside",
            textfont={"color": COLORS["muted"], "size": 11, "family": FONT_FAMILY},
            cliponaxis=False,
            customdata=chart[["age_hover", "share_pct"]],
            hovertemplate=f"<b>%{{customdata[0]}}</b><br>{ft(lang, 'share_of_respondents')}: %{{customdata[1]:.1f}}%<extra></extra>",
            width=0.58,
        )
    )
    fig.update_xaxes(title_text=ft(lang, "respondent_count"))
    fig.update_yaxes(title_text=ft(lang, "age_group"))
    fig.update_layout(barcornerradius=5)
    return apply_theme(fig, height=410)


def education_stack(df, lang: str | None = "EN") -> go.Figure:
    df = df.copy()
    df["age_short"] = df["age"].map(age_short_labels(lang))
    fig = go.Figure()
    levels = [column for column in df.columns if column not in ["age", "age_short"]]
    for index, level in enumerate(levels):
        fig.add_trace(
            go.Bar(
                x=df["age_short"],
                y=df[level],
                name=education_legend_label(level, lang),
                marker={"color": EDUCATION_COLORS[index % len(EDUCATION_COLORS)], "line": {"color": COLORS["surface"], "width": 0.7}},
                opacity=0.95,
                hovertemplate=(
                    f"<b>{education_legend_label(level, lang)}</b><br>"
                    f"{ft(lang, 'age_group')}: %{{x}}<br>"
                    f"{ft(lang, 'share_within_age')}: %{{y:.1f}}%<extra></extra>"
                ),
            )
        )
    fig.update_xaxes(title_text=ft(lang, "age_group"))
    fig.update_yaxes(title_text=ft(lang, "share_within_age_axis"), range=[0, 100])
    fig = apply_theme(fig, height=430)
    fig.update_layout(
        barmode="stack",
        legend={
            "orientation": "h",
            "x": 0,
            "xanchor": "left",
            "y": 1.08,
            "yanchor": "bottom",
            "font": {"size": 9},
            "itemsizing": "constant",
        },
        margin={"l": 8, "r": 28, "t": 42, "b": 40},
    )
    return fig


def compensation_box(summary_df, workstyle: str, y_max: float, lang: str | None = "EN") -> go.Figure:
    chart = summary_df[summary_df["workstyle"] == workstyle].copy()
    if not chart.empty:
        chart["experience_hover"] = chart["experience_band"].map(lambda value: experience_label(str(value), lang))
    fig = go.Figure()
    if not chart.empty:
        color = WORKSTYLE_COLORS.get(workstyle, COLORS["primary"])
        fill = hex_to_rgba(color, 0.48)
        fig.add_trace(
            go.Box(
                x=chart["experience_short"],
                q1=chart["q1"],
                median=chart["q2"],
                q3=chart["q3"],
                lowerfence=chart["lower"],
                upperfence=chart["upper"],
                boxpoints=False,
                marker={"color": color, "line": {"color": "#ffffff", "width": 1}},
                line={"color": color, "width": 1.8},
                fillcolor=fill,
                name="IQR",
                opacity=1,
                showlegend=False,
                width=0.48,
                whiskerwidth=0.7,
                customdata=chart[["experience_hover", "q2", "mean", "count", "lower", "upper"]],
                hovertemplate=(
                    "<b>%{customdata[0]}</b><br>"
                    f"{ft(lang, 'median')}: %{{customdata[1]:$,.0f}}<br>"
                    f"{ft(lang, 'mean')}: %{{customdata[2]:$,.0f}}<br>"
                    f"{ft(lang, 'whisker_range')}: %{{customdata[4]:$,.0f}} - %{{customdata[5]:$,.0f}}<br>"
                    f"{ft(lang, 'records')}: %{{customdata[3]:,.0f}}<extra></extra>"
                ),
            )
        )
        fig.add_trace(
            go.Scatter(
                x=chart["experience_short"],
                y=chart["mean"],
                mode="markers",
                name=ft(lang, "mean"),
                marker={
                    "symbol": "diamond",
                    "size": 7,
                    "color": "#ffffff",
                    "line": {"color": color, "width": 2},
                },
                customdata=chart[["experience_hover", "mean"]],
                hovertemplate=f"<b>%{{customdata[0]}}</b><br>{ft(lang, 'mean')}: %{{customdata[1]:$,.0f}}<extra></extra>",
            )
        )
    fig.update_xaxes(title_text=ft(lang, "years_experience"))
    fig.update_yaxes(title_text=ft(lang, "annual_compensation"), range=[0, max(y_max, 1)])
    fig.update_layout(legend={"orientation": "h", "x": 1, "xanchor": "right", "y": 1.08, "yanchor": "bottom"})
    return apply_theme(fig, height=420)


def country_map(df, lang: str | None = "EN") -> go.Figure:
    chart = df.copy()
    share = chart["share_pct"].astype(float)
    max_share = max(float(share.max()), 1.0) if not share.empty else 1.0
    decimal_separator = "," if lang == "ES" else "."
    chart["share_label"] = share.map(lambda value: format_share_pct(value, decimal_separator))
    chart["color_value"] = np.sqrt(share.clip(lower=0))
    chart["bubble_size"] = 7 + np.sqrt(share.clip(lower=0) / max_share) * 34
    tick_step = 5
    tick_upper = int(np.ceil(max_share / tick_step) * tick_step)
    ticks = list(range(0, tick_upper + tick_step, tick_step))
    fig = go.Figure(
        go.Scattergeo(
            lon=chart["longitude"],
            lat=chart["latitude"],
            text=chart["country"],
            customdata=chart[["share_label", "count"]],
            mode="markers",
            marker={
                "size": chart["bubble_size"],
                "color": chart["color_value"],
                "cmin": 0,
                "cmax": np.sqrt(tick_upper),
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
                    "title": ft(lang, "share_pct"),
                    "tickvals": [np.sqrt(value) for value in ticks],
                    "ticktext": [f"{value}" for value in ticks],
                },
            },
            hovertemplate=(
                f"<b>%{{text}}</b><br>{ft(lang, 'share')}: %{{customdata[0]}}<br>"
                f"{ft(lang, 'respondents')}: %{{customdata[1]:,.0f}}<extra></extra>"
            ),
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
    return apply_theme(fig, height=460)
