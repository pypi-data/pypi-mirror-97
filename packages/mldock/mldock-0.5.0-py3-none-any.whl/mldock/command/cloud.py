import os
import sys
import logging
import click

from mldock.platform_helpers.docker.auth import login_and_authenticate
from mldock.api.local import \
    docker_build
from mldock.api.cloud import \
    push_image_to_repository
from mldock.config.config_manager import \
    MLDockConfigManager

click.disable_unicode_literals_warning = True
logger=logging.getLogger('mldock')

@click.group()
def cloud():
    """
    Commands for local operations: train and deploy
    """
    pass

@click.command()
@click.option(
    '--dir',
    help='Set the working directory for your mldock container.',
    required=True,
    type=click.Path(
        exists=True,
        file_okay=False,
        dir_okay=True,
        writable=True,
        readable=True,
        resolve_path=False,
        allow_dash=False,
        path_type=None
    )
)
@click.option('--no-cache', help='builds container from scratch', is_flag=True)
@click.option(
    '--build',
    help='Set the working directory for your mldock container.',
    is_flag=True
)
@click.option(
    '--provider',
    help='Set the cloud provider',
    required=True,
    type=click.Choice(['ecr'],
    case_sensitive=False
    )
)
@click.pass_obj
def push(obj, dir, build, provider, no_cache):
    """
    Command to push docker container image to ECR using your default AWS sdk credentials.

    note: Override default AWS credentials by providing AWS_DEFAULT_PROFILE environment variable.
    """
    helper_library_path = obj['helper_library_path']
    try:
        mldock_manager = MLDockConfigManager(
            filepath=os.path.join(dir, ".mldock.json")
        )
        # get mldock_module_dir name
        mldock_config = mldock_manager.get_config()
        image_name = mldock_config.get("image_name", None)
        container_dir = mldock_config.get("container_dir", None)
        module_path = os.path.join(
            dir,
            mldock_config.get("mldock_module_dir", "src"),
        )
        dockerfile_path = os.path.join(
            dir,
            mldock_config.get("mldock_module_dir", "src"),
            container_dir
        )
        requirements_file_path = os.path.join(
            dir,
            mldock_config.get("requirements.txt", "requirements.txt")
        )
        if image_name is None:
            raise Exception("\nimage_name cannot be None")
        elif image_name.endswith(":latest"):
            raise Exception("\nImage version is not supported at this point. Please remove :latest versioning")
        else:

            # login and authenticate
            client, metadata = login_and_authenticate(provider=provider, region='eu-west-1')
            image_repository = "{}/{}".format(metadata['repository'], image_name)
            logger.info("\nLogin Complete! ヽ(´▽`)/\n")

            # build image for cloud repository
            docker_build(
                image_name=image_repository,
                dockerfile_path=dockerfile_path,
                module_path=module_path,
                target_dir_name=mldock_config.get("mldock_module_dir", "src"),
                requirements_file_path=requirements_file_path,
                no_cache=no_cache
            )

            # Push image to cloud repository
            push_image_to_repository(
                image_repository=image_repository,
                auth_config = {'username': metadata['username'], 'password': metadata['password']},
                tag='latest'
            )
            logger.info("\nPush Complete! ヽ(´▽`)/\n")

    except Exception as e:
        logger.error("{}".format(e))
        sys.exit(-1)

cloud.add_command(push)
