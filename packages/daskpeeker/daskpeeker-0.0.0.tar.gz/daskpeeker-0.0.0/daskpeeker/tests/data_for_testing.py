import random

import faker
import numpy as np
import pandas as pd

CATEG_COLS = ["c1", "c2"]
NUM_COLS = ["n1", "n2", "nlog", "nlog2"]


def get_test_df(n=500, seed=42069):

    fake = faker.Faker()
    np.random.seed(seed)
    faker.Faker.seed(seed)

    cs1 = [fake.name() for _ in range(7)]
    cs2 = [np.random.randint(10000) for _ in range(10)]

    return pd.DataFrame(
        {
            CATEG_COLS[0]: random.choices(cs1, k=n),
            CATEG_COLS[1]: random.choices(cs2, k=n),
            NUM_COLS[0]: np.random.rand(n),
            NUM_COLS[1]: np.random.randint(10000, size=n),
            NUM_COLS[2]: np.random.lognormal(8, 3, size=n),
            NUM_COLS[3]: np.random.lognormal(0, 10, size=n).astype(int),
        }
    )
