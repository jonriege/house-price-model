"""Test data loading from Statistisk Sentralbyrå"""

from src.data_loading import load_ssb_table


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
    assert data["source"] == "Statistisk sentralbyrå"
