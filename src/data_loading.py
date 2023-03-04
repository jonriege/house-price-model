"""Loading of data from Statistisk Sentralbyrå"""

from requests import post


def load_ssb_table(config: dict, table: str, query: list[dict]) -> dict:
    """Loads data from SSB API.

    Args:
      config: Config
      table: ID of the table to load.
      query: Query specifying what data to load from the table
        (see https://www.ssb.no/en/api/api-eksempler-pa-kode).

    Returns:
        Data returned by SSB API.
    """
    url = config["data_loading"]["ssb_api_url"] + table
    payload = {"query": query, "response": {"format": "json-stat2"}}
    response = post(url, json=payload)
    response.raise_for_status()
    return response.json()
