#!/usr/bin/env python
from git import Repo
import argparse
import os
import re
import sys

"""
Goal:
  * Check included .gitlab-ci.yml references.

How to:
  * Get help
    - check_included_ci_ref.py -h
    - python check_included_ci_ref.py <file1> <another_file> <path_to_file>
  * Files can be given as arguments to the script.

Optimizations:
  * Only simple words are considered in ref/branch name, using `\w+`
"""

parser = argparse.ArgumentParser(description='Check ref of included .gitlab-ci.yml files.', epilog="python check_included_ci_ref.py <path_to_gitlab_ci_file>", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
# parser.add_argument('-f', '--file', default="./.gitlab-ci.yml", help='Path to .gitlab-ci yml file.')
parser.add_argument('filenames', nargs='*', help='Filenames to check.')
args = parser.parse_args()


REF_LINE = re.compile("^[ ]*ref:[ ] *(\w+)")

STAGING_BRANCH = "staging"
MASTER_BRANCH = "master"

BRANCH_REF_MAP = {
    STAGING_BRANCH: (STAGING_BRANCH, MASTER_BRANCH),
    MASTER_BRANCH: (MASTER_BRANCH),
}


def get_appropriate_ref(ref_line, branch):
    # reference = REF_LINE.findall(ref_line, re.IGNORECASE)[0]
    reference = REF_LINE.findall(ref_line)[0]

    if not reference in BRANCH_REF_MAP[branch]:
        if STAGING_BRANCH == branch:
            new_reference = STAGING_BRANCH
        elif MASTER_BRANCH == branch:
            new_reference = MASTER_BRANCH
    else:
        new_reference = reference

    # replaced_line = re.sub(reference, new_reference, ref_line, flags=re.IGNORECASE)
    replaced_line = re.sub(reference, new_reference, ref_line)
    return replaced_line


def check_included_refs(filenames):
    working_files = 0
    retv = 0
    for filename in filenames:
        if not os.path.exists(filename) or not os.path.isfile(filename):
            print(f"Is this the correct file: {filename}")
            continue
        abs_path = os.path.realpath(filename)
        base_path = os.path.dirname(filename)
        file_name = os.path.basename(filename)
        # Get current branch
        repo = Repo(base_path)
        branch = repo.active_branch.name
        # Replace refs used in .gitlba-ci.yml
        content = None
        with open(filename, "r") as file_handler:
            content = file_handler.readlines()
        if content and branch in BRANCH_REF_MAP:
            new_content = list()
            replaced = False
            for line in content:
                # if REF_LINE.match(line, re.IGNORECASE):
                if REF_LINE.match(line):
                    new_line = get_appropriate_ref(ref_line=line, branch=branch)
                    if not new_line == line:
                        replaced = True
                else:
                    new_line = line
                new_content.append(new_line)
            # Rewrite the file, if changed
            if replaced:
                with open(filename, "w") as file_handler:
                    file_handler.write("".join(new_content))
                print(f"  >> Refs replaced in {filename}")
        working_files += 1
    if filenames and working_files == 0:
        retv = 1

    return retv


if __name__ == "__main__":
    sys.exit(check_included_refs(filenames=args.filenames))
