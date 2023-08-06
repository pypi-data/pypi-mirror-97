from dataclasses import dataclass, field
from typing import Union

import pandas as pd
import plotly.graph_objects as go
from plotly.basedatatypes import BaseTraceHierarchyType


@dataclass
class Metric:
    value: Union[int, str]
    name: str
    confidence_interval: list = field(default_factory=list)


@dataclass
class StandaloneFigure:
    fig: go.Figure
    col_width: int = 6


@dataclass
class SharedFigure:
    fig: go.Figure
    name: str
    col_width: int = 6


@dataclass
class SharedTrace:
    trace: BaseTraceHierarchyType
    figure_name: str


@dataclass
class Table:
    df: pd.DataFrame
