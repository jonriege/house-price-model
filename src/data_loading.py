"""Loading of data from Statistisk Sentralbyrå"""

import warnings

import pandas as pd
from pyjstat import pyjstat
from requests import post


def load_house_prices(config: dict) -> pd.DataFrame:
    """Loads annual sqm prices for existing dwellings.

    Args:
        config: Config

    Returns:
    """
    table = config["data_loading"]["house_prices"]["table"]
    query_config = config["data_loading"]["house_prices"]["query"]
    query = generate_ssb_query(query_config=query_config)
    ssb_api_output = load_ssb_table(config=config, table=table, query=query)
    return parse_ssb_data(ssb_api_output=ssb_api_output)


def load_ssb_table(config: dict, table: str, query: list[dict]) -> str:
    """Loads data from SSB API.

    Args:
        config: Config
        table: ID of the table to load.
        query: Query specifying what data to load from the table
            (see https://www.ssb.no/en/api/api-eksempler-pa-kode).

    Returns:
        Data returned by SSB API in string format.
    """
    url = config["data_loading"]["ssb_api_url"] + table
    payload = {"query": query, "response": {"format": "json-stat2"}}
    response = post(url, json=payload)
    response.raise_for_status()
    return response.text


def generate_ssb_query(query_config: list[dict]) -> list[dict]:
    """Generates a query with the format read by the SSB API.

    Args:
        query_config: List of selection filters.

    Returns:
        Dictionary with the selection formatted as an SSB API query.
    """
    query = []
    for item in query_config:
        query.append(
            {
                "code": item["key"],
                "selection": {
                    "filter": item["filter"],
                    "values": item["values"],
                },
            }
        )
    return query


def parse_ssb_data(ssb_api_output: str) -> pd.DataFrame:
    """Parses data from SSB API and converts it to a DataFrame.

    Args:
        ssb_api_output: JSON-stat formatted data returned by SSB API.

    Returns:
        Data converted to a pandas DataFrame.
    """
    dataset = pyjstat.Dataset.read(ssb_api_output)

    # The pyjstat library has a bug where a DeprecationWarning is raised when
    # converting the Dataset object to a DataFrame using .write(), although
    # there is no other way to perform this operation.
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        df = dataset.write("dataframe")
    return df
