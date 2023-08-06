import gzip
import inspect
import json
import logging
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

import numpy as np
import pandas as pd
import pkg_resources
import requests

import bdrk
from bdrk.backend.v1.exceptions import ApiException
from bdrk.backend.v1.models.blob_storage_signed_url_schema import BlobStorageSignedUrlSchema
from bdrk.backend.v1.models.xafai_upload_url_schema import XafaiUploadUrlSchema
from bdrk.tracking.client_old import BedrockApi

from . import explainability as exp
from . import fairness as fair
from .type import ModelTypes


class ModelAnalyzer:
    def __init__(
        self,
        model,
        model_name: str,
        model_type: Optional[ModelTypes] = None,
        description: str = "",
    ):
        """Object to capture model info and xafai metrics

        :param model: the target model
        :type model: Any
        :param model_name: model name e.g "Churn prediction model"
        :type model_name: str
        :param model_type: type of model, needed to use the correct explainer, defaults to None
        which require setting predict_func
        :type model_type: Optional[ModelTypes], optional
        :param description: long description of the model
        e.g "Model to predict customer churn, trained with public dataset", defaults to ""
        :type description: str, optional
        """
        self.model = model
        self.model_type = model_type
        self.model_name = model_name
        self.desc = description
        self.predict: Optional[Callable] = None
        self.train_feat: Optional[pd.Dataframe] = None
        self.test_feat: Optional[pd.Dataframe] = None
        self.test_inf: Optional[np.array] = None
        self.fconfig: Optional[Dict] = None
        self.test_lbs: Optional[np.array] = None
        self.base_values = None
        self.shap_values = None
        self.global_xai_data = None
        self.fairness_metrics = None
        self.sample_limit: Optional[int] = 200
        self.logger = logging.getLogger(__name__)
        self.api = BedrockApi(self.logger)

    def predict_func(self, f: Callable[..., Any]):
        """Setting predict function to use with model

        :param f: the predict function to use
        :type f: Callable[..., Any]
        """
        self.predict = f
        return self

    def train_features(self, df: pd.DataFrame):
        """Setting training data used to generate the model

        :param df: dataframe of training data
        :type df: pandas.DataFrame
        """
        self.train_feat = df
        return self

    def test_features(self, df: pd.DataFrame):
        """Setting test data used for calculating explainability and fairness metrics

        :param df: dataframe of training data
        :type df: pandas.DataFrame
        """
        self.test_feat = df
        return self

    def test_inference(self, y: np.array):
        """Setting model inference results done on test_features
        Used for calculating fairness metrics

        :param y: array of inference result
        :type y: numpy.array
        """
        self.test_inf = y
        return self

    def fairness_config(self, config: Dict[str, Dict[str, List]]):
        """Setting fairness configuration used for generating fairness metrics

        Required for generating fairness metrics

        :param config: config dictionary.

        Example::

                {
                    "FEATURE_NAME": {
                        "unprivileged_attribute_values": ["privileged value"],
                        "privileged_attribute_values": ["unprivileged value"]
                    }
                }

        :type config: Dict[str,  Dict[str, List]
        """
        self.fconfig = config
        return self

    def test_labels(self, labels: np.array):
        """Setting groundtruth labels of test set data test_features
        Used for calculating fairness metrics

        :param labels: Label for each row of test set data
        :type labels: numpy.array
        """
        self.test_lbs = labels
        return self

    def stored_sample_limit(self, sample_limit: Optional[int]):
        """Setting limit the number of samples stored
        Set to None to store everything in the feature dataframe

        :param sample_limit: number of samples stored
        :type sample_limit: Optional[int]
        """
        self.sample_limit = sample_limit
        return self

    def analyze(self):
        """Generating xafai metrics with model info and store on Bedrock

        :return:

            - shap_values: individual shap values corresponding for each inference on test_feature
            - base_values: mean of model output over the training data set
            - global_xai_data:  summary of effect each feature has on inference.
                Includes mean shap value of the feature and correlation coefficient with inference
                result
            - fairness_metrics: a combination of fairness measure and confusion matrices,
                based on fairness_config

        :rtype: Tuple
        """
        # Capture model's general info
        self._log_model_info()

        # TODO: use metrics collector to collect distribution
        # Only generate XAI if there is test data
        if self.test_feat is not None:
            if self.sample_limit is None:
                # Store everything
                sample_idx = list(range(self.test_feat.shape[0]))
            else:
                sample_idx = np.random.choice(
                    self.test_feat.shape[0],
                    size=min(self.sample_limit, self.test_feat.shape[0]),
                    replace=False,
                )
            exp_results = exp.get_explainability(
                self.test_feat,
                sample_idx=sample_idx,
                model=self.model,
                model_type=self.model_type,
                predict_func=self.predict,
                bkgrd_data=self.train_feat,
            )
            self._log_sample_data(
                self.test_feat, self.test_inf, self.test_lbs, sample_idx=sample_idx
            )
            shap_values, base_values = exp_results["indv_data"]
            self.shap_values = shap_values
            self.base_values = base_values
            self.global_xai_data = exp_results["global_data"]
            self._log_xai_data(
                exp_results["indv_data"], exp_results["global_data"], self.test_feat
            )
        if self.fconfig:
            if self.test_feat is None or self.test_lbs is None or self.test_inf is None:
                self.logger.warning(
                    "Calculating fairness metrics requires a test data set, "
                    "labels for the test set, and inference result produced from test_set"
                )
            else:
                self.fairness_metrics = fair.analyze_fairness(
                    self.fconfig, self.test_feat, self.test_inf, self.test_lbs
                )
                self._log_fai_data(self.fairness_metrics, self.fconfig)
        return (
            self.shap_values,
            self.base_values,
            self.global_xai_data,
            self.fairness_metrics,
        )

    def _log_model_info(self):
        module = inspect.getmodule(self.model)
        output = {
            "module_name": getattr(module, "__name__", ""),
            "module_dir": getattr(module, "__file__", ""),
            "module_doc": getattr(module, "__doc__", ""),
            "installed_packages": [
                {"name": pkg.key, "version": pkg.version} for pkg in pkg_resources.working_set
            ],
        }
        if self.api.has_api_settings:
            self._log_data(
                self.api.internal_api.get_model_info_upload_url(), output,
            )
        return output

    def _log_xai_data(
        self,
        indv_xai_data: Tuple[List[np.array], np.array],
        global_xai_data: Dict,
        train_feat: pd.DataFrame,
    ):
        shap_values, expected_value = indv_xai_data
        if self.api.has_api_settings:
            indv_data = {}
            shap_list = [
                pd.DataFrame(data=output_cls, columns=train_feat.columns).to_dict()
                for output_cls in shap_values
            ]
            indv_data["shap"] = shap_list
            indv_data["expected_value"] = expected_value.tolist()

            self._log_data(
                self.api.internal_api.get_individual_explainability_data_upload_url(), indv_data,
            )
            self._log_data(
                self.api.internal_api.get_global_explainability_data_upload_url(), global_xai_data,
            )

    def _log_fai_data(self, fai_data: Dict[str, pd.DataFrame], fairness_config: Dict):
        if self.api.has_api_settings:
            output = {"fairness_config": fairness_config}
            metrics: Dict = {}
            for att_name, fairness_metrics_by_class in fai_data.items():
                metrics[att_name] = {}
                for cl, fairness_metrics in fairness_metrics_by_class.items():
                    fmeasures, confusion_matrix = fairness_metrics
                    metrics[att_name][cl] = fmeasures.to_dict()
                    metrics[att_name][cl]["confusion_matrix"] = confusion_matrix
            output["fairness_metrics"] = metrics
            self._log_data(self.api.internal_api.get_fairness_metrics_upload_url(), output)

    def _log_sample_data(
        self,
        sample_data: pd.DataFrame,
        inf_data: Optional[np.array],
        sample_data_label: Optional[np.array],
        sample_idx: List[int],
    ):
        if self.api.has_api_settings:
            output = {}
            # sample Dataframe is converted to string first to
            # preserve NaN and Inf, which are not compliant JSON values
            features = sample_data.iloc[sample_idx].copy().reset_index(drop=True)
            output["features"] = features.applymap(str).to_dict()
            if sample_data_label is not None:
                output["ground_truth"] = sample_data_label[sample_idx].tolist()
            if inf_data is not None:
                output["inference_result"] = inf_data[sample_idx].tolist()
            self._log_data(
                self.api.internal_api.get_explainability_sample_data_upload_url(), output
            )

    def _log_data(
        self, upload_url: Union[XafaiUploadUrlSchema, BlobStorageSignedUrlSchema], data: Dict
    ):
        try:
            output = {"version": bdrk.__schema_version__, "data": data}
            output_json = json.dumps(output).encode("utf-8")
            compressed_json = gzip.compress(output_json)
            self.api.logger.debug(f"UploadURLData: {upload_url}")
            resp = requests.put(upload_url.url, data=compressed_json, headers=upload_url.headers)
            resp.raise_for_status()
        except ApiException as exc:
            self.api.logger.error(f"API Error: {exc}")
        except requests.exceptions.HTTPError as exc:
            self.api.logger.error(f"Upload request error: {exc}")
