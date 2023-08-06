from typing import TYPE_CHECKING

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from .elem_ids import ElemIds, SidedId
from .style import (
    CONTENT_STYLE,
    CONTENT_STYLE_HIDDEN,
    DEFAULT_VIEW_NAME,
    LEFT_COLOR,
    RIGHT_COLOR,
    SIDEBAR_HIDDEN,
    SIDEBAR_STYLE,
    colors,
)
from .util import table_from_pandas

if TYPE_CHECKING:
    from .default_report import DefaultReport
    from .peeker_class import Peeker


def add_base_layout_to_app(
    app: dash.Dash, peeker: "Peeker", default: "DefaultReport"
):

    navbar = _get_navbar(peeker.view_store.get_all_ids())
    sidebar = _get_sidebar(peeker)

    content = html.Div(
        _get_report_layout(peeker, default),
        id=ElemIds.main_content,
        style=CONTENT_STYLE,
    )

    app.layout = html.Div(
        [
            dcc.Store(id=ElemIds.click_store),
            dcc.Location(id=ElemIds.url),
            navbar,
            sidebar,
            content,
        ],
    )
    add_sidebar_callback(app)


def add_sidebar_callback(app):
    @app.callback(
        [
            Output(ElemIds.sidebar, "style"),
            Output(ElemIds.main_content, "style"),
            Output(ElemIds.click_store, "data"),
        ],
        [Input(ElemIds.sidebar_button, "n_clicks")],
        [
            State(ElemIds.click_store, "data"),
        ],
    )
    def toggle_sidebar(n, nclick):
        if n:
            if nclick == "SHOW":
                sidebar_style = SIDEBAR_HIDDEN
                content_style = CONTENT_STYLE_HIDDEN
                cur_nclick = "HIDDEN"
            else:
                sidebar_style = SIDEBAR_STYLE
                content_style = CONTENT_STYLE
                cur_nclick = "SHOW"
        else:
            sidebar_style = SIDEBAR_STYLE
            content_style = CONTENT_STYLE
            cur_nclick = "SHOW"

        return sidebar_style, content_style, cur_nclick


def _get_navbar(all_views):

    return dbc.Navbar(
        children=html.Div(
            [
                html.Div(
                    dbc.Button(
                        "Toggle Filters",
                        color="secondary",
                        className="mr-1",
                        id=ElemIds.sidebar_button,
                    ),
                    className="col-md-2",
                ),
                *_get_dd("Left Column", ElemIds.left.dd, all_views),
                *_get_dd("Right Column", ElemIds.right.dd, all_views),
            ],
            className="row w-100",
        ),
        color="dark",
        dark=True,
        fixed="top",
    )


def _get_dd(label, id_, options):
    return [
        html.Div(
            html.H2(label, style={"color": "white"}),
            className="col-md-2",
            style={"padding-top": 6},
        ),
        html.Div(
            dcc.Dropdown(
                options=[{"value": x, "label": x} for x in options],
                id=id_,
            ),
            className="col-md-3",
        ),
    ]


def _get_sidebar(peeker):
    return html.Div(
        children=dbc.Tabs(
            [
                dbc.Tab(
                    children=_get_filter_tab(peeker, ind),
                    label=DEFAULT_VIEW_NAME,
                    label_style={
                        "color": color,
                        "font-weight": "bold",
                        "padding": 18,
                    },
                    id=side.tab,
                )
                for color, side, ind in zip(colors, ElemIds.sides(), range(2))
            ],
            className="w-100",
        ),
        id=ElemIds.sidebar,
        style=SIDEBAR_STYLE,
    )


def _get_filter_tab(peeker, ind):

    side_ids = ElemIds.sides()[ind]
    elems = _get_filter_tab_top(side_ids)

    for col in peeker.cat_filter_cols:
        options = peeker.default_values[col]
        filter_id = peeker.id_repo.get_filter_id(col, ind)
        elems.append(_get_cat_filter_elem(col, options, options, filter_id))

    for col in peeker.num_filter_cols:
        filter_id = peeker.id_repo.get_filter_id(col, ind)
        selected = peeker.default_values[col]
        binends = peeker.num_ranges[col]
        elems.append(_get_num_filter_elem(col, binends, selected, filter_id))

    elems.append(html.Div(className="row", style={"height": 100}))
    return html.Div(elems, className="container")


def _get_filter_tab_top(side_id: SidedId):
    return [
        html.Div(
            [
                html.Div(html.H4("View Name:"), className="col-md-3"),
                html.Div(
                    dcc.Input(
                        value=DEFAULT_VIEW_NAME,
                        id=side_id.name_input,
                        maxLength=23,
                    ),
                    className="col-md-9",
                ),
            ],
            className="row",
            style={"padding": 10},
        ),
        html.Div(
            [
                html.Div(html.H4("View Description:"), className="col-md-12"),
                html.Div(
                    dcc.Textarea(
                        className="w-100",
                        id=side_id.desc_input,
                    ),
                    className="col-md-12",
                ),
            ],
            className="row",
            style={"padding": 10},
        ),
        html.Div(
            [
                html.Div(
                    dbc.Button(
                        "Save View", color="success", id=side_id.save_button
                    ),
                    className="col-md-3",
                ),
                html.Div(
                    dbc.Button(
                        "Apply Filters",
                        color="primary",
                        id=side_id.apply_button,
                    ),
                    className="col-md-3",
                ),
                html.Div(
                    dbc.Button(
                        "Delete View", color="danger", id=side_id.del_button
                    ),
                    className="col-md-3",
                ),
            ],
            className="d-flex justify-content-center row",
        ),
        html.Hr(),
    ]


def _get_report_layout(peeker, default):
    # TODO make these categories renamable
    report_bases = [
        html.Div(
            html.Div(
                [
                    html.Div(
                        html.H2(name),
                        className="row w-100",
                        style={"margin": 35},
                    ),
                    html.Div(
                        children=fun(peeker, default),
                        className="d-flex justify-content-center row",
                    ),
                ],
                className="col-md-12",
            ),
            className="row",
        )
        for name, fun in zip(
            ["Metrics", "Shared Figures", "Standalone Figures", "Tables"],
            [
                _get_metrics_base,
                _get_shared_figs_base,
                _get_so_figs_base,
                _get_tables_base,
            ],
        )
    ]

    return html.Div(
        report_bases
        + [
            dcc.Store(id=side_id.saved_view_option_store)
            for side_id in ElemIds.sides()
        ],
        className="container-fluid",
    )


def _get_metrics_base(peeker: "Peeker", default: "DefaultReport"):
    table_rows = [
        html.Tr(
            [
                html.Th(),
                html.Th(
                    DEFAULT_VIEW_NAME,
                    style={"color": LEFT_COLOR},
                    id=ElemIds.left.metric_table_header,
                ),
                html.Th(
                    DEFAULT_VIEW_NAME,
                    style={"color": RIGHT_COLOR},
                    id=ElemIds.right.metric_table_header,
                ),
                html.Th("Diff"),
            ]
        )
    ]

    for m in default.default_metrics:
        v = m.value
        mid = peeker.id_repo.new_metric_id(m.name)
        table_rows.append(
            html.Tr(
                [
                    html.Td(html.B(m.name)),
                    html.Td(v, id=mid.left),
                    html.Td(v, id=mid.right),
                    html.Td(id=mid.diff),
                ]
            )
        )

    return html.Div(
        html.Table(table_rows),
        className="d-flex justify-content-center col-md-12",
    )


def _get_shared_figs_base(peeker: "Peeker", default: "DefaultReport"):
    fig_divs = []
    for fig_elem in default.shared_figures:
        trace = default.get_default_trace(fig_elem.name)
        trace.name = DEFAULT_VIEW_NAME
        trace.marker.color = LEFT_COLOR
        trace2 = type(trace)(trace)
        fig = fig_elem.fig
        fig.add_trace(trace)
        trace2.marker.color = RIGHT_COLOR
        fig.add_trace(trace2)
        fig_id = peeker.id_repo.new_shared_fig_id(fig_elem.name)
        fig_divs.append(
            html.Div(
                [
                    dcc.Graph(figure=fig, id=fig_id.id_),
                    dcc.Store(data=trace, id=fig_id.left),
                    dcc.Store(data=trace2, id=fig_id.right),
                ],
                className=f"col-md-{fig_elem.col_width}",
            )
        )

    return fig_divs


def _get_so_figs_base(peeker: "Peeker", default: "DefaultReport"):

    so_figs = []
    for i, fig_elem in enumerate(default.default_standalone_figures):
        fig_id = peeker.id_repo.new_so_fig_id(f"so-fig-{i}")
        for id_, color in zip(fig_id, colors):
            so_figs.append(
                html.Div(
                    dcc.Graph(figure=fig_elem.fig, id=id_),
                    className=f"col-md-{fig_elem.col_width}",
                    style={
                        "border-color": color,
                        "border-style": "solid",
                        "border-radius": "10px",
                        "padding": 4,
                    },
                )
            )

    return so_figs


def _get_tables_base(peeker: "Peeker", default: "DefaultReport"):
    table_divs = []
    for i, table_elem in enumerate(default.default_tables):
        table_id = peeker.id_repo.new_table_id(f"tabl-{i}")
        table_divs += [
            html.Div(id=table_id.diff, className="col-md-4"),
            *[
                html.Div(
                    table_from_pandas(table_elem.df),
                    id=id_,
                    className="col-md-4",
                    style={
                        "border-color": color,
                        "border-style": "solid",
                        "border-radius": "10px",
                        "padding": 4,
                    },
                )
                for color, id_ in zip(colors, table_id)
            ],
        ]
    return table_divs


def _get_cat_filter_elem(col, choices, selected, filter_id):

    chlist = dcc.Checklist(
        id=filter_id.id_,
        options=[{"label": v, "value": v} for v in choices],
        value=selected,
        labelStyle={"margin": 3},
        inputStyle={"margin": 3},
    )
    toggle_but = dbc.Button("Toggle", id=filter_id.toggle, className="mr-2")

    return html.Div(
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            html.H4(col.replace("_", " ").title()),
                            className="col-md-9",
                        ),
                        html.Div(toggle_but, className="col-md-3"),
                    ],
                    className="row",
                ),
                chlist,
                html.Hr(),
            ],
        ),
        className="col-md-12",
        style={"padding": 7},
    )


def _get_num_filter_elem(col, choices, selected, filter_id):
    n = len(choices) - 1
    slider = dcc.RangeSlider(
        id=filter_id.id_,
        min=0,
        max=n,
        value=selected or [0, n],
        marks={
            i: _format_slider_v(v)
            for i, v in enumerate(choices)
            if (i % 2 == 0) or (i == n)
        },
    )

    return html.Div(
        html.Div(
            [
                html.H4(col.replace("_", " ").title()),
                slider,
                html.Hr(),
            ],
        ),
        className="col-md-12",
        style={"padding": 3},
    )


def _format_slider_v(v):
    if v < 10:
        return "{:.2f}".format(float(v))
    return str(int(v))
