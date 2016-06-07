#!/usr/bin/env python3

import yaml
import sys
import os

from subprocess import check_output


def main():
    tech_debts = load_tech_debts()
    files_in_commit = load_files_in_commit()
    filtered_files = filter_files(files_in_commit, ['A', 'M', 'D', 'MM'])
    matched_tech_debts = match_files_against_tech_debts(filtered_files, tech_debts)
    missing_tech_debt_files = check_for_missing_tech_debt_files(tech_debts)
    was_report_printed = print_report(matched_tech_debts, missing_tech_debt_files)
    ask_commiter_about_halting_commit(was_report_printed)


def get_input(message):
    sys.stdin = open('/dev/tty')
    answer = input(message)
    sys.stdin = open('/dev/null')
    return answer


def do_exit(code):
    return exit(code)


def do_print(message):
    return print(message)


def file_exists(file):
    return True if file is None else os.path.exists(file)


def print_report(matched_tech_debts, missing_tech_debt_files):
    result = False
    if len(matched_tech_debts) > 0:
        do_print("TECH DEBTS FOUND: The following Tech Debts are linked to files you're trying to commit:")
        for tech_debt in matched_tech_debts:
            do_print('- Title: {}\n  File: {}'.format(tech_debt['title'], tech_debt['file']))
        do_print('\n')
        result = True

    if len(missing_tech_debt_files) > 0:
        do_print("TECH DEBTS MISSING: The following Tech Debts files are missing from :")
        for tech_debt in missing_tech_debt_files:
            do_print('- Title: {}\n  File: {}'.format(tech_debt['title'], tech_debt['file']))
        do_print('\n')
        result = True

    return result


def ask_commiter_about_halting_commit(was_report_printed=False, prompt_user=True):
    if was_report_printed and prompt_user:
        answer = get_input("Do you want to halt committing? yes/[no]")
        if answer == 'yes':
            do_print(' >> Commit HALTED!\n')
            do_exit(1)
        else:
            do_print(' >> Commit continued...\n')


def load_tech_debts():
    with open('tech_debts.yml', 'r') as stream:
        try:
            tech_debts = yaml.load(stream)
        except yaml.YAMLError as e:
            print(e)
            do_exit(1)
    return tech_debts


def load_files_in_commit():
    result = check_output(['git', 'status', '-s'], universal_newlines=True)
    files = result.split('\n')
    files = [f.lstrip() for f in files if f]
    return_files = []
    for file in files:
        [type, *_, value] = file.split(' ')
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


def check_for_missing_tech_debt_files(tech_debts):
    missing_tech_debts = [tech_debt for tech_debt in tech_debts if not file_exists(tech_debt['file'])]
    return missing_tech_debts

if __name__ == "__main__":
    main()
