#!/usr/bin/env python

import sys
import os
import re


class Actioner(object):

    actions = ['SUM', 'MIN', 'AVERAGE', 'MAX']

    def __init__(self, numbers):
        self.numbers = numbers

    def run(self, action):
        if not action in self.actions:
            raise NotImplementedError("Action: %s not supported" % action)

        return getattr(self, action.lower())()

    def sum(self):
        return sum(self.numbers)

    def average(self):
        return sum(self.numbers) / len(self.numbers)

    def min(self):
        return min(self.numbers)

    def max(self):
        return max(self.numbers)


if __name__ == '__main__':

    if len(sys.argv) < 2:
        sys.exit('Usage: %s filename' % sys.argv[0])

    file_name = sys.argv[1]
    if not os.path.exists(file_name):
        sys.exit('ERROR: data file %s was not found!' % sys.argv[1])

    line_regex = re.compile(r'(?P<action>\w+)\s*:(?P<numbers>.*)')
    with open(file_name, 'r', 0) as data_file:

        for line in data_file:
            match = line_regex.match(line.strip())

            if not match:
                # print "Invalid line detected, skipping..."
                continue

            action, num_line = match.groupdict().values()

            try:
                numbers = [int(n) for n in num_line.split(',')]

            except ValueError:
                # print "Format error detected, skipping..."
                continue

            try:
                actioner = Actioner(numbers)
                print "%s %s" % (action, actioner.run(action))
            except NotImplementedError:
                # print action, "Not supported"
                continue

