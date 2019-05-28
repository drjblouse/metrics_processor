from os import environ


class Constants:  # pylint: disable=too-few-public-methods
    """ Constants for metrics modules """
    BUILDS_METRIC_ID = 'builds'
    UNKNOWN_VALUE = 'N/A'
    UNKNOWN_DURATION_VALUE = -1
    DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'
    AUTH_TOKEN = environ.get('AZURE_DEVOPS_TOKEN')
    AUTH_TOKEN_HEADER = {'Authorization': f'Basic {AUTH_TOKEN}'}
    BUILD_URL = 'https://quadpay.visualstudio.com/quadpay-services/_apis/build/builds/'
    BUILD_VALUE_KEY = 'value'
    ID_KEY = 'id'
    METRIC_VALUE_KEY = 'metric_value'
    BUILD_NUMBER_KEY = 'buildNumber'
    QUEUED_TIME_KEY = 'queueTime'
    START_TIME_KEY = 'startTime'
    BUILD_DATE_KEY = 'buildDate'
    FINISH_TIME_KEY = 'finishTime'
    RESULT_KEY = 'result'
    STATUS_KEY = 'status'
    DURATION_KEY = 'duration'
    PASSED_KEY = 'passed'
    BUILD_SUCCESS_RESULT = 'succeeded'
