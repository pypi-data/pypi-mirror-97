# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Static featurizer suggestions."""

from typing import Any, cast, List, Optional

import logging
import math

from azureml.automl.core.constants import (
    _OperatorNames,
    _TransformerOperatorMappings,
    FeatureType,
    SupportedTransformersInternal)
from azureml.automl.core.featurization import FeaturizationConfig
from azureml.automl.core.shared import constants, logging_utilities
from azureml.automl.runtime._engineered_feature_names import (
    _FeatureTransformers,
    _GenerateEngineeredFeatureNames,
    _TransformerParamsHelper,
    _Transformer)
from azureml.automl.runtime.featurizer.transformer import (AutoMLTransformer, CategoricalFeaturizers,
                                                           DateTimeFeaturizers, DateTimeFeaturesTransformer,
                                                           featurization_utilities, GenericFeaturizers, get_ngram_len,
                                                           max_ngram_len, TextFeaturizers, TFIDF_VECTORIZER_CONFIG)

from azureml.automl.runtime.shared.types import DataSingleColumnInputType, TransformerType

UNSUPPORTED_PARAMETER_WARNING_MSG = "Unsupported parameter passed to {t}, proceeding with default values"

logger = logging.getLogger(__name__)


def get_drop_column_transform(
        column_name: str,
        column_purpose: str,
        engineered_featurenames_generator_and_holder: _GenerateEngineeredFeatureNames
) -> List[TransformerType]:
    """
    Get featurizers for case of columns being dropped.

    :param column_name: Column name.
    :param column_purpose: Column purpose or feature type.
    :param engineered_featurenames_generator_and_holder: Engineered feature names generator and holder.
    :return: List of transformers to be applied on specific columns with alias name.
    """
    tr = []  # type:  List[TransformerType]

    # Add the transformations to be done and get the alias name
    # for the drop transform.
    drop_transformer = _Transformer(parent_feature_list=[str(column_name)],
                                    transformation_fnc=SupportedTransformersInternal.Drop,
                                    operator=None,
                                    feature_type=column_purpose,
                                    should_output=True)
    # Create an object to convert transformations into JSON object
    feature_transformers = _FeatureTransformers([drop_transformer])

    # Create the JSON object
    json_obj = feature_transformers.encode_transformations_from_list()
    # Persist the JSON object for later use
    engineered_featurenames_generator_and_holder.get_raw_feature_alias_name(json_obj)
    return tr


def get_categorical_hash_transforms(
        column: str,
        column_name: str,
        num_unique_categories: int,
        engineered_featurenames_generator_and_holder: _GenerateEngineeredFeatureNames,
        featurization_config: Optional[FeaturizationConfig] = None,
) -> List[TransformerType]:
    """
    Create a list of transforms for categorical hash data.

    :param column: The column in the data frame.
    :param column_name: Name of the column.
    :param num_unique_categories: Number of unique categories.
    :param engineered_featurenames_generator_and_holder: Engineered feature names generator and holder.
    :param featurization_config: Custom featurization configuration.
    :return: List of transformers to be applied on specific columns with alias name.
    """
    # Add the transformations to be done and get the alias name
    # for the hashing one hot encode transform.
    tr = []  # type:  List[TransformerType]

    transformer_fncs = [SupportedTransformersInternal.StringCast,
                        SupportedTransformersInternal.HashOneHotEncoder]

    # Check whether the transformer functions are in blocked list
    if featurization_config is not None:
        transformers_in_blocked_list = featurization_utilities \
            .transformers_in_blocked_list(transformer_fncs, featurization_config.blocked_transformers)
        if transformers_in_blocked_list:
            logger.info("Excluding blocked transformer(s): {0}".format(transformers_in_blocked_list))
            return tr

    string_cast = TextFeaturizers.string_cast()

    transformer_params = featurization_utilities.get_transformer_params_by_column_names(
        SupportedTransformersInternal.HashOneHotEncoder, [column], featurization_config)

    try:
        # TODO: update HashOneHotVectorizerTransformer to accept number_of_bits instead of num_cols
        if transformer_params.get("number_of_bits"):
            number_of_bits = transformer_params.pop("number_of_bits")
        else:
            number_of_bits = int(math.log(num_unique_categories, 2))
        num_cols = pow(2, number_of_bits)
        hashonehot_vectorizer = CategoricalFeaturizers.hashonehot_vectorizer(
            **{
                'hashing_seed_val': constants.hashing_seed_value,
                'num_cols': int(num_cols)
            }
        )
        if len(transformer_params) > 0:
            logger.warning("Ignoring unsupported parameters")
    except Exception as e:
        logging_utilities.log_traceback(e, logger, is_critical=False)
        logger.warning(
            UNSUPPORTED_PARAMETER_WARNING_MSG.format(t=SupportedTransformersInternal.HashOneHotEncoder)
        )
        hashonehot_vectorizer = CategoricalFeaturizers.hashonehot_vectorizer(
            **{
                'hashing_seed_val': constants.hashing_seed_value,
                'num_cols': int(pow(2, int(math.log(num_unique_categories, 2))))
            }
        )

    categorical_hash_string_cast_transformer = _Transformer(
        parent_feature_list=[str(column_name)],
        transformation_fnc=transformer_fncs[0],
        operator=None,
        feature_type=FeatureType.CategoricalHash,
        should_output=False)
    # This transformation depends on the previous transformation
    categorical_hash_onehot_encode_transformer = _Transformer(
        parent_feature_list=[1],
        transformation_fnc=transformer_fncs[1],
        operator=None,
        feature_type=None,
        should_output=True,
        transformer_params=_TransformerParamsHelper.to_dict(hashonehot_vectorizer))
    # Create an object to convert transformations into JSON object
    feature_transformers = \
        _FeatureTransformers(
            [categorical_hash_string_cast_transformer,
             categorical_hash_onehot_encode_transformer])

    # Create the JSON object
    json_obj = feature_transformers.encode_transformations_from_list()

    # Persist the JSON object for later use and obtain an alias name
    alias_column_name = engineered_featurenames_generator_and_holder.get_raw_feature_alias_name(json_obj)

    # Add the transformations to be done and get the alias name
    # for the raw column.

    tr = [(column, [string_cast, hashonehot_vectorizer], {'alias': str(alias_column_name)})]
    return tr


def get_datetime_transforms(
        column: str,
        column_name: str,
        engineered_featurenames_generator_and_holder: _GenerateEngineeredFeatureNames,
        featurization_config: Optional[FeaturizationConfig] = None,
) -> List[TransformerType]:
    """
    Create a list of transforms for datetime data.

    :param column: The column in the data frame.
    :param column_name: Name of the column.
    :param engineered_featurenames_generator_and_holder: Engineered feature names generator and holder.
    :param featurization_config: Custom featurization configuration.
    :return: List of transformers to be applied on specific columns with alias name.
    """
    cat_imputer = CategoricalFeaturizers.cat_imputer(
        **{
            **featurization_utilities.get_transformer_params_by_column_names(
                SupportedTransformersInternal.CatImputer, [column], featurization_config)
        })
    string_cast = TextFeaturizers.string_cast()
    datetime_transformer = DateTimeFeaturesTransformer()
    # Add the transformations to be done and get the alias name
    # for the date time transform.
    datatime_imputer_transformer = _Transformer(
        parent_feature_list=[str(column_name)],
        transformation_fnc=SupportedTransformersInternal.CatImputer,
        operator=_OperatorNames.Mode,
        feature_type=FeatureType.DateTime,
        should_output=True,
        transformer_params=_TransformerParamsHelper.to_dict(cat_imputer))
    # This transformation depends on the previous transformation
    datatime_string_cast_transformer = _Transformer(
        parent_feature_list=[1],
        transformation_fnc=SupportedTransformersInternal.StringCast,
        operator=None,
        feature_type=None,
        should_output=False)
    # This transformation depends on the previous transformation
    datatime_datetime_transformer = _Transformer(
        parent_feature_list=[2],
        transformation_fnc=SupportedTransformersInternal.DateTimeTransformer,
        operator=None,
        feature_type=None,
        should_output=False)
    # Create an object to convert transformations into JSON object
    feature_transformers = _FeatureTransformers(
        [datatime_imputer_transformer,
         datatime_string_cast_transformer,
         datatime_datetime_transformer])
    # Create the JSON object
    json_obj = feature_transformers.encode_transformations_from_list()

    # Persist the JSON object for later use and obtain an alias name
    alias_column_name = engineered_featurenames_generator_and_holder.get_raw_feature_alias_name(json_obj)

    # Add the transformations to be done and get the alias name
    # for the raw column.
    tr = []  # type:  List[TransformerType]
    tr = [(column, [cat_imputer, string_cast, datetime_transformer], {'alias': str(alias_column_name)})]
    return tr


def get_categorical_transforms(
        column: str,
        column_name: str,
        num_unique_categories: int,
        engineered_featurenames_generator_and_holder: _GenerateEngineeredFeatureNames,
        featurization_config: Optional[FeaturizationConfig] = None,
        is_onnx_compatible: bool = False
) -> List[TransformerType]:
    """
    Create a list of transforms for categorical data.

    :param column: The column in the data frame.
    :param column_name: Name of the column.
    :param num_unique_categories: Number of unique categories.
    :param engineered_featurenames_generator_and_holder: Engineered feature names generator and holder.
    :param featurization_config: Custom featurization configuration.
    :param is_onnx_compatible: If the model is expected to be ONNX compatible.
    :return: List of transformers to be applied on specific columns with alias name.
    """
    tr = []  # type:  List[TransformerType]

    if num_unique_categories <= 2:

        transformer_fncs = [SupportedTransformersInternal.CatImputer,
                            SupportedTransformersInternal.StringCast,
                            SupportedTransformersInternal.LabelEncoder]

        # Check whether the transformer functions are in blocked list
        if featurization_config is not None:
            transformers_in_blocked_list = featurization_utilities \
                .transformers_in_blocked_list(transformer_fncs, featurization_config.blocked_transformers)
            if transformers_in_blocked_list:
                logger.info("Excluding blocked transformer(s): {0}".format(transformers_in_blocked_list))
                return tr

        # Add the transformations to be done and get the alias name
        # for the hashing label encode transform.
        cat_two_category_imputer = CategoricalFeaturizers.cat_imputer(
            **{
                **featurization_utilities.get_transformer_params_by_column_names(
                    SupportedTransformersInternal.CatImputer, [column], featurization_config)
            })
        cat_two_category_string_cast = TextFeaturizers.string_cast()
        cat_two_category_labelencoder = CategoricalFeaturizers.labelencoder(
            **{
                'hashing_seed_val': constants.hashing_seed_value,
                **featurization_utilities.get_transformer_params_by_column_names(
                    SupportedTransformersInternal.LabelEncoder, [column], featurization_config)
            })
        cat_two_category_imputer_transformer = _Transformer(
            parent_feature_list=[str(column_name)],
            transformation_fnc=transformer_fncs[0],
            operator=_OperatorNames.Mode,
            feature_type=FeatureType.Categorical,
            should_output=True,
            transformer_params=_TransformerParamsHelper.to_dict(cat_two_category_imputer))
        # This transformation depends on the previous transformation
        cat_two_category_string_cast_transformer = _Transformer(
            parent_feature_list=[1],
            transformation_fnc=transformer_fncs[1],
            operator=None,
            feature_type=None,
            should_output=False)
        # This transformation depends on the previous transformation
        cat_two_category_label_encode_transformer = _Transformer(
            parent_feature_list=[2],
            transformation_fnc=transformer_fncs[2],
            operator=None,
            feature_type=None,
            should_output=True,
            transformer_params=_TransformerParamsHelper.to_dict(cat_two_category_labelencoder))
        # Create an object to convert transformations into JSON object
        feature_transformers = _FeatureTransformers(
            [cat_two_category_imputer_transformer,
             cat_two_category_string_cast_transformer,
             cat_two_category_label_encode_transformer])
        # Create the JSON object
        json_obj = \
            feature_transformers.encode_transformations_from_list()

        # Persist the JSON object for later use and obtain an alias name
        alias_column_name = engineered_featurenames_generator_and_holder.get_raw_feature_alias_name(json_obj)

        # Add the transformations to be done and get the alias name
        # for the raw column.
        tr = [(column, [cat_two_category_imputer, cat_two_category_string_cast,
                        cat_two_category_labelencoder], {'alias': str(alias_column_name)})]
        return tr
    else:

        transformer_fncs = [SupportedTransformersInternal.StringCast,
                            SupportedTransformersInternal.CountVectorizer]

        # Check whether the transformer functions are in blocked list
        if featurization_config is not None:
            transformers_in_blocked_list = featurization_utilities \
                .transformers_in_blocked_list(transformer_fncs, featurization_config.blocked_transformers)
            if transformers_in_blocked_list:
                logger.info("Excluding blocked transformer(s): {0}".format(transformers_in_blocked_list))
                return tr

        # Add the transformations to be done and get the alias name
        # for the hashing one hot encode transform.
        cat_multiple_category_string_cast = TextFeaturizers.string_cast()
        count_vect_lowercase = not is_onnx_compatible
        from azureml.automl.runtime.featurization.data_transformer import DataTransformer
        cat_multiple_category_count_vectorizer = \
            TextFeaturizers.count_vectorizer(
                **{
                    'tokenizer': DataTransformer._wrap_in_lst,
                    'binary': True,
                    'lowercase': count_vect_lowercase,
                    **featurization_utilities.get_transformer_params_by_column_names(
                        SupportedTransformersInternal.CountVectorizer, [column], featurization_config)
                })
        cat_multiple_category_string_cast_transformer = _Transformer(
            parent_feature_list=[str(column_name)],
            transformation_fnc=transformer_fncs[0],
            operator=None,
            feature_type=FeatureType.Categorical,
            should_output=False)
        # This transformation depends on the previous transformation
        cat_multiple_category_countvec_transformer = _Transformer(
            parent_feature_list=[1],
            transformation_fnc=transformer_fncs[1],
            operator=_OperatorNames.CharGram,
            feature_type=None,
            should_output=True,
            transformer_params=_TransformerParamsHelper.to_dict(cat_multiple_category_count_vectorizer))
        # Create an object to convert transformations into JSON object
        feature_transformers = _FeatureTransformers([
            cat_multiple_category_string_cast_transformer,
            cat_multiple_category_countvec_transformer])
        # Create the JSON object
        json_obj = feature_transformers.encode_transformations_from_list()

        # Persist the JSON object for later use and obtain an alias name
        alias_column_name = engineered_featurenames_generator_and_holder.get_raw_feature_alias_name(json_obj)

        # use CountVectorizer for both Hash and CategoricalHash for now
        tr = [(column, [cat_multiple_category_string_cast, cat_multiple_category_count_vectorizer],
               {'alias': str(alias_column_name)})]
        return tr


def get_numeric_transforms(
        column: str,
        column_name: str,
        engineered_featurenames_generator_and_holder: _GenerateEngineeredFeatureNames,
        featurization_config: Optional[FeaturizationConfig] = None,
) -> List[TransformerType]:
    """
    Create a list of transforms for numeric data.

    :param column: The column in the data frame.
    :param column_name: Name of the column.
    :param engineered_featurenames_generator_and_holder: Engineered feature names generator and holder.
    :param featurization_config: Custom featurization configuration.
    :return: List of transformers to be applied on specific columns with alias name.
    """
    # Add the transformations to be done and get the alias name
    # for the numerical transform
    transformer_params = featurization_utilities.get_transformer_params_by_column_names(
        SupportedTransformersInternal.Imputer, [column], featurization_config)
    operator = _TransformerOperatorMappings.Imputer.get(str(transformer_params.get('strategy')))
    if not operator:
        if transformer_params.get('strategy'):
            logger.warning("Given strategy is not supported, proceeding with default value")
        operator = _OperatorNames.Mean
        transformer_params['strategy'] = operator.lower()
    try:
        imputer = GenericFeaturizers.imputer(**transformer_params)
    except Exception as e:
        logging_utilities.log_traceback(e, logger, is_critical=False)
        logger.warning(
            UNSUPPORTED_PARAMETER_WARNING_MSG.format(t=SupportedTransformersInternal.Imputer)
        )
        imputer = GenericFeaturizers.imputer()
    numeric_transformer = _Transformer(
        parent_feature_list=[str(column_name)],
        transformation_fnc=SupportedTransformersInternal.Imputer,
        operator=operator,
        feature_type=FeatureType.Numeric,
        should_output=True,
        transformer_params=_TransformerParamsHelper.to_dict(imputer))
    # Create an object to convert transformations into JSON object
    feature_transformers = _FeatureTransformers([numeric_transformer])
    # Create the JSON object
    json_obj = feature_transformers.encode_transformations_from_list()

    # Persist the JSON object for later use and obtain an alias name
    alias_column_name = engineered_featurenames_generator_and_holder.get_raw_feature_alias_name(json_obj)

    # Add the transformations to be done and get the alias name
    # for the imputation marker transform.
    # floats or ints go as they are, we only fix NaN
    tr = [([column], [imputer], {'alias': str(alias_column_name)})]
    return cast(List[TransformerType], tr)


def get_imputation_marker_transforms(
        column: str,
        column_name: str,
        engineered_featurenames_generator_and_holder: _GenerateEngineeredFeatureNames) -> List[TransformerType]:
    """
    Create a list of transforms for numerical data in case of imputation markers needed.

    :param column: The column in the data frame.
    :param column_name: Name of the column.
    :param engineered_featurenames_generator_and_holder: Engineered feature names generator and holder.
    :return: List of transformers to be applied on specific columns with alias name.
    """
    # Add the transformations to be done and get the alias name
    # for the imputation marker transform.
    imputation_marker = GenericFeaturizers.imputation_marker()
    imputation_transformer = _Transformer(
        parent_feature_list=[str(column_name)],
        transformation_fnc=SupportedTransformersInternal.ImputationMarker,
        operator=None,
        feature_type=FeatureType.Numeric,
        should_output=True)
    # Create an object to convert transformations into JSON object
    feature_transformers = _FeatureTransformers([imputation_transformer])
    # Create the JSON object
    json_obj = feature_transformers.encode_transformations_from_list()

    # Add the transformations to be done and get the alias name
    # for the imputation marker transform.
    alias_column_name = engineered_featurenames_generator_and_holder.get_raw_feature_alias_name(json_obj)

    return [([column], [imputation_marker], {'alias': str(alias_column_name)})]


def wrap_into_a_list(x: Any) -> List[Any]:
    """
    Wrap an element in list. For backward compatibility in 1.20.0 and 1.21.0.

    :param x: Element like string or integer.
    """
    return [x]
