from datetime import datetime

import yaml


def get_config(configs):
    """
        Gathers query configurations.yml file data.
    """
    with open(configs, 'r') as file:
        config = yaml.safe_load(file)
    return config


def date_to_unix(date_string, fmt='%Y-%m-%d'):
    """
        Takes a standard date string and converts it into unix timestamp.
    """
    date = datetime.strptime(date_string, fmt)
    return date.strftime("%s")


def config_constructor(app_id, config_path=None):
    """
        Constructs a valid json payload for the OneSignal method.
        :api_key: str. the api key is required in the payload
        :config_path: str. filepath to the config.yml file
    """
    payload = {'app_id': app_id}

    # only add configs if there is a path
    if config_path:
        configs = get_config(config_path)

        # ensure last_active_since is unix
        if 'last_active_since' in configs:
            configs['last_active_since'] = date_to_unix(configs['last_active_since'])

        payload.update(configs)
    return payload
