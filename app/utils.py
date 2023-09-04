"""Utility functions used by other modules"""

import os

import yaml

SRC_PATH = os.path.abspath(os.path.dirname(__file__))
CONFIG_REL_PATH = "config.yaml"


def load_config() -> dict:
    """Loads config.yaml into a dict.

    Returns:
        A dict with the content of config.yaml.
    """
    config_path = os.path.join(SRC_PATH, CONFIG_REL_PATH)
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
    return config
