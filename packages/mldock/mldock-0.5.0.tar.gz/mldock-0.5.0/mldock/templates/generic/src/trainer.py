"""
    TRAINER SCRIPT - contains custom code for training your model
"""
import os
import sys
import json
import argparse
import logging
import pickle

from mldock.platform_helpers import environment as mldock_environment
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('mldock')

def str2bool(arg_value: str) -> bool:
    if isinstance(arg_value, bool):
        return arg_value
    if arg_value.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif arg_value.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def str2dict(arg_value: str) -> dict:
    d_argvalue = json.loads(arg_value)
    if isinstance(d_argvalue, dict):
        return d_argvalue
    else:
        raise argparse.ArgumentTypeError('Json Dictionary expected.')

def run_training():

    environment = mldock_environment.Environment(base_dir='/opt/ml/')

    PARSER= argparse.ArgumentParser()
    ## User set params which link to Sagemaker params
    PARSER.add_argument('--lookup', type=str,
                        default=os.path.join(environment.input_data_dir, 'lookup'),
                        help='Expects a .csv file, representing the lookup.')
    PARSER.add_argument('--detail', type=str,
                        default=os.path.join(environment.input_data_dir, 'detail'),
                        help='Expects a .csv file, representing the detail.')
    PARSER.add_argument('--factors', default=environment.hyperparameters.get('factors', 20),
                        type=int,
                        help='Number of factorization factors to compute during model fit.')
    PARSER.add_argument('--regularization', default=environment.hyperparameters.get('regularization', 0.3),
                        type=int,
                        help='Coefficient of regularization to apply during model fit.')
    PARSER.add_argument('--iterations', default=environment.hyperparameters.get('iterations', 10),
                        type=int,
                        help='Number iterations of the dataset should be run during model fit.')
    PARSER.add_argument('--run_eval', default=environment.hyperparameters.get('run_eval', True),
                        type=str2bool,
                        help='Whether to run metrics evaluation prior to training model on full data.')
    PARSER.add_argument('--refit', default=environment.hyperparameters.get('refit', True),
                        type=str2bool,
                        help='Whether or not to save model.')

    # Get args
    ARGS, _ = PARSER.parse_known_args()


    logger.info("Experiment id = {}".format(environment.environment_variables('MLDOCK_EXPERIMENT_ID', default=None)))
    if ARGS.run_eval:
        logger.info('Running Evaluation')
        # TODO Add your Evaluation Fitting here
        logger.info("Data found at {}\n{}".format(ARGS.lookup, os.listdir(ARGS.lookup)))
        logger.info("Some hyperparameters = factors={}, regularization={}, iterations={}".format(ARGS.factors, ARGS.regularization, ARGS.iterations))


    # save model to s3
    if ARGS.refit:
        logger.info('Refitting Final Model')
        # TODO Add model.fit(X) here again


        # save model to s3
        logger.info("Model saved in {}. This is written back to s3 at job completion.".format(environment.model_dir))
        model_path = os.path.join(environment.model_dir, 'model.pkl')
        # TODO add model saving workflow here

        model_fake = { "lion": "yellow", "kitty": "red" }

        with open(model_path, 'wb') as file_:
            pickle.dump(model_fake, file_)
    else:
        logger.debug("Skipping model save step. ")

if __name__ == '__main__':

    try:
        run_training()
    except Exception as exception:
        logger.error(exception)
