import warnings

import yaml


def get_queries(configs):
    """
        Gathers query configurations.yml file data.
    """
    with open(configs, 'r') as file:
        query_config = yaml.safe_load(file)
    return query_config.get('query_config')


class ConfigManager:
    """
        SailThru Config Manager
    """
    def __init__(self, sailthru_client, query):
        self.sailthru_client = sailthru_client
        self.query = query

    def get_stat_api(self):
        """
            Request various stats from Sailthru about primary list
            membership or campaign and triggered message activity.
            Endpoint URL: https://api.sailthru.com/stats

            :return: If there is no relevant data, none is
                     returned and reason is printed.
        """
        response = self.sailthru_client.api_get(
            action='stats',
            data=self.query
        )

        # fatal false negative is raised, this needs to be handled
        if not response.is_ok():
            error = response.get_error()
            message = 'APIError:{}, Status Code:{}, Error Code:{}'.format(
                error.get_message(),
                str(response.get_status_code()),
                str(error.get_error_code()))
            if (str(response.get_status_code()) != '404'
                    and str(error.get_error_code()) != '99'):
                raise RuntimeError(message)
            else:
                warnings.warn(message)

        elif response.is_ok():
            response_data = response.get_body()
            response_data.update({
                'stat': self.query.get('stat'),
                'template': self.query.get('template')
            })

            print(f'Response Data: {response_data}')
            return response_data
        else:
            return None
