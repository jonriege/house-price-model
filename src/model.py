"""Training and validating the forecasting model"""
from typing import Any

import pandas as pd
from sklearn.metrics import mean_absolute_percentage_error
from sklearn.model_selection import TimeSeriesSplit
from statsmodels.tsa.ar_model import AutoReg
from statsmodels.tsa.base.tsa_model import TimeSeriesModel


def get_model_class(config: dict) -> type[TimeSeriesModel]:
    """Returns the statsmodels class for the forecasting model.

    Args:
        config: Config

    Returns:
        Model class for forecasting model
    """
    model_str = config["model"]["class"]
    if model_str == "auto_regression":
        return AutoReg
    else:
        raise ValueError(f"'{model_str}' is not recognized as a model class.")


def validate_model_performance(
    data: pd.Series, model_class: type[TimeSeriesModel], model_kwargs: Any
) -> pd.Series:
    """Validates model performance with MAPE and time series cross-validation.

    Run 5-fold time series cross validation, calculating mean absolute
    percentage error (MAPE) for each fold. Each fold uses observations up to 2
    years in the future (i.e. 8 observations) for validation.

    Args:
        data: Time series data for training and validation
        model_class: Statsmodels model class
        model_kwargs: Model configuration

    Returns:
        MAPE per fold
    """
    tscv = TimeSeriesSplit(n_splits=5, test_size=8)
    metrics = []
    for train_idx, test_idx in tscv.split(data):
        train = data.iloc[train_idx]
        test = data.iloc[test_idx]
        model = model_class(endog=train, **model_kwargs).fit()
        pred = model.predict(start=test_idx[0], end=test_idx[-1])
        mape = mean_absolute_percentage_error(y_true=test, y_pred=pred)
        metrics.append(mape)
    return pd.Series(data=metrics, name="MAPE")


def train_validate_model(
    config: dict, data: pd.Series
) -> tuple[TimeSeriesModel, float]:
    """Trains the forecasting model and validate its performance.

    Args:
        config: Config
        data: Time series data

    Returns:
        Fitted forecasting model, avg. MAPE across validation folds
    """
    model_class = get_model_class(config=config)
    model_kwargs = config["model"]["kwargs"]
    model = model_class(endog=data, **model_kwargs)
    mape = validate_model_performance(
        data=data, model_class=model_class, model_kwargs=model_kwargs
    )
    return model, mape.mean()
