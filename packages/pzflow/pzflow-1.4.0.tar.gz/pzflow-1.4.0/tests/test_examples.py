import jax.numpy as np
import pandas as pd
from pzflow import examples
from pzflow import Flow


def test_load_two_moons_data():
    data = examples.two_moons_data()
    assert isinstance(data, pd.DataFrame)
    assert data.shape == (10000, 2)


def test_load_galaxy_data():
    data = examples.galaxy_data()
    assert isinstance(data, pd.DataFrame)
    assert data.shape == (100000, 7)


def test_load_example_flow():
    flow = examples.example_flow()
    assert isinstance(flow, Flow)
    assert isinstance(flow.info, str)

    samples = flow.sample(2)
    flow.log_prob(samples)

    grid = np.arange(0, 2.5, 0.5)
    flow.posterior(samples, column="redshift", grid=grid)
