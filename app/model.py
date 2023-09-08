"""Training and validating the forecasting model"""
import json

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


def validate_model_performance(config: dict, data: pd.Series) -> pd.Series:
    """Validates model performance with MAPE and time series cross-validation.

    Run 5-fold time series cross validation, calculating mean absolute
    percentage error (MAPE) for each fold. Each fold uses observations up to 2
    years in the future (i.e. 8 observations) for validation. This is controlled
    via the 'horizon' variable in the model config.

    Args:
        config: Config
        data: Time series data for training and validation

    Returns:
        MAPE per fold
    """
    model_class = get_model_class(config=config)
    tscv = TimeSeriesSplit(n_splits=5, test_size=config["model"]["horizon"])
    metrics = []
    for train_idx, test_idx in tscv.split(data):
        train = data.iloc[train_idx]
        test = data.iloc[test_idx]
        model = model_class(endog=train, **config["model"]["kwargs"]).fit()
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
    mape = validate_model_performance(config=config, data=data)
    return model, mape.mean()


def get_model_forecast(
    config: dict, model: TimeSeriesModel
) -> tuple[pd.Series, pd.DataFrame]:
    """Gets the mean prediction and confidence interval of the model.

    Args:
        config: config
        model: Forecasting model object with data

    Returns:
        Forecast mean, forecast 95% confidence interval
    """
    res = model.fit()
    data_len = res.nobs + model.hold_back
    n_pred = config["model"]["horizon"]
    forecast = res.get_prediction(start=data_len - 1, end=data_len + n_pred - 1)
    return forecast.predicted_mean, forecast.conf_int()


def serialize_timeseries(series: pd.Series) -> list[dict[str, float]]:
    """Serializes a pandas DatetimeIndex.

    Args:
        series: Pandas series with DatetimeIndex

    Returns:
        List of dicts with date and value
    """
    if not isinstance(series.index, pd.DatetimeIndex):
        raise ValueError("Date index must be a DatetimeIndex to be serialized.")
    return [
        {
            "date": date.strftime("%Y-%m-%d"),  # type: ignore
            "value": float(value),
        }
        for date, value in series.items()
    ]


def store_data_and_model_preds(
    config: dict, data: pd.Series, model: TimeSeriesModel, mape: float
) -> None:
    """Stores data and model predictions to display on the website.

    Args:
        config: Config
        data: Time series data
        model: Model object with data
        mape: Mean absolute percentage error of model
    """
    forecast_mean, forecast_ci = get_model_forecast(config=config, model=model)
    data_and_preds = {
        "data": serialize_timeseries(series=data),
        "model": {
            "mape": mape,
            "forecast_mean": serialize_timeseries(series=forecast_mean),
            "forecast_ci": {
                "upper": serialize_timeseries(series=forecast_ci.upper),
                "lower": serialize_timeseries(series=forecast_ci.lower),
            },
        },
    }
    with open(config["app"]["data_path"], "w") as file:
        json.dump(data_and_preds, file, indent=4)
