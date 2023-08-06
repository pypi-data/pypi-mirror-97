# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Utility methods for interacting with azureml.dataprep."""
import logging
from typing import Any, cast, List, NoReturn, Union

import numpy as np
import pandas as pd
from azureml._common._error_definition import AzureMLError
from azureml.automl.core.dataprep_utilities import is_dataflow, Dataflow
from azureml.automl.core.shared import logging_utilities
from azureml.automl.core.shared._diagnostics.automl_error_definitions import (ContentModified,
                                                                              Data,
                                                                              DatabaseQuery,
                                                                              DataPathInaccessible,
                                                                              DataPathNotFound,
                                                                              DataprepScriptExecution,
                                                                              DataprepStepTranslation,
                                                                              DataprepValidation,
                                                                              DatasetFileRead,
                                                                              DatastoreNotFound,
                                                                              InputDatasetEmpty,
                                                                              InsufficientMemory,
                                                                              MissingSecrets)
from azureml.automl.core.shared.exceptions import (AutoMLException,
                                                   ClientException,
                                                   ConfigException,
                                                   DataException,
                                                   ResourceException)
from azureml.automl.core.shared.reference_codes import ReferenceCodes
import azureml.dataprep as dprep
from azureml.dataprep import DataPrepException as DprepException

logger = logging.getLogger(__name__)

# DPrep exceptions currently can't be converted to ErrorResponses, hence the mapping below.
DATAPREP_ERROR_MAP = {
    "Validation": DataprepValidation,
    "StreamAccess.NotFound": DataPathNotFound,
    "StreamAccess.Authentication": DataPathInaccessible,
    # We've timed out on reading the data from the storage account.
    "StreamAccess.TimeoutExpired": DatasetFileRead,
    "StreamAccess.ContentModified": ContentModified,
    "ScriptExecution.StreamAccess": DataprepScriptExecution,
    "DatastoreResolution.NotFound": DatastoreNotFound,
    "ScriptExecution.DatastoreResolution": DataprepScriptExecution,
    "ScriptExecution.Transformation": DataprepScriptExecution,
    "ScriptExecution.ReadDataFrame": DataprepScriptExecution,
    "ScriptExecution.DatabaseQuery": DatabaseQuery,
    "ScriptExecution.Database": DataprepScriptExecution,
    "StepTranslation": DataprepStepTranslation,
    # This shouldn't happen once we've migrated completely to rely on TabularDatasets, since the credentials are
    # handled automatically by the Dataset infra.
    "MissingSecrets": MissingSecrets,
}


def materialize_dataflow(dataflow: Dataflow, as_numpy: bool = False) -> Union[pd.DataFrame, np.ndarray]:
    """
    Materializes the dataflow as a pandas DataFrame by fetching all the underlying data at once.
    If `as_numpy` is set to True, an ndarray is returned instead

    :param dataflow: The dataflow to retrieve
    :type: azureml.dataprep.Dataflow
    :param as_numpy: If the data needs to be materialized as a numpy array
    :return: Either a pandas DataFrame, or a numpy ndarray
    """
    if not is_dataflow(dataflow):
        return dataflow

    try:
        pandas_df = dataflow.to_pandas_dataframe(on_error='null', out_of_range_datetime='fail')
        if pandas_df is None or pandas_df.empty:
            # todo: `target` can be more specific here. Refactor to pass it in from the caller.
            raise DataException._with_error(
                AzureMLError.create(
                    InputDatasetEmpty, target="training_data",
                    reference_code=ReferenceCodes._DATAPREP_UTILITIES_MATERIALIZE_DATA_EMPTY
                )
            )
        if as_numpy:
            if pandas_df.shape[1] == 1:
                # if the DF is a single column ensure the resulting output is a 1 dim array by converting
                # to series first.
                return cast(np.ndarray, pandas_df[pandas_df.columns[0]].values)
            return cast(np.ndarray, pandas_df.values)

        return pandas_df
    except AutoMLException:
        raise
    except DprepException as e:
        dataprep_error_handler(e)
    except MemoryError as e:
        raise ResourceException._with_error(
            AzureMLError.create(
                InsufficientMemory,
                reference_code=ReferenceCodes._DATAPREP_UTILITIES_MATERIALIZE_DATA_MEMORY,
            ), inner_exception=e) from e
    except Exception as e:
        logging_utilities.log_traceback(e, logger)
        # at this point we don't know what went wrong, so raising a system error
        raise DataException._with_error(
            AzureMLError.create(Data, target="materialize_dataflow", error_details=str(e),
                                reference_code=ReferenceCodes._DATAPREP_UTILITIES_MATERIALIZE_DATA),
            inner_exception=e
        ) from e


def retrieve_numpy_array(dataflow: Any) -> np.ndarray:
    """Retrieve pandas dataframe from dataflow and return underlying ndarray.

    param dataflow: The dataflow to retrieve
    type: azureml.dataprep.Dataflow
    return: The retrieved np.ndarray, or the original dataflow value when it is of incorrect type
    """
    return materialize_dataflow(dataflow, as_numpy=True)


def retrieve_pandas_dataframe(dataflow: Any) -> pd.DataFrame:
    """Retrieve pandas dataframe from dataflow.

    param dataflow: The dataflow to retrieve
    type: azureml.dataprep.Dataflow
    return: The retrieved pandas DataFrame, or the original dataflow value when it is of incorrect type
    """
    return materialize_dataflow(dataflow)


def resolve_cv_splits_indices(cv_splits_indices: List[dprep.Dataflow]) -> List[List[np.ndarray]]:
    """Resolve cv splits indices.

    param cv_splits_indices: The list of dataflow where each represents a set of split indices
    type: list(azureml.dataprep.Dataflow)
    return: The resolved cv_splits_indices, or the original passed in value when it is of incorrect type
    """
    if cv_splits_indices is None:
        return None
    cv_splits_indices_list = []
    for split in cv_splits_indices:
        if not is_dataflow(split):
            return cv_splits_indices
        else:
            is_train_list = materialize_dataflow(split, as_numpy=True)
            train_indices = []
            valid_indices = []
            for i in range(len(is_train_list)):
                if is_train_list[i] == 1:
                    train_indices.append(i)
                elif is_train_list[i] == 0:
                    valid_indices.append(i)
            cv_splits_indices_list.append(
                [np.array(train_indices), np.array(valid_indices)])
    return cv_splits_indices_list


def dataprep_error_handler(e: DprepException) -> NoReturn:
    """Handle dataprep errors.

    param e: The exception raised by dataprep service
    type: DprepException
    """
    generic_msg = 'Failed to get data from DataPrep. ErrorCode: {0}. Message: {1}'.format(
        e.error_code, getattr(e, 'compliant_message', ''))
    logger.error(generic_msg)
    if "OutOfMemory" in e.error_code:
        raise ResourceException._with_error(AzureMLError.create(InsufficientMemory,), inner_exception=e) from e
    for error_substring in DATAPREP_ERROR_MAP:
        if error_substring in e.error_code:
            error = AzureMLError.create(DATAPREP_ERROR_MAP[error_substring], dprep_error=str(e))
            raise ConfigException(azureml_error=error, inner_exception=e)
    raise ClientException.from_exception(e).with_generic_msg(generic_msg)
