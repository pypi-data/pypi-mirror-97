#!/usr/bin/env python

"""
Use the Python DTrace consumer and sum the num of bytes read.

Created on Oct 10, 2011

@author: tmetsch
"""
from __future__ import print_function

import dtrace

SCRIPT = 'sysinfo:::readch { @bytes[execname] = sum(arg0); }'


def main():
    """
    Run DTrace...
    """
    print('Hint: if you don\'t get any output try running it with pfexec...')

    consumer = dtrace.DTraceConsumer()
    consumer.run(SCRIPT, 4)


if __name__ == '__main__':
    main()
