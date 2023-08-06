import json
from abc import abstractmethod
from datetime import datetime
from typing import Any, AnyStr, BinaryIO, List, Mapping, Optional, Union
from uuid import UUID

from ..monitoring.context import PredictionContext
from ..monitoring.registry import is_single_value

# Predict output can be a str, float, int, or dictionary of class probability
ScoreVector = Union[List[str], List[float], List[int], List[Mapping[str, float]]]


class ExpressConfig:
    log_top_score: bool = True


class BaseModel:
    """
    All Models declared in serve.py should inherit from BaseModel.
    """

    # self.config contains logging and other settings
    config: ExpressConfig = ExpressConfig()

    def pre_process(
        self, http_body: AnyStr, files: Optional[Mapping[str, BinaryIO]] = None
    ) -> List[List[float]]:
        """
        Converts http_body (or files) to something that can be passed into predict().
        Typically, the result is an array of feature vectors.

        :param http_body: The serialized http request body
        :type http_body: AnyStr
        :param files: A dictionary of field names to file handles
        :type files: Optional[Mapping[str, BinaryIO]], defaults to None
        :return: Array of feature vectors
        :rtype: List[List[float]]
        """
        samples = json.loads(http_body)
        return [[float(x) for x in s] for s in samples]

    def post_process(
        self, score: ScoreVector, prediction_id: str
    ) -> Union[AnyStr, Mapping[str, Any]]:
        """
        Converts the output from predict() into a http response body, either as bytes or json.

        :param score: The array of inference results returned from predict
        :type score: Union[List[str], List[float], List[int], List[Mapping[str, float]]]
        :param prediction_id: A generated id that can be used to look up this prediction
        :type prediction_id: str
        :return: The http response body
        :rtype: Union[AnyStr, Mapping[str, Any]]
        """
        return {"result": score, "prediction_id": prediction_id}

    @abstractmethod
    def predict(self, features: List[List[float]]) -> ScoreVector:
        """
        Makes an inference using the initialised model.

        :param features: The array of feature vectors returned from pre_process
        :type features: List[List[float]]
        :return: The array of inference results
        :rtype: Union[List[str], List[float], List[int], List[Mapping[str, float]]]
        """
        raise NotImplementedError

    def validate(self, skip_preprocess: bool = False, **kwargs):
        """
        Validates the call chain: post_process(predict(pre_process(http_body)), prediction_id)
        for any runtime error, including mismatched argument and return types, unsupported
        serialisation format, etc.

        :param skip_preprocess: Whether to skip checking the return value of pre_process
        :type skip_preprocess: bool
        """
        # Check predict function can be chained
        processed_sample = self.pre_process(**kwargs)
        prediction = self.predict(features=processed_sample)
        context = PredictionContext(
            entity_id=UUID("88888888-4444-4444-4444-cccccccccccc"),
            features=[],
            request_body="",
            server_id="localhost",
            output=1,
            created_at=datetime(year=2018, month=9, day=1),
        )
        processed_prediction = self.post_process(
            score=prediction, prediction_id=context.prediction_id
        )

        if not skip_preprocess:
            # Check sample features are iterable and flattened for instrumentation
            assert (
                not is_single_value(processed_sample)
                and not any(is_single_value(f) for f in processed_sample)
                and all(all(is_single_value(f) for f in s) for s in processed_sample)
            ), "self.pre_process() should output List[List[float]]"

        # Check predicted scores are iterable
        assert not is_single_value(prediction) and all(is_single_value(p) for p in prediction), (
            "self.predict() should output List[str], List[float], List[int], "
            "or List[Mapping[str, float]]"
        )
        assert len(processed_sample) == len(
            prediction
        ), "self.predict() should output an equal length vector as its input features"

        # Check response body is serialisable
        assert is_single_value(
            processed_prediction
        ), "self.post_process() should output str, bytes, or Mapping[str, Any]"

        return processed_prediction
