import os
import io
import csv
import logging
import numpy as np
from mldock.platform_helpers.mldock.errors import extract_stack_trace
from mldock.platform_helpers import environment as mldock_environment
from mldock.platform_helpers.mldock.model_service import base

environment = mldock_environment.Environment(base_dir='/opt/ml')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(None)
logger.setLevel(logging.INFO)

class ModelService(base.ModelService):
    model = None

    @classmethod
    def load_model(cls, model_path):
        """Get the model object for this instance, loading it if it's not already loaded."""
        if cls.model == None:
            # TODO place your model load code here
            # get your model from MODEL_DIR
            cls.model = None
        return cls.model

    @staticmethod
    def input_transform(input):
        """
            Custom input transformer

            args:
                input: raw input from request
        """
        return input

    @staticmethod
    def output_transform_json(pred):
        """transform numpy array of predictions into json payload"""
        results = pred.tolist()
        return {'results': results}

    @staticmethod
    def output_transform_csv(pred, headers=False):
        """Transform numpy array of predictions in to csv"""
        predictions = pred.tolist()

        # create results
        results = []
        if headers == True:
            results.append(('idx','prediction'))
        # append values
        [
            results.append(
                (i,
                pred)
            ) for (i, pred) in enumerate(predictions)
        ]

        return results

    @classmethod
    def output_transform(cls, predictions, **kwargs):
        """
            Custom output transformation code
        """
        content_type = kwargs.get('content_type')
        if  content_type == 'csv':
            return cls.output_transform_csv(
                predictions,
                headers=kwargs.get('headers', False)
            )
        elif content_type == 'json':
            return cls.output_transform_json(predictions)
        else:
            raise Exception((
                "{} content type not supported. "
                "Only supports json or csv.".format(content_type)
            ))

    @classmethod
    def predict(cls, input):
        """For the input, do the predictions and return them.

        Args:
            input (a pandas dataframe): The data on which to do the predictions. There will be
                one prediction per row in the dataframe"""
        try:
            # TODO replace this with your model.predict
            pred = np.array(['pred_1', 'pred_2', 'pred_3'])
            logger.info(pred)
            return pred
        except Exception as exception:
            # get stack trace as exception
            stack_trace = extract_stack_trace()
            reformatted_log_msg = (
                    'Server Error: {ex}'.format(ex=stack_trace)
            )
            return reformatted_log_msg


def handler(json_input, content_type='json'):
    """
    Prediction given the request input
    :param json_input: [dict], request input
    :return: [dict], prediction
    """
    
    model_service = ModelService(model_path=os.path.join(environment.model_dir, "model.joblib"))

    # TODO input transformer
    model_input = model_service.input_transform(input)

    # TODO model prediction
    pred = model_service.predict(model_input)
    logger.info(pred)
    # TODO Add any output processing
    results = model_service.output_transform(
        predictions=pred,
        content_type=content_type,
        headers=environment.environment_variables.bool('MLDOCK_HEADERS')
    )

    return results
