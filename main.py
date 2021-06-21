#!/usr/bin/env python3

import logging
import argparse
from amfi import getinfo

loglevel='debug'


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', action='store', default='',
                                dest='isin', help='ISIN')
    parser.add_argument('-n', action='store', default='',
                                dest='mf_name',help='MF Name')
    parser.add_argument('-t', action='store_true', default=False,
                                dest='mf_types', help='Print MF Scheme types')
    parser.add_argument('-m', action='store_true', default=False,
                                dest='mf_names', help='Print MF AMC Names')
    parser.add_argument('-d', action='store_true', default=False,
                                dest='download', help='download data')
    results = parser.parse_args()
    logging.info('Arguments =  %s', results)
    return results

def main():
    nlevel = getattr(logging, loglevel.upper(), None)
    if not isinstance(nlevel, int):
            raise ValueError('Invalid log level: %s' % loglevel)
    logging.basicConfig(filename='debug.log', filemode="w", level=nlevel, 
            format='%(asctime)s %(levelname)s:%(message)s')
    args = parse_arguments()
    try:
        getinfo(args)
    except:
        logging.error('Exited Waiting')

if __name__ == "__main__":
    main()
