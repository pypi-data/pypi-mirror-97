"""
    Set up the sdc_helpers package
"""
from setuptools import setup

setup(
    name='sdc_dp_helpers',
    packages=
    [
        'sdc_dp_helpers',
        'sdc_dp_helpers.google_analytics',
        'sdc_dp_helpers.sailthru',
        'sdc_dp_helpers.azure',
        'sdc_dp_helpers.api_utilities',
        'sdc_dp_helpers.falcon',
        'sdc_dp_helpers.onesignal',
    ],
    install_requires=[
        'boto3',
        'google-api-python-client',
        'httplib2',
        'pathlib',
        'oauth2client',
        'numpy',
        'pandas',
        'pyOpenSSL',
        'python-interface',
        'sailthru-client',
        'azure-storage-blob',
        'sdc-helpers==1.6.2'
    ],
    description='A module for developing data pipelines from external api\'s',
    version='0.8.1',
    url='http://github.com/RingierIMU/sdc-dataPipeline-helpers',
    author='Ringier South Africa',
    author_email='tools@ringier.co.za',
    keywords=[
        'pip',
        'datapipeline',
        'helpers',
    ],
    download_url='https://github.com/RingierIMU/sdc-global-dataPipeline-helpers/archive/v0.7.3.zip'
)
