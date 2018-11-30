#!/usr/bin/env python3
"""
Author : kyclark
Date   : 2018-11-30
Purpose: Compare the comparisons
"""

import argparse
import os
import pandas as pd
import sys


# --------------------------------------------------
def get_args():
    """get command-line arguments"""
    parser = argparse.ArgumentParser(
        description='Compare the comparisons',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('in_dir', metavar='DIR', help='Input directory')

    # parser.add_argument(
    #     '-a',
    #     '--arg',
    #     help='A named string argument',
    #     metavar='str',
    #     type=str,
    #     default='')

    # parser.add_argument(
    #     '-i',
    #     '--int',
    #     help='A named integer argument',
    #     metavar='int',
    #     type=int,
    #     default=0)

    # parser.add_argument(
    #     '-f', '--flag', help='A boolean flag', action='store_true')

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
    """Make a jazz noise here"""
    args = get_args()
    in_dir = args.in_dir

    if not os.path.isdir(in_dir):
        die('"{}" is not a directory'.format(in_dir))

    runs = []
    for file in os.scandir(in_dir):
        basename, _ = os.path.splitext(os.path.basename(file))
        print(basename)
        df = pd.read_csv(file)
        means = df.groupby('model_name')['accuracy'].mean()
        for model_name, accuracy in means.iteritems():
            runs.append(('none', basename, model_name, accuracy))

    meta = pd.DataFrame(
        columns=['normalization', 'file', 'model_name', 'accuracy'], data=runs)
    print(meta)
    print("Done.")


# --------------------------------------------------
if __name__ == '__main__':
    main()
