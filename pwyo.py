#!/usr/bin/env python

import argparse
import yaml


"""
 PWYO - Pay What You Owe
"""

def parse_args():
    pass

def main(args=None):
    print('[PWYO] Pre-commit Hook')
    with open('tech_debts.yml', 'r') as stream:
        try:
            tech_debts = yaml.load(stream)
            for tech_debt in tech_debts:
                print(tech_debt)
        except yaml.YAMLError as e:
            print(e)
            exit(1)
    # exit(1)
 
if __name__ == "__main__":
    args = parse_args()
    main(args)
