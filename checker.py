from sys import stderr
import zipfile
import os
from argparse import ArgumentParser

extract_to_directory = "tmp/"
path_to_lists_folder = extract_to_directory + "connections/followers_and_following/"
path_to_following_folder = path_to_lists_folder + "following.html"
path_to_followers_folder = path_to_lists_folder + "followers_1.html"
username_prefix = "instagram.com/"

class InstaUnfollowChecker:

    def __init__(
        self,
        filepath: str,
        search_name: str,
        case_insensitive: bool,
        verbose: bool 
        ):
        self.filepath = filepath
        self.search_name = search_name
        self.case_insensitive = case_insensitive
        self.verbose = verbose

        self.following = []
        self.followers = []

    def unzip(self) -> None:
        # Specify the path to the ZIP file and the directory to extract to

        # Create the directory if it doesn't exist
        os.makedirs(extract_to_directory, exist_ok=True)

        # Open the ZIP file
        with zipfile.ZipFile(self.filepath, 'r') as zip_ref:
            # Extract all the contents into the specified directory
            zip_ref.extractall(extract_to_directory)

        print(f'Extracted all files to {extract_to_directory}')

    def parse_list(self, listpath: str) -> list[str]:
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
                results.append(extracted_string)

        print(results)


    def run(self) -> None:
        try:
            self.unzip()
            self.parse_list(path_to_following_folder)
        except Exception as e:
            print(f"Error: {e}\n", file=stderr)



def parse_args():
    """Set up argparse and return the given arguments."""
    parser = ArgumentParser(
        description="Return a list of usernames that are not following you back.."
    )
    parser.add_argument(
        'zipfile', type=str, help='the zip file to process'
    )
    parser.add_argument(
        '-v', '--verbose', action='store_true', help="Enable verbose mode.")
    parser.add_argument(
        '-s', '--search-string', type=str, help='enable single username search')
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
            args.search_string,
            args.case_insensitive,
            args.verbose
            )

    checker.run()
