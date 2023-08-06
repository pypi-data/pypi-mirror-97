from typing import TYPE_CHECKING, Iterable

from .report_classes import Metric, SharedTrace, StandaloneFigure, Table

if TYPE_CHECKING:
    from .peeker_class import Peeker  # noqa: F401


class DefaultReport:
    def __init__(self, elems, shared_figures):

        self.shared_figures = shared_figures
        self.default_elems = elems

        self._traces = {
            e.figure_name: e.trace for e in elems if isinstance(e, SharedTrace)
        }

    @property
    def default_metrics(self) -> Iterable[Metric]:
        return self._get_type_elem(Metric)

    @property
    def default_standalone_figures(self) -> Iterable[StandaloneFigure]:
        return self._get_type_elem(StandaloneFigure)

    @property
    def default_tables(self) -> Iterable[Table]:
        return self._get_type_elem(Table)

    def get_default_trace(self, figname):
        return self._traces[figname]

    def _get_type_elem(self, kls):
        return [e for e in self.default_elems if isinstance(e, kls)]
