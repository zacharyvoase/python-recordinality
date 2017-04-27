#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import argparse
import math
import os
import struct
import sys

from csiphash import siphash24
from cskipdict import SkipDict


class Element(object):
    __slots__ = ('value', 'count')

    def __init__(self, value):
        self.value = value
        self.count = 1


class Recordinality(object):

    def __init__(self, size, hash_key=None, store_values=True):
        if hash_key is None:
            hash_key = os.urandom(16)
        self.hash = lambda val: struct.unpack('Q', siphash24(hash_key, val))[0]
        self.k_records = SkipDict()
        self.size = size
        self.modifications = 0
        self.store_values = store_values

    def add(self, value):
        hash = self.hash(value)
        if hash in self.k_records:
            element = self.k_records[hash]
            if self.store_values and element.value == value:
                element.count += 1
        elif len(self.k_records) < self.size:
            self.k_records[hash] = Element(value if self.store_values else None)
            self.modifications += 1
        else:
            min_key, min_val = self.k_records.minimum()
            if min_key < hash:
                del self.k_records[min_key]
                self.k_records[hash] = Element(value if self.store_values else None)
                self.modifications += 1

    def cardinality(self):
        # We have an exact cardinality up to self.size
        if self.modifications <= self.size:
            return self.modifications
        pow = self.modifications - self.size + 1
        estimate = (self.size * math.pow(1 + (1.0 / self.size), pow)) - 1
        return int(estimate)

    def error(self):
        cardinality = self.cardinality()
        return math.sqrt(math.pow(cardinality / (self.size * math.e), 1.0 / self.size) - 1)

    @property
    def sample(self):
        if not self.store_values:
            raise AttributeError("This Recordinality is not configured to store values for sampling")
        for key, elem in self.k_records.iteritems():
            yield (elem.value, elem.count)


def hash_key_argument(arg):
    if len(arg) == 32:
        return arg.decode('hex')
    elif len(arg) == 16:
        return arg
    raise TypeError("-h/--hash-key must be either 16 ASCII chars or 32 hex digits")


PARSER = argparse.ArgumentParser()
PARSER.add_argument('size', type=int,
                    help="The size of the Recordinality sketch")
PARSER.add_argument('-k', '--hash-key', type=hash_key_argument, default=None,
                    help="A key to use for the SipHash function (as 16 ASCII chars or 32 hex digits)")
PARSER.add_argument('-s', '--sample', action='store_true', default=False,
                    help="Capture a k-sized random sample from the stream, printing it afterwards")


def main():
    args = PARSER.parse_args()
    sketch = Recordinality(size=args.size, hash_key=args.hash_key, store_values=args.sample)
    for line in sys.stdin:
        sketch.add(line.rstrip('\r\n').encode('utf-8'))
    print(sketch.cardinality())
    if args.sample:
        for value, count in sketch.sample:
            print('{}\t{}'.format(value, count))


if __name__ == '__main__':
    main()
