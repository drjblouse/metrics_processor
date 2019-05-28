import datetime
import requests
import numpy as np
from metrics.constants import Constants


class BuildsCollector:
    """ Class for retrieving build metrics for our CI server """

    def __init__(self, client=requests):
        """ Initialize build metrics collector """
        self.client = client

    def get_build_metrics(self):
        """ Get metrics from CI server and format for consumption """
        result = self.client.get(Constants.BUILD_URL, headers=Constants.AUTH_TOKEN_HEADER)
        return self._get_processed_metrics(result)

    def get_metrics_table(self):
        """ Get metrics table detail for output """
        build_metrics = self.get_aggregated_metrics()
        headers = ['Date', 'Count', 'Pass/Fail %', 'Duration Max',
                   'Duration Min', 'Duration 95th', 'Duration Avg']
        table_list = list()
        for key, value in build_metrics.items():
            table_list.append(
                [key, len(value[Constants.DURATION_KEY]),
                 int(np.average(value[Constants.PASSED_KEY]) * 100),
                 int(np.max(value[Constants.DURATION_KEY]) / 60),
                 int(np.min(value[Constants.DURATION_KEY]) / 60),
                 int(round(np.percentile(value[Constants.DURATION_KEY], 95), 2) / 60),
                 int(round(np.average(value[Constants.DURATION_KEY]), 2) / 60)])
        return table_list, headers

    def get_aggregated_metrics(self):
        """ Get the build metrics rolled up by date """
        aggregate_metrics = dict()
        result = self.client.get(Constants.BUILD_URL, headers=Constants.AUTH_TOKEN_HEADER)
        build_metrics = self._get_unprocessed_metrics(result)
        for metric in build_metrics:
            date = metric.get(Constants.BUILD_DATE_KEY, Constants.UNKNOWN_VALUE)
            duration = metric.get(Constants.DURATION_KEY, Constants.UNKNOWN_VALUE)
            passed = metric.get(Constants.PASSED_KEY, Constants.UNKNOWN_VALUE)
            if date not in aggregate_metrics.keys():
                aggregate_metrics[date] = dict()
                aggregate_metrics[date][Constants.DURATION_KEY] = list()
                aggregate_metrics[date][Constants.PASSED_KEY] = list()
            aggregate_metrics[date][Constants.DURATION_KEY].append(duration)
            aggregate_metrics[date][Constants.PASSED_KEY].append(passed)
        return aggregate_metrics

    def _get_single_build_metric(self, result):
        try:
            build_item = self._get_raw_metric_values(result)
            return build_item
        except AttributeError:
            return None

    def _get_unprocessed_metrics(self, result):
        build_metrics = list()
        results = result.json()
        for result_value in results.get(Constants.BUILD_VALUE_KEY, {}):
            build_metrics.append(self._get_raw_metric_values(result_value))
        return build_metrics

    def _get_processed_metrics(self, result):
        build_metrics = list()
        results = result.json()
        for result_value in results.get(Constants.BUILD_VALUE_KEY, {}):
            build_metrics.append(self._get_single_build_metric(result_value))
        return build_metrics

    def _get_raw_metric_values(self, result):
        build_item = dict()
        build_item[Constants.ID_KEY] = result.get(Constants.ID_KEY)
        build_item[Constants.BUILD_NUMBER_KEY] = result.get(Constants.BUILD_NUMBER_KEY)
        build_item[Constants.START_TIME_KEY] = result.get(Constants.START_TIME_KEY)
        build_item[Constants.BUILD_DATE_KEY] = self.get_date(build_item[Constants.START_TIME_KEY])
        build_item[Constants.QUEUED_TIME_KEY] = result.get(Constants.QUEUED_TIME_KEY)
        build_item[Constants.FINISH_TIME_KEY] = result.get(Constants.FINISH_TIME_KEY)
        build_item[Constants.STATUS_KEY] = result.get(Constants.STATUS_KEY)
        build_item[Constants.RESULT_KEY] = result.get(Constants.RESULT_KEY)
        build_item[Constants.PASSED_KEY] = \
            build_item[Constants.RESULT_KEY] == Constants.BUILD_SUCCESS_RESULT
        build_item[Constants.DURATION_KEY] = self.get_build_duration(
            build_item[Constants.START_TIME_KEY], build_item[Constants.FINISH_TIME_KEY])
        return build_item

    @staticmethod
    def get_build_duration(start_time, finish_time):
        """ Get the duration from the build start and stop strings """
        try:
            start = BuildsCollector.get_datetime(start_time)
            finish = BuildsCollector.get_datetime(finish_time)
            total_time = finish - start
            return total_time.seconds
        except (AttributeError, ValueError):
            return Constants.UNKNOWN_DURATION_VALUE

    @staticmethod
    def get_datetime(date_string):
        """ Get a datetime from the returned string """
        date_split = date_string.split('.')
        date_microseconds = date_split[-1].replace('Z', '')[:6]
        return datetime.datetime.strptime(
            f'{date_split[0]}.{date_microseconds}Z', Constants.DATETIME_FORMAT)

    @staticmethod
    def get_date(datetime_string):
        """ Get the date without the time from the timestamp string """
        return datetime_string.split('T')[0]
