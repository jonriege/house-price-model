"""Test utility functions."""


def test_load_config(config: dict):
    """Tests loading of config.yaml"""
    assert isinstance(config, dict)
    assert "data_loading" in config
