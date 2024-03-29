"""Pytest fixtures shared by all test modules"""
import pytest

from app.utils import load_config


@pytest.fixture(scope="function")
def config() -> dict:
    return load_config()
