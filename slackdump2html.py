import os.path
import sys

from src.HtmlPrinter import HtmlPrinter
from src.SlackDataCleaner import SlackDataCleaner
from src.SlackDumpReader import SlackDumpReader


def get_input_file_path() -> str:
    if len(sys.argv) != 2:
        raise ValueError('Please provide an input file argument.')
    if not os.path.exists(sys.argv[1]):
        raise ValueError('Please provide an existing input file.')
    return sys.argv[1]


if __name__ == '__main__':
    input_file = get_input_file_path()

    print("Reading slack dump...", flush=True)
    reader = SlackDumpReader()
    slack_data = reader.read(input_file)

    print("Cleaning data...", flush=True)
    data_cleaner = SlackDataCleaner()
    data_cleaner.replace_names(slack_data)

    print("Printing output file...", flush=True)
    html_printer = HtmlPrinter(slack_data)
    html_printer.print()
