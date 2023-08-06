"""
    PLATFORM HELPERS

    utils used to interact with specific platform from a docker perspective.
    E.g. cloud storage tools to upload and download objects.
"""
import os
import glob
from google.cloud import storage
from pathlib import Path
import tarfile
import zipfile
from typing import Iterator
import logging
from urllib.parse import urlparse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(None)
logger.setLevel(logging.INFO)

def _mkdir(dir_path: str):
    """make directory structure

    Args:
        dir_path (str): directory path to build
    """
    p = Path(dir_path)
    p.mkdir(parents=True, exist_ok=True)

def _iter_nested_dir(root_dir: str) -> Iterator[str]:
    """Iterate through nested folders.

    Args:
        root_dir (str): name of the directory to start form

    Yields:
        Iterator[str]: path iterator
    """
    rootdir = Path(root_dir)
    for path in rootdir.glob('**/*'):
        yield path

def _delete_file(file_path):
    """Delete a file

    Args:
        file_path (str): path to file

    Raises:
        TypeError: Expected a file_path of type file. Cannot be directory or other.
    """
    path = Path(file_path)
    if not path.is_file():
        raise TypeError("Expected a file_path of type file. Only deletes files")

    os.remove(path)

def _check_if_cloud_scheme(url: str, scheme: str = 's3') -> bool:
    parsed_url = urlparse(url)
    return parsed_url.scheme == scheme

def parse_url(url: str, scheme: str = 's3'):
    """Returns an (s3 bucket, key name/prefix) tuple from a url with an s3
    scheme.
    Args:
        url (str):
    Returns:
        tuple: A tuple containing:
            - str: S3 bucket name
            - str: S3 key
    """
    parsed_url = urlparse(url)
    if parsed_url.scheme != scheme:
        raise ValueError("Expecting '{}' scheme, got: {} in {}.".format(scheme, parsed_url.scheme, url))
    return parsed_url.netloc, parsed_url.path.lstrip("/")

def zip_folder(dir_path, output_file, rm_original=True):
    """zip in directory and optionally throw away unzipped"""

    with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in _iter_nested_dir(dir_path):
            if file.name != Path(output_file).name and file.is_file():
                zipf.write(os.path.join(file), arcname=file.relative_to(dir_path))
                if rm_original:
                    _delete_file(file)

def zip_folder_as_tarfile(dir_path, output_file, rm_original=True):
    """zip folder as tarfile and optionally throw away original files"""
    with tarfile.open(output_file, "w:gz") as tar:
        for file in _iter_nested_dir(dir_path):
            if file.name != Path(output_file).name and file.is_file():
                tar.add(file, arcname=file.relative_to(dir_path))
                if rm_original:
                    _delete_file(file)

def unzip_file(filename, output_dir, rm_zipped=True):
    """unzip in directory and optionally throw away zipped"""
    with zipfile.ZipFile(filename, 'r', zipfile.ZIP_DEFLATED) as zipf:
        logger.info("Unzipping {} => {}".format(filename, output_dir))
        zipf.extractall(output_dir)
        if rm_zipped:
            logger.info("Removing {}".format(filename))
            _delete_file(filename)

def unzip_file_from_tarfile(filename, output_dir, rm_zipped=True):
    """untar in directory and optionally throw away zipped"""
    with tarfile.open(filename, "r:gz") as tar:
        logger.info("Zipping {} => {}".format(filename, output_dir))
        tar.extractall(output_dir)
        if rm_zipped:
            logger.info("Removing {}".format(filename))
            _delete_file(filename)

def download_folder(
    bucket_name: str,
    prefix: str,
    target: str
):
    """download folder from google cloud storage, ignoring folders.

    Args:
        bucket_name (str): [description]
        prefix (str): [description]
        target (str): [description]
    """
    logger.info("Starting Folder download from cloud storage")
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blobs = bucket.list_blobs(prefix=prefix)  # Get list of files
    for blob in blobs:
        filename = blob.name.rsplit('/',1)[1]#.replace('/', '_')

        if len(filename) > 0:
            
            fullpath = os.path.join(bucket_name, prefix, filename)
            dst_filepath = os.path.join(target, os.path.basename(prefix))
            file_destination = os.path.join(dst_filepath, filename)

            logger.info("Download {} to local at {}".format(filename, file_destination))
            # make directory
            _mkdir(dst_filepath)
            # download
            blob.download_to_filename(file_destination)

def upload_folder(local_path: str, bucket_name: str, prefix: str):
    """Upload folder and contents to cloud storage

    Args:
        local_path (str): path to local directory
        bucket_name (str): bucket name to upload files to
        prefix (str): cloud filepath to write files to
    """
    logger.info("Starting Folder Upload to cloud storage")
    # get bucket
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    assert os.path.isdir(local_path)
    for path in _iter_nested_dir(local_path):
        filepath = path.relative_to(local_path)
        storage_destination = os.path.join(prefix, filepath)
        if path.is_file():
            logger.info("Upload {} to cloud at {}".format(path, storage_destination))
            blob = bucket.blob(storage_destination)
            blob.upload_from_filename(path)

def download_input_assets(storage_dir_path: str, local_path: str, scheme: str = 'gs'):
    """download input asset folder from path, given that path is cloud storage path.

    Args:
        storage_dir_path (str): path to data in cloud storage
        local_path (str): where data should be stored (this comes from the environment).
        scheme (str, optional): scheme for cloud storage url. Defaults to 'gs'.
    """
    is_cloud_storage = _check_if_cloud_scheme(url=storage_dir_path, scheme=scheme)

    if is_cloud_storage:
        # download data if cloud storage path
        bucket, prefix = parse_url(url=storage_dir_path, scheme=scheme)
        download_folder(bucket_name=bucket, prefix=prefix, target=local_path)
    else:
        Exception("No Cloud storage url was found. Must have gs:// schema")

def package_and_upload_model_dir(local_path: str, storage_dir_path: str, scheme: str = 'gs'):
    """
        Packages model/ dir as .tar.gz and uploads to cloud storage, given that storage_dir_path
        is cloud storage url path.

        Args:
            local_path (str): path to model directory
            storage_dir_path (str): cloud storage path destination
            scheme (str, optional): cloud storage url scheme. Defaults to 'gs'.
    """
    is_cloud_storage = _check_if_cloud_scheme(url=storage_dir_path, scheme=scheme)
    if is_cloud_storage:
        zip_folder_as_tarfile(
            dir_path=local_path,
            output_file=os.path.join(local_path, 'model.tar.gz'),
            rm_original=True
        )
        bucket, prefix = parse_url(url=storage_dir_path, scheme=scheme)
        upload_folder(local_path=local_path, bucket_name=bucket, prefix=prefix)
    else:
        Exception("No Cloud storage url was found. Must have gs:// schema")

def package_and_upload_output_data_dir(local_path: str, storage_dir_path: str, scheme: str = 'gs'):
    """
        Packages output/ dir as .tar.gz and uploads to cloud storage, given that storage_dir_path
        is cloud storage url path.

        Args:
            local_path (str): path to model directory
            storage_dir_path (str): cloud storage path destination
            scheme (str, optional): cloud storage url scheme. Defaults to 'gs'.
    """
    is_cloud_storage = _check_if_cloud_scheme(url=storage_dir_path, scheme=scheme)

    if is_cloud_storage:
        bucket, prefix = parse_url(url=storage_dir_path, scheme=scheme)
        upload_folder(local_path=local_path, bucket_name=bucket, prefix=prefix)
    else:
        Exception("No Cloud storage url was found. Must have gs:// schema")
