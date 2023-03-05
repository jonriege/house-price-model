"""Test data loading from Statistisk Sentralbyrå"""
import json

import pandas as pd
import pytest

from src.data_loading import load_ssb_table, parse_ssb_data


@pytest.fixture(scope="function")
def ssb_api_output() -> str:
    """Loads example output from SSB API."""
    with open("tests/data/ssb_api_output.json", "r") as f:
        data = f.read()
    return data


def test_load_ssb_table(config: dict):
    """Tests data loading from SSB API."""
    table = "07240"
    query = [
        {
            "code": "Boligtype",
            "selection": {"filter": "item", "values": ["01"]},
        },
        {
            "code": "ContentsCode",
            "selection": {"filter": "item", "values": ["KvPris"]},
        },
    ]
    data = load_ssb_table(config=config, table=table, query=query)
    assert isinstance(data, str)
    data_dict = json.loads(data)
    assert data_dict["source"] == "Statistisk sentralbyrå"


def test_parse_ssb_data(ssb_api_output: str):
    """Tests parsing of SSB API output into DataFrame."""
    df = parse_ssb_data(ssb_api_output=ssb_api_output)
    assert isinstance(df, pd.DataFrame)
    assert df.shape[0] == 1
    assert df.loc[0, "value"] == 44599
