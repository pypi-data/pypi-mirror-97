# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Definitions for classification metrics."""
import logging
import numpy as np
import sklearn.metrics

from abc import abstractmethod
from typing import cast, Any, Dict, List, Optional

from azureml.automl.core.shared.exceptions import ClientException, DataErrorException
from azureml.automl.runtime.shared.score import _scoring_utilities, constants
from azureml.automl.runtime.shared.score._metric_base import Metric, NonScalarMetric, ScalarMetric


class ClassificationMetric(Metric):
    """Abstract class for classification metrics."""

    MICRO_AVERAGE = 'micro'
    MACRO_AVERAGE = 'macro'
    WEIGHTED_AVERAGE = 'weighted'

    def __init__(self,
                 y_test: np.ndarray,
                 y_pred_proba: np.ndarray,
                 y_test_bin: np.ndarray,
                 y_pred: np.ndarray,
                 class_labels: np.ndarray,
                 sample_weight: Optional[np.ndarray] = None,
                 use_binary: bool = False,
                 logger: Optional[logging.Logger] = None) -> None:
        """
        Initialize the classification metric class.

        :param y_test: True labels for the test set.
        :param y_pred_proba: Predicted probabilities for each sample and class.
        :param y_test_bin: Binarized true labels.
        :param y_pred: The model's predictions.
        :param class_labels: Class labels for the full dataset.
        :param sample_weight: Weighting of each sample in the calculation.
        :param use_binary: Compute metrics on only the second class for binary classification.
            This is usually the true class (when labels are 0 and 1 or false and true).
        :param logger: Logger for errors and warnings.
        """
        if y_test.shape[0] != y_pred_proba.shape[0]:
            raise DataErrorException(
                "Mismatched input shapes: y_test={}, y_pred={}".format(y_test.shape, y_pred.shape),
                target="y_pred", reference_code="_classification.ClassificationMetric.__init__",
                has_pii=True).with_generic_msg("Mismatched input shapes: y_test, y_pred")

        self._y_test = y_test
        self._y_pred_proba = y_pred_proba
        self._y_test_bin = y_test_bin
        self._y_pred = y_pred
        self._test_labels = np.unique(y_test)
        self._class_labels = class_labels
        self._sample_weight = sample_weight
        self._use_binary = use_binary

        super().__init__(logger=logger)

    @abstractmethod
    def compute(self) -> Any:
        """Compute the metric."""
        ...


class Accuracy(ClassificationMetric, ScalarMetric):
    """Wrapper class for accuracy."""

    def compute(self):
        """Compute the score for the metric."""
        return sklearn.metrics.accuracy_score(y_true=self._y_test, y_pred=self._y_pred,
                                              sample_weight=self._sample_weight)


class WeightedAccuracy(ClassificationMetric, ScalarMetric):
    """Accuracy weighted by number of elements for each class."""

    def compute(self):
        """Compute the score for the metric."""
        updated_weights = np.ones(self._y_test.shape[0])
        for idx, i in enumerate(np.bincount(self._y_test.ravel())):
            updated_weights[self._y_test.ravel() == idx] *= (i / float(self._y_test.ravel().shape[0]))

        return sklearn.metrics.accuracy_score(y_true=self._y_test, y_pred=self._y_pred,
                                              sample_weight=updated_weights)


class BalancedAccuracy(ClassificationMetric, ScalarMetric):
    """Wrapper class for balanced accuracy."""

    def compute(self):
        """Compute the score for the metric."""
        average_type = ClassificationMetric.MACRO_AVERAGE
        return sklearn.metrics.recall_score(y_true=self._y_test, y_pred=self._y_pred,
                                            average=average_type,
                                            sample_weight=self._sample_weight)


class NormMacroRecall(ClassificationMetric, ScalarMetric):
    """
    Normalized macro averaged recall metric.

    https://github.com/ch-imad/AutoMl_Challenge/blob/2353ec0/Starting_kit/scoring_program/libscores.py#L187
    For the AutoML challenge
    https://competitions.codalab.org/competitions/2321#learn_the_details-evaluation
    This is a normalized macro averaged recall, rather than accuracy
    https://github.com/scikit-learn/scikit-learn/issues/6747#issuecomment-217587210
    Random performance is 0.0 perfect performance is 1.0
    """

    def _norm_macro_recall(self, y_test_bin, y_pred_proba, n_classes,
                           sample_weight=None, logger=None, **kwargs):
        # need to use the actual prediction not the matrix here but need
        # the matrix passed to utilities.class_averaged_score
        # if we start doing calibration we need to change this
        if y_test_bin.shape[1] > 1:
            y_test_bin = np.argmax(y_test_bin, 1)

        # Binarize the predicted probabilities with a static cutoff
        binary_cutoff = .5
        if y_pred_proba.ndim == 1:
            y_pred = np.array(y_pred_proba > binary_cutoff, dtype=int)
        else:
            y_pred = np.argmax(y_pred_proba, 1)
        cmat = sklearn.metrics.confusion_matrix(y_true=y_test_bin, y_pred=y_pred,
                                                sample_weight=sample_weight)
        if isinstance(cmat, float):
            return constants.DEFAULT_PIPELINE_SCORE

        if cmat.sum(axis=1).sum() == 0:
            return constants.DEFAULT_PIPELINE_SCORE

        R = 1 / n_classes
        return max(0.0, (np.mean(cmat.diagonal() / cmat.sum(axis=1)) - R) / (1 - R))

    def compute(self):
        """Compute the score for the metric."""
        use_true_class = self._use_binary and self._class_labels.shape[0] == 2
        y_pred_proba = self._y_pred_proba[:, 1] if use_true_class else self._y_pred_proba
        average_type = ClassificationMetric.MACRO_AVERAGE
        name = constants.NORM_MACRO_RECALL
        return _scoring_utilities.class_averaged_score(
            self._norm_macro_recall, self._y_test_bin, y_pred_proba,
            self._class_labels, self._test_labels, average_type, name,
            sample_weight=self._sample_weight, logger=self._logger)


class LogLoss(ClassificationMetric, ScalarMetric):
    """Wrapper class for log loss."""

    def compute(self):
        """Compute the score for the metric."""
        use_true_class = self._use_binary and self._class_labels.shape[0] == 2
        y_pred_proba = self._y_pred_proba[:, 1] if use_true_class else self._y_pred_proba
        return sklearn.metrics.log_loss(y_true=self._y_test, y_pred=y_pred_proba,
                                        labels=self._class_labels,
                                        sample_weight=self._sample_weight)


class F1(ClassificationMetric, ScalarMetric):
    """Wrapper class for recall."""

    def __init__(self, average_type, *args, **kwargs):
        """Initialize F1."""
        self._average_type = average_type
        super().__init__(*args, **kwargs)

    def compute(self):
        """Compute the score for the metric."""
        return sklearn.metrics.f1_score(y_true=self._y_test, y_pred=self._y_pred,
                                        average=self._average_type, sample_weight=self._sample_weight)


class F1Macro(F1):
    """Wrapper class for macro-averaged F1 score."""

    def __init__(self, *args, **kwargs):
        """Initialize F1Macro."""
        super().__init__(ClassificationMetric.MACRO_AVERAGE, *args, **kwargs)


class F1Micro(F1):
    """Wrapper class for micro-averaged F1 score."""

    def __init__(self, *args, **kwargs):
        """Initialize F1Micro."""
        super().__init__(ClassificationMetric.MICRO_AVERAGE, *args, **kwargs)


class F1Weighted(F1):
    """Wrapper class for weighted-averaged F1 score."""

    def __init__(self, *args, **kwargs):
        """Initialize F1Weighted."""
        super().__init__(ClassificationMetric.WEIGHTED_AVERAGE, *args, **kwargs)


class Precision(ClassificationMetric, ScalarMetric):
    """Wrapper class for precision."""

    def __init__(self, average_type, *args, **kwargs):
        """Initialize Precision."""
        self._average_type = average_type
        super().__init__(*args, **kwargs)

    def compute(self):
        """Compute the score for the metric."""
        return sklearn.metrics.precision_score(y_true=self._y_test, y_pred=self._y_pred,
                                               average=self._average_type, sample_weight=self._sample_weight)


class PrecisionMacro(Precision):
    """Wrapper class for macro-averaged precision."""

    def __init__(self, *args, **kwargs):
        """Initialize PrecisionMacro."""
        self._average_type = ClassificationMetric.MACRO_AVERAGE
        super().__init__(ClassificationMetric.MACRO_AVERAGE, *args, **kwargs)


class PrecisionMicro(Precision):
    """Wrapper class for micro-averaged precision."""

    def __init__(self, *args, **kwargs):
        """Initialize PrecisionMicro."""
        super().__init__(ClassificationMetric.MICRO_AVERAGE, *args, **kwargs)


class PrecisionWeighted(Precision):
    """Wrapper class for weighted-averaged precision."""

    def __init__(self, *args, **kwargs):
        """Initialize PrecisionWeighted."""
        super().__init__(ClassificationMetric.WEIGHTED_AVERAGE, *args, **kwargs)


class Recall(ClassificationMetric, ScalarMetric):
    """Wrapper class for recall."""

    def __init__(self, average_type, *args, **kwargs):
        """Initialize Recall."""
        self._average_type = average_type
        super().__init__(*args, **kwargs)

    def compute(self):
        """Compute the score for the metric."""
        return sklearn.metrics.recall_score(y_true=self._y_test, y_pred=self._y_pred,
                                            average=self._average_type, sample_weight=self._sample_weight)


class RecallMacro(Recall):
    """Wrapper class for macro-averaged recall."""

    def __init__(self, *args, **kwargs):
        """Initialize RecallMacro."""
        super().__init__(ClassificationMetric.MACRO_AVERAGE, *args, **kwargs)


class RecallMicro(Recall):
    """Wrapper class for micro-averaged recall."""

    def __init__(self, *args, **kwargs):
        """Initialize RecallMicro."""
        super().__init__(ClassificationMetric.MICRO_AVERAGE, *args, **kwargs)


class RecallWeighted(Recall):
    """Wrapper class for weighted-averaged recall."""

    def __init__(self, *args, **kwargs):
        """Initialize RecallWeighted."""
        super().__init__(ClassificationMetric.WEIGHTED_AVERAGE, *args, **kwargs)


class AveragePrecision(ClassificationMetric, ScalarMetric):
    """Wrapper class for average precision."""

    def __init__(self, average_type, name, *args, **kwargs):
        """Initialize AveragePrecision."""
        self._average_type = average_type
        self._name = name
        super().__init__(*args, **kwargs)

    def compute(self):
        """Compute the score for the metric."""
        use_true_class = self._use_binary and self._class_labels.shape[0] == 2
        y_pred_proba = self._y_pred_proba[:, 1] if use_true_class else self._y_pred_proba
        y_test_bin = self._y_test_bin[:, 1] if use_true_class else self._y_test_bin
        return _scoring_utilities.class_averaged_score(
            sklearn.metrics.average_precision_score, y_test_bin, y_pred_proba,
            self._class_labels, self._test_labels, self._average_type, self._name,
            sample_weight=self._sample_weight, logger=self._logger)


class AveragePrecisionMacro(AveragePrecision):
    """Wrapper class for macro-averaged average precision."""

    def __init__(self, *args, **kwargs):
        """Initialize AveragePrecisionMacro."""
        super().__init__(
            ClassificationMetric.MACRO_AVERAGE,
            constants.AVERAGE_PRECISION_MACRO,
            *args,
            **kwargs
        )


class AveragePrecisionMicro(AveragePrecision):
    """Wrapper class for micro-averaged average precision."""

    def __init__(self, *args, **kwargs):
        """Initialize AveragePrecisionMicro."""
        super().__init__(
            ClassificationMetric.MICRO_AVERAGE,
            constants.AVERAGE_PRECISION_MICRO,
            *args,
            **kwargs
        )


class AveragePrecisionWeighted(AveragePrecision):
    """Wrapper class for weighted-averaged average precision."""

    def __init__(self, *args, **kwargs):
        """Initialize AveragePrecisionWeighted."""
        super().__init__(
            ClassificationMetric.WEIGHTED_AVERAGE,
            constants.AVERAGE_PRECISION_WEIGHTED,
            *args,
            **kwargs
        )


class AUC(ClassificationMetric, ScalarMetric):
    """Wrapper class for AUC (area under the ROC curve)."""

    def __init__(self, average_type, name, *args, **kwargs):
        """Initialize AUC."""
        self._average_type = average_type
        self._name = name
        super().__init__(*args, **kwargs)

    def compute(self):
        """Compute the score for the metric."""
        self._validate_one_class()
        use_true_class = self._use_binary and self._class_labels.shape[0] == 2
        y_pred_proba = self._y_pred_proba[:, 1] if use_true_class else self._y_pred_proba
        y_test_bin = self._y_test_bin[:, 1] if use_true_class else self._y_test_bin
        return _scoring_utilities.class_averaged_score(
            sklearn.metrics.roc_auc_score, y_test_bin, y_pred_proba,
            self._class_labels, self._test_labels, self._average_type, self._name,
            sample_weight=self._sample_weight, logger=self._logger)

    def _validate_one_class(self):
        """
        Validate that y_test has more than one unique class label or that this is
        micro-averaged AUC with indicators passed rather than labels.
        """
        is_one_class = self._test_labels.shape[0] == 1
        is_class_averaged = self._average_type in [ClassificationMetric.MACRO_AVERAGE,
                                                   ClassificationMetric.WEIGHTED_AVERAGE]

        if is_one_class and (self._use_binary or is_class_averaged):
            safe_message = "AUC {} is undefined when y_test has only one unique class.".format(self._average_type)
            message = "AUC {} is undefined. y_test has only one unique class: {}".format(
                self._average_type, self._test_labels[0])
            raise ClientException(message).with_generic_msg(safe_message)


class AUCMacro(AUC):
    """Wrapper class for macro-averaged AUC."""

    def __init__(self, *args, **kwargs):
        """Initialize AUCMacro."""
        super().__init__(
            ClassificationMetric.MACRO_AVERAGE,
            constants.AUC_MACRO,
            *args,
            **kwargs
        )


class AUCMicro(AUC):
    """Wrapper class for micro-averaged AUC."""

    def __init__(self, *args, **kwargs):
        """Initialize AUCMicro."""
        super().__init__(
            ClassificationMetric.MICRO_AVERAGE,
            constants.AUC_MICRO,
            *args,
            **kwargs
        )


class AUCWeighted(AUC):
    """Wrapper class for weighted-averaged AUC."""

    def __init__(self, *args, **kwargs):
        """Initialize AUCWeighted."""
        super().__init__(
            ClassificationMetric.WEIGHTED_AVERAGE,
            constants.AUC_WEIGHTED,
            *args,
            **kwargs
        )


class MatthewsCorrelation(ClassificationMetric, ScalarMetric):
    """Wrapper class for Matthews Correlation."""

    def compute(self):
        """Compute the score for the metric."""
        ret = sklearn.metrics.matthews_corrcoef(
            y_true=self._y_test, y_pred=self._y_pred,
            sample_weight=self._sample_weight)
        name = constants.MATTHEWS_CORRELATION
        return _scoring_utilities.clip_score(ret, *constants.CLASSIFICATION_RANGES[name], name)


class AccuracyTable(ClassificationMetric, NonScalarMetric):
    """
    Accuracy Table Metric.

    The accuracy table metric is a multi-use non-scalar metric
    that can be used to produce multiple types of line charts
    that vary continuously over the space of predicted probabilities.
    Examples of these charts are receiver operating characteristic,
    precision-recall, and lift curves.

    The calculation of the accuracy table is similar to the calculation
    of a receiver operating characteristic curve. A receiver operating
    characteristic curve stores true positive rates and
    false positive rates at many different probability thresholds.
    The accuracy table stores the raw number of
    true positives, false positives, true negatives, and false negatives
    at many probability thresholds.

    Probability thresholds are evenly spaced thresholds between 0 and 1.
    If NUM_POINTS were 5 the probability thresholds would be
    [0.0, 0.25, 0.5, 0.75, 1.0].
    These thresholds are useful for computing charts where you want to
    sample evenly over the space of predicted probabilities.

    Percentile thresholds are spaced according to the distribution of
    predicted probabilities. Each threshold corresponds to the percentile
    of the data at a probability threshold.
    For example, if NUM_POINTS were 5, then the first threshold would be at
    the 0th percentile, the second at the 25th percentile, the
    third at the 50th, and so on.

    The probability tables and percentile tables are both 3D lists where
    the first dimension represents the class label*, the second dimension
    represents the sample at one threshold (scales with NUM_POINTS),
    and the third dimension always has 4 values: TP, FP, TN, FN, and
    always in that order.

    * The confusion values (TP, FP, TN, FN) are computed with the
    one vs. rest strategy. See the following link for more details:
    `https://en.wikipedia.org/wiki/Multiclass_classification`
    """

    SCHEMA_TYPE = constants.SCHEMA_TYPE_ACCURACY_TABLE
    SCHEMA_VERSION = '1.0.1'

    NUM_POINTS = 100

    PROB_TABLES = 'probability_tables'
    PERC_TABLES = 'percentile_tables'
    PROB_THOLDS = 'probability_thresholds'
    PERC_THOLDS = 'percentile_thresholds'
    CLASS_LABELS = 'class_labels'

    @staticmethod
    def _data_to_dict(data):
        schema_type = AccuracyTable.SCHEMA_TYPE
        schema_version = AccuracyTable.SCHEMA_VERSION
        return NonScalarMetric._data_to_dict(schema_type, schema_version, data)

    def _make_thresholds(self):
        probability_thresholds = np.linspace(0, 1, AccuracyTable.NUM_POINTS)
        all_predictions = self._y_pred_proba.ravel()
        percentile_thresholds = np.percentile(all_predictions, probability_thresholds * 100)
        return probability_thresholds, percentile_thresholds

    def _build_tables(self, class_labels, thresholds):
        """
        Create the accuracy table per class.

        Sweeps the thresholds to find accuracy data over the space of
        predicted probabilities.
        """
        data = zip(self._y_test_bin.T, self._y_pred_proba.T)
        tables = [self._build_table(tbin, pred, thresholds) for tbin, pred in data]
        full_tables = self._pad_tables(class_labels, tables)
        return full_tables

    def _pad_tables(self, class_labels, tables):
        """Add padding tables for missing validation classes."""
        y_labels = np.unique(self._y_test)
        full_tables = []
        table_index = 0
        for class_label in class_labels:
            if class_label in y_labels:
                full_tables.append(tables[table_index])
                table_index += 1
            else:
                full_tables.append(np.zeros((AccuracyTable.NUM_POINTS, 4), dtype=int))
        return full_tables

    def _build_table(self, class_y_test_bin, class_y_pred_proba, thresholds):
        """Calculate the confusion values at all thresholds for one class."""
        table = []
        n_positive = np.sum(class_y_test_bin)
        n_samples = class_y_test_bin.shape[0]
        for threshold in thresholds:
            under_threshold = class_y_test_bin[class_y_pred_proba < threshold]
            fn = np.sum(under_threshold)
            tn = under_threshold.shape[0] - fn
            tp, fp = n_positive - fn, n_samples - n_positive - tn
            conf_values = np.array([tp, fp, tn, fn], dtype=int)
            table.append(conf_values)
        return table

    def compute(self):
        """Compute the score for the metric."""
        probability_thresholds, percentile_thresholds = self._make_thresholds()
        probability_tables = self._build_tables(self._class_labels, probability_thresholds)
        percentile_tables = self._build_tables(self._class_labels, percentile_thresholds)

        string_labels = [str(label) for label in self._class_labels]
        self._data[AccuracyTable.CLASS_LABELS] = string_labels
        self._data[AccuracyTable.PROB_TABLES] = probability_tables
        self._data[AccuracyTable.PERC_TABLES] = percentile_tables
        self._data[AccuracyTable.PROB_THOLDS] = probability_thresholds
        self._data[AccuracyTable.PERC_THOLDS] = percentile_thresholds
        ret = AccuracyTable._data_to_dict(self._data)
        return _scoring_utilities.make_json_safe(ret)

    @staticmethod
    def aggregate(
        scores: List[Dict[str, Any]],
        logger: Optional[logging.Logger] = None
    ) -> Dict[str, Any]:
        """
        Fold several scores from a computed metric together.

        :param scores: List of computed scores.
        :param logger: Debug logger.
        :return: Aggregated score.
        """
        if not Metric.check_aggregate_scores(scores, constants.ACCURACY_TABLE, logger=logger):
            return NonScalarMetric.get_error_metric()

        score_data = [score[NonScalarMetric.DATA] for score in scores]
        prob_tables = [d[AccuracyTable.PROB_TABLES] for d in score_data]
        perc_tables = [d[AccuracyTable.PERC_TABLES] for d in score_data]
        data_agg = {
            AccuracyTable.PROB_TABLES: (
                np.sum(prob_tables, axis=0)),
            AccuracyTable.PERC_TABLES: (
                np.sum(perc_tables, axis=0)),
            AccuracyTable.PROB_THOLDS: (
                score_data[0][AccuracyTable.PROB_THOLDS]),
            AccuracyTable.PERC_THOLDS: (
                score_data[0][AccuracyTable.PERC_THOLDS]),
            AccuracyTable.CLASS_LABELS: (
                score_data[0][AccuracyTable.CLASS_LABELS])
        }
        ret = AccuracyTable._data_to_dict(data_agg)
        return cast(Dict[str, Any], _scoring_utilities.make_json_safe(ret))


class ConfusionMatrix(ClassificationMetric, NonScalarMetric):
    """
    Confusion Matrix Metric.

    This metric is a wrapper around the sklearn confusion matrix.
    The metric data contains the class labels and a 2D list
    for the matrix itself.
    See the following link for more details on how the metric is computed:
    `https://scikit-learn.org/stable/modules/generated/sklearn.metrics.confusion_matrix.html`
    """

    SCHEMA_TYPE = constants.SCHEMA_TYPE_CONFUSION_MATRIX
    SCHEMA_VERSION = '1.0.0'

    MATRIX = 'matrix'
    CLASS_LABELS = 'class_labels'

    @staticmethod
    def _data_to_dict(data):
        schema_type = ConfusionMatrix.SCHEMA_TYPE
        schema_version = ConfusionMatrix.SCHEMA_VERSION
        return NonScalarMetric._data_to_dict(schema_type, schema_version, data)

    def _compute_matrix(self, class_labels, sample_weight=None):
        """Compute the matrix from prediction data."""
        y_pred_indexes = np.argmax(self._y_pred_proba, axis=1)
        y_pred_labels = class_labels[y_pred_indexes]
        y_test = self._y_test

        if y_pred_labels.dtype.kind == 'f':
            class_labels = class_labels.astype(str)
            y_test = y_test.astype(str)
            y_pred_labels = y_pred_labels.astype(str)

        try:
            matrix = sklearn.metrics.confusion_matrix(
                y_true=y_test, y_pred=y_pred_labels,
                sample_weight=sample_weight, labels=class_labels)
        except Exception:
            debug_stats = self._get_debug_stats(y_test, y_pred_labels, class_labels,
                                                self._y_pred_proba, sample_weight)
            message = "Confusion matrix failed with unexpected error, debug stats: {}".format(debug_stats)
            self._logger.error(message)
            raise
        return matrix

    def _get_debug_stats(self, y_test, y_pred, class_labels, y_pred_proba, sample_weight):
        return {
            'y_true_type': str(y_test.dtype),
            'y_pred_type': str(y_pred.dtype),
            'labels_type': str(class_labels.dtype),
            'proba_type': str(y_pred_proba.dtype),
            'y_true_kind': y_test.dtype.kind,
            'y_pred_kind': y_pred.dtype.kind,
            'labels_kind': class_labels.dtype.kind,
            'proba_kind': y_pred_proba.dtype.kind,
            'y_true_shape': y_test.shape,
            'y_pred_shape': y_pred.shape,
            'labels_shape': class_labels.shape,
            'proba_shape': y_pred_proba.shape,
            'sample_weight_passed': sample_weight is not None,
        }

    def compute(self):
        """Compute the score for the metric."""
        string_labels = [str(label) for label in self._class_labels]
        self._data[ConfusionMatrix.CLASS_LABELS] = string_labels
        matrix = self._compute_matrix(self._class_labels,
                                      sample_weight=self._sample_weight)
        self._data[ConfusionMatrix.MATRIX] = matrix
        ret = ConfusionMatrix._data_to_dict(self._data)
        return _scoring_utilities.make_json_safe(ret)

    @staticmethod
    def aggregate(
        scores: List[Dict[str, Any]],
        logger: Optional[logging.Logger] = None
    ) -> Dict[str, Any]:
        """
        Fold several scores from a computed metric together.

        :param scores: List of computed scores.
        :param logger: Debug logger.
        :return: Aggregated score.
        """
        if not Metric.check_aggregate_scores(scores, constants.CONFUSION_MATRIX, logger=logger):
            return NonScalarMetric.get_error_metric()

        score_data = [score[NonScalarMetric.DATA] for score in scores]
        matrices = [d[ConfusionMatrix.MATRIX] for d in score_data]
        matrix_sum = np.sum(matrices, axis=0)
        agg_class_labels = score_data[0][ConfusionMatrix.CLASS_LABELS]
        data_agg = {
            ConfusionMatrix.CLASS_LABELS: agg_class_labels,
            ConfusionMatrix.MATRIX: matrix_sum
        }
        ret = ConfusionMatrix._data_to_dict(data_agg)
        return cast(Dict[str, Any], _scoring_utilities.make_json_safe(ret))
