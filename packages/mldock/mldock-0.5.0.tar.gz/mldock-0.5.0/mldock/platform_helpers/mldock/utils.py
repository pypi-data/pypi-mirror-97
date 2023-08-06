import json

def _format_key_as_mldock_env_var(key, prefix=None):
    """
        Formats key as mldock env variable.
        Replace '\s' and '-', append mldock prefix
        and lastly transforms to uppercase
    """
    if prefix is not None:
        key = "{}_{}".format(prefix, key)
    key = key.replace(" ", "_").replace("-", "_")
    key = key.upper()
    return key

def _format_dictionary_as_env_vars(obj: dict, group=None):
    """
        format key and values as appropriate environment variables

        namely:
            - upper case
            - replace spaces with "_"
            - replace dashes with "_"
            - add owner prefix
    """
    new_keys = {}
    for _key,_value in obj.items():

        _key = _format_key_as_mldock_env_var(_key, prefix=group)

        if isinstance(_value, dict):
            _value = json.dumps(_value)

        new_keys.update(
            {
                _key: _value
            }
        )
    return new_keys

def collect_mldock_environment_variables(**env_vars):
    """Collect and format mldock environment variables"""
    return _format_dictionary_as_env_vars(
        env_vars,
        group='mldock'
    )
