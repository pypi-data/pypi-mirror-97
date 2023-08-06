# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Dynamic feature suggestions."""

from typing import Any, Dict, List, Optional, Tuple

import logging
import os

import pandas as pd
from azureml.automl.core.featurization import FeaturizationConfig
from azureml.automl.runtime._engineered_feature_names import _GenerateEngineeredFeatureNames
from azureml.automl.runtime.column_purpose_detection import StatsAndColumnPurposeType, ColumnPurposeSweeper
from azureml.automl.runtime.shared.types import DataSingleColumnInputType, TransformerType
from sklearn.pipeline import make_pipeline, Pipeline

logger = logging.getLogger(__name__)


def perform_feature_sweeping(
        task: str,
        X: pd.DataFrame,
        y: DataSingleColumnInputType,
        stats_and_column_purposes: List[StatsAndColumnPurposeType],
        all_new_column_names: List[str],
        engineered_featurenames_generator_and_holder: _GenerateEngineeredFeatureNames,
        featurization_config: Optional[FeaturizationConfig] = None,
        enable_feature_sweeping: bool = True,
        feature_sweeping_timeout: int = 60,
        is_cross_validation: bool = True,
        enable_dnn: bool = True,
        force_text_dnn: bool = False,
        feature_sweeping_config: Dict[str, Any] = {},
        working_dir: Optional[str] = None,
        feature_sweeper: Optional[Any] = None) -> List[TransformerType]:
    """
    Perform feature sweeping and return transforms.

    :param task: Task type.
    :param X: Input data.
    :param y: Input labels.
    :param stats_and_column_purposes: Statistics and column purposes.
    :param all_new_column_names: New column names merged with existing ones.
    :param engineered_featurenames_generator_and_holder: Engineered feature names generator and holder.
    :param featurization_config: Custom featurization configuration if provided by the user.
    :param enable_feature_sweeping: If feature sweeping is enabled.
    :param feature_sweeping_timeout: Feature sweeping timeout.
    :param is_cross_validation: If the current scenario is cross validation based.
    :param enable_dnn: If DNN is enabled.
    :param force_text_dnn: If DNN is to be forced.
    :param feature_sweeping_config: Feature sweeping configuration.
    :param working_dir: Working directory.
    :param feature_sweeper: Custom feature sweeper.
    :return: List of transformers to be applied on specific columns with alias name.
    """
    transforms = []  # type: List[TransformerType]

    try:
        if enable_feature_sweeping:
            logger.info("Performing feature sweeping")
            from azureml.automl.runtime.sweeping.meta_sweeper import MetaSweeper

            if feature_sweeper is None:
                feature_sweeper = MetaSweeper(task=task,
                                              timeout_sec=feature_sweeping_timeout,
                                              is_cross_validation=is_cross_validation,
                                              featurization_config=featurization_config,
                                              enable_dnn=enable_dnn,
                                              force_text_dnn=force_text_dnn,
                                              feature_sweeping_config=feature_sweeping_config)

            sweeped_transforms = feature_sweeper.sweep(working_dir or os.getcwd(),
                                                       X, y,
                                                       stats_and_column_purposes)

            if sweeped_transforms:
                added_transformers = ','.join(map(get_added_transformer_from_sweeped_transform, sweeped_transforms))
                logger.info('Sweeping added the following transforms: {}'.format(added_transformers))

                cols_list = []  # type: List[str]
                for cols, tfs in sweeped_transforms:
                    if not isinstance(cols, list):
                        stats_and_column_purpose = next((x for x in stats_and_column_purposes if x[2] == cols))
                        column_purpose = stats_and_column_purpose[1]
                        index = stats_and_column_purposes.index(stats_and_column_purpose)
                        new_column_name = all_new_column_names[index]
                        cols_list = [str(new_column_name)]
                    else:
                        for col in cols:
                            stats_and_column_purpose = next((x for x in stats_and_column_purposes if x[2] == col))
                            # Assumption here is that all the columns in the list will be of one type
                            column_purpose = stats_and_column_purpose[1]
                            index = stats_and_column_purposes.index(stats_and_column_purpose)
                            new_column_name = all_new_column_names[index]
                            cols_list.append(new_column_name)

                    column_name_alias = engineered_featurenames_generator_and_holder.\
                        get_alias_name_from_pipeline_object(cols_list, tfs, column_purpose)

                    transforms.append((cols,
                                       make_pipeline(tfs),
                                       {"alias": str(column_name_alias)}))
            else:
                logger.info('Sweeping did not add any transformers.')

        else:
            logger.info("Feature sweeping disabled.")
    except Exception:
        logger.info("Sweeping failed with an error.")
    finally:
        return transforms


def get_added_transformer_from_sweeped_transform(sweeped_transform: Tuple[str, Pipeline]) -> str:
    """
    Get the name of a transformer added during feature sweeping.

    :param sweeped_transform: A tuple containing the pipeline with the transformer in it generated by the MetaSweeper.
    :return: The name of the transformer object.
    """
    pipeline = sweeped_transform[1]
    return _pipeline_name_(pipeline)


def _pipeline_name_(pipeline: Pipeline) -> str:
    """
    Method for extracting the name of the last transformer in a pipeline.

    :param pipeline: The input pipeline.
    :return: The name of the last transformer or 'Unknown' if pipeline is None.
    """
    if pipeline is not None:
        if isinstance(pipeline, Pipeline):
            return type(pipeline.steps[-1][1]).__name__
        return type(pipeline).__name__

    return "Unknown"
