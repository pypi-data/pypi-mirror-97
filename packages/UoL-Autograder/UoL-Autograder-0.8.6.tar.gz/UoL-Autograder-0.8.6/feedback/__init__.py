import inspect, shutil
import json
from pathlib import Path
from collections import namedtuple
from tempfile import TemporaryDirectory
from . import cpp
from . import py
from .signature import Signature
from .general.util import create_feedback_json, get_current_dir, dict_to_namedtuple
from .general.constants import LOOKUP_DIR
from .general.result import CheckResult

__version__ = Signature.get_version()

def load_config(config_file):
    if not isinstance(config_file, Path):
        config_file = Path(config_file)
    assert config_file.is_file()                      # Check if config file exists
    with config_file.open() as json_file:                    # Load config file as a named tuple (so it can be indexed as names, not with strings)
        return dict_to_namedtuple(json.load(json_file))

# Setup script, prepare everything for testing, create tmp directory, and move all relevant files there
class TmpFiles:
    def __init__(self, tested_file, config):
        assert isinstance(tested_file, Path)
        self.my_dir = get_current_dir()     # Get this exact directory, regardless where it was called from.

        self.lookup_dir = Path(self.my_dir, LOOKUP_DIR)      # Define lookup directory, and check if it exists
        assert self.lookup_dir.is_dir()

        self.tmp_dir = TemporaryDirectory()

        assert tested_file.is_file(), tested_file.absolute().as_posix()                     # Check if tested file exists
        self.tested_path = Path(self.tmp_dir.name, tested_file.name)      # Copy it to tmp dir
        # shutil.copyfile(tested_file, self.tested_path)
        tested_dir = tested_file.parent.glob('**/*')
        for f in tested_dir:
            path = Path(self.tmp_dir.name, f.name)
            if f.is_file():
                shutil.copyfile(f, path)

        if hasattr(config, "tests"):
            for test in config.tests:
                if "tester_file" in test:
                    tester_file = Path(test["tester_file"])
                    assert tester_file.is_file()                                                  # Check if tester file exists
                    copied_tester_path = Path(self.tmp_dir.name, tester_file.name)                  # Copy tester file to tmp dir
                    test["tester_file"] = copied_tester_path
                    shutil.copyfile(tester_file, copied_tester_path)
    
    # Delete tmp dir and all its contents
    def teardown(self):
        self.tmp_dir.cleanup()

    def save_tmpdir(self, target_dir):
        if Path(target_dir).is_dir():
            shutil.rmtree(target_dir)
        if Path(self.tmp_dir.name).is_dir():
            shutil.copytree(self.tmp_dir.name, target_dir)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.teardown()

def missing_file_feedback(tested_file):
    return [CheckResult(
        {"number": "1", "visibility": "visible"},
        "Tested file is missing",
        0,
        f"Expected file {tested_file.name} to be submitted"
    )]


# Find the right testing function based on the tested file extension
def get_test_runner(tested_file):
    extension = tested_file.suffix      # Get the file extension
    if extension == ".cpp":
        return cpp.CppRunner
    elif extension == ".py":
        return py.PyRunner
    raise Exception(f"No runner found for extension {extension}")       # Throw error if the extension is invalid


# Actual entry point, with actual parameters
def run_test(tested_file, config_file, run_args={}, copy_tmp=None, precision=4):
    CheckResult.precision = precision

    config = load_config(config_file)

    tested_file = tested_file if isinstance(tested_file, Path) else Path(tested_file)

    if not tested_file.is_file():
        feedback = missing_file_feedback(tested_file)
        return create_feedback_json(feedback)


    with TmpFiles(tested_file, config) as tmp_files:
        test_runner = get_test_runner(tested_file)(tmp_files, run_args, config.globals if hasattr(config, "globals") else None)   # Get the right testing function
        feedback = test_runner.run_test(config.tests if hasattr(config, "tests") else None)

        if copy_tmp: tmp_files.save_tmpdir(copy_tmp)


    return create_feedback_json(feedback)            # Create json file
