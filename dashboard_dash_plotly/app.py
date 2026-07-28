from __future__ import annotations

from dash import Dash, Input, Output, State, callback_context, dcc, html

from dashboard_dash_plotly import data, figures


FULL_DF = data.load_dataset()
TECH_TOP_N = 10

app = Dash(__name__, suppress_callback_exceptions=True, title="Stack Overflow Developer Survey Dashboard")
server = app.server

TECH_FAMILIES = list(data.TECH_FAMILIES)
VIEW_IDS = [
    "languages",
    "databases",
    "platforms",
    "frameworks",
    "age-context",
    "compensation",
    "country-distribution",
]
TECH_COPY = {
    "current_tooltip": f"Shows the {TECH_TOP_N} most mentioned technologies currently used in this family under the active filters.",
    "future_tooltip": f"Shows the {TECH_TOP_N} most mentioned technologies respondents want to use next in this family under the active filters.",
    "momentum_tooltip": (
        f"Compares current use and future interest for the {TECH_TOP_N} technologies that appear most often in either the current or future ranking. "
        "It prioritizes overall visibility, not the technologies with the biggest increase or decrease."
    ),
}
SECTION_COPY = {
    "age_context": "Profile the respondent mix by age and education under the active filters.",
    "compensation": "Compare observed compensation ranges across experience bands and workstyles.",
    "country": "Explore geographic concentration. The local slider controls how many ranked countries appear on the map.",
}
CHART_TOOLTIPS = {
    "age_distribution": "Respondent distribution by age group.",
    "education_composition": "Education mix by age group, normalized to 100%.",
    "remote_compensation": "Remote compensation ranges by experience band.",
    "hybrid_compensation": "Hybrid compensation ranges by experience band.",
    "inperson_compensation": "In-person compensation ranges by experience band.",
}

I18N = {
    "EN": {
        "dashboard_title": "Developer Technology Trends Dashboard",
        "about": "About",
        "about_title": "Dash and Plotly dashboard using the cleaned Stack Overflow survey dataset.",
        "about_modal_title": "About this dashboard",
        "about_close": "Close",
        "about_sections": [
            (
                "Dashboard purpose",
                "This portfolio project analyzes developer technology adoption, future interest, respondent context, and compensation patterns to turn a large public survey into an explorable product-style dashboard.",
            ),
            (
                "Dataset origin",
                "The analysis uses a curated subset of the public Stack Overflow Developer Survey 2024 dataset. Stack Overflow reports 65,437 responses from 185 countries in the original survey; this project uses 18,845 records as its input. Source: https://survey.stackoverflow.co/2024/",
            ),
            (
                "Dashboard scope",
                "The dashboard uses the cleaned, normalized, and reduced survey dataset. Age and workstyle are global filters; technology rankings show the top 10 items per family; dumbbell charts compare high-visibility technologies across current use and future interest; and the map has its own country-count slider.",
            ),
            (
                "Tools",
                "Built with Python, pandas, NumPy, Jupyter notebooks, Dash, Plotly, HTML/CSS, and Git.",
            ),
        ],
        "global_filters": "Global filters",
        "filter_help": "Age and workstyle define the active respondent view.",
        "age": "Age",
        "workstyle": "Workstyle",
        "all_age_groups": "All age groups",
        "all_workstyles": "All workstyles",
        "reset_filters": "Reset filters",
        "navigation": "Navigation",
        "open_navigation": "Open navigation",
        "collapse_navigation": "Collapse navigation",
        "comparison_group": "Comparison and Momentum",
        "context_group": "Respondent Context",
        "respondents": "Respondents",
        "countries": "Countries",
        "average_compensation": "Average Compensation",
        "dataset_total": "Dataset total",
        "active_filters": "Active filters",
        "shown_on_map": "Active filters",
        "observed_records": "Observed records",
        "dataset_average": "Dataset average",
        "top_current": "Top Current {family}",
        "top_future": "Top Future {family}",
        "momentum": "Current vs Future {family} Momentum",
        "age_context": "Age and Education",
        "age_context_text": SECTION_COPY["age_context"],
        "age_distribution": "Age Distribution",
        "education_composition": "Education Level Composition by Age Group",
        "compensation": "Compensation by Experience",
        "compensation_text": SECTION_COPY["compensation"],
        "remote_compensation": "Remote Compensation",
        "hybrid_compensation": "Hybrid Compensation",
        "inperson_compensation": "In-person Compensation",
        "country_distribution": "Country Distribution",
        "country_text": SECTION_COPY["country"],
        "countries_shown": "Countries shown",
        "map_title": "Respondent Map by Country",
        "language": "Language",
        "families": {
            "Languages": "Languages",
            "Databases": "Databases",
            "Platforms": "Platforms",
            "Frameworks": "Frameworks",
        },
        "family_descriptions": {
            "Languages": "Programming, scripting, and markup languages developers use to build software.",
            "Databases": "Database engines and persistence tools used to store and query application data.",
            "Platforms": "Cloud, operating, and deployment platforms where developers run workloads.",
            "Frameworks": "Web frameworks developers use to build user-facing and backend applications.",
        },
        "tooltips": CHART_TOOLTIPS | TECH_COPY,
    },
    "ES": {
        "dashboard_title": "Dashboard de Tendencias Tecnológicas",
        "about": "Acerca de",
        "about_title": "Dashboard creado con Dash y Plotly a partir del dataset limpio de la encuesta de Stack Overflow.",
        "about_modal_title": "Acerca de este dashboard",
        "about_close": "Cerrar",
        "about_sections": [
            (
                "Propósito del dashboard",
                "Este proyecto de portafolio analiza adopción tecnológica, interés futuro, contexto de los encuestados y patrones de compensación para convertir una encuesta pública amplia en un dashboard exploratorio con enfoque de producto.",
            ),
            (
                "Origen del dataset",
                "El análisis usa un subconjunto curado del dataset público Stack Overflow Developer Survey 2024. Stack Overflow reporta 65,437 respuestas de 185 países en la encuesta original; este proyecto usa 18,845 registros como entrada. Fuente: https://survey.stackoverflow.co/2024/",
            ),
            (
                "Alcance del dashboard",
                "El dashboard usa el dataset limpio, normalizado y reducido. Edad y modalidad son filtros globales; los rankings tecnológicos muestran el Top 10 por familia; los gráficos dumbbell comparan tecnologías de alta visibilidad entre uso actual e interés futuro; y el mapa tiene su propio slider de cantidad de países.",
            ),
            (
                "Herramientas",
                "Construido con Python, pandas, NumPy, notebooks Jupyter, Dash, Plotly, HTML/CSS y Git.",
            ),
        ],
        "global_filters": "Filtros globales",
        "filter_help": "Edad y modalidad definen la vista activa de encuestados.",
        "age": "Edad",
        "workstyle": "Modalidad",
        "all_age_groups": "Todos los grupos de edad",
        "all_workstyles": "Todas las modalidades",
        "reset_filters": "Restablecer filtros",
        "navigation": "Navegación",
        "open_navigation": "Abrir navegación",
        "collapse_navigation": "Colapsar navegación",
        "comparison_group": "Comparación y momentum",
        "context_group": "Contexto de encuestados",
        "respondents": "Encuestados",
        "countries": "Países",
        "average_compensation": "Compensación promedio",
        "dataset_total": "Total del dataset",
        "active_filters": "Filtros activos",
        "shown_on_map": "Filtros activos",
        "observed_records": "Registros observados",
        "dataset_average": "Promedio del dataset",
        "top_current": "Top actual: {family}",
        "top_future": "Top futuro: {family}",
        "momentum": "Momentum actual vs futuro: {family}",
        "age_context": "Edad y educación",
        "age_context_text": "Perfila la composición de encuestados por edad y educación bajo los filtros activos.",
        "age_distribution": "Distribución por edad",
        "education_composition": "Composición educativa por grupo de edad",
        "compensation": "Compensación por experiencia",
        "compensation_text": "Compara los rangos de compensación observada por experiencia y modalidad de trabajo.",
        "remote_compensation": "Compensación remota",
        "hybrid_compensation": "Compensación híbrida",
        "inperson_compensation": "Compensación presencial",
        "country_distribution": "Distribución por país",
        "country_text": "Explora la concentración geográfica. El slider local controla cuántos países aparecen en el mapa.",
        "countries_shown": "Países mostrados",
        "map_title": "Mapa de encuestados por país",
        "language": "Idioma",
        "families": {
            "Languages": "Lenguajes",
            "Databases": "Bases de datos",
            "Platforms": "Plataformas",
            "Frameworks": "Frameworks",
        },
        "family_descriptions": {
            "Languages": "Lenguajes de programación, scripting y markup usados para construir software.",
            "Databases": "Motores de bases de datos y herramientas de persistencia para almacenar y consultar datos.",
            "Platforms": "Plataformas cloud, operativas y de despliegue donde se ejecutan cargas de trabajo.",
            "Frameworks": "Frameworks web usados para crear aplicaciones de usuario y servicios backend.",
        },
        "tooltips": {
            "current_tooltip": f"Muestra las {TECH_TOP_N} tecnologías más mencionadas en uso actual para esta familia bajo los filtros activos.",
            "future_tooltip": f"Muestra las {TECH_TOP_N} tecnologías más mencionadas que los encuestados quieren usar después para esta familia bajo los filtros activos.",
            "momentum_tooltip": (
                f"Compara uso actual e interés futuro para las {TECH_TOP_N} tecnologías que aparecen con más frecuencia en el ranking actual o futuro. "
                "Prioriza visibilidad general, no las tecnologías con mayor subida o caída."
            ),
            "age_distribution": "Distribución de encuestados por grupo de edad.",
            "education_composition": "Composición educativa por edad, normalizada a 100%.",
            "remote_compensation": "Rangos de compensación remota por experiencia.",
            "hybrid_compensation": "Rangos de compensación híbrida por experiencia.",
            "inperson_compensation": "Rangos de compensación presencial por experiencia.",
        },
    },
}


def normalize_lang(lang: str | None) -> str:
    return lang if lang in I18N else "EN"


def text(lang: str | None, key: str):
    return I18N[normalize_lang(lang)][key]


def family_label(family: str, lang: str | None) -> str:
    return text(lang, "families")[family]


def age_options(lang: str | None) -> list[dict]:
    undeclared = "Undeclared" if normalize_lang(lang) == "EN" else "No declarado"
    return [
        {"label": (undeclared if value == "Prefer not to say" else data.AGE_SHORT_LABELS[value]), "value": value}
        for value in data.AGE_ORDER
    ]


def workstyle_options(lang: str | None) -> list[dict]:
    labels = {
        "Remote": "Remote" if normalize_lang(lang) == "EN" else "Remoto",
        "Hybrid (some remote, some in-person)": "Hybrid" if normalize_lang(lang) == "EN" else "Híbrido",
        "In-person": "In-person" if normalize_lang(lang) == "EN" else "Presencial",
    }
    return [{"label": labels[value], "value": value} for value in data.REMOTE_WORK_LABELS]


def info_icon(content: str, icon_id: str | None = None) -> html.Span:
    return html.Span("i", id=icon_id, title=content, className="info-icon")


def about_modal_body(lang: str | None) -> list[html.Div]:
    return [
        html.Div(
            [
                html.H3(title),
                html.P(description),
            ],
            className="about-section",
        )
        for title, description in text(lang, "about_sections")
    ]


def kpi_card(title: str, total: str, total_label: str, filtered: str, filtered_label: str) -> html.Div:
    return html.Div(
        [
            html.Div(title, className="kpi-title"),
            html.Div(
                [
                    html.Div([html.Div(total, className="kpi-value"), html.Div(total_label, className="kpi-caption")]),
                    html.Div(
                        [html.Div(filtered, className="kpi-value filtered"), html.Div(filtered_label, className="kpi-caption")],
                        className="kpi-filtered",
                    ),
                ],
                className="kpi-body",
            ),
        ],
        className="kpi-card",
    )


def chart_card(title: str, tooltip: str, graph_id: str) -> html.Div:
    graph_config = {"displaylogo": False}
    card_class = "chart-card map-card" if graph_id == "country-map" else "chart-card"
    graph_class = "chart-graph map-graph" if graph_id == "country-map" else "chart-graph"
    if graph_id == "country-map":
        graph_config["responsive"] = True
    title_row = [html.H3(title, id=f"{graph_id}-title")]
    if graph_id != "country-map":
        title_row.append(info_icon(tooltip, icon_id=f"{graph_id}-info"))
    return html.Div(
        [
            html.Div(
                title_row,
                className="chart-title-row",
            ),
            dcc.Graph(id=graph_id, config=graph_config, className=graph_class),
        ],
        className=card_class,
    )


def technology_section(family: str) -> html.Section:
    slug = family.lower()
    return html.Section(
        [
            html.Div(
                [
                    html.H2(family, id=f"{slug}-section-title"),
                    html.P(data.TECH_FAMILIES[family]["description"], id=f"{slug}-section-copy"),
                ],
                className="section-heading",
            ),
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
    return html.Button("", id=f"nav-{view_id}", className="nav-button")


def nav_rail_icon(view_id: str) -> html.Span:
    return html.Span(className=f"nav-rail-icon nav-rail-icon-{view_id}")


def nav_rail_button(view_id: str) -> html.Button:
    return html.Button(nav_rail_icon(view_id), id=f"nav-rail-{view_id}", className="nav-rail-button")



def country_slider_marks(max_countries: int):
    return None


def clamp_country_count(value, max_countries: int) -> int:
    max_value = max(int(max_countries or 1), 1)
    try:
        numeric_value = int(value)
    except (TypeError, ValueError):
        numeric_value = max_value
    return min(max(numeric_value, 1), max_value)


def layout() -> html.Div:
    return html.Div(
        [
            dcc.Store(id="active-view", data="languages"),
            dcc.Store(id="nav-open", data=True),
            html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H2("About this dashboard", id="about-modal-title"),
                                    html.Button("Close", id="about-close", className="about-close-button", title="Close"),
                                ],
                                className="about-modal-header",
                            ),
                            html.Div(id="about-modal-body", className="about-modal-body"),
                        ],
                        className="about-modal-card",
                    )
                ],
                id="about-modal",
                className="about-modal hidden",
            ),
            html.Header(
                [
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H1("Developer Technology Trends Dashboard", id="dashboard-title"),
                                    html.Div(
                                        [
                                            html.Button(
                                                "About",
                                                id="about-button",
                                                title="Dash and Plotly dashboard using the cleaned Stack Overflow survey dataset.",
                                                className="about-button",
                                            ),
                                            html.Button(
                                                "EN",
                                                id="language-selector",
                                                value="EN",
                                                title="Toggle language",
                                                className="language-toggle",
                                            ),
                                        ],
                                        className="header-actions",
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
                                    html.Span("Global filters", id="filter-title", className="filter-title"),
                                    html.Span("Age and workstyle define the active respondent view.", id="filter-help", className="filter-help"),
                                ],
                                className="filter-title-row",
                            ),
                            html.Div(
                                [
                                    html.Label("Age", id="age-filter-label"),
                                    dcc.Dropdown(
                                        id="age-filter",
                                        options=age_options("EN"),
                                        value=[],
                                        multi=True,
                                        placeholder="All age groups",
                                        searchable=False,
                                        className="filter-dropdown",
                                    ),
                                    html.Label("Workstyle", id="workstyle-filter-label"),
                                    dcc.Dropdown(
                                        id="workstyle-filter",
                                        options=workstyle_options("EN"),
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
            html.Div(
                [
                    html.Nav(
                        [
                            html.Div(
                                [
                                    html.Div("Navigation", id="side-nav-title", className="side-nav-title"),
                                    html.Button("<", id="nav-collapse", className="nav-toggle", title="Collapse navigation"),
                                ],
                                className="side-nav-header",
                            ),
                            html.Div("Comparison and Momentum", id="comparison-nav-title", className="nav-group-title"),
                            nav_button("languages"),
                            nav_button("databases"),
                            nav_button("platforms"),
                            nav_button("frameworks"),
                            html.Div("Respondent Context", id="context-nav-title", className="nav-group-title"),
                            nav_button("age-context"),
                            nav_button("compensation"),
                            nav_button("country-distribution"),
                        ],
                        id="side-nav",
                        className="side-nav",
                    ),
                    html.Nav(
                        [
                            html.Button(">", id="nav-expand", className="nav-rail-toggle", title="Open navigation"),
                            *[nav_rail_button(view_id) for view_id in VIEW_IDS[:4]],
                            html.Div(className="nav-rail-divider"),
                            *[nav_rail_button(view_id) for view_id in VIEW_IDS[4:]],
                        ],
                        id="nav-rail",
                        className="nav-rail hidden",
                    ),
                    html.Main(
                        [
                            html.Div(id="kpi-row", className="kpi-grid"),
                            technology_section("Languages"),
                            technology_section("Databases"),
                            technology_section("Platforms"),
                            technology_section("Frameworks"),
                            html.Section(
                                [
                                    html.Div(
                                        [
                                            html.H2("Age and Education", id="age-context-title"),
                                            html.P(SECTION_COPY["age_context"], id="age-context-copy"),
                                        ],
                                        className="section-heading",
                                    ),
                                    html.Div(
                                        [
                                            chart_card("Age Distribution", CHART_TOOLTIPS["age_distribution"], "age-distribution"),
                                            chart_card(
                                                "Education Level Composition by Age Group",
                                                CHART_TOOLTIPS["education_composition"],
                                                "education-composition",
                                            ),
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
                                    html.Div(
                                        [
                                            html.H2("Compensation by Experience", id="compensation-title"),
                                            html.P(SECTION_COPY["compensation"], id="compensation-copy"),
                                        ],
                                        className="section-heading",
                                    ),
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
                                    html.Div(
                                        [
                                            html.H2("Country Distribution", id="country-title"),
                                            html.P(SECTION_COPY["country"], id="country-copy"),
                                        ],
                                        className="section-heading",
                                    ),
                                    html.Div(
                                        [
                                            html.Div(
                                                [
                                                    html.Div(
                                                        [
                                                            html.H3("Respondent Map by Country", id="country-map-title"),
                                                        ],
                                                        className="chart-title-row",
                                                    ),
                                                    html.Div(
                                                        [
                                                            html.Div(
                                                                [
                                                                    html.Label("Countries shown", id="country-slider-label"),
                                                                    dcc.Input(
                                                                        id="country-count-input",
                                                                        type="number",
                                                                        min=1,
                                                                        max=160,
                                                                        value=160,
                                                                        step=1,
                                                                        debounce=True,
                                                                        className="country-count-input",
                                                                    ),
                                                                    dcc.Slider(
                                                                        id="country-slider",
                                                                        className="teal-slider vertical-country-slider",
                                                                        min=1,
                                                                        max=160,
                                                                        value=160,
                                                                        step=1,
                                                                        marks=country_slider_marks(160),
                                                                        vertical=True,
                                                                        verticalHeight=340,
                                                                    ),
                                                                ],
                                                                className="map-control map-control-vertical",
                                                            ),
                                                            dcc.Graph(
                                                                id="country-map",
                                                                config={"displaylogo": False, "responsive": True},
                                                                className="chart-graph map-graph",
                                                            ),
                                                        ],
                                                        className="map-panel-body",
                                                    ),
                                                ],
                                                className="chart-card map-card map-panel",
                                            ),
                                        ],
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
                id="body-shell",
                className="body-shell",
            ),
        ],
        className="app-shell",
    )


app.layout = layout


STATIC_TEXT_OUTPUTS = [
    Output("dashboard-title", "children"),
    Output("about-button", "children"),
    Output("about-button", "title"),
    Output("about-modal-title", "children"),
    Output("about-modal-body", "children"),
    Output("about-close", "children"),
    Output("about-close", "title"),
    Output("filter-title", "children"),
    Output("filter-help", "children"),
    Output("age-filter-label", "children"),
    Output("age-filter", "placeholder"),
    Output("age-filter", "options"),
    Output("workstyle-filter-label", "children"),
    Output("workstyle-filter", "placeholder"),
    Output("workstyle-filter", "options"),
    Output("reset-filters", "children"),
    Output("side-nav-title", "children"),
    Output("nav-collapse", "title"),
    Output("nav-expand", "title"),
    *[Output(f"nav-rail-{view_id}", "title") for view_id in VIEW_IDS],
    Output("comparison-nav-title", "children"),
    Output("context-nav-title", "children"),
    *[Output(f"nav-{view_id}", "children") for view_id in VIEW_IDS],
    *[Output(f"{family.lower()}-section-title", "children") for family in TECH_FAMILIES],
    *[Output(f"{family.lower()}-section-copy", "children") for family in TECH_FAMILIES],
    *[Output(f"{family.lower()}-current-title", "children") for family in TECH_FAMILIES],
    *[Output(f"{family.lower()}-current-info", "title") for family in TECH_FAMILIES],
    *[Output(f"{family.lower()}-future-title", "children") for family in TECH_FAMILIES],
    *[Output(f"{family.lower()}-future-info", "title") for family in TECH_FAMILIES],
    *[Output(f"{family.lower()}-momentum-title", "children") for family in TECH_FAMILIES],
    *[Output(f"{family.lower()}-momentum-info", "title") for family in TECH_FAMILIES],
    Output("age-context-title", "children"),
    Output("age-context-copy", "children"),
    Output("age-distribution-title", "children"),
    Output("age-distribution-info", "title"),
    Output("education-composition-title", "children"),
    Output("education-composition-info", "title"),
    Output("compensation-title", "children"),
    Output("compensation-copy", "children"),
    Output("remote-compensation-title", "children"),
    Output("remote-compensation-info", "title"),
    Output("hybrid-compensation-title", "children"),
    Output("hybrid-compensation-info", "title"),
    Output("inperson-compensation-title", "children"),
    Output("inperson-compensation-info", "title"),
    Output("country-title", "children"),
    Output("country-copy", "children"),
    Output("country-slider-label", "children"),
    Output("country-map-title", "children"),
]


@app.callback(*STATIC_TEXT_OUTPUTS, Input("language-selector", "value"))
def update_static_text(lang):
    lang = normalize_lang(lang)
    tooltips = text(lang, "tooltips")
    nav_labels = [
        family_label("Languages", lang),
        family_label("Databases", lang),
        family_label("Platforms", lang),
        family_label("Frameworks", lang),
        text(lang, "age_context"),
        text(lang, "compensation"),
        text(lang, "country_distribution"),
    ]
    section_titles = [family_label(family, lang) for family in TECH_FAMILIES]
    section_copy = [text(lang, "family_descriptions")[family] for family in TECH_FAMILIES]
    current_titles = [text(lang, "top_current").format(family=family_label(family, lang)) for family in TECH_FAMILIES]
    future_titles = [text(lang, "top_future").format(family=family_label(family, lang)) for family in TECH_FAMILIES]
    momentum_titles = [text(lang, "momentum").format(family=family_label(family, lang)) for family in TECH_FAMILIES]

    return (
        text(lang, "dashboard_title"),
        text(lang, "about"),
        text(lang, "about_title"),
        text(lang, "about_modal_title"),
        about_modal_body(lang),
        text(lang, "about_close"),
        text(lang, "about_close"),
        text(lang, "global_filters"),
        text(lang, "filter_help"),
        text(lang, "age"),
        text(lang, "all_age_groups"),
        age_options(lang),
        text(lang, "workstyle"),
        text(lang, "all_workstyles"),
        workstyle_options(lang),
        text(lang, "reset_filters"),
        text(lang, "navigation"),
        text(lang, "collapse_navigation"),
        text(lang, "open_navigation"),
        *nav_labels,
        text(lang, "comparison_group"),
        text(lang, "context_group"),
        *nav_labels,
        *section_titles,
        *section_copy,
        *current_titles,
        *[tooltips["current_tooltip"] for _ in TECH_FAMILIES],
        *future_titles,
        *[tooltips["future_tooltip"] for _ in TECH_FAMILIES],
        *momentum_titles,
        *[tooltips["momentum_tooltip"] for _ in TECH_FAMILIES],
        text(lang, "age_context"),
        text(lang, "age_context_text"),
        text(lang, "age_distribution"),
        tooltips["age_distribution"],
        text(lang, "education_composition"),
        tooltips["education_composition"],
        text(lang, "compensation"),
        text(lang, "compensation_text"),
        text(lang, "remote_compensation"),
        tooltips["remote_compensation"],
        text(lang, "hybrid_compensation"),
        tooltips["hybrid_compensation"],
        text(lang, "inperson_compensation"),
        tooltips["inperson_compensation"],
        text(lang, "country_distribution"),
        text(lang, "country_text"),
        text(lang, "countries_shown"),
        text(lang, "map_title"),
    )


@app.callback(
    Output("language-selector", "value"),
    Output("language-selector", "children"),
    Output("language-selector", "title"),
    Input("language-selector", "n_clicks"),
    State("language-selector", "value"),
)
def toggle_language(_clicks, current_lang):
    current_lang = normalize_lang(current_lang)
    if not _clicks:
        next_lang = current_lang
    else:
        next_lang = "ES" if current_lang == "EN" else "EN"
    return next_lang, next_lang, text(next_lang, "language")


@app.callback(
    Output("about-modal", "className"),
    Input("about-button", "n_clicks"),
    Input("about-close", "n_clicks"),
    State("about-modal", "className"),
    prevent_initial_call=True,
)
def toggle_about_modal(_open_clicks, _close_clicks, class_name):
    triggered = callback_context.triggered_id
    if triggered == "about-button":
        return "about-modal"
    if triggered == "about-close":
        return "about-modal hidden"
    return class_name or "about-modal hidden"


@app.callback(
    Output("active-view", "data"),
    *[Input(f"nav-{view_id}", "n_clicks") for view_id in VIEW_IDS],
    *[Input(f"nav-rail-{view_id}", "n_clicks") for view_id in VIEW_IDS],
    prevent_initial_call=True,
)
def set_active_view(*_):
    triggered = callback_context.triggered_id
    if not triggered:
        return "languages"
    return triggered.replace("nav-rail-", "").replace("nav-", "")


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
    Output("body-shell", "className"),
    Output("side-nav", "className"),
    Output("nav-rail", "className"),
    Output("content-shell", "className"),
    Input("nav-open", "data"),
)
def update_navigation_shell(is_open):
    return (
        "body-shell" if is_open else "body-shell nav-collapsed",
        "side-nav" if is_open else "side-nav collapsed",
        "nav-rail hidden" if is_open else "nav-rail",
        "content" if is_open else "content nav-collapsed",
    )


@app.callback(
    *[Output(view_id, "style") for view_id in VIEW_IDS],
    *[Output(f"nav-{view_id}", "className") for view_id in VIEW_IDS],
    *[Output(f"nav-rail-{view_id}", "className") for view_id in VIEW_IDS],
    Input("active-view", "data"),
)
def show_active_view(active_view):
    styles = [{"display": "block" if view_id == active_view else "none"} for view_id in VIEW_IDS]
    classes = ["nav-button active" if view_id == active_view else "nav-button" for view_id in VIEW_IDS]
    rail_classes = ["nav-rail-button active" if view_id == active_view else "nav-rail-button" for view_id in VIEW_IDS]
    return (*styles, *classes, *rail_classes)


@app.callback(
    Output("age-filter", "value"),
    Output("workstyle-filter", "value"),
    Input("reset-filters", "n_clicks"),
    prevent_initial_call=True,
)
def reset_filters(_):
    return [], []


@app.callback(
    Output("country-slider", "max"),
    Output("country-slider", "marks"),
    Output("country-slider", "value"),
    Output("country-count-input", "max"),
    Output("country-count-input", "value"),
    Input("age-filter", "value"),
    Input("workstyle-filter", "value"),
    Input("active-view", "data"),
)
def update_country_slider_bounds(selected_ages, selected_workstyles, _active_view):
    filtered = data.filter_dataset(FULL_DF, selected_ages, selected_workstyles)
    max_countries = max(len(data.country_map_distribution(filtered, None)), 1)
    return max_countries, country_slider_marks(max_countries), max_countries, max_countries, max_countries


@app.callback(
    Output("country-slider", "value", allow_duplicate=True),
    Output("country-count-input", "value", allow_duplicate=True),
    Input("country-slider", "value"),
    Input("country-count-input", "value"),
    State("country-slider", "max"),
    prevent_initial_call=True,
)
def sync_country_count_control(slider_value, input_value, max_countries):
    triggered_id = callback_context.triggered[0]["prop_id"].split(".")[0] if callback_context.triggered else "country-slider"
    raw_value = input_value if triggered_id == "country-count-input" else slider_value
    value = clamp_country_count(raw_value, max_countries)
    return value, value


@app.callback(
    *[Output(f"{family.lower()}-current", "figure") for family in TECH_FAMILIES],
    *[Output(f"{family.lower()}-future", "figure") for family in TECH_FAMILIES],
    *[Output(f"{family.lower()}-momentum", "figure") for family in TECH_FAMILIES],
    Output("age-distribution", "figure"),
    Output("education-composition", "figure"),
    Output("remote-compensation", "figure"),
    Output("hybrid-compensation", "figure"),
    Output("inperson-compensation", "figure"),
    Input("age-filter", "value"),
    Input("workstyle-filter", "value"),
    Input("language-selector", "value"),
)
def update_dashboard(selected_ages, selected_workstyles, lang):
    lang = normalize_lang(lang)
    filtered = data.filter_dataset(FULL_DF, selected_ages, selected_workstyles)

    current_figs = []
    future_figs = []
    momentum_figs = []
    for family, config in data.TECH_FAMILIES.items():
        color = figures.TECH_COLORS[family]
        current = data.top_multiselect_counts(filtered, config["current"], TECH_TOP_N, config["label"])
        future = data.top_multiselect_counts(filtered, config["future"], TECH_TOP_N, config["label"])
        comparison = data.comparison_table(filtered, config["current"], config["future"], TECH_TOP_N, config["label"])
        current_figs.append(figures.horizontal_bar(current, config["label"], color, lang))
        future_figs.append(figures.horizontal_bar(future, config["label"], color, lang))
        momentum_figs.append(figures.dumbbell(comparison, config["label"], lang))

    compensation = data.compensation_records(filtered)
    compensation_summary = data.compensation_box_summary(compensation)
    compensation_y_max = float(compensation_summary["upper"].max() * 1.1) if not compensation_summary.empty else 1.0
    age_distribution_fig = figures.age_bar(data.age_distribution(filtered), lang)
    education_fig = figures.education_stack(data.age_education_distribution(filtered), lang)
    remote_fig = figures.compensation_box(compensation_summary, "Remote", compensation_y_max, lang)
    hybrid_fig = figures.compensation_box(compensation_summary, "Hybrid", compensation_y_max, lang)
    inperson_fig = figures.compensation_box(compensation_summary, "In-person", compensation_y_max, lang)

    return (
        *current_figs,
        *future_figs,
        *momentum_figs,
        age_distribution_fig,
        education_fig,
        remote_fig,
        hybrid_fig,
        inperson_fig,
    )


@app.callback(
    Output("kpi-row", "children"),
    Output("country-map", "figure"),
    Input("age-filter", "value"),
    Input("workstyle-filter", "value"),
    Input("country-slider", "value"),
    Input("language-selector", "value"),
)
def update_map_context(selected_ages, selected_workstyles, country_count, lang):
    lang = normalize_lang(lang)
    filtered = data.filter_dataset(FULL_DF, selected_ages, selected_workstyles)
    available_countries = data.country_map_distribution(filtered, None)
    max_countries = max(len(available_countries), 1)
    countries_to_show = min(max(int(country_count or max_countries), 1), max_countries)
    country_df = data.country_map_distribution(filtered, countries_to_show)
    kpis = data.build_kpis(FULL_DF, filtered, len(country_df))

    kpi_cards = [
        kpi_card(
            text(lang, "respondents"),
            f"{kpis['respondents_total']:,}",
            text(lang, "dataset_total"),
            f"{kpis['respondents_filtered']:,}",
            text(lang, "active_filters"),
        ),
        kpi_card(
            text(lang, "countries"),
            f"{kpis['countries_total']:,}",
            text(lang, "dataset_total"),
            f"{kpis['countries_on_map']:,}",
            text(lang, "shown_on_map"),
        ),
        kpi_card(
            text(lang, "average_compensation"),
            f"${kpis['salary_total']:,.0f}",
            text(lang, "dataset_average"),
            f"${kpis['salary_filtered']:,.0f}",
            text(lang, "active_filters"),
        ),
    ]

    return kpi_cards, figures.country_map(country_df, lang)


if __name__ == "__main__":
    app.run(debug=True, port=8050)
