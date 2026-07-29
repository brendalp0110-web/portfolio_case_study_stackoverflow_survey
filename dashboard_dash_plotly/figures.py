from __future__ import annotations

import math

import numpy as np
import plotly.graph_objects as go

from dashboard_dash_plotly import data


COLORS = {
    "page": "#f1f3ef",
    "surface": "#fffdfa",
    "header": "#17384c",
    "text": "#152331",
    "muted": "#5f6f7d",
    "border": "#d3ddd1",
    "primary": "#167c80",
    "primary_deep": "#0f6166",
    "accent": "#d4824a",
    "sage": "#7f9465",
    "clay": "#bf6b52",
    "violet": "#876f98",
    "grid": "#edf2eb",
}
FONT_FAMILY = "Segoe UI, Helvetica Neue, Arial, sans-serif"
TECH_COLORS = {
    "Languages": COLORS["primary"],
    "Databases": COLORS["accent"],
    "Platforms": COLORS["sage"],
    "Frameworks": COLORS["violet"],
}
EDUCATION_COLORS = [COLORS["primary"], COLORS["accent"], COLORS["sage"], COLORS["violet"], COLORS["clay"]]
WORKSTYLE_COLORS = {
    "Remote": COLORS["primary"],
    "Hybrid": COLORS["sage"],
    "In-person": COLORS["clay"],
}
WORKSTYLE_LINE_STYLES = {
    "Remote": "solid",
    "Hybrid": "dash",
    "In-person": "dot",
}
MIN_JOB_SAT_RECORDS = 10
TREEMAP_TILE_COLORS = {
    "Languages": [COLORS["primary"], COLORS["accent"], COLORS["sage"], COLORS["violet"], COLORS["clay"], "#4f7892", "#b79b61", "#697b8c", "#2f6f73", "#d19a66"],
    "Databases": [COLORS["accent"], COLORS["primary"], COLORS["sage"], COLORS["clay"], COLORS["violet"], "#b79b61", "#4f7892", "#697b8c", "#d19a66", "#2f6f73"],
    "Platforms": [COLORS["sage"], COLORS["primary"], COLORS["accent"], COLORS["clay"], COLORS["violet"], "#4f7892", "#b79b61", "#697b8c", "#2f6f73", "#d19a66"],
    "Frameworks": [COLORS["violet"], COLORS["primary"], COLORS["accent"], COLORS["sage"], COLORS["clay"], "#4f7892", "#b79b61", "#697b8c", "#2f6f73", "#d19a66"],
}
DEVTYPE_COLORS = [COLORS["primary"], COLORS["accent"], COLORS["sage"], COLORS["violet"], COLORS["clay"], "#4f7892", "#b79b61", "#697b8c", "#2f6f73"]

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
        "role_mentions": "Role mentions",
        "share_of_role_mentions": "Share of role mentions",
        "roles_included": "Top roles",
        "distinct_roles": "Distinct roles",
        "average_job_sat": "Average job satisfaction",
        "median_job_sat": "Median job satisfaction",
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
        "role_mentions": "Menciones de rol",
        "share_of_role_mentions": "Porcentaje de menciones de rol",
        "roles_included": "Roles principales",
        "distinct_roles": "Roles distintos",
        "average_job_sat": "Satisfacción laboral promedio",
        "median_job_sat": "Satisfacción laboral mediana",
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


def readable_text_color(hex_color: str) -> str:
    hex_color = hex_color.lstrip("#")
    red, green, blue = (int(hex_color[index : index + 2], 16) for index in (0, 2, 4))
    luminance = 0.2126 * red + 0.7152 * green + 0.0722 * blue
    return "#ffffff" if luminance < 142 else COLORS["text"]


def short_technology_label(value: str) -> str:
    replacements = {
        "Bash/Shell (all shells)": "Bash/Shell",
        "Amazon Web Services (AWS)": "AWS",
        "Microsoft Azure": "Azure",
        "Oracle Cloud Infrastructure (OCI)": "Oracle OCI",
        "Firebase Realtime Database": "Firebase RTDB",
        "Google Cloud Firestore": "Firestore",
        "ASP.NET CORE": "ASP.NET Core",
    }
    return replacements.get(value, value)


def devtype_group_label(value: str, lang: str | None = "EN") -> str:
    labels = {
        "Core software development": ("Core software development", "Desarrollo de software"),
        "Leadership & product": ("Leadership & product", "Liderazgo y producto"),
        "Infrastructure, cloud & operations": ("Infrastructure, cloud & operations", "Infraestructura, cloud y operaciones"),
        "Data, analytics & AI": ("Data, analytics & AI", "Datos, analítica e IA"),
        "Research & education": ("Research & education", "Investigación y educación"),
        "Unspecified": ("Unspecified", "No especificado"),
        "Developer relations & experience": ("Developer relations & experience", "Relaciones y experiencia dev"),
        "Security": ("Security", "Seguridad"),
        "Design & commercial": ("Design & commercial", "Diseño y comercial"),
    }
    if value in labels:
        return labels[value][1 if lang == "ES" else 0]
    return value


def compact_devtype_group_label(value: str, lang: str | None = "EN") -> str:
    labels = {
        "Core software development": ("Software Developer", "Desarrollo de software"),
        "Leadership & product": ("Leadership & product", "Liderazgo y producto"),
        "Infrastructure, cloud & operations": ("Infrastructure", "Infraestructura"),
        "Data, analytics & AI": ("Data Analytics & AI", "Datos, analítica e IA"),
        "Research & education": ("Research & Education", "Investigación y educación"),
        "Unspecified": ("Unspecified", "No especificado"),
        "Developer relations & experience": ("Developer Community", "Comunidad de desarrollo"),
        "Security": ("Security", "Seguridad"),
        "Design & commercial": ("Commercial", "Comercial"),
    }
    if value in labels:
        return labels[value][1 if lang == "ES" else 0]
    return devtype_group_label(value, lang)


def compact_role_label(value: str, lang: str | None = "EN") -> str:
    labels = {
        "Developer, full-stack": ("Full-stack", "Full-stack"),
        "Developer, back-end": ("Back-end", "Back-end"),
        "Developer, front-end": ("Front-end", "Front-end"),
        "Developer, desktop or enterprise applications": ("Desktop / enterprise", "Desktop / enterprise"),
        "Developer, mobile": ("Mobile", "Móvil"),
        "Developer, embedded applications or devices": ("Embedded", "Embedded"),
        "Developer, game or graphics": ("Game / graphics", "Juegos / gráficos"),
        "Developer, QA or test": ("QA / test", "QA / test"),
        "Developer, AI": ("AI developer", "Dev IA"),
        "Data engineer": ("Data engineer", "Data engineer"),
        "Data scientist or machine learning specialist": ("Data scientist / ML", "Data scientist / ML"),
        "Data or business analyst": ("Data / business analyst", "Analista datos / negocio"),
        "Scientist": ("Scientist", "Científico"),
        "DevOps specialist": ("DevOps", "DevOps"),
        "Cloud infrastructure engineer": ("Cloud infra.", "Infra. cloud"),
        "Engineer, site reliability": ("SRE", "SRE"),
        "System administrator": ("Sysadmin", "Sysadmin"),
        "Database administrator": ("DBA", "DBA"),
        "Blockchain": ("Blockchain", "Blockchain"),
        "Hardware Engineer": ("Hardware", "Hardware"),
        "Engineering manager": ("Eng. manager", "Eng. manager"),
        "Senior Executive (C-Suite, VP, etc.)": ("Executive", "Ejecutivo"),
        "Project manager": ("Project manager", "Project manager"),
        "Product manager": ("Product manager", "Product manager"),
        "Research & Development role": ("R&D", "I+D"),
        "Academic researcher": ("Academic researcher", "Investigador académico"),
        "Educator": ("Educator", "Educador"),
        "Student": ("Student", "Estudiante"),
        "Developer Experience": ("DevEx", "DevEx"),
        "Developer Advocate": ("Dev advocate", "Dev advocate"),
        "Security professional": ("Security", "Seguridad"),
        "Designer": ("Designer", "Diseñador"),
        "Marketing or sales professional": ("Marketing / sales", "Marketing / ventas"),
        "Other (please specify):": ("Unspecified", "No especificado"),
    }
    if value in labels:
        return labels[value][1 if lang == "ES" else 0]
    return value.replace("Developer, ", "")


def compact_roles_list(value: str, role_count: int, lang: str | None = "EN") -> str:
    role_labels = {
        "Developer, full-stack": ("Full-Stack Developer", "Desarrollador Full-Stack"),
        "Developer, back-end": ("Back-end Developer", "Desarrollador Back-end"),
        "Developer, front-end": ("Front-end Developer", "Desarrollador Front-end"),
        "Engineering manager": ("Engineering Manager", "Gerente de ingeniería"),
        "Senior Executive (C-Suite, VP, etc.)": ("Senior Executive", "Ejecutivo senior"),
        "Data engineer": ("Data Engineer", "Ingeniero de datos"),
        "Data scientist or machine learning specialist": ("Data Scientist", "Científico de datos"),
        "DevOps specialist": ("DevOps specialist", "Especialista DevOps"),
        "Cloud infrastructure engineer": ("Cloud infrastructure engineer", "Ingeniero de infraestructura cloud"),
        "Research & Development role": ("Research & Development", "Investigación y desarrollo"),
        "Student": ("Student", "Estudiante"),
        "Designer": ("Designer", "Diseñador"),
        "Marketing or sales professional": ("Marketing", "Marketing"),
        "Developer Experience": ("Developer Experience", "Developer Experience"),
        "Developer Advocate": ("Developer Advocate", "Developer Advocate"),
        "Security professional": ("Security professional", "Profesional de seguridad"),
    }
    roles = [
        role_labels.get(role, (role, role))[1 if lang == "ES" else 0]
        for role in value.split("; ")
        if role
    ]
    if not roles or roles == ["Other (please specify):"]:
        return ""
    suffix = ", etc." if role_count > len(roles) else ""
    return ", ".join(roles) + suffix


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
            "bgcolor": COLORS["surface"],
            "bordercolor": COLORS["border"],
            "font": {"family": FONT_FAMILY, "color": COLORS["text"], "size": 13},
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


def vertical_treemap(df, label_col: str, family: str, lang: str | None = "EN") -> go.Figure:
    chart = df.sort_values("count", ascending=False).reset_index(drop=True).copy()
    if chart.empty:
        return apply_theme(go.Figure(), height=335)

    chart["rank"] = np.arange(1, len(chart) + 1)
    top_total = max(float(chart["count"].sum()), 1.0)
    row_groups = [chart.iloc[0:3], chart.iloc[3:6], chart.iloc[6:10]]
    colors = TREEMAP_TILE_COLORS.get(family, TREEMAP_TILE_COLORS["Languages"])

    fig = go.Figure()
    annotations = []
    hover_x = []
    hover_y = []
    hover_custom = []
    hover_text = []
    y_top = 100.0
    color_index = 0

    for row_df in row_groups:
        if row_df.empty:
            continue
        row_height = 100.0 * row_df["count"].sum() / top_total
        y0 = y_top - row_height
        x0 = 0.0
        row_total = max(float(row_df["count"].sum()), 1.0)
        for row in row_df.itertuples(index=False):
            width = 100.0 * float(row.count) / row_total
            color = colors[color_index % len(colors)]
            text_color = readable_text_color(color)
            label = short_technology_label(getattr(row, label_col))
            tile_area = width * row_height
            fig.add_shape(
                type="rect",
                x0=x0,
                y0=y0,
                x1=x0 + width,
                y1=y_top,
                line={"color": COLORS["surface"], "width": 3},
                fillcolor=color,
                opacity=0.96,
            )
            if tile_area > 440:
                annotations.extend(
                    [
                        {
                            "x": x0 + 1.2,
                            "y": y_top - 3,
                            "text": f"#{int(row.rank)} {label}",
                            "showarrow": False,
                            "xanchor": "left",
                            "yanchor": "top",
                            "font": {"color": text_color, "size": 13, "family": FONT_FAMILY},
                        },
                        {
                            "x": x0 + 1.2,
                            "y": y0 + 2.4,
                            "text": f"{int(row.count):,} | {float(row.share_pct):.1f}%",
                            "showarrow": False,
                            "xanchor": "left",
                            "yanchor": "bottom",
                            "font": {"color": text_color, "size": 11, "family": FONT_FAMILY},
                        },
                    ]
                )
            elif tile_area > 200:
                annotations.append(
                    {
                        "x": x0 + width / 2,
                        "y": y0 + row_height / 2,
                        "text": f"#{int(row.rank)}<br>{label}<br>{float(row.share_pct):.1f}%",
                        "showarrow": False,
                        "xanchor": "center",
                        "yanchor": "middle",
                        "font": {"color": text_color, "size": 10, "family": FONT_FAMILY},
                    }
                )
            hover_x.append(x0 + width / 2)
            hover_y.append(y0 + row_height / 2)
            hover_text.append(label)
            hover_custom.append([row.rank, row.count, row.share_pct])
            x0 += width
            color_index += 1
        y_top = y0

    fig.add_trace(
        go.Scatter(
            x=hover_x,
            y=hover_y,
            text=hover_text,
            customdata=hover_custom,
            mode="markers",
            marker={"size": 18, "opacity": 0},
            hovertemplate=(
                "<b>%{text}</b><br>"
                "Rank: #%{customdata[0]:.0f}<br>"
                f"{ft(lang, 'respondent_count')}: %{{customdata[1]:,.0f}}<br>"
                f"{ft(lang, 'share_of_respondents')}: %{{customdata[2]:.1f}}%<extra></extra>"
            ),
            showlegend=False,
        )
    )
    fig.update_layout(annotations=annotations)
    fig.update_xaxes(visible=False, range=[0, 100], fixedrange=True)
    fig.update_yaxes(visible=False, range=[0, 100], fixedrange=True)
    fig = apply_theme(fig, height=335)
    fig.update_layout(margin={"l": 0, "r": 0, "t": 4, "b": 4}, dragmode=False)
    return fig


def dumbbell(df, label_col: str, lang: str | None = "EN") -> go.Figure:
    chart = df.sort_values("score", ascending=True)
    fig = go.Figure()
    for _, row in chart.iterrows():
        fig.add_trace(
            go.Scatter(
                x=[row["count_current"], row["count_future"]],
                y=[row[label_col], row[label_col]],
                mode="lines",
                line={"color": COLORS["border"], "width": 2.4},
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
            "bgcolor": "rgba(255,253,250,0.92)",
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
    fig.update_xaxes(title_text=ft(lang, "age_group"), categoryorder="array", categoryarray=df["age_short"].tolist())
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
            "font": {"family": FONT_FAMILY, "size": 11, "color": COLORS["text"]},
            "itemsizing": "constant",
        },
        margin={"l": 8, "r": 28, "t": 42, "b": 40},
    )
    return fig


def circle_pack_positions(radii: list[float]) -> list[tuple[float, float]]:
    gap = -0.12
    positions: list[tuple[float, float]] = []
    for index, radius in enumerate(radii):
        if index == 0:
            positions.append((0.0, 0.0))
            continue

        best: tuple[float, float] | None = None
        best_distance = float("inf")
        max_extent = max([abs(x) + r for (x, _y), r in zip(positions, radii[:index], strict=False)] + [radius])
        for search_radius in np.linspace(radius, max_extent + radius * 5.8, 110):
            for angle in np.linspace(0, 2 * math.pi, 160, endpoint=False):
                x = math.cos(angle) * search_radius
                y = math.sin(angle) * search_radius
                overlaps = any(
                    math.hypot(x - px, y - py) < radius + previous_radius + gap
                    for (px, py), previous_radius in zip(positions, radii[:index], strict=False)
                )
                if overlaps:
                    continue
                distance = math.hypot(x, y)
                if distance < best_distance:
                    best = (x, y)
                    best_distance = distance
            if best is not None:
                break
        positions.append(best or (max_extent + radius, 0.0))
    return positions


def devtype_packed_bubbles(df, lang: str | None = "EN") -> go.Figure:
    chart = df.sort_values("count", ascending=False).reset_index(drop=True).copy()
    if chart.empty:
        return apply_theme(go.Figure(), height=430)

    chart["rank"] = np.arange(1, len(chart) + 1)
    max_count = max(float(chart["count"].max()), 1.0)
    bubble_scale = 1.88
    bubble_floor = 0.36
    radii = (np.sqrt(chart["count"] / max_count) * bubble_scale + bubble_floor).tolist()
    positions = circle_pack_positions(radii)
    colors = [DEVTYPE_COLORS[index % len(DEVTYPE_COLORS)] for index in range(len(chart))]

    fig = go.Figure()
    annotations = []
    for row, position, radius, color in zip(chart.itertuples(index=False), positions, radii, colors, strict=False):
        label = compact_devtype_group_label(row.devtype_group, lang)
        text_color = readable_text_color(color)
        roles_included = compact_roles_list(row.roles_included, int(row.role_count), lang)
        roles_line = f"{ft(lang, 'roles_included')}: {roles_included}<br>" if roles_included else ""
        fig.add_shape(
            type="circle",
            x0=position[0] - radius,
            y0=position[1] - radius,
            x1=position[0] + radius,
            y1=position[1] + radius,
            fillcolor=color,
            opacity=0.94,
            line={"color": color, "width": 0},
        )
        annotations.append(
            {
                "x": position[0],
                "y": position[1],
                "text": f"{int(row.rank)}",
                "showarrow": False,
                "xanchor": "center",
                "yanchor": "middle",
                "font": {"family": FONT_FAMILY, "size": 13, "color": text_color},
            }
        )
        fig.add_trace(
            go.Scatter(
                x=[position[0]],
                y=[position[1]],
                mode="markers",
                marker={
                    "size": max(radius * 76, 24),
                    "color": color,
                    "opacity": 0,
                    "line": {"width": 0},
                },
                customdata=[[label, row.count, row.share_pct, row.role_count, roles_line]],
                hovertemplate=(
                    "<b>%{customdata[0]}</b><br>"
                    f"{ft(lang, 'role_mentions')}: %{{customdata[1]:,.0f}}<br>"
                    f"{ft(lang, 'share_of_role_mentions')}: %{{customdata[2]:.1f}}%<br>"
                    f"{ft(lang, 'distinct_roles')}: %{{customdata[3]:,.0f}}<br>"
                    "%{customdata[4]}<extra></extra>"
                ),
                showlegend=False,
            )
        )
        fig.add_trace(
            go.Scatter(
                x=[None],
                y=[None],
                mode="markers",
                name=f"#{int(row.rank)} {compact_devtype_group_label(row.devtype_group, lang)}",
                marker={"size": 10, "color": color, "opacity": 1, "line": {"width": 0}},
                hoverinfo="skip",
                showlegend=True,
            )
        )
    extents = [
        value
        for (x, y), radius in zip(positions, radii, strict=False)
        for value in (x - radius, x + radius, y - radius, y + radius)
    ]
    min_x = min(x - radius for (x, _y), radius in zip(positions, radii, strict=False))
    max_x = max(x + radius for (x, _y), radius in zip(positions, radii, strict=False))
    min_y = min(y - radius for (_x, y), radius in zip(positions, radii, strict=False))
    max_y = max(y + radius for (_x, y), radius in zip(positions, radii, strict=False))
    pad = max((max(extents) - min(extents)) * 0.002, 0.04)
    x_center = (min_x + max_x) / 2
    y_center = (min_y + max_y) / 2
    x_half = (max_x - min_x) / 2 + pad
    y_half = (max_y - min_y) / 2 + pad
    zoom_factor = 0.84
    fig.update_xaxes(visible=False, range=[x_center - x_half * zoom_factor, x_center + x_half * zoom_factor], fixedrange=True)
    fig.update_yaxes(visible=False, range=[y_center - y_half * zoom_factor, y_center + y_half * zoom_factor], fixedrange=True, scaleanchor="x", scaleratio=1)
    fig = apply_theme(fig, height=410)
    fig.update_layout(
        annotations=annotations,
        margin={"l": 0, "r": 0, "t": 86, "b": 4},
        dragmode=False,
        legend={
            "orientation": "h",
            "x": 0,
            "xanchor": "left",
            "y": 1.24,
            "yanchor": "top",
            "bgcolor": "rgba(255,253,250,0)",
            "borderwidth": 0,
            "font": {"family": FONT_FAMILY, "size": 11, "color": COLORS["text"]},
            "itemsizing": "constant",
            "entrywidth": 0.33,
            "entrywidthmode": "fraction",
        },
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


def job_satisfaction_axis_range(values) -> tuple[float, float, float]:
    clean = np.asarray(values, dtype=float)
    clean = clean[np.isfinite(clean)]
    if clean.size == 0:
        return 6.0, 8.0, 0.5

    low = float(clean.min())
    high = float(clean.max())
    span = high - low
    minimum_span = 1.0
    target_span = max(span * 1.35, minimum_span)
    center = (low + high) / 2
    axis_low = max(0.0, center - target_span / 2)
    axis_high = min(10.0, center + target_span / 2)

    if axis_high - axis_low < minimum_span:
        if axis_low == 0.0:
            axis_high = min(10.0, axis_low + minimum_span)
        elif axis_high == 10.0:
            axis_low = max(0.0, axis_high - minimum_span)

    tick = 0.25 if axis_high - axis_low <= 1.5 else 0.5
    return round(axis_low, 2), round(axis_high, 2), tick


def job_satisfaction_lines(summary_df, lang: str | None = "EN") -> go.Figure:
    chart = summary_df.copy()
    fig = go.Figure()
    has_low_sample = bool(((chart["count"] > 0) & (chart["count"] < MIN_JOB_SAT_RECORDS)).any())
    for workstyle, color in WORKSTYLE_COLORS.items():
        series = chart[chart["workstyle"] == workstyle].copy()
        if series.empty:
            continue
        series["experience_hover"] = series["experience_band"].map(lambda value: experience_label(str(value), lang))
        reliable = series[series["count"] >= MIN_JOB_SAT_RECORDS]
        low_sample = series[(series["count"] > 0) & (series["count"] < MIN_JOB_SAT_RECORDS)]
        if reliable.empty and low_sample.empty:
            continue
        if not reliable.empty:
            fig.add_trace(
                go.Scatter(
                    x=reliable["experience_short"],
                    y=reliable["mean"],
                    mode="lines+markers",
                    name=workstyle,
                    line={"color": color, "width": 3, "dash": WORKSTYLE_LINE_STYLES.get(workstyle, "solid")},
                    marker={"size": 9, "color": color, "line": {"color": COLORS["surface"], "width": 1.8}},
                    customdata=reliable[["experience_hover", "count"]],
                    hovertemplate=(
                        "<b>%{fullData.name}</b><br>"
                        "%{customdata[0]}<br>"
                        f"{ft(lang, 'average_job_sat')}: %{{y:.1f}}<br>"
                        f"{ft(lang, 'records')}: %{{customdata[1]:,.0f}}<extra></extra>"
                    ),
                )
            )
        if not low_sample.empty:
            fig.add_trace(
                go.Scatter(
                    x=low_sample["experience_short"],
                    y=low_sample["mean"],
                    mode="markers",
                    name=f"{workstyle} low sample",
                    marker={
                        "size": 14,
                        "color": "rgba(255,255,255,0)",
                        "line": {"color": color, "width": 2.2},
                        "symbol": "circle-open",
                    },
                    customdata=low_sample[["experience_hover", "count"]],
                    hovertemplate=(
                        f"<b>{workstyle} low sample</b><br>"
                        "%{customdata[0]}<br>"
                        f"{ft(lang, 'average_job_sat')}: %{{y:.1f}}<br>"
                        f"{ft(lang, 'records')}: %{{customdata[1]:,.0f}}<extra></extra>"
                    ),
                    showlegend=False,
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=low_sample["experience_short"],
                    y=low_sample["mean"],
                    mode="markers",
                    name=f"{workstyle} low sample center",
                    marker={
                        "size": 7,
                        "color": color,
                        "line": {"width": 0},
                        "symbol": "x",
                    },
                    hoverinfo="skip",
                    showlegend=False,
                )
            )
    if has_low_sample:
        fig.add_trace(
            go.Scatter(
                x=[None],
                y=[None],
                mode="markers",
                name="Low sample" if lang != "ES" else "Baja muestra",
                marker={
                    "size": 9,
                    "color": COLORS["muted"],
                    "line": {"width": 0},
                    "symbol": "x",
                },
                hoverinfo="skip",
                showlegend=True,
            )
        )
    fig.update_xaxes(title_text=ft(lang, "years_experience"), categoryorder="array", categoryarray=[band.replace(" years", "") for band in data.EXPERIENCE_BAND_ORDER])
    reliable_values = chart.loc[chart["count"] >= MIN_JOB_SAT_RECORDS, "mean"]
    axis_low, axis_high, axis_tick = job_satisfaction_axis_range(reliable_values)
    fig.update_yaxes(title_text=ft(lang, "average_job_sat"), range=[axis_low, axis_high], dtick=axis_tick)
    fig.update_layout(
        hovermode="x unified",
        legend={
            "orientation": "h",
            "x": 1,
            "xanchor": "right",
            "y": 1.08,
            "yanchor": "bottom",
            "bgcolor": "rgba(255,253,250,0.92)",
            "bordercolor": COLORS["border"],
            "borderwidth": 1,
        }
    )
    fig = apply_theme(fig, height=380)
    fig.update_layout(margin={"l": 8, "r": 28, "t": 26, "b": 42})
    return fig


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
                    [0.00, "#f2ddb1"],
                    [0.08, "#e2b778"],
                    [0.20, COLORS["accent"]],
                    [0.45, "#927f68"],
                    [0.70, "#598177"],
                    [1.00, COLORS["primary_deep"]],
                ],
                "line": {"color": COLORS["text"], "width": 1},
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
        landcolor="#e1e8e2",
        showcountries=True,
        countrycolor="#ffffff",
        showocean=True,
        oceancolor="#f7f8f5",
        showframe=False,
        lataxis_showgrid=False,
        lonaxis_showgrid=False,
    )
    fig.update_layout(margin={"l": 0, "r": 0, "t": 0, "b": 0})
    fig = apply_theme(fig, height=450)
    fig.update_layout(autosize=True)
    return fig
