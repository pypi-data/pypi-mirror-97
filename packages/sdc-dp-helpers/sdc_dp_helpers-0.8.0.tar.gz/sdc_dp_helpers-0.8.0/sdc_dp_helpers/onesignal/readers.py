# pylint: disable=no-self-use

import json
import os
import time
from datetime import datetime, timedelta
import gzip

import requests
import yaml

from sdc_dp_helpers.api_utilities.retry_managers import request_handler
from sdc_dp_helpers.onesignal.config_managers import config_constructor


class CustomOneSignalReader:
    """
        Custom OneSignal Reader
    """

    def __init__(self, api_key_path):
        self.api_key_path = api_key_path
        self.api_creds = self.get_api_key()

        self.app_id = self.api_creds.get('app_id')
        self.api_key = self.api_creds.get('api_key')

    def get_api_key(self) -> dict:
        """
            Gathers key and value pairs of key and their secret.
        """
        with open(self.api_key_path, 'r') as file:
            return yaml.safe_load(file)

    @request_handler(
        wait=int(os.environ.get('REQUEST_WAIT_TIME', 0.1)),
        backoff_factor=float(os.environ.get('REQUEST_BACKOFF_FACTOR', 0.01)),
        backoff_method=os.environ.get('REQUEST_BACKOFF_METHOD', 'random')
    )
    def get_csv_url_data(self, url):
        """
            Once the request is sent to retrieve the CSV url, a short period is needed
            before requesting the data from the server. It is handled here.
            :url: str.
        """
        # wait for csv to generate, this usually takes a few seconds
        attempts = 0
        while True:
            csv_response = requests.get(url)

            if csv_response.status_code == 403:
                print(f'Csv url response: {csv_response} attempt: {attempts}/10')
                time.sleep(1)
                attempts += 1
                # only try 5 times
                if attempts == 10:
                    raise EnvironmentError(f'Failed to retrieve csv data '
                                           f'after 5 attempts from {url}.')

            if csv_response.status_code == 200:
                break

        return gzip.decompress(csv_response.content)

    @request_handler(
        wait=int(os.environ.get('REQUEST_WAIT_TIME', 0.1)),
        backoff_factor=float(os.environ.get('REQUEST_BACKOFF_FACTOR', 0.01)),
        backoff_method=os.environ.get('REQUEST_BACKOFF_METHOD', 'random')
    )
    def get_csv_export(self, config_path=None, filter_now=True):
        """
            This method can be used to generate a compressed CSV
            export of all of your current user data.
            POST: https://onesignal.com/api/v1/players/csv_export?
            :filter_now: bool. Filter based on dynamic date, ie. yesterday.
        """

        url = 'https://onesignal.com/api/v1/players/csv_export'
        header = {'Authorization': f'Basic {self.api_key}'}
        json_payload = config_constructor(app_id=self.app_id, config_path=config_path)

        # if filter_now is true update last_active_since to current date
        if filter_now:
            now = (datetime.now() - timedelta(1)).strftime('%Y%m%d')
            json_payload['last_active_since'] = now

        print(f'Json Payload: {json_payload}')

        url_response = json.loads(
            requests.post(
                url=url,
                json=json_payload,
                headers=header
            ).text
        )
        url = url_response.get('csv_file_url')

        return self.get_csv_url_data(url)

    @request_handler(
        wait=int(os.environ.get('REQUEST_WAIT_TIME', 0.1)),
        backoff_factor=float(os.environ.get('REQUEST_BACKOFF_FACTOR', 0.01)),
        backoff_method=os.environ.get('REQUEST_BACKOFF_METHOD', 'random')
    )
    def get_view_notifications(self, config_path=None):
        """
            View the details of multiple notifications.
            Returns offsets so this can be managed with the context.
            GET: https://onesignal.com/api/v1/notifications
            :config_path: str.
        """
        url = 'https://onesignal.com/api/v1/notifications'
        header = {
            'Content-Type': 'application/json; charset=utf-8',
            'Authorization': f'Basic {self.api_key}'
        }
        json_payload = config_constructor(app_id=self.app_id, config_path=config_path)

        print(f'Json Payload: {json_payload}')

        with requests.session() as session:
            response = session.get(
                url=url,
                json=json_payload,
                headers=header
            ).json()

            # loop through all available pages and apply them to a list
            data_set, total_count = list(), response.get('total_count')
            for offset in range(0, total_count):
                print(f'At offset: {offset}/{total_count}')
                json_payload['offset'] = offset

                response = session.get(
                    url=url,
                    json=json_payload,
                    headers=header
                ).json()

                notifications = response.get('notifications', None)[0]

                # handle end of offset for extra security
                if not notifications:
                    break
                data_set.append(notifications)

            return json.dumps(data_set)
