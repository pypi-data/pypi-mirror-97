import logging
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
from aif360.datasets import BinaryLabelDataset
from aif360.metrics.classification_metric import ClassificationMetric

logger = logging.getLogger(__name__)


def prepare_dataset(
    features: pd.DataFrame,
    labels: np.array,
    protected_attribute: str,
    privileged_attribute_values: List[int],
    unprivileged_attribute_values: List[int],
    favorable_label=1.0,
    unfavorable_label=0.0,
) -> BinaryLabelDataset:
    """Prepare dataset for computing fairness metrics."""
    df = features[[protected_attribute]].copy()
    df["outcome"] = labels

    return BinaryLabelDataset(
        df=df,
        label_names=["outcome"],
        scores_names=[],
        protected_attribute_names=[protected_attribute],
        privileged_protected_attributes=[np.array(privileged_attribute_values)],
        unprivileged_protected_attributes=[np.array(unprivileged_attribute_values)],
        favorable_label=favorable_label,
        unfavorable_label=unfavorable_label,
    )


def get_fairness(
    features: pd.DataFrame,
    predictions: np.array,
    labels: np.array,
    protected_attribute: str,
    privileged_attribute_values: List[int],
    unprivileged_attribute_values: List[int],
    favorable_label=1.0,
    unfavorable_label=0.0,
    threshold=0.2,
) -> Tuple[pd.DataFrame, Dict]:
    """Fairness wrapper function."""
    predicted = prepare_dataset(
        features,
        predictions,
        protected_attribute,
        privileged_attribute_values,
        unprivileged_attribute_values,
        favorable_label=favorable_label,
        unfavorable_label=unfavorable_label,
    )
    grdtruth = prepare_dataset(
        features,
        labels,
        protected_attribute,
        privileged_attribute_values,
        unprivileged_attribute_values,
        favorable_label=favorable_label,
        unfavorable_label=unfavorable_label,
    )
    clf_metric = ClassificationMetric(
        grdtruth,
        predicted,
        unprivileged_groups=[{protected_attribute: v} for v in unprivileged_attribute_values],
        privileged_groups=[{protected_attribute: v} for v in privileged_attribute_values],
    )
    fmeasures = compute_fairness_metrics(clf_metric)
    fmeasures["fair?"] = fmeasures["ratio"].apply(
        lambda x: "Yes" if np.abs(x - 1) < threshold else "No"
    )

    confusion_matrix = {
        "all": clf_metric.binary_confusion_matrix(privileged=None),
        "privileged": clf_metric.binary_confusion_matrix(privileged=True),
        "unprivileged": clf_metric.binary_confusion_matrix(privileged=False),
    }

    return fmeasures, confusion_matrix


def compute_fairness_metrics(aif_metric: ClassificationMetric) -> pd.DataFrame:
    """Compute and report fairness metrics."""
    fmeasures = []

    # Equal opportunity: equal FNR
    fnr_ratio = aif_metric.false_negative_rate_ratio()
    fmeasures.append(
        [
            "Equal opportunity",
            "Separation",
            aif_metric.false_negative_rate(),
            aif_metric.false_negative_rate(False),
            aif_metric.false_negative_rate(True),
            fnr_ratio,
        ]
    )

    # Predictive parity: equal PPV
    ppv_all = aif_metric.positive_predictive_value()
    ppv_up = aif_metric.positive_predictive_value(False)
    ppv_p = aif_metric.positive_predictive_value(True)
    ppv_ratio = ppv_up / ppv_p
    fmeasures.append(["Predictive parity", "Sufficiency", ppv_all, ppv_up, ppv_p, ppv_ratio])

    # Statistical parity
    disparate_impact = aif_metric.disparate_impact()
    fmeasures.append(
        [
            "Statistical parity",
            "Independence",
            aif_metric.selection_rate(),
            aif_metric.selection_rate(False),
            aif_metric.selection_rate(True),
            disparate_impact,
        ]
    )

    # Predictive equality: equal FPR
    fpr_ratio = aif_metric.false_positive_rate_ratio()
    fmeasures.append(
        [
            "Predictive equality",
            "Separation",
            aif_metric.false_positive_rate(),
            aif_metric.false_positive_rate(False),
            aif_metric.false_positive_rate(True),
            fpr_ratio,
        ]
    )

    # Equalized odds: equal TPR and equal FPR
    eqodds_all = (aif_metric.true_positive_rate() + aif_metric.false_positive_rate()) / 2
    eqodds_up = (aif_metric.true_positive_rate(False) + aif_metric.false_positive_rate(False)) / 2
    eqodds_p = (aif_metric.true_positive_rate(True) + aif_metric.false_positive_rate(True)) / 2
    eqodds_ratio = eqodds_up / eqodds_p
    fmeasures.append(
        ["Equalized odd", "Separation", eqodds_all, eqodds_up, eqodds_p, eqodds_ratio]
    )

    # Conditional use accuracy equality: equal PPV and equal NPV
    acceq_all = (
        aif_metric.positive_predictive_value(False) + aif_metric.negative_predictive_value(False)
    ) / 2
    acceq_up = (
        aif_metric.positive_predictive_value(False) + aif_metric.negative_predictive_value(False)
    ) / 2
    acceq_p = (
        aif_metric.positive_predictive_value(True) + aif_metric.negative_predictive_value(True)
    ) / 2
    acceq_ratio = acceq_up / acceq_p
    fmeasures.append(
        [
            "Conditional use accuracy equality",
            "Sufficiency",
            acceq_all,
            acceq_up,
            acceq_p,
            acceq_ratio,
        ]
    )

    return pd.DataFrame(
        fmeasures, columns=["metric", "criterion", "all", "unprivileged", "privileged", "ratio"]
    )


def analyze_fairness(
    fconfig: Dict, features: pd.DataFrame, predictions: np.array, labels: np.array,
):
    fairness_metrics: Dict[str, Dict] = {}
    labels_cls = set(labels.ravel())
    for attr, attr_vals in fconfig.items():
        if attr not in features:
            logger.warning(f"Key '{attr}' in fairness config does not exist in test features")
        else:
            fairness_metrics[attr] = {}
            for cl in labels_cls:
                fairness_metrics[attr][f"class {cl}"] = get_fairness(
                    features,
                    binarize(predictions, cl),
                    binarize(labels, cl),
                    attr,
                    attr_vals["privileged_attribute_values"],
                    attr_vals["unprivileged_attribute_values"],
                )
    return fairness_metrics


def binarize(y, label):
    """Binarize array-like data according to label."""
    return (np.array(y) == label).astype(int)
