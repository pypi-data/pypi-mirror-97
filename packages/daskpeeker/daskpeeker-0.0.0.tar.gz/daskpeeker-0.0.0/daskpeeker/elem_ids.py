from typing import Iterable


class _IdBase:
    def __init__(self, name, suffix=None):
        self.name = name
        self.id_ = (
            name.replace(" ", "-") + "-" + (suffix or type(self).__name__)
        ).lower()


class _ReportElemIdBase(_IdBase):
    @property
    def left(self):
        return f"{self.id_}-left"

    @property
    def right(self):
        return f"{self.id_}-right"

    @property
    def diff(self):
        return f"{self.id_}-diff"

    def __iter__(self):
        yield self.left
        yield self.right

    def __getitem__(self, key):
        return [self.left, self.right][key]


class MetricId(_ReportElemIdBase):
    pass


class SharedFigId(_ReportElemIdBase):
    pass


class SoFigureId(_ReportElemIdBase):
    pass


class TableId(_ReportElemIdBase):
    pass


class FilterId(_IdBase):
    @property
    def toggle(self):
        return f"{self.id_}-toggle"


class IdRepo:
    def __init__(self):
        self.report_elem_ids = []
        self.filter_ids = {0: [], 1: []}

    def new_metric_id(self, metric_name):
        return self._new_id_type(metric_name, MetricId)

    def new_shared_fig_id(self, fig_name):
        return self._new_id_type(fig_name, SharedFigId)

    def new_so_fig_id(self, fig_name):
        return self._new_id_type(fig_name, SoFigureId)

    def new_table_id(self, name):
        return self._new_id_type(name, TableId)

    def new_filter_id(self, name):
        self.filter_ids[0].append(FilterId(name, "left"))
        self.filter_ids[1].append(FilterId(name, "right"))

    def get_filter_id(self, col, ind):
        for fid in self.filter_ids[ind]:
            if fid.name == col:
                return fid

    @property
    def shared_fig_ids(self):
        return [
            eid for eid in self.report_elem_ids if isinstance(eid, SharedFigId)
        ]

    @property
    def metric_ids(self):
        return [
            eid for eid in self.report_elem_ids if isinstance(eid, MetricId)
        ]

    @property
    def table_ids(self):
        return [
            eid for eid in self.report_elem_ids if isinstance(eid, TableId)
        ]

    def _new_id_type(self, name, kls):
        new_id = kls(name)
        self.report_elem_ids.append(new_id)
        return new_id


class SidedId:
    def __init__(self, side):
        self.dd = f"dd-{side}"
        self.tab = f"tab-{side}"

        self.name_input = f"name-{side}"
        self.desc_input = f"desc-{side}"

        self.save_button = f"save-button-{side}"
        self.del_button = f"del-button-{side}"
        self.apply_button = f"apply-button-{side}"

        self.saved_view_option_store = f"option-store-{side}"

        self.metric_table_header = f"metric-table-header-{side}"


class ElemIds:

    navbar = "navbar"
    sidebar = "sidebar"
    main_content = "main-content"

    sidebar_button = "sidebar-toggle"
    url = "url"
    click_store = "click-store"

    left = SidedId("left")
    right = SidedId("right")

    @classmethod
    def sides(cls) -> Iterable[SidedId]:
        return [cls.left, cls.right]

    @classmethod
    def is_dd(cls, prop_id):
        return SidedId("").dd in prop_id
