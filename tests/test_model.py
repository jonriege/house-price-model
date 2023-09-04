"""Test model training and validation."""
import pandas as pd
import pytest
from statsmodels.tsa.ar_model import AutoReg
from statsmodels.tsa.base.tsa_model import TimeSeriesModel

from app.model import (
    get_model_class,
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


def test_validate_model_performance(data: pd.Series):
    """Tests model validation."""
    model_class = AutoReg
    model_kwargs = {"lags": 1}
    metrics = validate_model_performance(
        data=data, model_class=model_class, model_kwargs=model_kwargs
    )
    assert isinstance(metrics, pd.Series)
    assert pd.api.types.is_float_dtype(metrics)
    assert all(metrics >= 0.0)


def test_train_validate_model(data: pd.Series, config: dict):
    """Tests model training and validation."""
    model, mape = train_validate_model(config=config, data=data)
    assert isinstance(model, TimeSeriesModel)
    assert isinstance(mape, float)
    assert mape >= 0.0
