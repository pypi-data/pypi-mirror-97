import os
import shutil
import json
import argparse
from zipfile import ZipFile
from pathlib import Path
from tempfile import TemporaryDirectory
from ..general.constants import RUNNER_USER
from ..general.util import get_current_dir

SOURCE_DIRECTORY = "/autograder/source"
RUN_AUTOGRADER_FILE = "run_autograder.sh"
RUN_AUTOGRADER_TARGET = "run_autograder"
SETUP_FILE = "setup.sh"
SETUP_TARGET = "setup.sh"
CONFIG_TARGET = "config.json"

def build(tested_file, config_file, output_zip, verbose=False):

    # Validate parameters
    assert os.path.isfile(config_file), "Config file not found"
    assert os.path.isfile(tested_file), "Tested file not found"

    tmp_dir = TemporaryDirectory()
    tested_file_name = os.path.basename(tested_file)
    assert tested_file_name, "Invalid tested file"
    current_dir = get_current_dir()

    
    # Load config file
    with open(config_file) as f:
        config = json.load(f)
    assert "tests" in config, "Invalid config format"

    # Find all files in config
    copied_files = []
    for test in config["tests"]:
        if "files" in test:
            # Store files to be copied
            copied_files += test["files"]
            # Change files path to autograder format
            test["files"] = [Path(SOURCE_DIRECTORY, os.path.basename(file)).as_posix() for file in test["files"]]
        if "tester_file" in test:
            # Store file to be copied
            copied_files.append(test["tester_file"])
            # Change file path to autograder format
            test["tester_file"] = Path(SOURCE_DIRECTORY, os.path.basename(test["tester_file"])).as_posix()
    
    # Write modified config file
    with open(os.path.join(tmp_dir.name, CONFIG_TARGET), "w") as f:
        json.dump(config, f, indent=4)

    # Copy all files mentioned in config
    for file_name in copied_files:
        assert os.path.isfile(file_name), f"Can't find file: {file_name}"
        shutil.copy(file_name, tmp_dir.name)

    # Open run_autograder template
    with open(os.path.join(current_dir, RUN_AUTOGRADER_FILE)) as f:
        run_autograder = f.read()
    # Fill in the required names
    run_autograder = run_autograder.format(tested_file_name)
    # Write run_autograder to tmp directory
    with open(os.path.join(tmp_dir.name, RUN_AUTOGRADER_TARGET), "w") as f:
        f.write(run_autograder)

    # Open setup.sh template
    with open(os.path.join(current_dir, SETUP_FILE)) as f:
        setup = f.read()
    # Fill in the required names
    setup = setup.format(RUNNER_USER)
    # Write setup.sh to tmp directory
    with open(os.path.join(tmp_dir.name, SETUP_TARGET), "w") as f:
        f.write(setup)
    
    if verbose: print("Adding files to Autograder:")
    # Write all files in tmp directory to zip
    with ZipFile(output_zip, "w") as zip_file:
        for f in os.listdir(tmp_dir.name):
            file_name = os.path.join(tmp_dir.name, f)
            if not os.path.isfile(file_name): continue
            if verbose: print(f"\t{f}")
            zip_file.write(file_name, arcname=f)
    if verbose: print(f"Created {output_zip}")

    tmp_dir.cleanup()
