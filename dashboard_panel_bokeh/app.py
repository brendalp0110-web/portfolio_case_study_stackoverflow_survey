from __future__ import annotations

from functools import lru_cache
from html import escape
import sys
from pathlib import Path

import panel as pn


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from dashboard_panel_bokeh.charts import (  # noqa: E402
    make_country_bubble_map,
    make_dumbbell_chart,
    make_age_percent_bar_chart,
    make_compensation_experience_box_plot,
    make_horizontal_bar_chart,
    make_percent_stacked_bar_chart,
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
          font-size: 18px;
          margin: 4px 0 8px 0;
        }
        .bk-root p,
        .bk-root li {
          font-size: 15px;
          line-height: 1.5;
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
          font-size: 15px;
          padding: 10px 16px;
        }
        .bk-root .bk-tab button,
        .bk-root .bk-tab div {
          font-size: 15px;
        }
        .filter-sidebar {
          border-radius: 10px;
          padding: 14px;
          font-size: 15px;
        }
        .filter-sidebar .bk-input,
        .filter-sidebar select,
        .filter-sidebar label {
          font-size: 14px;
        }
        .filter-sidebar .bk-btn {
          font-size: 13px;
        }
        .filter-sidebar h3 {
          font-size: 21px;
        }
        .filter-sidebar h4 {
          font-size: 18px;
        }
        .filter-sidebar p,
        .filter-sidebar li {
          font-size: 14px;
          line-height: 1.45;
        }
        .filter-rail {
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
          background: #18324a;
          color: #ffffff;
          border-radius: 6px;
          padding: 8px 10px;
          font-size: 15px;
          font-weight: 700;
          white-space: nowrap;
          box-shadow: 0 6px 14px rgba(16, 42, 67, 0.18);
        }
        .language-menu button {
          background: #2f6f73 !important;
          border-color: #24575a !important;
          color: #ffffff !important;
          min-width: 118px;
          min-height: 34px;
          font-size: 14px;
        }
        .language-menu .bk-menu,
        .language-menu .bk-menu-item,
        .language-menu [role="menu"],
        .language-menu [role="menuitem"] {
          min-width: 150px;
          font-size: 14px;
          line-height: 1.5;
        }
        .filter-sidebar .bk-btn-primary {
          background: #2f6f73 !important;
          border-color: #24575a !important;
          color: #ffffff !important;
        }
        .filter-rail button {
          color: #2f6f73 !important;
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
        "momentum_tab": "Comparison and Momentum",
        "respondent_context_tab": "Respondent Context",
        "momentum_heading": "Comparison and Momentum",
        "momentum_text": "Explore which technologies developers rely on today and which ones are gaining future interest. Use this view to spot momentum and possible shifts in demand.",
        "respondent_context_heading": "Respondent Context",
        "respondent_context_text": "Interpret the technology signals through respondent profile, compensation, and geography.",
        "age_education_tab": "Age and Education",
        "age_education_heading": "Age Profile and Education Composition",
        "age_education_text": "Understand who is represented in the survey and how education patterns vary.",
        "compensation_tab": "Compensation by Experience",
        "compensation_heading": "Compensation Distribution by Experience and Work Style",
        "compensation_text": "Compare how compensation ranges evolve with experience across remote, hybrid, and in-person work.",
        "country_tab": "Country Distribution",
        "country_heading": "Full Country Distribution Map",
        "country_text": "Locate where the respondent base is concentrated and how geographic distribution changes with the active filters.",
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
        "compensation_experience_chart": "{workstyle}",
        "current_ranking_subtitle": "Technologies developers report using in the current filtered view.",
        "future_ranking_subtitle": "Technologies developers want to work with next, ranked by respondent count.",
        "momentum_chart_subtitle": "Direct comparison between current use and future interest for the selected family.",
        "age_distribution_subtitle": "Respondent mix by age group under the active filters.",
        "education_age_subtitle": "Education composition within each age group, normalized to 100%.",
        "compensation_experience_subtitle": "Distribution by experience band.",
        "country_map_subtitle": "Geographic concentration of respondents shown by bubble size and share.",
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
        "converted_compensation": "Annual compensation (USD)",
        "work_style": "Work style",
        "experience_band": "Experience band",
        "median": "Median",
        "mean": "Mean",
        "language_label": "Language",
        "database_label": "Database",
        "platform_label": "Platform",
        "framework_label": "Web framework",
        "languages_family": "Languages",
        "databases_family": "Databases",
        "platforms_family": "Platforms",
        "frameworks_family": "Frameworks",
        "remote_label": "Remote",
        "hybrid_label": "Hybrid",
        "in_person_label": "In-person",
        "education_bachelors": "Bachelors degree",
        "education_masters": "Masters degree",
        "education_other": "Other",
        "education_secondary": "Secondary school",
        "education_some_college": "Some college/university study",
    },
    "ES": {
        "language": "Idioma",
        "dashboard_title": "Dashboard de Tendencias Tecnológicas",
        "dashboard_subtitle": "Dashboard interactivo creado con Panel y Bokeh a partir del dataset limpio y reducido de la encuesta de Stack Overflow.",
        "respondents": "Encuestados",
        "countries": "Países",
        "average_compensation": "Compensación promedio",
        "total_dataset": "Dataset total",
        "filtered_view": "Vista filtrada",
        "total_excluding_nomadic": "Total, excluye Nómada",
        "shown_on_map": "Mostrados en mapa",
        "filters": "Filtros",
        "reset_filters": "Reiniciar filtros",
        "filters_help": "Usa cada categoría para refinar el dashboard. Los botones de reset restauran los valores por defecto. La métrica fija es conteo de encuestados.",
        "top_n": "Top N",
        "top_n_help": "Define la profundidad del ranking para tecnologías y para el filtro Top N de países.",
        "top_5": "Top 5",
        "top_10": "Top 10",
        "top_12": "Top 12",
        "age": "Edad",
        "age_help": "Limita el dashboard a los grupos etarios seleccionados.",
        "workstyle": "Modalidad",
        "workstyle_help": "Incluye una o más modalidades de trabajo.",
        "countries_help": "Por defecto, el mapa se limita a los países del Top N seleccionado.",
        "check_all": "Seleccionar todo",
        "show_all_countries": "Mostrar todos los países",
        "apply_country_scope": "Aplicar alcance de países a todo el dashboard",
        "reset": "Reset",
        "momentum_tab": "Comparación y momentum",
        "respondent_context_tab": "Contexto de encuestados",
        "momentum_heading": "Comparación y momentum",
        "momentum_text": "Explora qué tecnologías usan hoy los desarrolladores y cuáles ganan interés futuro. Esta vista ayuda a detectar momentum y posibles cambios de demanda.",
        "respondent_context_heading": "Contexto de encuestados",
        "respondent_context_text": "Interpreta las señales tecnológicas a través del perfil, la compensación y la distribución geográfica de los encuestados.",
        "age_education_tab": "Edad y educación",
        "age_education_heading": "Perfil etario y composición educativa",
        "age_education_text": "Entiende quién está representado en la encuesta y cómo cambian los patrones educativos.",
        "compensation_tab": "Compensación por experiencia",
        "compensation_heading": "Distribución de compensación por experiencia y modalidad",
        "compensation_text": "Compara cómo evolucionan los rangos de compensación con la experiencia en trabajo remoto, híbrido y presencial.",
        "country_tab": "Distribución por país",
        "country_heading": "Mapa de distribución por país",
        "country_text": "Ubica dónde se concentra la base de encuestados y cómo cambia la distribución geográfica con los filtros activos.",
        "nomadic_respondents": "Encuestados nómadas",
        "not_plotted_country": "encuestados, no graficados como país",
        "languages_context": "Lenguajes de programación, scripting y markup usados para construir software.",
        "databases_context": "Tecnologías de almacenamiento y consulta que sostienen aplicaciones y analítica.",
        "platforms_context": "Plataformas cloud, hosting y despliegue que definen dónde corre el software.",
        "frameworks_context": "Frameworks y librerías web usados para construir aplicaciones orientadas al usuario.",
        "top_current_languages": "Lenguajes más usados actualmente",
        "top_future_languages": "Lenguajes con mayor interés futuro",
        "top_current_databases": "Bases de datos más usadas actualmente",
        "top_future_databases": "Bases de datos con mayor interés futuro",
        "top_current_platforms": "Plataformas más usadas actualmente",
        "top_future_platforms": "Plataformas con mayor interés futuro",
        "top_current_frameworks": "Frameworks web más usados actualmente",
        "top_future_frameworks": "Frameworks web con mayor interés futuro",
        "current_future_momentum": "Momentum actual vs futuro en {family}",
        "respondent_map": "Distribución de encuestados por país",
        "age_distribution_chart": "Distribución etaria de encuestados",
        "education_age_chart": "Composición educativa por grupo etario",
        "compensation_experience_chart": "{workstyle}",
        "current_ranking_subtitle": "Tecnologías que los desarrolladores reportan usar en la vista filtrada actual.",
        "future_ranking_subtitle": "Tecnologías que los desarrolladores quieren usar próximamente, ordenadas por conteo.",
        "momentum_chart_subtitle": "Comparación directa entre uso actual e interés futuro para la familia seleccionada.",
        "age_distribution_subtitle": "Composición de encuestados por grupo etario bajo los filtros activos.",
        "education_age_subtitle": "Composición educativa dentro de cada grupo etario, normalizada al 100%.",
        "compensation_experience_subtitle": "Distribución por rango de experiencia.",
        "country_map_subtitle": "Concentración geográfica de encuestados según tamaño de burbuja y porcentaje.",
        "respondent_count_axis": "Conteo de encuestados",
        "share_respondents_axis": "Porcentaje de encuestados (%)",
        "country": "País",
        "count": "Conteo",
        "share_filtered_respondents": "Porcentaje de encuestados",
        "share_filtered_country": "Porcentaje de encuestados",
        "current": "Actual",
        "future": "Futuro",
        "current_count": "Conteo actual",
        "future_count": "Conteo futuro",
        "current_share": "Porcentaje actual de encuestados",
        "future_share": "Porcentaje futuro de encuestados",
        "delta_share": "Diferencia porcentual de encuestados",
        "age_group": "Grupo etario",
        "education_level": "Nivel educativo",
        "share_within_age": "Porcentaje dentro del grupo etario",
        "share_within_age_axis": "Porcentaje dentro del grupo etario (%)",
        "years_experience": "Años de experiencia",
        "converted_compensation": "Compensación anual (USD)",
        "work_style": "Modalidad",
        "experience_band": "Rango de experiencia",
        "median": "Mediana",
        "mean": "Promedio",
        "language_label": "Lenguaje",
        "database_label": "Base de datos",
        "platform_label": "Plataforma",
        "framework_label": "Framework web",
        "languages_family": "Lenguajes",
        "databases_family": "Bases de datos",
        "platforms_family": "Plataformas",
        "frameworks_family": "Frameworks",
        "remote_label": "remota",
        "hybrid_label": "híbrida",
        "in_person_label": "presencial",
        "education_bachelors": "Licenciatura/grado universitario",
        "education_masters": "Maestría",
        "education_other": "Otro",
        "education_secondary": "Educación secundaria",
        "education_some_college": "Estudios universitarios incompletos",
    },
}
THEME = {
    "page_bg": "#f3f4f1",
    "header_bg": "#18324a",
    "header_text": "#ffffff",
    "surface": "#ffffff",
    "panel": "#ffffff",
    "border": "#d7ddd6",
    "text": "#1f2933",
    "muted": "#64748b",
    "muted_soft": "#7b8794",
    "filtered_value": "#2f6f73",
    "primary": "#2f6f73",
    "primary_dark": "#24575a",
    "accent": "#d99058",
    "positive": "#7a8f5a",
    "danger": "#c66b4e",
    "purple": "#8b6f9e",
    "connector": "#9aa6a1",
    "marker_line": "#ffffff",
    "rail_bg": "#ffffff",
    "tooltip_bg": "#18324a",
    "chart_bg": "#ffffff",
    "chart_grid": "#e6eae4",
    "chart_border": "#d7ddd6",
    "map_palette": ["#efe6d6", "#dfb778", "#d99058", "#8a6964", "#2f6f73"],
    "tech_colors": {
        "languages": "#2f6f73",
        "databases": "#d99058",
        "platforms": "#7a8f5a",
        "frameworks": "#c66b4e",
    },
    "remote_colors": {
        "Remote": "#2f6f73",
        "Hybrid": "#7a8f5a",
        "In-person": "#c66b4e",
    },
    "education_colors": ["#2f6f73", "#d99058", "#7a8f5a", "#8b6f9e", "#c66b4e"],
}


def _tab_stylesheet(theme: dict) -> str:
    return f"""
    :host {{
      font-size: 16px;
      background: {theme['page_bg']};
      color: {theme['text']};
    }}
    .bk-tab,
    .bk-tab button,
    .bk-tab div,
    button,
    [role="tab"] {{
      background: {theme['surface']} !important;
      border-color: {theme['border']} !important;
      color: {theme['text']} !important;
      font-size: 16px !important;
      line-height: 1.35 !important;
      padding: 12px 18px !important;
    }}
    .bk-tab.bk-active,
    .bk-tab.bk-active button,
    [aria-selected="true"] {{
      background: {theme['primary']} !important;
      border-color: {theme['primary_dark']} !important;
      color: #ffffff !important;
    }}
    """
FILTER_WIDGET_STYLESHEET = """
:host {
  font-size: 15px;
}
label,
.bk-input,
.bk-input-group,
.bk-checkbox-label,
.bk-label,
select,
button {
  font-size: 15px !important;
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
TECHNOLOGY_FAMILY_LABEL_KEYS = {
    "Languages": "languages_family",
    "Databases": "databases_family",
    "Platforms": "platforms_family",
    "Frameworks": "frameworks_family",
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
language_selector = pn.widgets.MenuButton(
    name="EN",
    icon="language",
    icon_size="1.4em",
    items=[("English ✓", "EN"), ("Español", "ES")],
    value="EN",
    button_type="primary",
    width=118,
    css_classes=["language-menu"],
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
    return language_selector.value or "EN"


def _text(key: str, lang: str | None = None) -> str:
    selected_lang = lang or _lang()
    return TEXT[selected_lang][key]


def _theme() -> dict:
    return THEME


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
    labels["education_levels"] = {
        "Bachelors degree": _text("education_bachelors", lang),
        "Masters degree": _text("education_masters", lang),
        "Other": _text("education_other", lang),
        "Secondary school": _text("education_secondary", lang),
        "Some college/university study": _text("education_some_college", lang),
    }
    if extra:
        labels.update(extra)
    return labels


def _technology_family_label(family: str, lang: str) -> str:
    return _text(TECHNOLOGY_FAMILY_LABEL_KEYS[family], lang)


def _workstyle_label(workstyle: str, lang: str) -> str:
    labels = {
        "Remote": _text("remote_label", lang),
        "Hybrid": _text("hybrid_label", lang),
        "In-person": _text("in_person_label", lang),
    }
    return labels.get(workstyle, workstyle)


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
    language_selector.name = lang
    language_selector.items = [
        ("English ✓" if lang == "EN" else "English", "EN"),
        ("Español ✓" if lang == "ES" else "Español", "ES"),
    ]
    filter_panel_collapse_button.description = "Collapse filters" if lang == "EN" else "Cerrar filtros"


def _language_menu_clicked(event) -> None:
    if event.new in TEXT and language_selector.value != event.new:
        language_selector.value = event.new


language_selector.param.watch(_language_menu_clicked, "clicked")
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


def _chart_card(item, theme: dict, title: str = "", subtitle: str = "", compact: bool = False) -> pn.Column:
    title_size = "16px" if compact else "17px"
    subtitle_size = "12px" if compact else "13px"
    padding = "12px 14px 8px 14px" if compact else "14px 16px 10px 16px"
    header = pn.pane.HTML(
        f"""
        <div style="padding:2px 2px 10px 2px;">
          <div style="font-size:{title_size};font-weight:750;letter-spacing:-0.01em;color:{theme['text']};line-height:1.25;">
            {escape(title)}
          </div>
          <div style="font-size:{subtitle_size};color:{theme['muted']};line-height:1.4;margin-top:4px;">
            {escape(subtitle)}
          </div>
        </div>
        """,
        sizing_mode="stretch_width",
        margin=(0, 0, 2, 0),
    )
    children = [header, item] if title or subtitle else [item]
    return pn.Column(
        *children,
        sizing_mode="stretch_width",
        styles={
            "background": theme["surface"],
            "border": f"1px solid {theme['border']}",
            "border-radius": "14px",
            "box-shadow": "0 10px 24px rgba(31, 41, 51, 0.07)",
            "padding": padding,
            "overflow": "hidden",
        },
    )


def _chart_grid_box(*items, ncols: int, theme: dict, compact: bool = False) -> pn.GridBox:
    cards = [
        _chart_card(item[0], theme, item[1], item[2], compact=compact)
        if isinstance(item, tuple)
        else _chart_card(item, theme, compact=compact)
        for item in items
    ]
    return pn.GridBox(
        *cards,
        ncols=ncols,
        sizing_mode="stretch_width",
        styles={"gap": "18px"},
    )


def _page_background_style(theme: dict) -> pn.pane.HTML:
    return pn.pane.HTML(
        f"""
        <style>
          html,
          body,
          body .bk-root {{
            background: {theme['page_bg']} !important;
          }}
          body {{
            min-height: 100vh;
          }}
        </style>
        """,
        height=0,
        margin=0,
    )


def _info_markdown(text: str, theme: dict | None = None, **kwargs) -> pn.pane.Markdown:
    colors = theme or _theme()
    stylesheet = f"""
    :host {{
      color: {colors['text']};
      font-family: inherit;
      font-size: 16px;
      line-height: 1.55;
    }}
    h3 {{
      color: {colors['text']};
      font-size: 23px;
      margin: 10px 0 8px 0;
    }}
    p {{
      color: {colors['text']};
      font-size: 16px;
      line-height: 1.55;
    }}
    code {{
      color: inherit;
      font-family: inherit;
      font-size: 15px;
    }}
    """
    return pn.pane.Markdown(text, stylesheets=[stylesheet], **kwargs)


def _filter_markdown(text: str, theme: dict | None = None, **kwargs) -> pn.pane.Markdown:
    colors = theme or _theme()
    stylesheet = f"""
    :host {{
      color: {colors['text']};
      font-size: 15px;
      line-height: 1.5;
    }}
    h3 {{
      color: {colors['text']};
      font-size: 22px;
    }}
    h4 {{
      color: {colors['text']};
      font-size: 18px;
    }}
    p {{
      color: {colors['text']};
      font-size: 15px;
      line-height: 1.5;
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
    color = theme["tech_colors"][config["color_key"]]
    context = _text(TECHNOLOGY_CONTEXT_KEYS[selected_family], lang)

    rankings_grid = _chart_grid_box(
        (
            make_horizontal_bar_chart(
                current_ranking,
                config["label"],
                value_col,
                "",
                METRIC_MODE,
                color,
                labels=chart_labels,
                theme=theme,
            ),
            _text(config["current_title_key"], lang),
            _text("current_ranking_subtitle", lang),
        ),
        (
            make_horizontal_bar_chart(
                future_ranking,
                config["label"],
                value_col,
                "",
                METRIC_MODE,
                color,
                labels=chart_labels,
                theme=theme,
            ),
            _text(config["future_title_key"], lang),
            _text("future_ranking_subtitle", lang),
        ),
        ncols=2,
        theme=theme,
    )

    return pn.Column(
        _info_markdown(f"{context}", theme=theme, margin=(0, 0, 8, 0)),
        rankings_grid,
        _chart_card(
            make_dumbbell_chart(
                comparison,
                config["label"],
                "count_current",
                "count_future",
                "",
                METRIC_MODE,
                labels=chart_labels,
                theme=theme,
            ),
            theme,
            _text("current_future_momentum", lang).format(family=_technology_family_label(selected_family, lang)),
            _text("momentum_chart_subtitle", lang),
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
)
def dashboard_kpis(
    show_all_countries,
    apply_country_scope,
    selected_ages,
    selected_remote,
    top_n,
    lang,
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
    theme = _theme()
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
    )
    def technology_view(
        show_all_countries,
        apply_country_scope,
        selected_ages,
        selected_remote,
        top_n,
        lang,
    ):
        effective_top_n = _effective_top_n(top_n)
        filter_key = _filter_key_from_filter_values(
            selected_ages,
            selected_remote,
            show_all_countries,
            apply_country_scope,
            top_n,
        )
        return _technology_momentum_view(filter_key, effective_top_n, selected_family, lang, _theme())

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
            (_technology_family_label(family, lang), _technology_momentum_panel(family))
            for family in MOMENTUM_OPTIONS
        ],
        sizing_mode="stretch_width",
        dynamic=True,
        stylesheets=[_tab_stylesheet(theme)],
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
        _chart_grid_box(
            (
                make_age_percent_bar_chart(
                    age_profile,
                    "",
                    METRIC_MODE,
                    labels=chart_labels,
                    theme=theme,
                ),
                _text("age_distribution_chart", lang),
                _text("age_distribution_subtitle", lang),
            ),
            (
                make_percent_stacked_bar_chart(
                    age_education,
                    "",
                    labels=chart_labels,
                    theme=theme,
                ),
                _text("education_age_chart", lang),
                _text("education_age_subtitle", lang),
            ),
            ncols=2,
            theme=theme,
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

        workstyle_title = _workstyle_label(remote_label, lang)
        chart_title = _text("compensation_experience_chart", lang).format(
            workstyle=workstyle_title[:1].upper() + workstyle_title[1:]
        )
        charts.append(
            (
                make_compensation_experience_box_plot(
                    chart_data,
                    "",
                    y_max,
                    theme["remote_colors"].get(remote_label, theme["primary"]),
                    labels=chart_labels,
                    theme=theme,
                ),
                chart_title,
                _text("compensation_experience_subtitle", lang),
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
        _chart_grid_box(*charts, ncols=3, theme=theme, compact=True),
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
        _chart_card(
            make_country_bubble_map(
                map_data,
                "",
                METRIC_MODE,
                height=640,
                labels=chart_labels,
                theme=theme,
            ),
            theme,
            _text("respondent_map", lang),
            _text("country_map_subtitle", lang),
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
        stylesheets=[_tab_stylesheet(theme)],
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
        )

    def _collapsed_filter_rail(theme: dict) -> pn.Column:
        return pn.Column(
            filter_panel_expand_button,
            css_classes=["filter-rail"],
            styles={
                "background": theme["rail_bg"],
                "border": f"1px solid {theme['border']}",
                "color": theme["primary"],
            },
            width=56,
            align="start",
        )

    @pn.depends(language_selector.param.value)
    def header(lang: str):
        theme = _theme()
        title_row = pn.Row(
            pn.pane.HTML(
                f"""
                <div style="font-size:26px;font-weight:700;line-height:1.2;color:{theme['header_text']};">
                  {_text('dashboard_title', lang)}
                </div>
                """,
                sizing_mode="stretch_width",
            ),
            pn.Row(
                language_selector,
                align="center",
                width=128,
                margin=(0, 10, 0, 16),
            ),
            sizing_mode="stretch_width",
        )
        return pn.Column(
            title_row,
            pn.pane.HTML(
                f"""
                <div style="font-size:14px;line-height:1.45;max-width:980px;color:{theme['header_text']};">
                  {_text('dashboard_subtitle', lang)}
                </div>
                """,
                sizing_mode="stretch_width",
                margin=(0, 0, 0, 0),
            ),
            styles={
                "background": theme["header_bg"],
                "color": theme["header_text"],
                "padding": "18px 22px",
                "border-radius": "0 0 10px 10px",
            },
            sizing_mode="stretch_width",
        )

    @pn.depends(filter_panel_open.param.value, language_selector.param.value)
    def filter_sidebar(is_open: bool, lang: str):
        theme = _theme()
        return _open_filter_sidebar(lang, theme) if is_open else _collapsed_filter_rail(theme)

    @pn.depends(language_selector.param.value)
    def dashboard_content(lang: str):
        theme = _theme()
        tabs = pn.Tabs(
            (_text("momentum_tab", lang), momentum_comparison()),
            (_text("respondent_context_tab", lang), detailed_views()),
            sizing_mode="stretch_width",
            dynamic=True,
            stylesheets=[_tab_stylesheet(theme)],
        )
        body = pn.Row(
            filter_sidebar,
            tabs,
            sizing_mode="stretch_width",
        )
        return pn.Column(
            _page_background_style(theme),
            pn.panel(dashboard_kpis),
            body,
            styles={
                "background": theme["page_bg"],
                "color": theme["text"],
                "padding": "0 0 16px 0",
                "min-height": "100vh",
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
