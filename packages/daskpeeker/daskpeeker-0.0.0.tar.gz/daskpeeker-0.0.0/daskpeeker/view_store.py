import glob
import json
import os
from dataclasses import dataclass, field

DESCRIPTION_KEY = "peekview-description"


@dataclass
class PeekView:

    name: str
    description: str = ""
    filters: dict = field(default_factory=dict)


@dataclass
class ViewStore:
    root_dir: str
    _views: dict = field(default_factory=dict, init=False)

    def __post_init__(self):
        os.makedirs(self.root_dir, exist_ok=True)
        for jspath in glob.glob(os.path.join(self.root_dir, "*.json")):
            name = os.path.split(jspath)[-1].replace(".json", "")
            with open(jspath) as fp:
                d = json.load(fp)
                desc = d.pop(DESCRIPTION_KEY, "")
                self._views[name] = PeekView(name, desc, d)

    def get(self, view_id):
        return self._views.get(view_id, PeekView(view_id))

    def set(self, view_id, desc, dic):
        d = {DESCRIPTION_KEY: desc, **dic}
        jspath = os.path.join(self.root_dir, f"{view_id}.json")
        with open(jspath, "w") as fp:
            json.dump(d, fp)
        self._views[view_id] = PeekView(view_id, desc, dic)

    def get_all_ids(self):
        return self._views.keys()
