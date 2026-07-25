from __future__ import annotations

import os

import panel as pn


os.environ["PANEL_BOKEH_IMPORT_ONLY"] = "1"

from dashboard_panel_bokeh import app as base  # noqa: E402


pn.extension(sizing_mode="stretch_width")

ACTIVE_VIEW_DEFAULT = "Languages"
TECH_TOP_N = 12
active_view = pn.widgets.TextInput(value=ACTIVE_VIEW_DEFAULT, visible=False)
country_count_slider = pn.widgets.IntSlider(
    name="Countries shown",
    start=1,
    end=base.TOTAL_KPIS["countries"],
    value=12,
    sizing_mode="stretch_width",
)
age_select_all_button = pn.widgets.Button(name="Check All", width=92)
global_reset_button = pn.widgets.Button(name="Reset filters", button_type="primary", width=112)
redesign_age_selector = pn.widgets.MultiChoice(
    name="",
    options=base.AGE_ORDER,
    value=[],
    placeholder="All age groups",
    solid=False,
    width=440,
    max_height=48,
)
redesign_remote_selector = pn.widgets.MultiChoice(
    name="",
    options=base.REMOTE_OPTIONS,
    value=[],
    placeholder="All workstyles",
    solid=False,
    width=440,
    max_height=48,
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
    _sync_redesign_filter_selectors(clear_all=True)


def _selector_value(current, all_options) -> list:
    selected = list(current)
    return [] if set(selected) == set(all_options) else selected


def _sync_redesign_filter_selectors(clear_all: bool = False) -> None:
    global _syncing_redesign_filters
    _syncing_redesign_filters = True
    redesign_age_selector.value = [] if clear_all else _selector_value(base.age_filter.value, base.AGE_ORDER)
    redesign_remote_selector.value = [] if clear_all else _selector_value(base.remote_filter.value, base.REMOTE_OPTIONS)
    _syncing_redesign_filters = False


def _redesign_age_changed(event) -> None:
    if _syncing_redesign_filters:
        return
    if event.new:
        base._set_age_values(event.new)
    else:
        base._set_age_values(base.AGE_ORDER)
    _sync_redesign_filter_selectors(clear_all=not event.new)


def _redesign_remote_changed(event) -> None:
    if _syncing_redesign_filters:
        return
    if event.new:
        base._set_remote_values(event.new)
    else:
        base._set_remote_values(base.REMOTE_OPTIONS)
    _sync_redesign_filter_selectors(clear_all=not event.new)


age_select_all_button.on_click(base.reset_age)
global_reset_button.on_click(_reset_global_filters)
redesign_age_selector.param.watch(_redesign_age_changed, "value")
redesign_remote_selector.param.watch(_redesign_remote_changed, "value")


def _redesign_css(theme: dict) -> pn.pane.HTML:
    return pn.pane.HTML(
        f"""
        <style>
          html,
          body,
          body .bk-root {{
            background: {theme['page_bg']} !important;
          }}
          .redesign-fixed-header-spacer {{
            height: 236px;
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
            height: 108px;
            padding: 10px 14px;
            overflow: hidden;
          }}
          .redesign-filter-title {{
            color: {theme['text']};
            font-size: 14px;
            font-weight: 750;
            letter-spacing: 0.02em;
            text-transform: uppercase;
          }}
          .redesign-filter-label {{
            color: {theme['muted']};
            font-size: 13px;
            font-weight: 700;
            white-space: nowrap;
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
            min-height: 38px !important;
            max-height: 48px !important;
          }}
          .redesign-filter-panel .choices__list--multiple {{
            max-height: 42px !important;
            overflow-y: auto !important;
            overflow-x: hidden !important;
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
            background: {theme['surface']};
            border: 1px solid {theme['border']};
            border-radius: 14px;
            padding: 14px;
            box-shadow: 0 10px 24px rgba(31, 41, 51, 0.06);
          }}
          .redesign-sidebar .bk-btn {{
            justify-content: flex-start;
            text-align: left;
            font-size: 14px;
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


@pn.depends(base.language_selector.param.value)
def filter_bar(lang: str) -> pn.Column:
    global_reset_button.name = base._text("reset_filters", lang)
    redesign_age_selector.placeholder = "All age groups" if lang == "EN" else "Todos los grupos de edad"
    redesign_remote_selector.placeholder = "All workstyles" if lang == "EN" else "Todas las modalidades"
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
                    pn.pane.HTML(f'<span class="redesign-filter-label">{age_label}</span>', width=56),
                    redesign_age_selector,
                    align="center",
                    margin=(0, 24, 0, 0),
                ),
                pn.Row(
                    pn.pane.HTML(f'<span class="redesign-filter-label">{workstyle_label}</span>', width=82),
                    redesign_remote_selector,
                    align="center",
                    margin=(0, 24, 0, 0),
                ),
                global_reset_button,
                pn.Spacer(sizing_mode="stretch_width"),
                sizing_mode="stretch_width",
                align="center",
                height=48,
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
    return pn.Spacer(height=236, css_classes=["redesign-fixed-header-spacer"])


@pn.depends(active_view.param.value, base.language_selector.param.value)
def navigation(selected: str, lang: str) -> pn.Column:
    theme = base._theme()
    sections = [
        base._filter_markdown(
            f"### {'Navigation' if lang == 'EN' else 'Navegacion'}",
            theme=theme,
            margin=(0, 0, 8, 0),
        )
    ]
    for group, views in NAV_GROUPS.items():
        title = group if lang == "EN" else (
            "Comparacion y momentum" if group == "Comparison and Momentum" else "Contexto de encuestados"
        )
        sections.append(base._filter_markdown(f"#### {title}", theme=theme, margin=(8, 0, 4, 0)))
        sections.extend(_nav_button(view, lang) for view in views)

    return pn.Column(
        *sections,
        active_view,
        css_classes=["redesign-sidebar"],
        width=260,
        styles={"color": theme["text"]},
    )


def _technology_view(view_name: str):
    @pn.depends(
        base.age_filter.param.value,
        base.remote_filter.param.value,
        base.language_selector.param.value,
    )
    def view(selected_ages, selected_remote, lang):
        filter_key = base._filter_key(selected_ages, selected_remote, "All countries", TECH_TOP_N)
        return base._technology_momentum_view(filter_key, TECH_TOP_N, view_name, lang, base._theme())

    return pn.panel(view, sizing_mode="stretch_width")


@pn.depends(
    base.age_filter.param.value,
    base.remote_filter.param.value,
    base.language_selector.param.value,
)
def redesign_kpis(selected_ages, selected_remote, lang):
    filter_key = base._filter_key(selected_ages, selected_remote, "All countries", TECH_TOP_N)
    kpis = base._cached_kpis(filter_key)
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
            f"{kpis['countries']:,}",
            base._text("filtered_view", lang),
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
    base.age_filter.param.value,
    base.remote_filter.param.value,
    country_count_slider.param.value,
    base.language_selector.param.value,
)
def redesign_country_distribution(selected_ages, selected_remote, country_count, lang):
    theme = base._theme()
    filter_key = base._filter_key(selected_ages, selected_remote, "All countries", TECH_TOP_N)
    nomadic_context = base._cached_filtered_df(*filter_key)
    available_countries = base._cached_country_map_distribution(filter_key, None)
    selected_count = min(int(country_count), max(len(available_countries), 1))
    map_data = base._cached_country_map_distribution(filter_key, selected_count)
    nomadic_count = int((nomadic_context["Country"] == "Nomadic").sum())
    nomadic_share = nomadic_count / max(len(nomadic_context), 1) * 100
    nomadic_share_label = "<0.1%" if 0 < nomadic_share < 0.1 else f"{nomadic_share:.1f}%"
    chart_labels = base._chart_labels(lang)
    country_count_slider.name = (
        f"Countries shown: {selected_count} of {len(available_countries)}"
        if lang == "EN"
        else f"Paises mostrados: {selected_count} de {len(available_countries)}"
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
        view = pn.panel(base.detailed_age_education, sizing_mode="stretch_width")
    elif selected == "Compensation":
        view = pn.panel(base.detailed_compensation_experience, sizing_mode="stretch_width")
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
        pn.panel(redesign_kpis, sizing_mode="stretch_width"),
        pn.Row(
            navigation,
            content,
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
