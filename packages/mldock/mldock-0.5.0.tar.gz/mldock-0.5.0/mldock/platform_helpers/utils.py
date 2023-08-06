import json

def _write_json(obj, path):  # type: (object, str) -> None
    """Write a serializeable object as a JSON file."""
    with open(path, "w") as f:
        json.dump(obj, f, indent=4)
        f.write('\n')

def _make_sagemaker_input_data_configs(data_channels: list):
    """restructures a list of data names as sagemaker input data configs"""
    return {name: {} for name in data_channels}

def _extract_data_channels_from_mldock(mldock_data: list):

    data_channels = [
        data_config['channel'] for data_config in mldock_data
    ]

    return _make_sagemaker_input_data_configs(data_channels=data_channels)