import tempfile
import time
from multiprocessing import Process
from typing import Optional

import dask.dataframe as dd
import requests

from daskpeeker import Peeker
from daskpeeker.tests.data_for_testing import CATEG_COLS, NUM_COLS, get_test_df

# from dask.distributed import Client, get_client


test_app_default_port = 5677
test_peeker_default_address = f"http://localhost:{test_app_default_port}"


class PeekerRunner:
    def __init__(self, port_no=test_app_default_port, verbose=True):
        self._tmpdir = tempfile.TemporaryDirectory()
        self._port_no = port_no
        self.app_address = f"http://localhost:{port_no}"
        self._process: Optional[Process] = None
        self._verbose = verbose
        # try:
        #    self.client = get_client()
        # except ValueError as e:
        #    print("new client started: ", e)
        #    self.client = Client()
        nparts = 4  # sum(self.client.nthreads().values()

        test_ddf = dd.from_pandas(get_test_df(), npartitions=nparts).persist()

        self.peeker = Peeker(test_ddf, CATEG_COLS, NUM_COLS, self._tmpdir.name)

    def start(self):
        self._process = Process(
            target=self.peeker.app.run_server, kwargs={"port": self._port_no}
        )
        self._process.start()
        while True:
            try:
                requests.get(self.app_address, timeout=5)
                break
            except requests.exceptions.ConnectionError:
                pass
            time.sleep(0.2)

    def stop(self):
        # self.client.shutdown()
        # self.client.close()
        self._process.kill()
        self._tmpdir.cleanup()
