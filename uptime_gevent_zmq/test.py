#!/usr/bin/env python
import unittest
import re


class TestUptimeParsing(unittest.TestCase):

    def test_uptime_parser(self):
        uptime_results = {
            "16:50  up 10 days, 22:52, 10 users, load averages: 1.33 1.06 1.22": "10 days, 22:52",
            "16:50  up 10 days, 22:52, 1 user, load averages: 1.33 1.06 1.22": "10 days, 22:52",
            "16:50  up 22:52, 10 users, load averages: 1.33 1.06 1.22": "22:52",
            "16:50  up 10 days, 10 users, load averages: 1.33 1.06 1.22": "10 days",
        }
        # make sure the results are parsed correctly.
        for raw_result, parsed_result in uptime_results.iteritems():
            res_dict = re.match(r'.*up\s+(?P<uptime>.*?),\s+([0-9]+) users?', raw_result).groupdict()
            self.assertEqual(parsed_result, res_dict['uptime'])


if __name__ == '__main__':
    unittest.main()
