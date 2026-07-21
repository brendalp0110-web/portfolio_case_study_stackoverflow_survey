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
          font-size: 16px;
        }
        .bk-root h2 {
          font-size: 26px;
        }
        .bk-root h3 {
          font-size: 24px;
          margin: 8px 0 8px 0;
        }
        .bk-root h4 {
          font-size: 19px;
          margin: 4px 0 8px 0;
        }
        .bk-root p,
        .bk-root li {
          font-size: 16px;
          line-height: 1.55;
        }
        .bk-root .bk-input,
        .bk-root select,
        .bk-root label {
          font-size: 15px;
        }
        .bk-root .bk-btn {
          font-size: 14px;
        }
        .bk-root .bk-tab {
          font-size: 16px;
          padding: 12px 18px;
        }
        .bk-root .bk-tab button,
        .bk-root .bk-tab div {
          font-size: 16px;
        }
        .filter-sidebar {
          background: #ffffff;
          border: 1px solid #d9e2ec;
          border-radius: 10px;
          padding: 14px;
          font-size: 16px;
        }
        .filter-sidebar .bk-input,
        .filter-sidebar select,
        .filter-sidebar label {
          font-size: 15px;
        }
        .filter-sidebar .bk-btn {
          font-size: 14px;
        }
        .filter-sidebar h3 {
          font-size: 23px;
        }
        .filter-sidebar h4 {
          font-size: 19px;
        }
        .filter-sidebar p,
        .filter-sidebar li {
          font-size: 15px;
          line-height: 1.5;
        }
        .filter-rail {
          background: #ffffff;
          border: 1px solid #d9e2ec;
          border-radius: 10px;
          padding: 8px;
          position: relative;
          display: flex;
          align-items: center;
          justify-content: center;
          min-height: 58px;
        }
        .filter-rail:hover::after {
          content: "Open filters";
          position: absolute;
          left: 58px;
          top: 8px;
          z-index: 1000;
          background: #102a43;
          color: #ffffff;
          border-radius: 6px;
          padding: 8px 10px;
          font-size: 16px;
          font-weight: 700;
          white-space: nowrap;
          box-shadow: 0 6px 14px rgba(16, 42, 67, 0.18);
        }
        """
    ],
)

DATASET_PATH = PROJECT_ROOT / "data" / "survey_data_cleaned_reduced.csv"
BASE_DF = load_dataset(DATASET_PATH)
TOTAL_KPIS = build_kpis(BASE_DF)
REMOTE_OPTIONS = BASE_DF["RemoteWork"].value_counts().index.tolist()
METRIC_MODE = "Respondent count"
TEXT = {
    "EN": {
        "language": "Language",
        "dark_mode": "Dark mode",
        "dashboard_title": "Developer Technology Trends Dashboard",
        "dashboard_subtitle": "Interactive dashboard built with Panel and Bokeh from the cleaned and reduced Stack Overflow survey dataset.",
        "respondents": "Respondents",
        "countries": "Countries",
        "average_compensation": "Average compensation",
        "total_dataset": "Total dataset",
        "filtered_view": "Filtered view",
        "total_excluding_nomadic": "Total, excluding Nomadic",
        "shown_on_map": "Shown on map",
        "filters": "Filters",
        "reset_filters": "Reset filters",
        "filters_help": "Use each category to refine the dashboard. Reset buttons restore category defaults where available. The dashboard uses respondent counts as its fixed metric.",
        "top_n": "Top N",
        "top_n_help": "Choose the ranking depth used by technology rankings and Top N country filtering.",
        "top_5": "Top 5",
        "top_10": "Top 10",
        "top_12": "Top 12",
        "age": "Age",
        "age_help": "Limit the dashboard to selected age groups.",
        "workstyle": "Workstyle",
        "workstyle_help": "Include one or more workstyle categories.",
        "countries_help": "By default, the map is limited by the selected Top N countries.",
        "check_all": "Check All",
        "show_all_countries": "Show all countries",
        "apply_country_scope": "Apply country scope to full dashboard",
        "reset": "Reset",
        "momentum_tab": "Momentum and Comparison",
        "respondent_context_tab": "Respondent Context",
        "momentum_heading": "Momentum and Comparison",
        "momentum_text": "Explore which technologies developers rely on today and which ones are gaining future interest. Use this view to spot momentum, maturity, and possible shifts in demand.",
        "respondent_context_heading": "Respondent Context",
        "respondent_context_text": "Interpret the technology signals through respondent profile, compensation, and geography.",
        "age_education_tab": "Age and Education",
        "age_education_heading": "Age Profile and Education Composition",
        "age_education_text": "Understand who is represented in the survey and how education patterns vary across career stages.",
        "compensation_tab": "Compensation by Experience",
        "compensation_heading": "Compensation Distribution by Experience and Work Style",
        "compensation_text": "Compare how compensation ranges evolve with experience across remote, hybrid, and in-person work.",
        "country_tab": "Country Distribution",
        "country_heading": "Full Country Distribution Map",
        "country_text": "Locate where the respondent base is concentrated and how geography changes with the active filters.",
        "nomadic_respondents": "Nomadic respondents",
        "not_plotted_country": "respondents, not plotted as a country",
        "languages_context": "Programming, scripting, and markup languages developers use to build software.",
        "databases_context": "Data storage and query technologies that support application and analytics work.",
        "platforms_context": "Cloud, hosting, and deployment platforms shaping where software runs.",
        "frameworks_context": "Web frameworks and libraries developers use to build user-facing applications.",
        "top_current_languages": "Top Current Languages",
        "top_future_languages": "Top Future Languages",
        "top_current_databases": "Top Current Databases",
        "top_future_databases": "Top Future Databases",
        "top_current_platforms": "Top Current Platforms",
        "top_future_platforms": "Top Future Platforms",
        "top_current_frameworks": "Top Current Web Frameworks",
        "top_future_frameworks": "Top Future Web Frameworks",
        "current_future_momentum": "Current vs Future {family} Momentum",
        "respondent_map": "Respondent Distribution by Country",
        "age_distribution_chart": "Respondent Age Distribution",
        "education_age_chart": "Education Level Composition by Age Group",
        "compensation_experience_chart": "{workstyle} Compensation by Experience",
        "respondent_count_axis": "Respondent count",
        "share_respondents_axis": "Share of respondents (%)",
        "country": "Country",
        "count": "Count",
        "share_filtered_respondents": "Share of filtered respondents",
        "share_filtered_country": "Share of filtered country respondents",
        "current": "Current",
        "future": "Future",
        "current_count": "Current count",
        "future_count": "Future count",
        "current_share": "Current share of filtered respondents",
        "future_share": "Future share of filtered respondents",
        "delta_share": "Delta share of filtered respondents",
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
        "language_label": "Language",
        "database_label": "Database",
        "platform_label": "Platform",
        "framework_label": "Web framework",
    },
    "ES": {
        "language": "Idioma",
        "dark_mode": "Modo oscuro",
        "dashboard_title": "Dashboard de Tendencias Tecnologicas",
        "dashboard_subtitle": "Dashboard interactivo creado con Panel y Bokeh a partir del dataset limpio y reducido de la encuesta de Stack Overflow.",
        "respondents": "Respondientes",
        "countries": "Paises",
        "average_compensation": "Compensacion promedio",
        "total_dataset": "Dataset total",
        "filtered_view": "Vista filtrada",
        "total_excluding_nomadic": "Total, excluye Nomadic",
        "shown_on_map": "Mostrados en mapa",
        "filters": "Filtros",
        "reset_filters": "Reiniciar filtros",
        "filters_help": "Usa cada categoria para refinar el dashboard. Los botones de reset restauran los valores por defecto. La metrica fija es conteo de respondientes.",
        "top_n": "Top N",
        "top_n_help": "Define la profundidad del ranking para tecnologias y para el filtro Top N de paises.",
        "top_5": "Top 5",
        "top_10": "Top 10",
        "top_12": "Top 12",
        "age": "Edad",
        "age_help": "Limita el dashboard a los grupos etareos seleccionados.",
        "workstyle": "Modalidad",
        "workstyle_help": "Incluye una o mas modalidades de trabajo.",
        "countries_help": "Por defecto, el mapa se limita a los paises del Top N seleccionado.",
        "check_all": "Seleccionar todo",
        "show_all_countries": "Mostrar todos los paises",
        "apply_country_scope": "Aplicar alcance de paises a todo el dashboard",
        "reset": "Reset",
        "momentum_tab": "Momentum y Comparacion",
        "respondent_context_tab": "Contexto de Respondientes",
        "momentum_heading": "Momentum y Comparacion",
        "momentum_text": "Explora que tecnologias usan hoy los desarrolladores y cuales ganan interes futuro. Esta vista ayuda a detectar momentum, madurez y posibles cambios de demanda.",
        "respondent_context_heading": "Contexto de Respondientes",
        "respondent_context_text": "Interpreta las senales tecnologicas a traves del perfil, la compensacion y la geografia de los respondientes.",
        "age_education_tab": "Edad y Educacion",
        "age_education_heading": "Perfil Etareo y Composicion Educativa",
        "age_education_text": "Entiende quien esta representado en la encuesta y como cambian los patrones educativos a traves de etapas de carrera.",
        "compensation_tab": "Compensacion por Experiencia",
        "compensation_heading": "Distribucion de Compensacion por Experiencia y Modalidad",
        "compensation_text": "Compara como evolucionan los rangos de compensacion con la experiencia en trabajo remoto, hibrido y presencial.",
        "country_tab": "Distribucion por Pais",
        "country_heading": "Mapa de Distribucion por Pais",
        "country_text": "Ubica donde se concentra la base de respondientes y como cambia la geografia con los filtros activos.",
        "nomadic_respondents": "Respondientes nomadicos",
        "not_plotted_country": "respondientes, no graficados como pais",
        "languages_context": "Lenguajes de programacion, scripting y marcado usados para construir software.",
        "databases_context": "Tecnologias de almacenamiento y consulta que sostienen aplicaciones y analitica.",
        "platforms_context": "Plataformas cloud, hosting y despliegue que definen donde corre el software.",
        "frameworks_context": "Frameworks y librerias web usados para construir aplicaciones orientadas al usuario.",
        "top_current_languages": "Lenguajes Mas Usados Actualmente",
        "top_future_languages": "Lenguajes con Mayor Interes Futuro",
        "top_current_databases": "Bases de Datos Mas Usadas Actualmente",
        "top_future_databases": "Bases de Datos con Mayor Interes Futuro",
        "top_current_platforms": "Plataformas Mas Usadas Actualmente",
        "top_future_platforms": "Plataformas con Mayor Interes Futuro",
        "top_current_frameworks": "Frameworks Web Mas Usados Actualmente",
        "top_future_frameworks": "Frameworks Web con Mayor Interes Futuro",
        "current_future_momentum": "Momentum Actual vs Futuro en {family}",
        "respondent_map": "Distribucion de Respondientes por Pais",
        "age_distribution_chart": "Distribucion Etarea de Respondientes",
        "education_age_chart": "Composicion Educativa por Grupo Etareo",
        "compensation_experience_chart": "Compensacion {workstyle} por Experiencia",
        "respondent_count_axis": "Conteo de respondientes",
        "share_respondents_axis": "Porcentaje de respondientes (%)",
        "country": "Pais",
        "count": "Conteo",
        "share_filtered_respondents": "Porcentaje de respondientes filtrados",
        "share_filtered_country": "Porcentaje de respondientes filtrados por pais",
        "current": "Actual",
        "future": "Futuro",
        "current_count": "Conteo actual",
        "future_count": "Conteo futuro",
        "current_share": "Porcentaje actual de respondientes filtrados",
        "future_share": "Porcentaje futuro de respondientes filtrados",
        "delta_share": "Diferencia porcentual de respondientes filtrados",
        "age_group": "Grupo etareo",
        "education_level": "Nivel educativo",
        "share_within_age": "Porcentaje dentro del grupo etareo",
        "share_within_age_axis": "Porcentaje dentro del grupo etareo (%)",
        "years_experience": "Anos de experiencia",
        "converted_compensation": "Compensacion anual convertida",
        "work_style": "Modalidad",
        "experience_band": "Rango de experiencia",
        "median": "Mediana",
        "mean": "Promedio",
        "language_label": "Lenguaje",
        "database_label": "Base de datos",
        "platform_label": "Plataforma",
        "framework_label": "Framework web",
    },
}
THEMES = {
    "light": {
        "page_bg": "#ffffff",
        "header_bg": "#102a43",
        "header_text": "#ffffff",
        "surface": "#f5f7fb",
        "panel": "#ffffff",
        "border": "#d9e2ec",
        "text": "#102a43",
        "muted": "#627d98",
        "muted_soft": "#829ab1",
        "filtered_value": "#334e68",
        "rail_bg": "#ffffff",
        "tooltip_bg": "#102a43",
        "chart_bg": "#ffffff",
        "chart_grid": "#edf2f7",
        "chart_border": "#d9e2ec",
        "map_tile": "light",
    },
    "dark": {
        "page_bg": "#07111f",
        "header_bg": "#0f2a3f",
        "header_text": "#f7fbff",
        "surface": "#111d2e",
        "panel": "#0f1726",
        "border": "#2a3a50",
        "text": "#e5edf7",
        "muted": "#a8b6c8",
        "muted_soft": "#7f8da1",
        "filtered_value": "#d7e3f2",
        "rail_bg": "#101827",
        "tooltip_bg": "#d7e3f2",
        "chart_bg": "#0f1726",
        "chart_grid": "#223148",
        "chart_border": "#2a3a50",
        "map_tile": "dark",
    },
}
TAB_STYLESHEET = """
:host {
  font-size: 18px;
}
.bk-tab,
.bk-tab button,
.bk-tab div,
button,
[role="tab"] {
  font-size: 18px !important;
  line-height: 1.35 !important;
  padding: 12px 18px !important;
}
"""
FILTER_WIDGET_STYLESHEET = """
:host {
  font-size: 16px;
}
label,
.bk-input,
.bk-input-group,
.bk-checkbox-label,
.bk-label,
select,
button {
  font-size: 16px !important;
  line-height: 1.45 !important;
}
input[type="checkbox"] {
  transform: scale(1.06);
  margin-right: 8px;
}
"""
MOMENTUM_OPTIONS = {
    "Languages": {
        "current_column": "LanguageHaveWorkedWith",
        "future_column": "LanguageWantToWorkWith",
        "label": "language",
        "label_key": "language_label",
        "color_key": "languages",
        "current_title_key": "top_current_languages",
        "future_title_key": "top_future_languages",
    },
    "Databases": {
        "current_column": "DatabaseHaveWorkedWith",
        "future_column": "DatabaseWantToWorkWith",
        "label": "database",
        "label_key": "database_label",
        "color_key": "databases",
        "current_title_key": "top_current_databases",
        "future_title_key": "top_future_databases",
    },
    "Platforms": {
        "current_column": "PlatformHaveWorkedWith",
        "future_column": "PlatformWantToWorkWith",
        "label": "platform",
        "label_key": "platform_label",
        "color_key": "platforms",
        "current_title_key": "top_current_platforms",
        "future_title_key": "top_future_platforms",
    },
    "Frameworks": {
        "current_column": "WebframeHaveWorkedWith",
        "future_column": "WebframeWantToWorkWith",
        "label": "web_framework",
        "label_key": "framework_label",
        "color_key": "frameworks",
        "current_title_key": "top_current_frameworks",
        "future_title_key": "top_future_frameworks",
    },
}
TECHNOLOGY_CONTEXT_KEYS = {
    "Languages": "languages_context",
    "Databases": "databases_context",
    "Platforms": "platforms_context",
    "Frameworks": "frameworks_context",
}


age_check_all = pn.widgets.Checkbox(name="Check All", value=True, stylesheets=[FILTER_WIDGET_STYLESHEET])
age_filter = pn.widgets.CheckBoxGroup(
    name="Age groups",
    options=AGE_ORDER,
    value=AGE_ORDER,
    stylesheets=[FILTER_WIDGET_STYLESHEET],
)
age_reset_button = pn.widgets.Button(name="Reset", width=64, stylesheets=[FILTER_WIDGET_STYLESHEET])
remote_check_all = pn.widgets.Checkbox(name="Check All", value=True, stylesheets=[FILTER_WIDGET_STYLESHEET])
remote_filter = pn.widgets.CheckBoxGroup(
    name="Workstyle",
    options=REMOTE_OPTIONS,
    value=REMOTE_OPTIONS,
    stylesheets=[FILTER_WIDGET_STYLESHEET],
)
remote_reset_button = pn.widgets.Button(name="Reset", width=64, stylesheets=[FILTER_WIDGET_STYLESHEET])
country_show_all = pn.widgets.Checkbox(name="Show all countries", value=False, stylesheets=[FILTER_WIDGET_STYLESHEET])
country_apply_dashboard = pn.widgets.Checkbox(
    name="Apply country scope to full dashboard",
    value=False,
    stylesheets=[FILTER_WIDGET_STYLESHEET],
)
country_reset_button = pn.widgets.Button(name="Reset", width=64, stylesheets=[FILTER_WIDGET_STYLESHEET])
TOP_N_DEFAULT = 10
top_n_value = pn.widgets.IntInput(name="Top N value", value=TOP_N_DEFAULT)
top_n_5_checkbox = pn.widgets.Checkbox(name="Top 5", value=False, stylesheets=[FILTER_WIDGET_STYLESHEET])
top_n_10_checkbox = pn.widgets.Checkbox(name="Top 10", value=True, stylesheets=[FILTER_WIDGET_STYLESHEET])
top_n_12_checkbox = pn.widgets.Checkbox(name="Top 12", value=False, stylesheets=[FILTER_WIDGET_STYLESHEET])
top_n_reset_button = pn.widgets.Button(name="Reset", width=64, stylesheets=[FILTER_WIDGET_STYLESHEET])
language_selector = pn.widgets.RadioButtonGroup(
    name="Language",
    options=["EN", "ES"],
    value="EN",
    button_type="primary",
    width=112,
)
theme_toggle = pn.widgets.Toggle(
    name="Dark mode",
    value=False,
    button_type="default",
    width=120,
)
reset_button = pn.widgets.Button(
    name="Reset filters",
    button_type="primary",
    width=120,
    stylesheets=[FILTER_WIDGET_STYLESHEET],
)
filter_panel_open = pn.widgets.Toggle(value=False, visible=False)
filter_panel_collapse_button = pn.widgets.ButtonIcon(
    icon="chevrons-left",
    description="Collapse filters",
    width=34,
    height=34,
)
filter_panel_expand_button = pn.widgets.ButtonIcon(
    icon="filter",
    description="",
    width=42,
    height=42,
    margin=0,
    align="center",
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


def _lang() -> str:
    return language_selector.value


def _text(key: str, lang: str | None = None) -> str:
    selected_lang = lang or _lang()
    return TEXT[selected_lang][key]


def _theme_name(is_dark: bool | None = None) -> str:
    dark = theme_toggle.value if is_dark is None else is_dark
    return "dark" if dark else "light"


def _theme(is_dark: bool | None = None) -> dict:
    return THEMES[_theme_name(is_dark)]


def _chart_labels(lang: str, extra: dict | None = None) -> dict:
    keys = [
        "respondent_count_axis",
        "share_respondents_axis",
        "country",
        "count",
        "share_filtered_respondents",
        "share_filtered_country",
        "current",
        "future",
        "current_count",
        "future_count",
        "current_share",
        "future_share",
        "delta_share",
        "age_group",
        "education_level",
        "share_within_age",
        "share_within_age_axis",
        "years_experience",
        "converted_compensation",
        "work_style",
        "experience_band",
        "median",
        "mean",
    ]
    labels = {key: _text(key, lang) for key in keys}
    if extra:
        labels.update(extra)
    return labels


def _update_control_labels(event=None) -> None:
    lang = _lang()
    age_check_all.name = _text("check_all", lang)
    remote_check_all.name = _text("check_all", lang)
    country_show_all.name = _text("show_all_countries", lang)
    country_apply_dashboard.name = _text("apply_country_scope", lang)
    top_n_5_checkbox.name = _text("top_5", lang)
    top_n_10_checkbox.name = _text("top_10", lang)
    top_n_12_checkbox.name = _text("top_12", lang)
    for button in [age_reset_button, remote_reset_button, country_reset_button, top_n_reset_button]:
        button.name = _text("reset", lang)
    reset_button.name = _text("reset_filters", lang)
    language_selector.name = _text("language", lang)
    theme_toggle.name = _text("dark_mode", lang)
    filter_panel_collapse_button.description = "Collapse filters" if lang == "EN" else "Cerrar filtros"


language_selector.param.watch(_update_control_labels, "value")
_update_control_labels()


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


def _kpi_card(
    title: str,
    total_value: str,
    total_label: str,
    filtered_value: str,
    filtered_label: str,
    theme: dict,
) -> pn.pane.HTML:
    html = f"""
    <div style="background:{theme['surface']};border:1px solid {theme['border']};border-radius:8px;padding:14px 18px;height:112px;">
      <div style="font-size:13px;color:{theme['muted']};text-transform:uppercase;letter-spacing:0.06em;">{title}</div>
      <div style="display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);column-gap:18px;margin-top:8px;">
        <div style="min-width:0;">
          <div style="font-size:29px;font-weight:700;color:{theme['text']};line-height:1.05;">{total_value}</div>
          <div style="font-size:13px;color:{theme['muted']};line-height:1.35;margin-top:6px;">{total_label}</div>
        </div>
        <div style="min-width:0;border-left:2px solid {theme['border']};padding-left:18px;">
          <div style="font-size:23px;font-weight:700;color:{theme['filtered_value']};line-height:1.15;">{filtered_value}</div>
          <div style="font-size:13px;color:{theme['muted_soft']};line-height:1.35;margin-top:6px;">{filtered_label}</div>
        </div>
      </div>
    </div>
    """
    return pn.pane.HTML(html, sizing_mode="stretch_width")


def _grid_box(*items, ncols: int) -> pn.GridBox:
    return pn.GridBox(*items, ncols=ncols, sizing_mode="stretch_width")


def _info_markdown(text: str, theme: dict | None = None, **kwargs) -> pn.pane.Markdown:
    colors = theme or _theme()
    stylesheet = f"""
    :host {{
      color: {colors['text']};
      font-family: inherit;
      font-size: 18px;
      line-height: 1.62;
    }}
    h3 {{
      color: {colors['text']};
      font-size: 25px;
      margin: 10px 0 8px 0;
    }}
    p {{
      color: {colors['text']};
      font-size: 18px;
      line-height: 1.62;
    }}
    code {{
      color: inherit;
      font-family: inherit;
      font-size: 16px;
    }}
    """
    return pn.pane.Markdown(text, stylesheets=[stylesheet], **kwargs)


def _filter_markdown(text: str, theme: dict | None = None, **kwargs) -> pn.pane.Markdown:
    colors = theme or _theme()
    stylesheet = f"""
    :host {{
      color: {colors['text']};
      font-size: 16px;
      line-height: 1.55;
    }}
    h3 {{
      color: {colors['text']};
      font-size: 24px;
    }}
    h4 {{
      color: {colors['text']};
      font-size: 20px;
    }}
    p {{
      color: {colors['text']};
      font-size: 16px;
      line-height: 1.55;
    }}
    """
    return pn.pane.Markdown(text, stylesheets=[stylesheet], **kwargs)


def _technology_momentum_view(filter_key, top_n, selected_family, lang: str, theme: dict):
    value_col = "count"
    config = MOMENTUM_OPTIONS[selected_family]
    chart_labels = _chart_labels(lang, {config["label"]: _text(config["label_key"], lang)})
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
    context = _text(TECHNOLOGY_CONTEXT_KEYS[selected_family], lang)

    rankings_grid = _grid_box(
        make_horizontal_bar_chart(
            current_ranking,
            config["label"],
            value_col,
            _text(config["current_title_key"], lang),
            METRIC_MODE,
            color,
            labels=chart_labels,
            theme=theme,
        ),
        make_horizontal_bar_chart(
            future_ranking,
            config["label"],
            value_col,
            _text(config["future_title_key"], lang),
            METRIC_MODE,
            color,
            labels=chart_labels,
            theme=theme,
        ),
        ncols=2,
    )

    return pn.Column(
        _info_markdown(f"{context}", theme=theme, margin=(0, 0, 8, 0)),
        rankings_grid,
        make_dumbbell_chart(
            comparison,
            config["label"],
            "count_current",
            "count_future",
            _text("current_future_momentum", lang).format(family=selected_family),
            METRIC_MODE,
            labels=chart_labels,
            theme=theme,
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
    language_selector.param.value,
    theme_toggle.param.value,
)
def dashboard_kpis(
    show_all_countries,
    apply_country_scope,
    selected_ages,
    selected_remote,
    top_n,
    lang,
    is_dark,
):
    filter_key = _filter_key_from_filter_values(
        selected_ages,
        selected_remote,
        show_all_countries,
        apply_country_scope,
        top_n,
    )
    map_filter_key = _map_filter_key_from_filter_values(
        selected_ages,
        selected_remote,
        show_all_countries,
        top_n,
    )
    kpis = _cached_kpis(filter_key)
    countries_shown_on_map = _cached_country_map_distribution(map_filter_key, None)["country"].nunique()
    theme = _theme(is_dark)
    return _grid_box(
        _kpi_card(
            _text("respondents", lang),
            f"{TOTAL_KPIS['respondents']:,}",
            _text("total_dataset", lang),
            f"{kpis['respondents']:,}",
            _text("filtered_view", lang),
            theme,
        ),
        _kpi_card(
            _text("countries", lang),
            f"{TOTAL_KPIS['countries']:,}",
            _text("total_excluding_nomadic", lang),
            f"{countries_shown_on_map:,}",
            _text("shown_on_map", lang),
            theme,
        ),
        _kpi_card(
            _text("average_compensation", lang),
            f"${TOTAL_KPIS['average_salary']:,.0f}",
            _text("total_dataset", lang),
            f"${kpis['average_salary']:,.0f}",
            _text("filtered_view", lang),
            theme,
        ),
        ncols=3,
    )


def _technology_momentum_panel(selected_family):
    @pn.depends(
        country_show_all.param.value,
        country_apply_dashboard.param.value,
        age_filter.param.value,
        remote_filter.param.value,
        top_n_value.param.value,
        language_selector.param.value,
        theme_toggle.param.value,
    )
    def technology_view(
        show_all_countries,
        apply_country_scope,
        selected_ages,
        selected_remote,
        top_n,
        lang,
        is_dark,
    ):
        effective_top_n = _effective_top_n(top_n)
        filter_key = _filter_key_from_filter_values(
            selected_ages,
            selected_remote,
            show_all_countries,
            apply_country_scope,
            top_n,
        )
        return _technology_momentum_view(filter_key, effective_top_n, selected_family, lang, _theme(is_dark))

    return pn.panel(technology_view, sizing_mode="stretch_width")


def momentum_comparison():
    lang = _lang()
    theme = _theme()
    heading = _info_markdown(
            f"""
            ### {_text("momentum_heading", lang)}

            {_text("momentum_text", lang)}
            """,
            theme=theme,
    )
    technology_tabs = pn.Tabs(
        *[
            (family, _technology_momentum_panel(family))
            for family in MOMENTUM_OPTIONS
        ],
        sizing_mode="stretch_width",
        dynamic=True,
        stylesheets=[TAB_STYLESHEET],
    )
    return pn.Column(
        heading,
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

    heading = _info_markdown(
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
    lang = _lang()
    theme = _theme()
    filter_key = _filter_key_from_filter_values(
        selected_ages,
        selected_remote,
        show_all_countries,
        apply_country_scope,
        top_n,
    )
    age_profile = _cached_age_distribution(filter_key)
    age_education = _cached_age_education_distribution(filter_key)
    chart_labels = _chart_labels(lang)

    return pn.Column(
        _info_markdown(
            f"""
            ### {_text("age_education_heading", lang)}

            {_text("age_education_text", lang)}
            """,
            theme=theme,
        ),
        _grid_box(
            make_age_percent_bar_chart(
                age_profile,
                _text("age_distribution_chart", lang),
                METRIC_MODE,
                labels=chart_labels,
                theme=theme,
            ),
            make_percent_stacked_bar_chart(
                age_education,
                _text("education_age_chart", lang),
                labels=chart_labels,
                theme=theme,
            ),
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
    lang = _lang()
    theme = _theme()
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
    chart_labels = _chart_labels(lang)

    charts = []
    for remote_label in remote_labels:
        chart_data = salary_box[salary_box["remote_label"] == remote_label]
        if chart_data.empty:
            continue

        charts.append(
            make_compensation_experience_box_plot(
                chart_data,
                _text("compensation_experience_chart", lang).format(workstyle=remote_label),
                y_max,
                REMOTE_COLORS.get(remote_label, "#2f6690"),
                labels=chart_labels,
                theme=theme,
            )
        )

    return pn.Column(
        _info_markdown(
            f"""
            ### {_text("compensation_heading", lang)}

            {_text("compensation_text", lang)}
            """,
            theme=theme,
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
    lang = _lang()
    theme = _theme()
    filter_key = _map_filter_key_from_filter_values(
        selected_ages,
        selected_remote,
        show_all_countries,
        top_n,
    )
    nomadic_context_key = _filter_key(
        selected_ages,
        selected_remote,
        "All countries",
        top_n,
    )
    nomadic_context = _cached_filtered_df(*nomadic_context_key)
    map_data = _cached_country_map_distribution(filter_key, None)
    nomadic_count = int((nomadic_context["Country"] == "Nomadic").sum())
    nomadic_share = nomadic_count / max(len(nomadic_context), 1) * 100
    nomadic_share_label = "<0.1%" if 0 < nomadic_share < 0.1 else f"{nomadic_share:.1f}%"
    chart_labels = _chart_labels(lang)

    return pn.Column(
        _info_markdown(
            f"""
            ### {_text("country_heading", lang)}

            {_text("country_text", lang)}
            """,
            theme=theme,
        ),
        pn.pane.HTML(
            f"""
            <div style="display:inline-flex;align-items:center;gap:10px;background:{theme['surface']};border:1px solid {theme['border']};border-radius:8px;padding:10px 12px;color:{theme['filtered_value']};font-size:15px;margin:0 0 8px 0;">
              <span style="font-weight:700;color:{theme['text']};">{_text("nomadic_respondents", lang)}</span>
              <span>{nomadic_share_label}</span>
              <span style="color:{theme['muted_soft']};">({nomadic_count:,} {_text("not_plotted_country", lang)})</span>
            </div>
            """,
            sizing_mode="stretch_width",
        ),
        make_country_bubble_map(
            map_data,
            _text("respondent_map", lang),
            METRIC_MODE,
            height=640,
            labels=chart_labels,
            theme=theme,
        ),
        sizing_mode="stretch_width",
    )


def detailed_views() -> pn.Column:
    lang = _lang()
    theme = _theme()
    subtabs = pn.Tabs(
        (_text("age_education_tab", lang), pn.panel(detailed_age_education)),
        (_text("compensation_tab", lang), pn.panel(detailed_compensation_experience)),
        (_text("country_tab", lang), pn.panel(detailed_country_distribution)),
        sizing_mode="stretch_width",
        dynamic=True,
        stylesheets=[TAB_STYLESHEET],
    )
    return pn.Column(
        _info_markdown(
            f"""
            ### {_text("respondent_context_heading", lang)}

            {_text("respondent_context_text", lang)}
            """,
            theme=theme,
        ),
        subtabs,
        sizing_mode="stretch_width",
    )


def create_dashboard():
    def _filter_section(title: str, reset: pn.widgets.Button, help_text: str, *items) -> pn.Column:
        return pn.Column(
            pn.Row(
                _filter_markdown(f"#### {title}", margin=(0, 0, 0, 0)),
                pn.Spacer(width=10),
                reset,
                sizing_mode="stretch_width",
            ),
            _filter_markdown(help_text),
            *items,
            sizing_mode="stretch_width",
        )

    def _build_filter_accordion(lang: str) -> pn.Accordion:
        return pn.Accordion(
            (
                _text("top_n", lang),
                _filter_section(
                    _text("top_n", lang),
                    top_n_reset_button,
                    _text("top_n_help", lang),
                    top_n_5_checkbox,
                    top_n_10_checkbox,
                    top_n_12_checkbox,
                ),
            ),
            (
                _text("age", lang),
                _filter_section(
                    _text("age", lang),
                    age_reset_button,
                    _text("age_help", lang),
                    age_check_all,
                    age_filter,
                ),
            ),
            (
                _text("workstyle", lang),
                _filter_section(
                    _text("workstyle", lang),
                    remote_reset_button,
                    _text("workstyle_help", lang),
                    remote_check_all,
                    remote_filter,
                ),
            ),
            (
                _text("countries", lang),
                _filter_section(
                    _text("countries", lang),
                    country_reset_button,
                    _text("countries_help", lang),
                    country_show_all,
                    country_apply_dashboard,
                ),
            ),
            active=[0],
            sizing_mode="stretch_width",
            stylesheets=[FILTER_WIDGET_STYLESHEET],
        )

    def _open_filter_sidebar(lang: str, theme: dict) -> pn.Column:
        return pn.Column(
            pn.Row(
                _filter_markdown(f"### {_text('filters', lang)}", theme=theme, margin=(2, 8, 0, 0)),
                pn.Spacer(sizing_mode="stretch_width"),
                filter_panel_collapse_button,
                sizing_mode="stretch_width",
                margin=(0, 0, 4, 0),
            ),
            reset_button,
            _filter_markdown(_text("filters_help", lang), theme=theme, margin=(0, 0, 10, 0)),
            _build_filter_accordion(lang),
            css_classes=["filter-sidebar"],
            styles={
                "background": theme["panel"],
                "border": f"1px solid {theme['border']}",
                "color": theme["text"],
            },
            width=310,
            sizing_mode="fixed",
        )

    def _collapsed_filter_rail(theme: dict) -> pn.Column:
        return pn.Column(
            filter_panel_expand_button,
            css_classes=["filter-rail"],
            styles={
                "background": theme["rail_bg"],
                "border": f"1px solid {theme['border']}",
            },
            width=56,
            sizing_mode="fixed",
            align="start",
        )

    @pn.depends(language_selector.param.value, theme_toggle.param.value)
    def header(lang: str, is_dark: bool):
        theme = _theme(is_dark)
        return pn.Row(
            pn.pane.HTML(
                f"""
                <div>
                  <div style="font-size:28px;font-weight:700;margin-bottom:6px;">{_text('dashboard_title', lang)}</div>
                  <div style="font-size:15px;line-height:1.5;max-width:980px;">{_text('dashboard_subtitle', lang)}</div>
                </div>
                """,
                sizing_mode="stretch_width",
            ),
            pn.Row(
                pn.pane.HTML(
                    '<div style="font-size:24px;line-height:1;">&#127760;</div>',
                    width=28,
                    align="center",
                ),
                language_selector,
                theme_toggle,
                align="center",
                width=290,
            ),
            styles={
                "background": theme["header_bg"],
                "color": theme["header_text"],
                "padding": "18px 22px",
                "border-radius": "10px",
            },
            sizing_mode="stretch_width",
        )

    @pn.depends(filter_panel_open.param.value, language_selector.param.value, theme_toggle.param.value)
    def filter_sidebar(is_open: bool, lang: str, is_dark: bool):
        theme = _theme(is_dark)
        return _open_filter_sidebar(lang, theme) if is_open else _collapsed_filter_rail(theme)

    @pn.depends(language_selector.param.value, theme_toggle.param.value)
    def dashboard_content(lang: str, is_dark: bool):
        theme = _theme(is_dark)
        tabs = pn.Tabs(
            (_text("momentum_tab", lang), momentum_comparison()),
            (_text("respondent_context_tab", lang), detailed_views()),
            sizing_mode="stretch_width",
            dynamic=True,
            stylesheets=[TAB_STYLESHEET],
        )
        body = pn.Row(
            filter_sidebar,
            tabs,
            sizing_mode="stretch_width",
        )
        return pn.Column(
            pn.panel(dashboard_kpis),
            body,
            styles={
                "background": theme["page_bg"],
                "color": theme["text"],
                "padding": "0 0 16px 0",
            },
            sizing_mode="stretch_width",
        )

    return pn.Column(
        header,
        dashboard_content,
        sizing_mode="stretch_width",
        min_width=1200,
    )


dashboard = create_dashboard()
dashboard.servable(title="Stack Overflow Developer Survey Dashboard v1")
