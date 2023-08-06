from functools import reduce
from operator import and_

import dash
import dash_html_components as html
import pandas as pd

bt_root = "https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/"

external_stylesheets = [
    "https://codepen.io/chriddyp/pen/bWLwgP.css",
    f"{bt_root}css/bootstrap.min.css",
    f"{bt_root}css/bootstrap-theme.min.css",
    "https://use.fontawesome.com/releases/v5.7.2/css/all.css",
]

external_scripts = [f"{bt_root}js/bootstrap.min.js"]


def get_app_base(name=__name__, suppress_cbe=False):
    return dash.Dash(
        name,
        external_stylesheets=external_stylesheets,
        external_scripts=external_scripts,
        suppress_callback_exceptions=suppress_cbe,
    )


def table_from_pandas(df):
    index_name = df.index.name
    headers = []
    if index_name:
        headers.append(index_name)
    rows = [html.Tr([html.Th(c) for c in [*headers, *df.columns]])]

    for ind, r in df.iterrows():
        elems = []
        if index_name:
            elems.append(ind)
        rows.append(html.Tr([html.Td(e) for e in [*elems, *r]]))
    return html.Table(rows)


def pandas_from_table(tabdic):
    rows = tabdic["props"]["children"]
    colnames = [td["props"]["children"] for td in rows[0]["props"]["children"]]
    records = [
        [td["props"]["children"] for td in row["props"]["children"]]
        for row in rows[1:]
    ]

    return pd.DataFrame(records, columns=colnames)


def get_profile_df(profiler, topn=15):
    to_drop = [
        "tornado",
        "IPython",
        "ipython",
        "ipykernel",
        "runpy.py",
        "asyncio",
        "werkzeug/",
        "flask/",
        "dash/",
        "socketserver.py",
        "threading.py",
        "http/server",
        "importlib",
        "dask/",
    ]
    return (
        pd.DataFrame(
            [
                {
                    "time": r[1],
                    **dict(zip(["function", "file", "line"], p.split("\x00"))),
                }
                for r in profiler.frame_records
                for p in r[0]
            ]
        )
        .loc[
            lambda df: reduce(
                and_, [~df["file"].str.contains(s) for s in to_drop]
            )
        ]
        .assign(
            pend=lambda df: df["file"].str.split("/").str[-4:].str.join("/")
        )
        .groupby(["pend", "line", "function"])
        .sum()
        .nlargest(topn, "time")
    )


def log_profiler(profiler, logger, topn=15):
    for (path, line_no, function), r in get_profile_df(
        profiler, topn
    ).iterrows():
        logger.info(
            "profiled period top",
            duration=r["time"],
            function=function,
            path=path,
            line_no=line_no,
        )
