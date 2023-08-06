import json
import os
import shutil

from pathlib import Path


def write_json(data, filename):
    """Write data to a json file, and add a line break at the end"""
    with open(filename, "w+") as outfile:
        json.dump(data, outfile, indent=4, separators=(",", ": "))
        outfile.write("\n")


def read_json(filename, folder):
    """Reads a json file. Can leave .json out of filename"""
    if filename[-5:] != ".json":
        filename = filename + ".json"

    with open(Path(folder) / filename, "r") as json_data:
        return json.load(json_data)


def prepare_folder(folder, clear_content=True):
    """Check if a path already exists, and make the necessary folders if it doesn't.
    Otherwise, delete existing files and recreate it as a fresh folder. This DOESN'T
    carry warnings before deletion so all files will be lost! Option allows you to skip
    deleting existing content if you wish."""
    destination = Path.cwd() / folder
    if not os.path.exists(destination):
        os.makedirs(destination)
    elif clear_content is True:
        shutil.rmtree(destination)
        os.makedirs(destination)
