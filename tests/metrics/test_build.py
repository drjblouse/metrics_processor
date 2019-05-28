import json
import os
from unittest import TestCase, skip
from unittest.mock import MagicMock
from metrics.build import BuildsCollector


class BuildCollectorTests(TestCase):
    def test_create(self):
        collector = BuildsCollector()
        self.assertIsNotNone(collector)

    def test_duration(self):
        start_time = '2019-02-25T19:40:53.4822105Z'
        finish_time = '2019-02-25T19:54:40.6249666Z'
        self.assertEqual(BuildsCollector.get_build_duration(start_time, finish_time), 827)
        self.assertEqual(BuildsCollector.get_build_duration(start_time, None), -1)
        self.assertEqual(BuildsCollector.get_build_duration(None, None), -1)
        self.assertEqual(BuildsCollector.get_build_duration(None, finish_time), -1)
        self.assertEqual(BuildsCollector.get_build_duration('1234', finish_time), -1)
        self.assertEqual(BuildsCollector.get_build_duration('dummy', finish_time), -1)

    def test_collect_small(self):
        mock = MagicMock()
        mock.get.return_value = mock
        mock.json.return_value = self.get_mock_output('test_files/small_build_output.json')
        sender = BuildsCollector(client=mock)
        self.assertEqual(len(sender.get_build_metrics()), 2)

    def test_collect_large(self):
        mock = MagicMock()
        mock.get.return_value = mock
        mock.json.return_value = self.get_mock_output('test_files/full_build_output.json')
        sender = BuildsCollector(client=mock)
        self.assertEqual(len(sender.get_build_metrics()), 547)

    def test_get_datetime(self):
        date_string = '2019-03-12T16:02:44.217605Z'
        date_value = BuildsCollector.get_datetime(date_string)
        self.assertEqual(date_value.year, 2019)
        self.assertEqual(date_value.day, 12)
        self.assertEqual(date_value.second, 44)
        self.assertEqual(date_value.microsecond, 217605)
        date_string = '2019-03-12T16:02:44.21760589Z'
        date_value = BuildsCollector.get_datetime(date_string)
        self.assertEqual(date_value.year, 2019)
        self.assertEqual(date_value.day, 12)
        self.assertEqual(date_value.second, 44)
        self.assertEqual(date_value.microsecond, 217605)

    @skip
    def test_real_api(self):
        sender = BuildsCollector()
        metrics = sender.get_build_metrics()
        print(metrics)
        self.assertGreater(len(metrics), 550)

    @staticmethod
    def get_mock_output(file_name):
        test_path = os.path.join(
            os.path.dirname(__file__), file_name)
        with open(test_path) as test_file:
            return json.load(test_file)
