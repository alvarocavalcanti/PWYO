#!/usr/bin/env python3

import argparse
import yaml

from subprocess import check_output


def parse_args():
    pass

def main(args=None):
    tech_debts = load_tech_debts()
    files_in_commit = load_files_in_commit()
    filtered_files = filter_files(files_in_commit, ['A', 'M', 'D'])
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
    result = check_output(['git','status','-s'], universal_newlines=True)
    files = result.split('\n')
    files = [f.lstrip() for f in files if f]
    return_files = []
    for file in files:
        [type, value] = file.split(' ')
        return_files.append({
            "type": type,
            "file": value
        })
    return return_files

def filter_files(source_files, types):
    filtered_files = [file for file in source_files if file['type'] in types]
    return filtered_files

def match_files_against_tech_debts(files, tech_debts):
    files = [file['file'] for file in files]
    result = [tech_debt for tech_debt in tech_debts if tech_debt['file'] in files]
    return result

if __name__ == "__main__":
    print('----------------------')
    print('|PWYO| Pre-commit Hook')
    print('----------------------')
    args = parse_args()
    main(args)
