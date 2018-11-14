#!/usr/bin/env python3
"""
Author : kyclark
Date   : 2018-11-02
Purpose: Rock the Casbah
"""

import argparse
import pandas as pd
import matplotlib.pyplot as plt
import sys


# --------------------------------------------------
def get_args():
    """get args"""
    parser = argparse.ArgumentParser(
        description='Argparse Python script',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument(
        'file', metavar='str', help='A positional argument')

    parser.add_argument(
        '-o',
        '--outfile`',
        help='Save to outfile',
        metavar='str',
        type=str,
        default=None)

    return parser.parse_args()


# --------------------------------------------------
def warn(msg):
    """Print a message to STDERR"""
    print(msg, file=sys.stderr)


# --------------------------------------------------
def die(msg='Something bad happened'):
    """warn() and exit with error"""
    warn(msg)
    sys.exit(1)


# --------------------------------------------------
def main():
    """main"""
    args = get_args()
    data = pd.read_csv(args.file, names=['term', 'desc', 'domain', 'count'])
    counts = data['counts']
    #data.drop(data[data['count'] > 2 * data['count'].std()].index, inplace=True)
    #std = data.describe['std']
    print(data.describe())
    plt.hist(counts[counts > 0])
    plt.show()



# --------------------------------------------------
if __name__ == '__main__':
    main()
