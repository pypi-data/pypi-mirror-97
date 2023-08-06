import inspect, os, sys
import json
import datetime
import time
from collections.abc import Mapping
from collections import namedtuple
from pathlib import Path

class Lookup:
    def __init__(self, lookup_dir):
        for name, value in inspect.getmembers(self):
            if "__" not in name and name.startswith("_") and not os.path.isabs(value):
                setattr(self, name.lstrip("_"), Path(lookup_dir, value))

decoder = lambda x: str(x.decode('UTF-8'))
dumb_decoder = lambda x: str(x).lstrip("b'").rstrip("'")

def read_from_start(file):
    file.seek(0)
    return file.read()

# Create the feedback.json file in correct format
def create_feedback_json(fb_array):
    dictionary = {
        "tests": [ item.to_dict() for item in fb_array ]
    }

    return dictionary

def save_feedback_file(dictionary, filename="result.json", verbose=False):
    f = json.dumps(dictionary, indent=4)
    
    with open(filename, "w+") as ofile:
        ofile.write(f)
    if verbose: print(f"Saved result to {os.path.abspath(filename)}")

def get_current_dir():
    origin = sys._getframe(1) if hasattr(sys, "_getframe") else None
    return os.path.dirname(os.path.abspath(inspect.getfile(origin)))


def dict_to_namedtuple(mapping):
    if isinstance(mapping, Mapping):
        for key, value in mapping.items():
            mapping[key] = dict_to_namedtuple(value)
        return namedtuple_from_mapping(mapping)
    return mapping

def namedtuple_from_mapping(mapping, name="Tupperware"):
    this_namedtuple_maker = namedtuple(name, mapping.keys())
    return this_namedtuple_maker(**mapping)

def get_files_in_dir(dir_path):
    assert dir_path.is_dir()
    return [f for f in dir_path.glob('**/*') if f.is_file()]

def as_md_code(lines):
    return "```\n{}\n```".format('\n'.join(lines))
