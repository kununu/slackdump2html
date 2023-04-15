import os.path
import sys
from typing import List

from src.HtmlPrinter import HtmlPrinter
from src.SlackDataCleaner import SlackDataCleaner
from src.SlackDumpReader import SlackDumpReader


def get_export_path_and_channel_id() -> List[str]:
    if len(sys.argv) != 3:
        raise ValueError("Please provide an export folder and a channel ID.")
    if not os.path.exists(sys.argv[1]):
        raise ValueError("Please provide an existing export folder.")
    return [sys.argv[1], sys.argv[2]]


if __name__ == "__main__":
    path_and_channel = get_export_path_and_channel_id()
    export_path = path_and_channel[0]
    channel_id = path_and_channel[1]

    input_file = export_path + "/" + channel_id + ".json"

    data_cleaner = SlackDataCleaner()

    print("Reading slack dump...", flush=True)
    reader = SlackDumpReader(data_cleaner)
    slack_data = reader.read(input_file)

    print("Cleaning data...", flush=True)
    data_cleaner.replace_names(slack_data)

    print("Printing output file...", flush=True)
    html_printer = HtmlPrinter(slack_data, channel_id)
    html_printer.print()
