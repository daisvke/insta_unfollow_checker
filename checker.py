#!/usr/bin/env python3

from sys import stderr
import zipfile
import os
from argparse import ArgumentParser
from ascii_format import DONE, ERROR, YELLOW, RESET, INFO

extract_to_directory = "tmp/"
save_to_file = "unfollowers.txt"
path_to_lists_folder = \
    extract_to_directory + "connections/followers_and_following/"
path_to_following_folder = path_to_lists_folder + "following.html"
path_to_followers_folder = path_to_lists_folder + "followers_1.html"
username_prefix = "instagram.com/"


class InstaUnfollowChecker:

    def __init__(
        self,
        filepath: str,
        search_name: str,
        case_insensitive: bool,
        verbose: bool,
        save: bool
            ):
        self.filepath = filepath
        self.search_name = search_name
        self.case_insensitive = case_insensitive
        self.verbose = verbose
        self.save = save

        self.following: list[str] = []
        self.followers: list[str] = []

    def unzip(self) -> None:
        """Unzip the ZIP file and extract its content in the given directory"""
        # Create the directory if it doesn't exist
        os.makedirs(extract_to_directory, exist_ok=True)

        # Open the ZIP file
        with zipfile.ZipFile(self.filepath, 'r') as zip_ref:
            # Extract all the contents into the specified directory
            zip_ref.extractall(extract_to_directory)

        if self.verbose:
            print(f"{DONE} Extracted all files to {extract_to_directory}\n")

    def parse_list(self, listpath: str) -> list[str]:
        """Parse the ZIP file content to get a list of usernames"""
        results = []

        with open(listpath, 'r') as list:
            # Use strip() to remove any leading/trailing whitespace
            list_content = list.read().strip()

        stripped_list = list_content.split(username_prefix)

        for part in stripped_list:
            # Find the index of the first occurrence of '"'
            quote_index = part.find('"')
            if quote_index != -1:  # If '"' is found
                # Extract the substring from the start to the index of '"'
                extracted_string = part[:quote_index]
                if '<' not in extracted_string:
                    results.append(extracted_string)

        return results

    def get_unfollowers(
        self, following: list[str], followers: list[str]
            ) -> tuple[list[str], int]:
        """
        Get the unfollowers' list by comparing the followers'
        and the following's lists
        """

        unfollowers = []
        count = 0

        for username in following:
            if username not in followers:
                unfollowers.append(username)
                count += 1
        return unfollowers, count

    def print_results(self, unfollowers: list[str], count: int) -> None:
        """Print the results."""
        # If the mode is on, open the file in which we will save the resuts
        if self.save:
            file = open(save_to_file, 'w')

        # Print each username and write it on the outfile if the mode is on
        for username in unfollowers:
            if self.save:
                file.write(f"{username}\n")
            print(username)

        # Print some useful information at the end
        if self.verbose:
            print(f"\n{INFO} Total: {YELLOW}{count}{RESET} unfollowers.")
            if self.save:
                print(f"{INFO} Saved results in {YELLOW}{save_to_file}{RESET}")

    def run(self) -> None:
        """Run the checker"""

        following: list[str] = []
        followers: list[str] = []
        unfollowers: list[str] = []

        try:
            # Unzip the ZIP file to get its content
            self.unzip()

            # Get the following usernames
            following = self.parse_list(path_to_following_folder)
            # Get the followers' usernames
            followers = self.parse_list(path_to_followers_folder)

            # Get the unfollowers' list and print the results
            unfollowers, count = self.get_unfollowers(following, followers)
            self.print_results(unfollowers, count)

        except Exception as e:
            print(f"{ERROR} {e}\n", file=stderr)


def parse_args():
    """Set up argparse and return the given arguments."""
    parser = ArgumentParser(
        description="Return a list of usernames that are not"
                    "following you back."
    )
    parser.add_argument(
        'zipfile', type=str, help='the zip file to process'
    )
    parser.add_argument(
        '-v', '--verbose', action='store_true', help="Enable verbose mode.")
    parser.add_argument(
        '-o', '--outfile', action='store_true',
        help="Save the unfollowers' list in a file"
    )
    parser.add_argument(
        '-s', '--search-username', type=str,
        help='enable single username search')
    parser.add_argument(
        '-i', '--case-insensitive', action='store_true',
        help='Enable case-insensitive mode'
        )

    args = parser.parse_args()

    if (args.case_insensitive and not args.search_string):
        parser.error(
            "-i/--case-insensitive option can only be used "
            "with -s/--search-string."
            )

    return parser.parse_args()


if __name__ == "__main__":
    # Parse command-line arguments
    args = parse_args()

    checker = InstaUnfollowChecker(
            args.zipfile,
            args.search_username,
            args.case_insensitive,
            args.verbose,
            args.outfile
            )

    checker.run()
