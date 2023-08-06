import os
import environs
import json
from pathlib import Path
import logging
import re

from mldock.platform_helpers import utils

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(None)

def get_env_vars(regex, flat=True):
    """Get all environ vars matching contains='<PREFIX>'"""
    if flat:
        filtered_env_vars = []
    else:
        filtered_env_vars = {}

    regex_pattern = re.compile(regex)

    for key,value in os.environ.items():
        if regex_pattern.match(key):
            # get all keys matching the regex
            if flat:
                filtered_env_vars.append({'key': key, 'value': value})
            else:
                filtered_env_vars.append({key: value})
    return filtered_env_vars

class Environment:

    input_channel_regex = None
    model_channel_regex = None
    output_channel_regex = None
    output_channel_regex = None
    hyperparameters_file = None
    environment_variables = environs.Env()

    def __init__(self, base_dir, **kwargs):

        
        self.environment_variables.read_env()
        self.base_dir = base_dir
        self.hyperparameters_file = kwargs.get(
            'hyperparameters_file', 'hyperparameters.json'
        )

        self.input_channel_regex = kwargs.get(
            'input_channel_regex', 'INPUT_CHANNEL_.*'
        )
        self.model_channel_regex = kwargs.get(
            'model_channel_regex', 'MODEL_.*'
        )
        self.output_channel_regex = kwargs.get(
            'output_channel_regex', 'OUTPUT_DIR'
        )
        self.hyperparamters_regex = kwargs.get(
            'hyperparamters_regex', 'hyperparameters'
        )

        self._create_training_directories()
        self.setup_hyperparameters()

    def _create_training_directories(self):
        """Create the directory structure, if not exists
        """
        logger.debug("Creating a new training folder under {} .".format(self.base_dir))

        try:
            self.input_data_dir.mkdir(parents=True, exist_ok=True)
            self.model_dir.mkdir(parents=True, exist_ok=True)
            self.input_config_dir.mkdir(parents=True, exist_ok=True)
            self.output_data_dir.mkdir(parents=True, exist_ok=True)
            if not self.hyperparameters_filepath.exists():
                self._write_json({}, self.hyperparameters_filepath)
        except Exception as exception:
            logger.error(exception)

    @property
    def input_dir(self):
        return Path(self.base_dir, 'input')

    @property
    def input_data_dir(self):
        return Path(self.input_dir, 'data')

    @property
    def input_config_dir(self):
        return Path(self.input_dir, 'config')

    @property
    def hyperparameters_filepath(self):
        return Path(self.input_config_dir, self.hyperparameters_file)

    @property
    def model_dir(self):
        return Path(self.base_dir, 'model')
    
    @property
    def output_data_dir(self):
        return Path(self.base_dir, 'output')

    @property
    def hyperparameters(self):
        """Returns: Iterable of the input channels
        """
        return self._read_json(
            self.hyperparameters_filepath
        )
    
    @staticmethod
    def _read_json(path):  # type: (str) -> dict
        """Read a JSON file.
        Args:
            path (str): Path to the file.
        Returns:
            (dict[object, object]): A dictionary representation of the JSON file.
        """
        with open(path, "r") as f:
            return json.load(f)

    def setup_hyperparameters(self):
        """Retrieves the env vars matching hyperparameters regex and updates config"""
        hyperparameters = self._read_json(
            self.hyperparameters_filepath
        )

        updated_hparams = get_env_vars(
            regex=self.hyperparamters_regex,
            flat=False
        )
        
        hyperparameters.update(
            updated_hparams
        )

        utils._write_json(
            obj=hyperparameters,
            path=self.hyperparameters_filepath
        )

    def get_input_channel_iter(self):
        """Returns: Iterable of the input channels
        """
        return get_env_vars(regex=self.input_channel_regex)

    def get_output_channel_iter(self):
        """Returns: Iterable of the output channel
        """
        return get_env_vars(regex=self.output_channel_regex)

    def get_model_channel_iter(self):
        """Returns: Iterable of the model channel
        """
        return get_env_vars(regex=self.model_channel_regex)
