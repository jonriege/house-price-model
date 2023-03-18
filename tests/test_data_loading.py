"""Test data loading from Statistisk Sentralbyrå"""
import json

import pandas as pd
import pytest

from src.data_loading import (
    _generate_ssb_query,
    _load_ssb_table,
    _parse_ssb_data,
    load_house_prices,
)


@pytest.fixture(scope="function")
def ssb_api_output() -> str:
    """Loads example output from SSB API."""
    with open("tests/data/ssb_api_output.json", "r") as f:
        data = f.read()
    return data


@pytest.fixture(scope="function")
def ssb_api_query() -> str:
    """Loads example query for SSB API."""
    with open("tests/data/ssb_api_query.json", "r") as f:
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
    data = _load_ssb_table(config=config, table=table, query=query)
    assert isinstance(data, str)
    data_dict = json.loads(data)
    assert data_dict["source"] == "Statistisk sentralbyrå"


def test_parse_ssb_data(ssb_api_output: str):
    """Tests parsing of SSB API output into DataFrame."""
    df = _parse_ssb_data(ssb_api_output=ssb_api_output)
    assert isinstance(df, pd.DataFrame)
    assert df.shape[0] == 1
    assert df.loc[0, "value"] == 44599


def test_generating_ssb_query(config: dict, ssb_api_query: str):
    """Tests generating SSB query."""
    query_config = config["data_loading"]["house_prices"]["query"]
    query_generated = _generate_ssb_query(query_config=query_config)
    assert isinstance(query_generated, list)
    ssb_api_query = json.loads(ssb_api_query)
    for gen_clause, correct_clause in zip(query_generated, ssb_api_query):
        assert gen_clause == correct_clause


def test_load_house_prices(config: dict):
    """Tests loading of house prices."""
    df = load_house_prices(config=config)
    columns = ["boligtype", "statistikkvariabel", "kvartal", "value"]
    assert isinstance(df, pd.DataFrame)
    assert set(columns).issubset(df.columns)
