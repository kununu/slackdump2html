import os.path
import sys
from typing import List

from src.HtmlPrinter import HtmlPrinter
from src.SlackDataCleaner import SlackDataCleaner
from src.SlackDumpReader import SlackDumpReader

def get_input_paths() -> List[str]:
    if len(sys.argv) != 3:
        raise ValueError('Please provide an input file and image folder argument.')
    if not os.path.exists(sys.argv[1]) or not os.path.exists(sys.argv[2]):
        raise ValueError('Please provide an existing input file and image folder.')
    return [sys.argv[1],sys.argv[2]]

if __name__ == '__main__':
    input_paths = get_input_paths()
    input_file = input_paths[0]
    image_folder = input_paths[1]

    data_cleaner = SlackDataCleaner()

    print("Reading slack dump...", flush=True)
    reader = SlackDumpReader(data_cleaner)
    slack_data = reader.read(input_file)

    print("Cleaning data...", flush=True)
    data_cleaner.replace_names(slack_data)

    print("Printing output file...", flush=True)
    html_printer = HtmlPrinter(slack_data, image_folder)
    html_printer.print()
