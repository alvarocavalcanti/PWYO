#!/usr/bin/env python3

import argparse
import yaml

from subprocess import check_output


def parse_args():
    pass

def main(args=None):
    tech_debts = load_tech_debts()
    files_in_commit = load_files_in_commit()
    # exit(1)

def load_tech_debts():
    with open('tech_debts.yml', 'r') as stream:
        try:
            tech_debts = yaml.load(stream)
        except yaml.YAMLError as e:
            print(e)
            exit(1)
    return tech_debts

def load_files_in_commit():
    result = check_output(['git','status','-s'])
    return result

if __name__ == "__main__":
    print('----------------------')
    print('|PWYO| Pre-commit Hook')
    print('----------------------')
    args = parse_args()
    main(args)
