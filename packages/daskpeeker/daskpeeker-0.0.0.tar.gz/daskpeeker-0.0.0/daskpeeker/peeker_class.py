"""
TODO:
- use conf intervals of metrics (maybe groups of metrics)
- prep for gunicorn
- publish
- some pattern detection in remaining data
  - isolation forest ?
  - DBSCAN


## TESTS:

change name, add some filter, press apply button
  - updates shared fig / metric header names, updates report, updates tab label

change name, add some filter, press save button
  - updates shared fig / metric header names, updates report, updates tab label
  - updates one dd value, updates both dd options, saves json

- updates to correct new name - input vs dep

- proper update on dd select

"""

import time
from functools import reduce
from operator import and_
from typing import List, Union

import dash
import dash_html_components as html
import dask.dataframe as dd
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
from pyinstrument import Profiler
from structlog import get_logger

from .default_report import DefaultReport
from .elem_ids import (
    ElemIds,
    IdRepo,
    MetricId,
    SharedFigId,
    SoFigureId,
    TableId,
)
from .peeker_layout import add_base_layout_to_app
from .report_classes import (
    Metric,
    SharedFigure,
    SharedTrace,
    StandaloneFigure,
    Table,
)
from .style import LEFT_COLOR, RIGHT_COLOR, colors
from .util import (
    get_app_base,
    log_profiler,
    pandas_from_table,
    table_from_pandas,
)
from .view_store import ViewStore

logger = get_logger()


class Peeker:
    """
    API for creating and launching a peeker app

    create a subclass and properly define get_shared_figures
    and get_report_elems
    """
    def __init__(
        self,
        app_data: dd.DataFrame,
        cat_filter_cols: List[str] = None,
        num_filter_cols: List[str] = None,
        view_store_dir: str = None,
        use_profiler=False,
        range_resolution=11,
    ):
        self.ddf = app_data
        self.cat_filter_cols = cat_filter_cols or []
        self.num_filter_cols = num_filter_cols or []
        self.id_repo = IdRepo()

        self.default_values = {}
        self.num_ranges = {}
        self._set_filter_bases(range_resolution)

        self.view_store = ViewStore(view_store_dir or "./view_store_data")

        self.app = get_app_base(__name__)

        add_base_layout_to_app(
            self.app,
            self,
            DefaultReport(
                self.get_report_elems(self.ddf) or [],
                self.get_shared_figures() or [],
            ),
        )

        self._add_callbacks()

        self._timing = use_profiler

    def run(self, port_no=5666, host="0.0.0.0", debug=True):
        self.app.run_server(host=host, port=port_no, debug=debug)

    def get_shared_figures(self) -> List[SharedFigure]:
        """overwrite this function

        returns a list of figures that provides a frame for
        the shared traces from get_anal_elems
        """

        return [
            SharedFigure(go.Figure(layout=go.Layout(title=c.title())), c)
            for c in self.cat_filter_cols
        ]

    def get_report_elems(
        self, filtered_ddf: dd.DataFrame
    ) -> List[Union[Metric, SharedTrace, StandaloneFigure, Table]]:
        """overwrite this function

        returns analysis elements
        """
        elems = [
            Metric(filtered_ddf.shape[0].compute(), "Size"),
            Table(filtered_ddf.head(3).iloc[:, :3]),
        ]

        if self.num_filter_cols:
            c = self.num_filter_cols[0]
            elems.append(
                Metric(filtered_ddf.loc[:, c].mean().compute(), f"Average {c}")
            )

        for c in self.cat_filter_cols:
            s = filtered_ddf.loc[:, c].value_counts().compute()
            elems.append(
                SharedTrace(go.Bar(x=s.index.tolist(), y=s.tolist()), c)
            )

        if self.cat_filter_cols and self.num_filter_cols:
            c = self.cat_filter_cols[0]
            nc = self.num_filter_cols[0]
            s = filtered_ddf.groupby(c)[nc].mean().compute()
            elems.append(
                StandaloneFigure(
                    go.Figure(data=[go.Bar(x=s.index.tolist(), y=s.tolist())])
                )
            )

        return elems

    def _set_filter_bases(self, range_resolution):
        for col in self.cat_filter_cols:
            self.id_repo.new_filter_id(col)
            self.default_values[col] = sorted(
                self.ddf.loc[:, col].drop_duplicates().compute().tolist()
            )

        for col in self.num_filter_cols:
            self.id_repo.new_filter_id(col)
            binends = (
                self.ddf.loc[:, col]
                .quantile(np.linspace(0, 1, range_resolution))
                .compute()
                .drop_duplicates()
                .tolist()
            )
            selected = [0, len(binends) - 1]
            self.default_values[col] = selected
            self.num_ranges[col] = binends

    def _add_callbacks(self):

        self._add_saving_callbacks()
        self._add_report_callbacks()
        self._add_dd_callbacks()
        self._add_metric_diff_callbacks()
        self._add_shared_trace_callbacks()
        self._add_table_diff_callbacks()

    def _add_saving_callbacks(self):

        for ind, side_id in enumerate(ElemIds.sides()):
            self.app.callback(
                Output(side_id.dd, "value"),
                Output(side_id.saved_view_option_store, "data"),
                Input(side_id.save_button, "n_clicks"),
                State(side_id.name_input, "value"),
                State(side_id.desc_input, "value"),
                *self._get_filter_states(ind),
                prevent_initial_call=True,
            )(self._save_side)

        @self.app.callback(
            Output(ElemIds.left.dd, "options"),
            Output(ElemIds.right.dd, "options"),
            Input(ElemIds.left.saved_view_option_store, "data"),
            Input(ElemIds.right.saved_view_option_store, "data"),
            prevent_initial_call=True,
        )
        def add_option(_, __):
            options = [
                {"value": x, "label": x} for x in self.view_store.get_all_ids()
            ]
            return options, options

    def _add_report_callbacks(self):

        for ind, side_id in enumerate(ElemIds.sides()):
            self.app.callback(
                Output(side_id.metric_table_header, "children"),
                Output(side_id.tab, "label"),
                *self._get_report_output_dependencies(ind),
                Input(side_id.apply_button, "n_clicks"),
                State(side_id.dd, "value"),
                State(side_id.name_input, "value"),
                *self._get_filter_states(ind),
                prevent_initial_call=True,
            )(self._report_from_filters)

    def _add_dd_callbacks(self):
        for ind, side_id in enumerate(ElemIds.sides()):

            @self.app.callback(
                Output(side_id.apply_button, "n_clicks"),
                Output(side_id.name_input, "value"),
                Output(side_id.desc_input, "value"),
                *[
                    Output(fid.id_, "value")
                    for fid in self._get_filter_ids(ind)
                ],
                Input(side_id.dd, "value"),
                *[
                    Input(fid.toggle, "n_clicks")
                    for fid in self._get_cat_filter_ids(ind)
                ],
                State(side_id.name_input, "value"),
                State(side_id.desc_input, "value"),
                *[self._get_filter_states(ind)],
                prevent_initial_call=True,
            )
            def update_vals(view_id, *toggles_values):

                name = toggles_values[self._n_cat_filters]
                desc = toggles_values[self._n_cat_filters + 1]

                # toggles = toggles_values[: self._n_cat_filters]
                _vindl = self._n_cat_filters + 2
                values = list(toggles_values[_vindl:])
                n_clicks = 0

                for elem in dash.callback_context.triggered:
                    if ElemIds.is_dd(elem["prop_id"]):
                        n_clicks = 1
                        peek_view = self.view_store.get(
                            view_id or "Unnamed View"
                        )
                        name = peek_view.name
                        desc = peek_view.description
                        for i, fid in enumerate(self._get_filter_ids(ind)):
                            col = fid.name
                            values[i] = peek_view.filters.get(
                                col, self.default_values[col]
                            )
                    if elem["prop_id"].endswith(".n_clicks"):
                        nclicks = elem["value"]
                        col, f_ind = self._get_toggle_col_and_ind(
                            elem["prop_id"]
                        )
                        if nclicks % 2 == 0:
                            nuvals = self.default_values[col]
                        else:
                            nuvals = []
                        values[f_ind] = nuvals

                return (n_clicks, name, desc, *values)

    def _add_metric_diff_callbacks(self):
        for mid in self._get_metric_ids():

            @self.app.callback(
                Output(mid.diff, "children"),
                Output(mid.diff, "style"),
                Input(mid.left, "children"),
                Input(mid.right, "children"),
            )
            def update_mdiff(val1, val2):
                nv1 = float(val1 or "nan")
                nv2 = float(val2 or "nan")
                m = (abs(nv1) + abs(nv2)) / 2

                color = colors[int(nv1 < nv2)]

                diff = "+ {:.02f}%".format(abs(nv1 - nv2) * 100 / m)

                return diff, {"color": color}

    def _add_shared_trace_callbacks(self):
        for shid in self._get_shared_report_ids():

            @self.app.callback(
                Output(shid.id_, "figure"),
                Input(shid.left, "data"),
                Input(shid.right, "data"),
                State(shid.id_, "figure"),
                prevent_initial_call=True,
            )
            def update_shared_fig(trace1, trace2, fig):
                for trace, ntrace in zip(fig["data"], [trace1, trace2]):
                    trace.update(ntrace)
                return fig

    def _add_table_diff_callbacks(self):
        for tabid in self._get_table_ids():

            @self.app.callback(
                Output(tabid.diff, "children"),
                Input(tabid.left, "children"),
                Input(tabid.right, "children"),
            )
            def update_tabdiff(tab1, tab2):
                df1 = pandas_from_table(tab1)
                dfi1 = df1.iterrows()
                dfi2 = pandas_from_table(tab2).iterrows()

                recs = []
                for (i1, r1), (i2, r2) in zip(dfi1, dfi2):
                    recs.append(
                        [
                            html.B(e1)
                            if (e1 == e2)
                            else [
                                html.Span(e1, style={"color": LEFT_COLOR}),
                                html.B(" vs "),
                                html.Span(e2, style={"color": RIGHT_COLOR}),
                            ]
                            for e1, e2 in zip(r1, r2)
                        ]
                    )

                return table_from_pandas(
                    pd.DataFrame(recs, columns=df1.columns)
                )

    def _save_side(
        self,
        _,
        name,
        desc,
        *side_filter_vals,
    ):

        d = {}
        for fid, val in zip(self._get_filter_ids(), side_filter_vals):
            d[fid.name] = val
        self.view_store.set(name, desc, d)

        return name, list(self.view_store.get_all_ids())

    def _report_from_filters(
        self, n_clicks, dd_name, input_name, *filter_values
    ):

        if n_clicks == 0:
            raise ValueError("no true report request, only toggle")

        stime = time.time()
        name = input_name
        for elem in dash.callback_context.triggered:
            if ElemIds.is_dd(elem["prop_id"]):
                name = dd_name

        logger.info("start filtering")
        if self._timing:
            logger.info("starting time profiling")
            profiler = Profiler()
            profiler.start()

        filtered_ddf = self._filter_ddf(filter_values)

        logger.info("calculating elements")
        elems = self.get_report_elems(filtered_ddf)
        logger.info(f"{len(elems)} elements returned")

        logger.info("parsing elements to output values")
        outputs = self._parse_report_elems_to_outputs(elems, name)
        logger.info(f"{len(outputs)} outputs parsed")
        logger.info("report done", runtime=round(time.time() - stime, 3))

        if self._timing:
            profiler.stop()
            log_profiler(profiler, logger, 20)

        return (name, name, *outputs)

    def _filter_ddf(self, filter_values):
        filt_series = []

        for fval, col in zip(filter_values, self._filter_cols):
            s = self.ddf.loc[:, col]
            if col in self.cat_filter_cols:
                new_filt_series = s.isin(fval)
            else:
                num_range = self.num_ranges[col]
                vmin = num_range[fval[0]]
                vmax = num_range[fval[1]]
                new_filt_series = (s >= vmin) & (s <= vmax)

            filt_series.append(new_filt_series)

        return self.ddf.loc[reduce(and_, filt_series), :]

    def _parse_report_elems_to_outputs(self, elems, name):

        metric_out = []
        shared_out = []
        so_out = []
        table_out = []

        for elem in elems:
            if isinstance(elem, Metric):
                # TODO conf interval here
                metric_out.append(elem.value)
            if isinstance(elem, SharedTrace):
                trace = elem.trace
                trace.name = name
                shared_out.append(trace)
            if isinstance(elem, StandaloneFigure):
                so_out.append(elem.fig)
            if isinstance(elem, Table):
                table_out.append(table_from_pandas(elem.df))
        return [*metric_out, *shared_out, *so_out, *table_out]

    def _get_filter_ids(self, ind=0):
        return self.id_repo.filter_ids[ind]

    def _get_cat_filter_ids(self, ind=0):
        return [
            fid
            for fid in self.id_repo.filter_ids[ind]
            if fid.name in self.cat_filter_cols
        ]

    def _get_filter_states(self, ind):
        return [State(fid.id_, "value") for fid in self._get_filter_ids(ind)]

    def _get_toggle_col_and_ind(self, prop_id):
        for i, (fidl, fidr) in enumerate(
            zip(*self.id_repo.filter_ids.values())
        ):
            if prop_id.startswith(fidl.toggle) or prop_id.startswith(
                fidr.toggle
            ):
                return fidr.name, i

    def _get_shared_report_ids(self):
        return self.id_repo.shared_fig_ids

    def _get_metric_ids(self):
        return self.id_repo.metric_ids

    def _get_table_ids(self):
        return self.id_repo.table_ids

    def _get_report_output_dependencies(self, ind):

        outputs = []
        for eid in self.id_repo.report_elem_ids:
            if isinstance(eid, (MetricId, TableId)):
                outputs.append(Output(eid[ind], "children"))
            if isinstance(eid, SharedFigId):
                outputs.append(Output(eid[ind], "data"))
            if isinstance(eid, SoFigureId):
                outputs.append(Output(eid[ind], "figure"))
        return outputs

    @property
    def _n_shared_states(self):
        return len(self.id_repo.shared_fig_ids)

    @property
    def _n_cat_filters(self):
        return len(self.cat_filter_cols)

    @property
    def _filter_cols(self):
        return [*self.cat_filter_cols, *self.num_filter_cols]
