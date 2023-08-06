"""
    CUSTOM FALCON READER CLASSES
"""
from contextlib import contextmanager
from datetime import datetime, timedelta

import os
import requests
import simplejson
import yaml
from sdc_dp_helpers.api_utilities.retry_managers import request_handler


class CustomFalconReader:
    """
        Custom Falcon Reader
    """

    def __init__(self, api_key_path, config_path=None):
        self.api_key_path = api_key_path
        self.config_path = config_path

        self.api_key = self.get_api_key()
        self.config = self.get_configuration()

        self.request_session = requests.Session()

    def get_api_key(self):
        """
            Gathers key and value pairs of client and their token.
        """
        with open(self.api_key_path, 'r') as file:
            data = yaml.safe_load(file)
            return data.get('api_key')

    def get_configuration(self):
        """
            Gathers optional and required configuration that
            defines the params for the api. This is optional.
            The configuration resembles the parameters of the
            given api method. eg:

            since: '2020-10-01T22:00:00.000Z'
            until: '2021-02-09T22:00:00.000Z'
            channels:
                - 'twitter_110592_91962761'
                - 'linkedin_110592_4840205'
            statuses:
                - 'all'
            limit: '30'
        """
        if self.config_path is not None:
            with open(self.config_path, 'r') as file:
                data = yaml.safe_load(file)
                return data
        return None

    def get_channel_ids(self):
        """
            Gather all available channel ids.
        """
        url = 'https://api.falcon.io/channels?apikey={apikey}' \
            .format(apikey=self.api_key)

        # no configs required, everything should be fetched, set limit to as high as possible
        try:
            response = requests.get(url=url, params={'limit': '999'}).json()
        except simplejson.errors.JSONDecodeError as err:
            raise EnvironmentError from err

        data_set = []
        for items in response['items']:
            data_set.append(items['id'])

        return data_set

    @request_handler(
        wait=int(os.environ.get('REQUEST_WAIT_TIME', 0.1)),
        backoff_factor=float(os.environ.get('REQUEST_BACKOFF_FACTOR', 0.01)),
        backoff_method=os.environ.get('REQUEST_BACKOFF_METHOD', 'random')
    )
    @contextmanager
    def metrics_by_channel_context(self,
                                   channel_ids,
                                   offset=0,
                                   filter_now_type='all',
                                   filter_now=True):
        """
        Get metrics by channel Id context returns a request session with the ability
        to page with offsets.
        :channel_ids: list. List of channels for the API to return metrics on.
        :offset: int. Offset number from 0 until None is returned.
        :filter_now_type: str. filter type of 'all', 'default' or 'post'
        :filter_now: bool. Flag to set date filter to dynamic, in this case yesterdays data.
                     (today often returns none)

        To use the context use 'with', expect none when no more data is available in the
        context request session:

        offset = 0
        while True:
            with reader.metrics_by_channel_context(channel_ids=channels, offset=offset) as response:
                data = response.json()

                if data is None:
                    break

            print(data)
            offset += 1

        """
        url = 'https://api.falcon.io/measure/api/v1/content/metrics?apikey={apikey}' \
            .format(apikey=self.api_key)

        params = self.config
        params['channels'] = channel_ids

        # there are three options for dynamic time filtering
        if filter_now:
            now = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')
            if filter_now_type == 'default':
                params['since'] = now
                params['until'] = now
            elif filter_now_type == 'post':
                params['postsSince'] = now
                params['postsUntil'] = now
            elif filter_now_type == 'all':
                params['since'] = now
                params['until'] = now
                params['postsSince'] = now
                params['postsUntil'] = now
            else:
                raise ValueError('{val} is not a valid filter_today_type option'.format(
                    val=filter_now_type
                ))

        params['offset'] = offset
        try:
            yield self.request_session.post(url=url, json=params)
        except Exception as err:
            raise err
