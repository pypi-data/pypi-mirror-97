from typing import Any, Callable, Dict, List, Optional

import numpy as np
import pandas as pd
import shap

from .type import DeepLearningFramework, ModelTypes


def get_explainability(
    x: pd.DataFrame,
    sample_idx: Optional[List[int]] = None,
    model: Optional[Any] = None,
    model_type: Optional[ModelTypes] = None,
    predict_func: Optional[Callable] = None,
    bkgrd_data: Optional[pd.DataFrame] = None,
    kmeans_size: int = 10,
):
    shap_values, base_values = compute_shap_values(
        x,
        model=model,
        model_type=model_type,
        predict_func=predict_func,
        bkgrd_data=bkgrd_data,
        kmeans_size=kmeans_size,
    )

    global_data = get_global_explainability(x, shap_values)

    if sample_idx is not None and len(sample_idx) != x.shape[0]:
        shap_values = [shap_value[sample_idx] for shap_value in shap_values]

    return {"indv_data": (shap_values, base_values), "global_data": global_data}


def compute_shap_values(
    x: pd.DataFrame,
    model: Optional[Any] = None,
    model_type: Optional[ModelTypes] = None,
    predict_func: Optional[Callable] = None,
    bkgrd_data: Optional[pd.DataFrame] = None,
    kmeans_size: int = 10,
):
    """Function to compute SHAP values, which are used for XAI.

    Use the relevant explainer for each type of model.

    :param pandas.DataFrame x: Validation/test data to use for explanation
    :param Optional model: Model to compute shap values for. In case model is of unsupported
        type, use predict_func to pass in a generic function instead
    :param Optional[ModelTypes] model_type: Type of the model
    :param Optional[Callable] predict_func: Generic function to compute shap values for.
        It should take a matrix of samples (# samples x # features) and compute the
        output of the model for those samples.
        The output can be a vector (# samples) or a matrix (# samples x # model outputs).
    :param: Optional[pandas.DataFrame] bkgrd_data: background data for explainability analysis
    :param: int kmeans_size: Number of k-means clusters. Only required for explaining generic
        predict_func
    :return Tuple[list(numpy.array), numpy_array]: shap_values, base_value.
    len(base_value) must be the same as len(shap_values)
    """
    if model_type == ModelTypes.TREE:
        explainer = shap.TreeExplainer(model, data=bkgrd_data)
    else:
        if bkgrd_data is None:
            raise ValueError("Non tree model requires background data")
        if model_type == ModelTypes.LINEAR:
            explainer = shap.LinearExplainer(model, bkgrd_data)
        elif model_type == ModelTypes.DEEP:
            explainer, x, bkgrd_data = _get_deep_explainer(x, model, bkgrd_data)
        else:
            explainer = _get_kernel_explainer(predict_func, bkgrd_data, kmeans_size)

    shap_values = explainer.shap_values(x)
    base_value = explainer.expected_value
    return check_values(shap_values, base_value)


def compute_corrcoef(features: pd.DataFrame, shap_values: List[np.array]) -> np.array:
    """
    Compute correlation between each feature and its SHAP values.
    :param pandas.DataFrame features:
    :param numpy.array shap_values:
    :return numpy.array: (shape = (dim of predict output, number of features))
    """
    all_corrs = list()
    for cls_shap_val in shap_values:
        corrcoef = list()
        for i in range(features.shape[1]):
            df_ = pd.DataFrame({"x": features.iloc[:, i], "y": cls_shap_val[:, i]})
            corr = df_.corr(method="pearson").values[0, 1]
            corr = None if np.isnan(corr) else corr
            corrcoef.append(corr)
        all_corrs.append(corrcoef)
    return np.array(all_corrs)


def check_values(shap_values: List[np.array], base_value: List[np.array]):
    """
    Check shape of shap_values and base_value.
    len(base_value) == len(shap_values) and type(shap_values) must be a list
    :param numpy.array shap_values:
    :param numpy.array base_value:
    """
    if isinstance(shap_values, np.ndarray) and len(shap_values.shape) == 2:
        shap_values = [shap_values]
    return shap_values, np.array(base_value).reshape(-1)


def _get_kernel_explainer(
    predict_func: Optional[Callable], bkgrd_data: pd.DataFrame, kmeans_size: int
):
    if predict_func is None:
        raise ValueError("No target to compute shap values. Expected either model or predict_func")
    # rather than use the whole training set to estimate expected values,
    # summarize with a set of weighted kmeans, each weighted by
    # the number of points they represent.
    x_bkgrd_summary = shap.kmeans(bkgrd_data, kmeans_size)
    return shap.KernelExplainer(predict_func, x_bkgrd_summary)


def _get_deep_explainer(x: pd.DataFrame, model, bkgrd_data: pd.DataFrame):
    framework = _get_deep_learning_framework(model)

    if framework == DeepLearningFramework.PYTORCH:
        # Convert background data and input to torch tensor
        # since torch doesn't operate on pandas dataframe
        import torch

        bkgrd_data = torch.Tensor(bkgrd_data.to_numpy())
        x = torch.Tensor(x.to_numpy())
    elif framework == DeepLearningFramework.TENSORFLOW:
        # Need to use numpy arrays for both
        bkgrd_data = bkgrd_data.to_numpy()
        x = x.to_numpy()

    return shap.DeepExplainer(model, bkgrd_data), x, bkgrd_data


def _get_deep_learning_framework(model) -> DeepLearningFramework:
    """Detect framework either pytorch or tensorflow
    Only use with deep model type. Inspired by
    https://github.com/slundberg/shap/blob/fc30c661339e89e0132f5f89e5385e3681090e1f/shap/explainers/deep/__init__.py#L64
    """
    if hasattr(model, "named_parameters"):
        return DeepLearningFramework.PYTORCH
    return DeepLearningFramework.TENSORFLOW


def get_global_explainability(features: pd.DataFrame, shap_values: List[np.array]) -> Dict:
    shap_summary = np.abs(shap_values).mean(axis=1)
    corrcoefs = compute_corrcoef(features, shap_values)
    output = {}
    for i in range(shap_summary.shape[0]):
        class_summary: Dict[str, Dict[str, float]] = {}
        for j, col_name in enumerate(features.columns):
            class_summary[col_name] = {
                "mean_abs_shap": shap_summary[i, j],
                "corrcoeff": corrcoefs[i, j],
            }

        output[f"class {i}"] = class_summary

    return output
