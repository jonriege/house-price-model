"""Training and validating the forecasting model"""
from typing import Any

import pandas as pd
from sklearn.metrics import mean_absolute_percentage_error
from sklearn.model_selection import TimeSeriesSplit
from statsmodels.tsa.base.tsa_model import TimeSeriesModel


def validate_model_performance(
    data: pd.Series, model_class: type[TimeSeriesModel], model_kwargs: Any
) -> pd.Series:
    """Validate model performance with MAPE and time series cross-validation.

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
