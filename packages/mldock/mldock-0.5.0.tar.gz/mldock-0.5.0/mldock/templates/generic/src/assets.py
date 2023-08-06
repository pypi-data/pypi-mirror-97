import os
from pathlib import Path
import logging

from mldock.platform_helpers.environment import Environment, get_env_vars

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(None)

class CustomEnvironment(Environment):
    """
        Extends the Environment class to give us
        more specific environment setup functionality
    """

    def setup_inputs(self):
        """ Iterates and downloads assets remoate -> input channels
        """
        for channel in self.get_input_channel_iter():
            logger.info("Setup Inputs: Must implement download scripts from remote")

    def cleanup_outputs(self):
        """ Iterates and uploads output channel -> remote
        """
        for channel in self.get_output_channel_iter():
            logger.info("Cleanup Outputs: Must implement download scripts to remote")

    def setup_model_artifacts(self):
        """ Iterates and downloads assets remoate -> model channel
        """
        for channel in self.get_model_channel_iter():
            logger.info("Setup Model: Must implement download scripts from remote")

    def cleanup_model_artifacts(self):
        """ Iterates and uploads from model channel -> remote
        """
        for channel in self.get_model_channel_iter():
            logger.info("Cleanup Model: Must implement download scripts to remote")

class TrainingContainer:
    """
        A set of tasks for setup and cleanup of container
    """
    def __init__(self):
        self.environment = CustomEnvironment(base_dir='/opt/ml')

    def startup(self):
        logger.info("\n\n --- Running Startup Script ---")
        if self.environment.environment_variables('stage', default='dev') == "prod":
            logger.debug("Env == Prod")
            self.environment.setup_inputs()
            self.environment.setup_model_artifacts()
        logger.info("--- Setup Complete --- \n\n")

    def cleanup(self):
        """clean up tasks executed on container task complete"""
        logger.info("\n\n --- Running Cleanup Script ---")
        logger.info("Cleaning Up Training Container")
        if self.environment.environment_variables('stage', default='dev') == "prod":
            logger.info("Env == Prod")
            self.environment.setup_inputs()
            self.environment.cleanup_model_artifacts()
        logger.info("--- Cleanup Complete --- \n\n")

class ServingContainer:
    """
        A set of tasks for setup and cleanup of container
    
        note:
            - Only supports a startup script. Cleanup is a bit fuzzy for serving.
    """
    def __init__(self):
        self.environment = CustomEnvironment(base_dir='/opt/ml')

    def startup(self):
        logger.info("\n\n --- Running Startup Script ---")
        logger.info("Setting Up Training Container")
        
        if self.environment.environment_variables('stage', default='dev') == "prod":
            logger.info("Env == Prod")
            self.environment.setup_model_artifacts()
        logger.info("\n\n --- Setup Complete --- \n\n")

    def cleanup(self):
        """clean up tasks executed on container task complete"""
        pass
