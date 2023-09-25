"""Test model training and validation."""
from unittest.mock import mock_open, patch

import pandas as pd
import pytest
from statsmodels.tsa.ar_model import AutoReg
from statsmodels.tsa.base.tsa_model import TimeSeriesModel

from app.model import (
    get_model_class,
    get_model_forecast,
    serialize_timeseries,
    store_data_and_model_preds,
    train_validate_model,
    validate_model_performance,
)


@pytest.fixture(scope="function")
def data() -> pd.Series:
    """Generates dummy data for testing model training."""
    data = pd.Series(range(100))
    index = pd.date_range(start="28/04/1996", periods=100, freq="Q")
    data.index = index
    return data


def test_get_model_class(config: dict):
    """Tests getting model class from config."""
    config["model"]["class"] = "auto_regression"
    cls = get_model_class(config=config)
    assert cls == AutoReg

    config["model"]["class"] = "unknown_model"
    with pytest.raises(ValueError):
        get_model_class(config=config)


def test_validate_model_performance(config: dict, data: pd.Series):
    """Tests model validation."""
    config["model"]["class"] = "auto_regression"
    config["model"]["kwargs"] = {"lags": 1}
    metrics = validate_model_performance(config=config, data=data)
    assert isinstance(metrics, pd.Series)
    assert pd.api.types.is_float_dtype(metrics)
    assert all(metrics >= 0.0)


def test_train_validate_model(data: pd.Series, config: dict):
    """Tests model training and validation."""
    model, mape = train_validate_model(config=config, data=data)
    assert isinstance(model, TimeSeriesModel)
    assert isinstance(mape, float)
    assert mape >= 0.0


def test_get_model_forecast(config: dict, data: pd.Series):
    """Tests getting the model forecast."""
    config["model"]["horizon"] = 8
    model = AutoReg(endog=data, lags=1)
    forecast_mean, forecast_ci = get_model_forecast(config=config, model=model)
    assert isinstance(forecast_mean, pd.Series)
    assert isinstance(forecast_ci, pd.DataFrame)
    assert len(forecast_mean) == 9
    assert len(forecast_ci) == 9


def test_timeseries_serialization(data: pd.Series):
    """Tests serialization of timeseries."""
    serialized = serialize_timeseries(data)
    assert len(serialized) == len(data)
    for item in serialized:
        assert isinstance(item["date"], str)
        assert isinstance(item["value"], float)


def test_store_data_and_model_preds(config: dict, data: pd.Series):
    """Tests storage of model data."""
    model = AutoReg(endog=data, lags=1)
    mape = 0.0
    m = mock_open()
    with patch(target="builtins.open", new=m):
        store_data_and_model_preds(
            config=config, data=data, model=model, mape=mape
        )
    m.assert_called_once()
