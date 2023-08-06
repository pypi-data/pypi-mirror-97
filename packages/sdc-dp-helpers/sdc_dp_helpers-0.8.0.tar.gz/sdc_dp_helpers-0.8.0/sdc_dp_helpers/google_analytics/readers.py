"""
    CUSTOM READERS CLASSES
        - Class which manages reader tasks like auth, requests, pagination
"""
import os
from typing import Callable

import httplib2
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

from sdc_dp_helpers.api_utilities.retry_managers import request_handler


class BaseGAV4Reader:
    """
        Base Google Analytics V4 reader class.

        Used as basis for building custom GA V4 readers, it requires that you
        add your own Authentication through the auth_credentials method.
        The basic workflow is:
        (1) Create credentials
        (2) Build google service object
        (3) Return an iterable of the get_report method
        (4) Iterate until no pagination token is found. A.k.a. pageToken==None
    """
    analytics = None
    max_pages = None

    class ReaderIter:
        """Inner Class - Iterator that yields queries until max pages or pageToken == None."""
        page_counter = 0

        def __init__(
                self,
                *,
                query_fn: Callable,
                query: list,
                page_token: str = None,
                **kwargs
        ):
            self.query_fn = query_fn
            self.max_pages = kwargs.get("max_pages", None)
            self.page_token = page_token
            self.query = query

        def __iter__(self):
            """Iterator method for iterator class"""
            return self

        def __next__(self):
            """
                Next method for iterator class which includes
                the StopIteration criteria for iterable
            """
            # check StopIteration criteria
            if self.max_pages is not None:
                if self.page_counter >= self.max_pages:
                    print("stopping iteration on max pages = {}".format(self.max_pages))
                    raise StopIteration

            if self.page_counter > 0 and self.page_token is None:
                print("stopping iteration on pageToken = {}".format(self.page_token))
                raise StopIteration

            # run get_report
            report, self.page_token = self.query_fn(
                queries=self.query,
                page_token=self.page_token
            )
            print(
                'Finished query function for page {page} of view ID {view_id}'.format(
                    page=self.page_counter + 1,
                    view_id=self.query[0].get('viewId')
                )
            )

            # increment pagination counter
            self.page_counter += 1

            return report

    # pylint: disable=no-member
    def build_analytics_service_object(
            self,
            api_name: str = 'analyticsreporting',
            api_version: str = 'v4'
    ):
        """Initializes the analytics reporting service object.
        args:
        client_secrets_path (json) : Google API OAuth2 API credentials
        scopes (list or iterable) : scopes for Google OAuth2 authentication

        Returns:
        analytics an authorized analyticsreporting service object.
        """
        # authorize HTTP object
        http = self.credentials.authorize(http=httplib2.Http())
        # Build the service object.
        return build(api_name, api_version, http=http)

    @request_handler(
        wait=int(os.environ.get('REQUEST_WAIT_TIME', 0)),
        backoff_factor=float(os.environ.get('REQUEST_BACKOFF_FACTOR', 0.01)),
        backoff_method=os.environ.get('REQUEST_BACKOFF_METHOD', 0.01)
    )
    def get_report(
            self,
            queries: list,
            page_token: str = None
    ):
        """
            Use the Analytics Service Object to query the Analytics Reporting API V4.

            args:
            analytics : analytics reporting service object
            query (list): array of queries. [max. 5]
            page_token (str): token sent denoting the last scraped data point
            return:
            analytics report data (json)

        """
        if page_token is not None:
            for query in queries:
                query.update({'page_token': page_token})

        # run batch query
        report = self.analytics.reports().batchGet(body={
            'reportRequests': queries}).execute().get('reports')
        page_token = report[0].get('nextPageToken')

        return report, page_token

    def run_query(self, query: list, page_token: str = None):
        """
            returns a sync iterator
        """
        iter_ = self.ReaderIter(
            query_fn=self.get_report,
            query=query,
            max_pages=self.max_pages,
            page_token=page_token)
        return iter_


class CustomGoogleAnalyticsReaderWithServiceAcc(BaseGAV4Reader):
    """
        Custom Google Analytics Reader which authenticates with Service account
    """

    # pylint: disable=super-init-not-called
    def __init__(
            self,
            service_account_secrets_path: str,
            service_account_email: str,
            scopes: list,
            **kwargs
    ):
        self.max_pages = kwargs.get("max_pages", None)
        self.credentials = self.auth_credentials(
            service_account_secrets_path, service_account_email, scopes)
        # build analytics object
        self.analytics = self.build_analytics_service_object()

    @staticmethod
    def auth_credentials(
            service_account_secrets_path,
            service_account_email,
            scopes
    ):
        """Get a service that communicates to a Google API.
        Args:
            service_account_secrets_path: The filepath to service secrets.
            api_name: The name of the api to connect to.
            api_version: The api version to connect to.
            scope: A list auth scopes to authorize for the application.
            key_file_location: The path to a valid service account p12 key file.
            service_account_email: The service account email address.
            scopes: Allowed scopes for the given credentials
        Returns:
            A service that is connected to the specified API.
        """
        return ServiceAccountCredentials.from_p12_keyfile(
            service_account_email, service_account_secrets_path, scopes=scopes)
