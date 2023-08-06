# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Fix the dtypes after the infertence."""
from typing import Optional, cast, List, Any

import numpy as np
import pandas as pd
from azureml._common._error_definition import AzureMLError
from azureml.automl.core.shared._diagnostics.automl_error_definitions import (
    TimeseriesDfInvalidValOfNumberTypeInTestData)
from azureml.automl.core.shared.constants import TimeSeriesInternal
from azureml.automl.core.shared.forecasting_exception import ForecastingDataException
from azureml.automl.core.shared.logging_utilities import function_debug_log_wrapped
from azureml.automl.core.shared.reference_codes import ReferenceCodes
from azureml.automl.runtime.shared.time_series_data_frame import TimeSeriesDataFrame

from ..automltransformer import AutoMLTransformer


class RestoreDtypesTransformer(AutoMLTransformer):
    """Restore the dtypes of numerical data types."""

    def __init__(self,
                 tsdf: TimeSeriesDataFrame) -> None:
        """
        Construct for RestoreDtypesTransformer.

        :param tsdf: The initial time series data frame before
                     transforms application.
        :type tsdf: azureml.automl.runtime.shared.time_series_data_frame.TimeSeriesDataFrame
        """
        super().__init__()
        self._target_column = tsdf.ts_value_colname  # type: Optional[str]
        # The actual fit have to happen in the constructor
        # because during fit-transform the dataframe will be modified
        # and the dtypes will be changed.
        col_na = set()
        for col in tsdf.columns:
            if all([pd.isna(val) for val in tsdf[col]]):
                col_na.add(col)
        if len(col_na) == tsdf.shape[1]:
            # Nothing to do, the types can not be determined.
            self._dtypes = None  # type: Optional[pd.Series]
            return
        # We do not want to fix the type of dummy order column.
        col_na.add(TimeSeriesInternal.DUMMY_ORDER_COLUMN)
        x_no_na = tsdf[list(set(tsdf.columns.values).difference(col_na))]
        self._dtypes = x_no_na.dtypes

    @function_debug_log_wrapped('info')
    def fit(self,
            x: TimeSeriesDataFrame,
            y: Optional[np.ndarray] = None) -> 'RestoreDtypesTransformer':
        """
        Fit function for RestoreDtypesTransformer.

        :param x: Input data.
        :type x: azureml.runtime.core.shared.time_series_data_frame.TimeSeriesDataFrame
        :param y: Unused.
        :type y: numpy.ndarray
        :return: Class object itself.
        """
        return self

    @function_debug_log_wrapped('info')
    def transform(self,
                  x: TimeSeriesDataFrame) -> TimeSeriesDataFrame:
        """
        Transform the data frame.

        :param x: Input data.
        :type x: azureml.automl.runtime.shared.time_series_data_frame.TimeSeriesDataFrame
        :return: The data frame with correct dtypes.
        """
        # Ensure the data types are the same as before featurization
        # for numeric columns.
        if self._dtypes is None:
            return x
        for col in self._dtypes.index:
            if col == self._target_column:
                # Skip the type for target column
                continue
            if not type(self._dtypes[col]).__module__.startswith('pandas') and \
                    np.issubdtype(self._dtypes[col], np.number) and col in x.columns:
                try:
                    # We should not set value to int type to be safe to NaN in the test set.
                    x[col] = x[col].astype('float')
                except ValueError:
                    raise ForecastingDataException._with_error(
                        AzureMLError.create(TimeseriesDfInvalidValOfNumberTypeInTestData, target='x',
                                            reference_code=ReferenceCodes._TSDF_INV_VAL_OF_NUMBER_TYPE_IN_TEST_DATA,
                                            column=col)
                    )
        return x

    def get_non_numeric_columns(self) -> List[Any]:
        """
        Return the list of caegorical columns.

        :return: The list of categorical columns.
        """
        if self._dtypes is None:
            return []

        def filter_fun(x):
            """The function to filter columns."""
            return type(cast(pd.Series, self._dtypes)[x]).__module__.startswith('pandas') or\
                not np.issubdtype(cast(pd.Series, self._dtypes)[x], np.number)

        return list(
            filter(
                filter_fun,
                self._dtypes.index))
