# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import numpy as np

from azureml.automl.core.shared.constants import Tasks

from .materialized_tabular_data_validator import MaterializedTabularDataValidator


class TimeseriesMaterializedTabularDataValidator(MaterializedTabularDataValidator):
    """
    Validator for validating the materialized tabular data for a timeseries task.
    """
    def __init__(self, primary_metric: str) -> None:
        """
        Construct a TimeseriesMaterializedTabularDataValidator to validate the tabular data.
        :param primary_metric: The metric to optimize for.
        """
        super(TimeseriesMaterializedTabularDataValidator, self).__init__(
            task_type=Tasks.FORECASTING,
            primary_metric=primary_metric,
            is_onnx_enabled=False,
            is_featurization_required=True
        )

    # override
    def _check_target_column(self, y: np.ndarray) -> None:
        """
        Validate the time / grain column.

        :param y: The input target column to validate
        :return: None
        """
        # TODO: Move timeseries specific time/grain column validations here
        pass
