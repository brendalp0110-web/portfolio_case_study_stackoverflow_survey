from __future__ import annotations

import os

import panel as pn


os.environ["PANEL_BOKEH_IMPORT_ONLY"] = "1"

from dashboard_panel_bokeh import app as base  # noqa: E402


pn.extension(sizing_mode="stretch_width")

ACTIVE_VIEW_DEFAULT = "Languages"
TECH_TOP_N = 12
FIXED_HEADER_HEIGHT = 254
NAV_TOP_GAP = 12
active_view = pn.widgets.TextInput(value=ACTIVE_VIEW_DEFAULT, visible=False)
nav_panel_open = pn.widgets.Checkbox(value=True, visible=False)
country_count_slider = pn.widgets.IntSlider(
    name="Countries shown",
    start=1,
    end=base.TOTAL_KPIS["countries"],
    value=base.TOTAL_KPIS["countries"],
    sizing_mode="stretch_width",
)
age_select_all_button = pn.widgets.Button(name="Check All", width=92)
global_reset_button = pn.widgets.Button(name="Reset filters", button_type="primary", width=112, height=42)
nav_collapse_button = pn.widgets.ButtonIcon(icon="chevron-left", width=34, height=32)
nav_expand_button = pn.widgets.ButtonIcon(icon="menu-2", width=36, height=36)
AGE_CHIP_LABELS = {
    "Under 18 years old": "<18",
    "18-24 years old": "18-24",
    "25-34 years old": "25-34",
    "35-44 years old": "35-44",
    "45-54 years old": "45-54",
    "55-64 years old": "55-64",
    "65 years or older": "65+",
    "Prefer not to say": "Undeclared",
}
WORKSTYLE_CHIP_LABELS = {
    "Remote": "Remote",
    "Hybrid (some remote, some in-person)": "Hybrid",
    "In-person": "In-person",
}
CHIP_SELECTOR_STYLESHEET = """
:host {
  background: #ffffff;
}
.choices,
.choices__inner,
.choices__input {
  background: #ffffff !important;
}
.choices__inner {
  border-color: #d7ddd6 !important;
  min-height: 42px !important;
}
.choices__list--multiple {
  overflow: visible !important;
}
.choices__list--multiple:not(:empty) ~ .choices__input::placeholder {
  color: transparent !important;
  opacity: 0 !important;
}
.choices__list--multiple:not(:empty) ~ .choices__input {
  min-width: 1ch !important;
  width: 1ch !important;
}
.choices__list--multiple .choices__item {
  margin-bottom: 3px !important;
}
.choices__list--dropdown {
  background: #ffffff !important;
  z-index: 1000 !important;
}
"""
redesign_age_selector = pn.widgets.MultiChoice(
    name="",
    options={label: value for value, label in AGE_CHIP_LABELS.items()},
    value=[],
    placeholder="All age groups",
    solid=True,
    width=520,
    styles={"background": "#ffffff"},
    stylesheets=[CHIP_SELECTOR_STYLESHEET],
)
redesign_remote_selector = pn.widgets.MultiChoice(
    name="",
    options={label: value for value, label in WORKSTYLE_CHIP_LABELS.items()},
    value=[],
    placeholder="All workstyles",
    solid=True,
    width=360,
    styles={"background": "#ffffff"},
    stylesheets=[CHIP_SELECTOR_STYLESHEET],
)

NAV_GROUPS = {
    "Comparison and Momentum": ["Languages", "Databases", "Platforms", "Frameworks"],
    "Respondent Context": ["Age and Education", "Compensation", "Country Distribution"],
}

VIEW_LABEL_KEYS = {
    "Languages": "languages_family",
    "Databases": "databases_family",
    "Platforms": "platforms_family",
    "Frameworks": "frameworks_family",
    "Age and Education": "age_education_tab",
    "Compensation": "compensation_tab",
    "Country Distribution": "country_tab",
}

NAV_BUTTONS: dict[str, pn.widgets.Button] = {}
_syncing_redesign_filters = False


def _reset_global_filters(event=None) -> None:
    base.reset_age()
    base.reset_remote()
    country_count_slider.end = base.TOTAL_KPIS["countries"]
    country_count_slider.value = base.TOTAL_KPIS["countries"]
    _clear_redesign_filter_selectors()


def _clear_redesign_filter_selectors() -> None:
    _clear_redesign_age_selector()
    _clear_redesign_remote_selector()
    _update_selector_placeholders()


def _clear_redesign_age_selector() -> None:
    global _syncing_redesign_filters
    _syncing_redesign_filters = True
    redesign_age_selector.value = []
    _syncing_redesign_filters = False


def _clear_redesign_remote_selector() -> None:
    global _syncing_redesign_filters
    _syncing_redesign_filters = True
    redesign_remote_selector.value = []
    _syncing_redesign_filters = False


def _update_selector_placeholders(lang: str | None = None) -> None:
    selected_lang = lang or base._lang()
    redesign_age_selector.placeholder = (
        "" if redesign_age_selector.value else ("All age groups" if selected_lang == "EN" else "Todos los grupos de edad")
    )
    redesign_remote_selector.placeholder = (
        "" if redesign_remote_selector.value else ("All workstyles" if selected_lang == "EN" else "Todas las modalidades")
    )


def _available_country_count(selected_ages, selected_remote) -> int:
    filter_key = _redesign_filter_key(selected_ages, selected_remote)
    available_countries = base._cached_country_map_distribution(filter_key, None)
    return max(len(available_countries), 1)


def _restore_country_slider_to_available_max(selected_ages=None, selected_remote=None) -> None:
    available_count = _available_country_count(
        redesign_age_selector.value if selected_ages is None else selected_ages,
        redesign_remote_selector.value if selected_remote is None else selected_remote,
    )
    if country_count_slider.end != available_count:
        country_count_slider.end = available_count
    if country_count_slider.value != available_count:
        country_count_slider.value = available_count


def _redesign_age_changed(event) -> None:
    if _syncing_redesign_filters:
        return
    selected = list(event.new)
    if selected:
        base._set_age_values(selected)
    else:
        base._set_age_values(base.AGE_ORDER)
    _restore_country_slider_to_available_max(selected_ages=selected)
    _update_selector_placeholders()


def _redesign_remote_changed(event) -> None:
    if _syncing_redesign_filters:
        return
    selected = list(event.new)
    if selected:
        base._set_remote_values(selected)
    else:
        base._set_remote_values(base.REMOTE_OPTIONS)
    _restore_country_slider_to_available_max(selected_remote=selected)
    _update_selector_placeholders()


def _selected_redesign_ages(selected_ages) -> list[str]:
    return list(selected_ages) if selected_ages else list(base.AGE_ORDER)


def _selected_redesign_remote(selected_remote) -> list[str]:
    return list(selected_remote) if selected_remote else list(base.REMOTE_OPTIONS)


def _redesign_filter_key(selected_ages, selected_remote):
    return base._filter_key(
        _selected_redesign_ages(selected_ages),
        _selected_redesign_remote(selected_remote),
        "All countries",
        TECH_TOP_N,
    )


age_select_all_button.on_click(base.reset_age)
global_reset_button.on_click(_reset_global_filters)
redesign_age_selector.param.watch(_redesign_age_changed, "value")
redesign_remote_selector.param.watch(_redesign_remote_changed, "value")


def _toggle_navigation(is_open: bool) -> None:
    nav_panel_open.value = is_open


nav_collapse_button.on_click(lambda event: _toggle_navigation(False))
nav_expand_button.on_click(lambda event: _toggle_navigation(True))


def _redesign_css(theme: dict) -> pn.pane.HTML:
    return pn.pane.HTML(
        f"""
        <style>
          :root {{
            --redesign-fixed-header-height: {FIXED_HEADER_HEIGHT}px;
            --redesign-nav-top-gap: {NAV_TOP_GAP}px;
            --redesign-nav-top: calc(var(--redesign-fixed-header-height) + var(--redesign-nav-top-gap));
          }}
          html,
          body,
          body .bk-root {{
            background: {theme['page_bg']} !important;
          }}
          .redesign-fixed-header-spacer {{
            height: var(--redesign-fixed-header-height);
          }}
          .redesign-filter-bar {{
            background: {theme['page_bg']};
            padding: 8px 0 0 0;
          }}
          .redesign-filter-panel {{
            background: {theme['surface']};
            border: 1px solid {theme['border']};
            border-radius: 12px;
            box-shadow: 0 10px 24px rgba(31, 41, 51, 0.08);
            min-height: 126px;
            padding: 10px 14px;
            overflow: visible;
          }}
          .redesign-filter-title {{
            color: {theme['text']};
            font-size: 14px;
            font-weight: 750;
            letter-spacing: 0.02em;
            text-transform: uppercase;
          }}
          .redesign-filter-label {{
            color: {theme['text']};
            display: inline-flex;
            align-items: center;
            height: 42px;
            font-size: 15px;
            font-weight: 750;
            line-height: 42px;
            white-space: nowrap;
          }}
          .redesign-filter-control-row {{
            align-items: flex-start;
          }}
          .redesign-filter-control-group {{
            align-items: flex-start;
          }}
          .redesign-filter-panel .bk-input,
          .redesign-filter-panel input,
          .redesign-filter-panel select {{
            background: #ffffff !important;
          }}
          .redesign-filter-panel .choices,
          .redesign-filter-panel .choices__inner {{
            background: #ffffff !important;
            border-color: {theme['border']} !important;
            min-height: 42px !important;
            font-size: 14px !important;
          }}
          .redesign-filter-panel .choices__list--multiple {{
            overflow: visible !important;
          }}
          .redesign-filter-panel .choices__list--dropdown {{
            background: #ffffff !important;
            z-index: 1000 !important;
          }}
          .redesign-filter-card {{
            background: {theme['surface']};
            border: 1px solid {theme['border']};
            border-radius: 12px;
            padding: 12px;
            min-height: 132px;
            box-shadow: 0 8px 18px rgba(31, 41, 51, 0.05);
          }}
          .redesign-filter-dropdown {{
            background: {theme['surface']};
            border: 1px solid {theme['border']};
            border-radius: 12px;
            box-shadow: 0 10px 24px rgba(31, 41, 51, 0.08);
            overflow: hidden;
          }}
          .redesign-sidebar {{
            background: #d7ded3;
            border: 1px solid #aeb9aa;
            border-radius: 14px;
            padding: 16px 14px;
            box-shadow: 0 18px 34px rgba(31, 41, 51, 0.16);
            max-height: calc(100vh - var(--redesign-nav-top) - 18px);
            overflow-y: auto;
            overflow-x: hidden;
            scrollbar-width: thin;
          }}
          .redesign-sidebar-shell {{
            flex: 0 0 auto;
            align-self: flex-start;
            z-index: 8;
          }}
          .redesign-sidebar-rail {{
            background: #d7ded3;
            border: 1px solid #aeb9aa;
            border-radius: 14px;
            padding: 10px 8px;
            box-shadow: 0 18px 34px rgba(31, 41, 51, 0.16);
            min-height: 58px;
            display: flex;
            align-items: center;
            justify-content: center;
          }}
          .redesign-sidebar-header {{
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 8px;
          }}
          .redesign-sidebar .bk-btn {{
            justify-content: flex-start;
            text-align: left;
            font-size: 14px;
            font-weight: 650;
            border-radius: 10px;
            min-height: 38px;
            padding-left: 14px;
            transition: background 0.12s ease, color 0.12s ease, border-color 0.12s ease;
          }}
          .redesign-sidebar .bk-btn-primary {{
            background: {theme['primary']} !important;
            border-color: {theme['primary']} !important;
            box-shadow: inset 4px 0 0 {theme['accent']};
          }}
          .redesign-sidebar .bk-btn-light {{
            background: rgba(255, 255, 255, 0.82) !important;
            border-color: transparent !important;
            color: {theme['text']} !important;
          }}
          .redesign-sidebar .bk-btn-light:hover {{
            background: {theme['page_bg']} !important;
            border-color: {theme['border']} !important;
          }}
          .redesign-nav-title {{
            color: {theme['text']};
            font-size: 18px;
            font-weight: 800;
            letter-spacing: -0.01em;
            line-height: 32px;
          }}
          .redesign-nav-section {{
            color: {theme['primary_dark']};
            font-size: 12px;
            font-weight: 800;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            margin: 16px 0 8px 0;
          }}
          .redesign-nav-rule {{
            height: 1px;
            background: {theme['border']};
            margin: 12px 0 4px 0;
          }}
          .redesign-view-frame {{
            background: {theme['page_bg']};
            border-radius: 14px;
          }}
        </style>
        """,
        height=0,
        margin=0,
    )


def _set_active_view(view_name: str) -> None:
    active_view.value = view_name
    for name, button in NAV_BUTTONS.items():
        button.button_type = "primary" if name == view_name else "light"


def _nav_button(view_name: str, lang: str) -> pn.widgets.Button:
    if view_name not in NAV_BUTTONS:
        button = pn.widgets.Button(
            name=base._text(VIEW_LABEL_KEYS[view_name], lang),
            button_type="primary" if view_name == active_view.value else "light",
            sizing_mode="stretch_width",
            height=36,
        )
        button.on_click(lambda event, view=view_name: _set_active_view(view))
        NAV_BUTTONS[view_name] = button
    else:
        button = NAV_BUTTONS[view_name]
        button.name = base._text(VIEW_LABEL_KEYS[view_name], lang)
        button.button_type = "primary" if view_name == active_view.value else "light"
    return button


def _filter_card(title: str, reset, help_text: str, *items) -> pn.Column:
    theme = base._theme()
    header_items = [base._filter_markdown(f"#### {title}", margin=(0, 0, 0, 0)), pn.Spacer(sizing_mode="stretch_width")]
    if reset is not None:
        header_items.append(reset)
    return pn.Column(
        pn.Row(
            *header_items,
            sizing_mode="stretch_width",
            margin=(0, 0, 4, 0),
        ),
        base._filter_markdown(help_text, margin=(0, 0, 6, 0)),
        *items,
        css_classes=["redesign-filter-card"],
        styles={"color": theme["text"]},
        sizing_mode="stretch_width",
    )


@pn.depends(base.language_selector.param.value)
def header(lang: str) -> pn.Column:
    theme = base._theme()
    about_button = pn.widgets.ButtonIcon(
        icon="info-circle",
        description="About" if lang == "EN" else "Acerca de",
        width=36,
        height=36,
    )
    return pn.Column(
        pn.Row(
            pn.pane.HTML(
                f"""
                <div style="font-size:26px;font-weight:750;color:{theme['header_text']};line-height:1.2;">
                  {base._text('dashboard_title', lang)}
                </div>
                """,
                sizing_mode="stretch_width",
            ),
            about_button,
            pn.Row(base.language_selector, width=132, margin=(0, 0, 0, 8)),
            sizing_mode="stretch_width",
            align="center",
        ),
        pn.pane.HTML(
            f"""
            <div style="font-size:14px;color:{theme['header_text']};line-height:1.45;max-width:960px;">
              {base._text('dashboard_subtitle', lang)}
            </div>
            """,
            sizing_mode="stretch_width",
        ),
        styles={
            "background": theme["header_bg"],
            "border-radius": "0 0 12px 12px",
            "padding": "18px 22px",
        },
        sizing_mode="stretch_width",
    )


def _filter_label(text: str, width: int) -> pn.pane.HTML:
    theme = base._theme()
    return pn.pane.HTML(
        f"""
        <div class="redesign-filter-label" style="height:42px;line-height:42px;font-size:15px;font-weight:750;color:{theme['text']};">
          {text}
        </div>
        """,
        width=width,
        height=42,
        margin=(0, 8, 0, 0),
    )


@pn.depends(base.language_selector.param.value)
def filter_bar(lang: str) -> pn.Column:
    global_reset_button.name = base._text("reset_filters", lang)
    _update_selector_placeholders(lang)
    title = "Global filters" if lang == "EN" else "Filtros globales"
    subtitle = (
        "Age and workstyle control the dashboard data."
        if lang == "EN"
        else "Edad y modalidad controlan la data del dashboard."
    )
    age_label = base._text("age", lang)
    workstyle_label = base._text("workstyle", lang)

    return pn.Column(
        pn.Column(
            pn.Row(
                pn.pane.HTML(
                    f"""
                    <div style="display:flex;align-items:baseline;gap:10px;">
                      <span class="redesign-filter-title">{title}</span>
                      <span style="font-size:12px;color:{base._theme()['muted']};line-height:1.25;">{subtitle}</span>
                    </div>
                    """,
                    sizing_mode="stretch_width",
                ),
                sizing_mode="stretch_width",
                height=28,
                align="center",
                margin=(0, 0, 8, 0),
            ),
            pn.Row(
                pn.Row(
                    _filter_label(age_label, 58),
                    redesign_age_selector,
                    align="start",
                    margin=(0, 24, 0, 0),
                    css_classes=["redesign-filter-control-group"],
                ),
                pn.Row(
                    _filter_label(workstyle_label, 92),
                    redesign_remote_selector,
                    align="start",
                    margin=(0, 24, 0, 0),
                    css_classes=["redesign-filter-control-group"],
                ),
                global_reset_button,
                pn.Spacer(sizing_mode="stretch_width"),
                sizing_mode="stretch_width",
                align="start",
                css_classes=["redesign-filter-control-row"],
            ),
            css_classes=["redesign-filter-panel"],
            sizing_mode="stretch_width",
        ),
        css_classes=["redesign-filter-bar"],
        sizing_mode="stretch_width",
    )


def sticky_header() -> pn.Column:
    theme = base._theme()
    return pn.Column(
        header,
        filter_bar,
        styles={
            "position": "fixed",
            "top": "0",
            "left": "0",
            "right": "0",
            "z-index": "50",
            "background": theme["page_bg"],
            "padding": "0 10px 10px 10px",
            "box-shadow": "0 12px 26px rgba(31, 41, 51, 0.08)",
        },
        sizing_mode="stretch_width",
    )


def fixed_header_spacer() -> pn.Spacer:
    return pn.Spacer(height=FIXED_HEADER_HEIGHT, css_classes=["redesign-fixed-header-spacer"])


@pn.depends(active_view.param.value, base.language_selector.param.value)
def navigation(selected: str, lang: str) -> pn.Column:
    theme = base._theme()
    nav_collapse_button.description = "Hide navigation" if lang == "EN" else "Ocultar navegación"
    sections = [
        pn.Row(
            pn.pane.HTML(
                f"""<div class="redesign-nav-title">{'Navigation' if lang == 'EN' else 'Navegación'}</div>""",
                margin=0,
                sizing_mode="stretch_width",
            ),
            nav_collapse_button,
            css_classes=["redesign-sidebar-header"],
            sizing_mode="stretch_width",
        )
    ]
    for index, (group, views) in enumerate(NAV_GROUPS.items()):
        title = group if lang == "EN" else (
            "Comparación y momentum" if group == "Comparison and Momentum" else "Contexto de encuestados"
        )
        if index:
            sections.append(pn.pane.HTML('<div class="redesign-nav-rule"></div>', margin=0, height=12))
        sections.append(
            pn.pane.HTML(
                f"""<div class="redesign-nav-section">{title}</div>""",
                margin=(0, 0, 0, 0),
                sizing_mode="stretch_width",
            )
        )
        sections.extend(_nav_button(view, lang) for view in views)

    return pn.Column(
        *sections,
        active_view,
        css_classes=["redesign-sidebar"],
        width=260,
        styles={"color": theme["text"]},
    )


@pn.depends(nav_panel_open.param.value, active_view.param.value, base.language_selector.param.value)
def navigation_shell(is_open: bool, selected: str, lang: str):
    theme = base._theme()
    if is_open:
        fixed_panel = pn.Column(
            navigation,
            styles={
                "position": "fixed",
                "top": "var(--redesign-nav-top)",
                "left": "10px",
                "width": "260px",
                "z-index": "20",
            },
            width=260,
        )
        return pn.Column(
            pn.Spacer(width=260, height=1),
            fixed_panel,
            nav_panel_open,
            css_classes=["redesign-sidebar-shell"],
            width=260,
            styles={"color": theme["text"]},
        )

    nav_expand_button.description = "Open navigation" if lang == "EN" else "Abrir navegación"
    fixed_rail = pn.Column(
        pn.Column(
            nav_expand_button,
            css_classes=["redesign-sidebar-rail"],
            width=52,
        ),
        styles={
            "position": "fixed",
            "top": "var(--redesign-nav-top)",
            "left": "10px",
            "width": "52px",
            "z-index": "20",
        },
        width=52,
    )
    return pn.Column(
        pn.Spacer(width=52, height=1),
        fixed_rail,
        nav_panel_open,
        css_classes=["redesign-sidebar-shell"],
        width=52,
    )


def _technology_view(view_name: str):
    @pn.depends(
        redesign_age_selector.param.value,
        redesign_remote_selector.param.value,
        base.language_selector.param.value,
    )
    def view(selected_ages, selected_remote, lang):
        filter_key = _redesign_filter_key(selected_ages, selected_remote)
        return base._technology_momentum_view(filter_key, TECH_TOP_N, view_name, lang, base._theme())

    return pn.panel(view, sizing_mode="stretch_width")


@pn.depends(
    redesign_age_selector.param.value,
    redesign_remote_selector.param.value,
    country_count_slider.param.value,
    base.language_selector.param.value,
)
def redesign_kpis(selected_ages, selected_remote, country_count, lang):
    filter_key = _redesign_filter_key(selected_ages, selected_remote)
    kpis = base._cached_kpis(filter_key)
    available_countries = base._cached_country_map_distribution(filter_key, None)
    countries_shown_on_map = min(int(country_count), len(available_countries))
    theme = base._theme()
    return base._grid_box(
        base._kpi_card(
            base._text("respondents", lang),
            f"{base.TOTAL_KPIS['respondents']:,}",
            base._text("total_dataset", lang),
            f"{kpis['respondents']:,}",
            base._text("filtered_view", lang),
            theme,
        ),
        base._kpi_card(
            base._text("countries", lang),
            f"{base.TOTAL_KPIS['countries']:,}",
            base._text("total_excluding_nomadic", lang),
            f"{countries_shown_on_map:,}",
            base._text("shown_on_map", lang),
            theme,
        ),
        base._kpi_card(
            base._text("average_compensation", lang),
            f"${base.TOTAL_KPIS['average_salary']:,.0f}",
            base._text("observed_salary_records", lang),
            f"${kpis['average_salary']:,.0f}",
            base._text("filtered_salary_records", lang),
            theme,
        ),
        ncols=3,
    )


@pn.depends(
    redesign_age_selector.param.value,
    redesign_remote_selector.param.value,
    base.language_selector.param.value,
)
def redesign_age_education(selected_ages, selected_remote, lang):
    theme = base._theme()
    filter_key = _redesign_filter_key(selected_ages, selected_remote)
    age_profile = base._cached_age_distribution(filter_key)
    age_education = base._cached_age_education_distribution(filter_key)
    chart_labels = base._chart_labels(lang)

    return pn.Column(
        base._info_markdown(
            f"""
            ### {base._text("age_education_heading", lang)}

            {base._text("age_education_text", lang)}
            """,
            theme=theme,
        ),
        base._chart_grid_box(
            (
                base.make_age_percent_bar_chart(
                    age_profile,
                    "",
                    base.METRIC_MODE,
                    labels=chart_labels,
                    theme=theme,
                ),
                base._text("age_distribution_chart", lang),
                base._text("age_distribution_subtitle", lang),
            ),
            (
                base.make_percent_stacked_bar_chart(
                    age_education,
                    "",
                    labels=chart_labels,
                    theme=theme,
                ),
                base._text("education_age_chart", lang),
                base._text("education_age_subtitle", lang),
            ),
            ncols=2,
            theme=theme,
        ),
        sizing_mode="stretch_width",
    )


@pn.depends(
    redesign_age_selector.param.value,
    redesign_remote_selector.param.value,
    base.language_selector.param.value,
)
def redesign_compensation_experience(selected_ages, selected_remote, lang):
    theme = base._theme()
    filter_key = _redesign_filter_key(selected_ages, selected_remote)
    salary_box = base._cached_salary_remote_experience_box_summary(filter_key)
    y_max = float(salary_box["upper"].max() * 1.1) if not salary_box.empty else 1.0
    remote_labels = [base.REMOTE_WORK_LABELS[option] for option in base.REMOTE_OPTIONS if option in base.REMOTE_WORK_LABELS]
    chart_labels = base._chart_labels(lang)

    charts = []
    for remote_label in remote_labels:
        chart_data = salary_box[salary_box["remote_label"] == remote_label]
        if chart_data.empty:
            continue

        workstyle_title = base._workstyle_label(remote_label, lang)
        chart_title = base._text("compensation_experience_chart", lang).format(
            workstyle=workstyle_title[:1].upper() + workstyle_title[1:]
        )
        charts.append(
            (
                base.make_compensation_experience_box_plot(
                    chart_data,
                    "",
                    y_max,
                    theme["remote_colors"].get(remote_label, theme["primary"]),
                    labels=chart_labels,
                    theme=theme,
                ),
                chart_title,
                base._text("compensation_experience_subtitle", lang),
            )
        )

    return pn.Column(
        base._info_markdown(
            f"""
            ### {base._text("compensation_heading", lang)}

            {base._text("compensation_text", lang)}
            """,
            theme=theme,
        ),
        base._chart_grid_box(*charts, ncols=3, theme=theme, compact=True),
        sizing_mode="stretch_width",
    )


@pn.depends(
    redesign_age_selector.param.value,
    redesign_remote_selector.param.value,
    country_count_slider.param.value,
    base.language_selector.param.value,
)
def redesign_country_distribution(selected_ages, selected_remote, country_count, lang):
    theme = base._theme()
    filter_key = _redesign_filter_key(selected_ages, selected_remote)
    available_countries = base._cached_country_map_distribution(filter_key, None)
    available_count = max(len(available_countries), 1)
    if country_count_slider.end != available_count:
        country_count_slider.end = available_count
    if int(country_count) > available_count:
        country_count_slider.value = available_count
        country_count = available_count
    selected_count = min(int(country_count), available_count)
    map_data = base._cached_country_map_distribution(filter_key, selected_count)
    nomadic_count = int((base.BASE_DF["Country"] == "Nomadic").sum())
    nomadic_share = nomadic_count / max(len(base.BASE_DF), 1) * 100
    nomadic_share_label = "<0.1%" if 0 < nomadic_share < 0.1 else f"{nomadic_share:.1f}%"
    chart_labels = base._chart_labels(lang)
    country_count_slider.name = (
        f"Countries shown: {selected_count} of {len(available_countries)}"
        if lang == "EN"
        else f"Países mostrados: {selected_count} de {len(available_countries)}"
    )

    return pn.Column(
        base._info_markdown(
            f"""
            ### {base._text("country_heading", lang)}

            {base._text("country_text", lang)}
            """,
            theme=theme,
        ),
        pn.Row(
            country_count_slider,
            pn.pane.HTML(
                f"""
                <div style="display:inline-flex;align-items:center;gap:10px;background:{theme['surface']};border:1px solid {theme['border']};border-radius:8px;padding:10px 12px;color:{theme['filtered_value']};font-size:15px;">
                  <span style="font-weight:700;color:{theme['text']};">{base._text("nomadic_respondents", lang)}</span>
                  <span>{nomadic_share_label}</span>
                  <span style="color:{theme['muted_soft']};">({nomadic_count:,} {base._text("not_plotted_country", lang)})</span>
                </div>
                """,
                sizing_mode="stretch_width",
            ),
            sizing_mode="stretch_width",
            align="center",
            margin=(0, 0, 8, 0),
        ),
        base._chart_card(
            base.make_country_bubble_map(
                map_data,
                "",
                base.METRIC_MODE,
                height=640,
                labels=chart_labels,
                theme=theme,
            ),
            theme,
            base._text("respondent_map", lang),
            base._text("country_map_subtitle", lang),
        ),
        sizing_mode="stretch_width",
    )


@pn.depends(active_view.param.value, base.language_selector.param.value)
def content(selected: str, lang: str) -> pn.Column:
    theme = base._theme()
    if selected in base.MOMENTUM_OPTIONS:
        view = _technology_view(selected)
    elif selected == "Age and Education":
        view = pn.panel(redesign_age_education, sizing_mode="stretch_width")
    elif selected == "Compensation":
        view = pn.panel(redesign_compensation_experience, sizing_mode="stretch_width")
    else:
        view = pn.panel(redesign_country_distribution, sizing_mode="stretch_width")

    return pn.Column(
        view,
        css_classes=["redesign-view-frame"],
        styles={"background": theme["page_bg"]},
        sizing_mode="stretch_width",
    )


def create_redesign_dashboard() -> pn.Column:
    theme = base._theme()
    return pn.Column(
        _redesign_css(theme),
        sticky_header(),
        fixed_header_spacer(),
        pn.Row(
            navigation_shell,
            pn.Column(
                pn.panel(redesign_kpis, sizing_mode="stretch_width"),
                content,
                sizing_mode="stretch_width",
            ),
            sizing_mode="stretch_width",
            styles={"gap": "16px"},
        ),
        styles={
            "background": theme["page_bg"],
            "color": theme["text"],
            "padding": "0 10px 18px 10px",
            "min-height": "100vh",
        },
        sizing_mode="stretch_width",
        min_width=1200,
    )


dashboard = create_redesign_dashboard()
dashboard.servable(title="Stack Overflow Dashboard Redesign Mockup")
