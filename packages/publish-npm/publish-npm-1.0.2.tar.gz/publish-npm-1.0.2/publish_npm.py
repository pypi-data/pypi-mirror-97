#!/usr/bin/env python

import argparse
import json
import os
import pkg_resources
import re
import subprocess
import sys

# Constants
VERSION = pkg_resources.get_distribution("publish_npm").version
DIR = os.getcwd()
PROJECT_NAME = os.path.basename(DIR)
PACKAGE_JSON_PATH = os.path.join(DIR, "package.json")


def main():
    if sys.version_info < (3, 0):
        print("Error: This script requires Python 3.")
        sys.exit(1)

    args = parse_command_line_arguments()

    # Check to see if the "package.json" file exists
    if not os.path.isfile(PACKAGE_JSON_PATH):
        error(
            'Failed to find the "package.json" file in the current working directory.'
        )

    # Check to see if we are logged in to npm
    completed_process = subprocess.run(
        ["npm", "whoami"],
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    if completed_process.returncode != 0:
        error(
            'The "npm whoami" command failed, so you are probably not logged in. Try doing "npm login".'
        )

    # Update the dependencies to the latest versions
    completed_process = subprocess.run(
        ["npx", "npm-check-updates", "--upgrade", "--packageFile", "package.json"],
        shell=True,
    )
    if completed_process.returncode != 0:
        error(
            'Failed to update the "package.json" dependencies to the latest versions.'
        )

    if is_typescript_project():
        # Check to make sure that the project compiles
        completed_process = subprocess.run(["npx", "tsc"], shell=True)
        if completed_process.returncode != 0:
            error("Failed to build the project.")

    if args.skip_increment:
        version = get_version_from_package_json()
    else:
        version = increment_version_in_package_json()

    git_commit_if_changes(version)

    # Publish
    completed_process = subprocess.run(
        [
            "npm",
            "publish",
            "--access",
            "public",
        ],
        shell=True,
    )
    if completed_process.returncode != 0:
        error("Failed to npm publish.")

    # Done
    print("Published {} version {} successfully.".format(PROJECT_NAME, version))


def parse_command_line_arguments():
    parser = argparse.ArgumentParser(
        description="Publish a new version of this package to NPM."
    )

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        help="display the version",
        version=VERSION,
    )

    parser.add_argument(
        "-s",
        "--skip-increment",
        action="store_true",
        help='do not increment the version number in the "package.json" file',
    )

    return parser.parse_args()


def get_version_from_package_json():
    with open(PACKAGE_JSON_PATH, "r") as file_handle:
        package_json = json.load(file_handle)

    if "version" not in package_json:
        error('Failed to find the version in the "{}" file.'.format(PACKAGE_JSON_PATH))

    return package_json["version"]


def increment_version_in_package_json():
    with open(PACKAGE_JSON_PATH, "r") as file_handle:
        package_json = json.load(file_handle)

    if "version" not in package_json:
        error('Failed to find the version in the "{}" file.'.format(PACKAGE_JSON_PATH))

    match = re.search(r"(.+\..+\.)(.+)", package_json["version"])
    if not match:
        error(
            'Failed to parse the version number of "{}".'.format(
                package_json["version"]
            )
        )
    version_prefix = match.group(1)
    patch_version = int(match.group(2))  # i.e. the third number
    incremented_patch_version = patch_version + 1
    incremented_version = version_prefix + str(incremented_patch_version)
    package_json["version"] = incremented_version

    with open(PACKAGE_JSON_PATH, "w", newline="\n") as file_handle:
        json.dump(package_json, file_handle, indent=2, separators=(",", ": "))
        file_handle.write("\n")

    completed_process = subprocess.run(["npx", "sort-package-json"], shell=True)
    if completed_process.returncode != 0:
        error('Failed to sort the "package.json" file.')

    return incremented_version


def is_typescript_project():
    with open(PACKAGE_JSON_PATH, "r") as file_handle:
        package_json = json.load(file_handle)

    return (
        "dependencies" in package_json and "typescript" in package_json["dependencies"]
    ) or (
        "devDependencies" in package_json
        and "typescript" in package_json["devDependencies"]
    )


def git_commit_if_changes(version):
    # Check to see if this is a git repository
    completed_process = subprocess.run(["git", "status"])
    if completed_process.returncode != 0:
        error("This is not a git repository.")

    # Check to see if there are any changes
    # https://stackoverflow.com/questions/3878624/how-do-i-programmatically-determine-if-there-are-uncommitted-changes
    completed_process = subprocess.run(["git", "diff-index", "--quiet", "HEAD", "--"])
    if completed_process.returncode == 0:
        # There are no changes
        return

    # Commit to the repository
    completed_process = subprocess.run(["git", "add", "-A"])
    if completed_process.returncode != 0:
        error("Failed to git add.")
    completed_process = subprocess.run(["git", "commit", "-m", version])
    if completed_process.returncode != 0:
        error("Failed to git commit.")
    completed_process = subprocess.run(["git", "push"])
    if completed_process.returncode != 0:
        error("Failed to git push.")


def error(msg):
    print("Error: {}".format(msg))
    sys.exit(1)


if __name__ == "__main__":
    main()
