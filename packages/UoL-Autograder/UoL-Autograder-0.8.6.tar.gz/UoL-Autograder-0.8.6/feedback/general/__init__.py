import subprocess
import os
import shutil
from pathlib import Path
import json
import re
from collections.abc import Iterable
from subprocess import TimeoutExpired
from . import util
from . import execution
from . import config_tools
from .constants import *
from .result import CheckResult
from .validation import Validation, FailedValidation
from .py_eval_util import get_eval_util_path

class GeneralLookup(util.Lookup):
    _comment_feedback = "comment_feedback.json"

class BadExecutionError(Exception):
    def __init__(self, result):
        self.result = result
        super().__init__(f"Bad execution: {result}")

class Runner:
    def __init__(self, tmp_files, run_args={}, runner_config=None):
        self.general_lookup = GeneralLookup(tmp_files.lookup_dir)
        self.feedbacks = []
        self.tmp_files = tmp_files
        self.tested_path = tmp_files.tested_path.absolute().as_posix()
        self.tmp_dir = tmp_files.tmp_dir.name
        self.verbose = run_args.get("verbose", False)
        self.check_validity = run_args.get("check_validity", True)
        self._test_lookup = {
            "comments": self.test_comments,
            "replace_files": self.replace_files,
        }
    
    def _copy_py_eval_util(self):
        shutil.copy(get_eval_util_path(), Path(self.tmp_dir, "py_eval_util.py").absolute().as_posix())

    def print_verbose(self, *args):
        if self.verbose:
            print(*args)

    def run_test(self, config):
        self.feedbacks = []

        for test in config:
            self._test_lookup[test["type"]](util.dict_to_namedtuple(test))

        return self.feedbacks

    def test_comments(self, config):
        self.print_verbose("Testing comments")
        # cloc - Count Lines of Code
        exec_result = execution.execute(['cloc', self.tested_path, "--csv", "--quiet"], self.tmp_dir)
        lines = list(exec_result.stdout.splitlines())

        # Find the correct line in the result             
        result = None
        for line in lines:
            match = re.search(r'(?P<files>\d*),(?P<language>.*),(?P<blank>\d*),(?P<comment>\d*),(?P<code>\d*)', line)
            if match:
                result = match
        
        if result:
            # Unpack results
            n_blank, n_comments, n_code = [int(result.group(name)) for name in ["blank", "comment", "code"] ]
            comment_density = n_comments / (n_code + n_comments)
        else:
            n_blank, n_comments, n_code, comment_density = 0, 0, 0, 0

        self.print_verbose(f"Blank lines: {n_blank}, Comment lines: {n_comments}, Code lines: {n_code}, Comment density: {comment_density}")
        

        with open(self.general_lookup.comment_feedback) as json_file:
            comment_feedback = json.load(json_file)

        # Format feedback with results
        fb = comment_feedback["stats"].format(n_code, n_comments, n_blank)
        score = comment_density

        # Find the right feedback line
        density_feedback = comment_feedback["density_feedback"]
        density_feedback.sort(key=lambda x: x["threshold"])

        for band in density_feedback:
            if comment_density <= band["threshold"]:
                fb += band["text"]
                score += band["bonus"]
                break

        score = min(score, 1.0)

        self.feedbacks.append(CheckResult(config, "comments", score, fb))

    def replace_files(self, config):
        self.print_verbose("Replacing files")
        files = (config.get("files", None)) if type(config) == dict else (config.files if hasattr(config, "files") else None)
        override = (config.get("override", True)) if type(config) == dict else (config.override if hasattr(config, "override") else True)
        if not files:
            self.print_verbose("No files to replace")
            return
        
        file_paths = [Path(file) for file in files]
        for path in file_paths:
            target_path = Path(self.tmp_dir, path.name)
            if target_path.is_file() and override:
                self.print_verbose(f"Found file {path.name} in tmp directory, deleting")
                target_path.unlink()
            if not target_path.is_file():
                shutil.copyfile(path, target_path)
            self.print_verbose(f"Copied {path.name} to {target_path}")
    
    def _test_run_executable(self, base_command, config, child_limit=0):
        output_file = Path(self.tmp_dir, "result.json")

        timeout = config_tools.get_timeout(config, EXECUTABLE_TIMEOUT)
        child_limit = config_tools.get_child_limit(config, child_limit)
        memory_limit = config_tools.get_memory_limit(config, MAX_VIRTUAL_MEMORY)
        allow_connections = config.allow_connections if hasattr(config, "allow_connections") else False

        result = None
        try:
            result = self._get_results(output_file, base_command, child_limit=child_limit, executable_timeout=timeout, memory_limit=memory_limit, allow_connections=allow_connections)
        except FileNotFoundError:   # TODO: Write tests for these exceptions # TODO: if python execution runs out of memory a validation error is raised for some reason. Fix this.
            self.feedbacks.append(CheckResult(config, "functionality", 0, "Test execution failed: Result not generated"))
            return
        except json.decoder.JSONDecodeError:
            self.feedbacks.append(CheckResult(config, "functionality", 0, "Test execution failed: Failed to process result"))
            return
        except FailedValidation:
            self.feedbacks.append(CheckResult(config, "functionality", 0, "Test execution failed: Result file failed validation"))
            return
        except BadExecutionError as e:
            self.feedbacks.append(CheckResult(config, "functionality", 0, f"Test execution failed: During execution an error occured:\n{e.result.stderr}"))
            return
        
        
        if result is not None:
            for i, r in enumerate(result):
                self.feedbacks.append(
                    CheckResult(config, r["question"], r["mark"], r["feedback"], i + 1, r["weight"])
                )
        else:
            self.feedbacks.append(CheckResult(config, "functionality", 0, f"Test execution failed"))

    # TODO: Write tests for this
    def _get_results(self, output_file, base_command, executable_timeout=EXECUTABLE_TIMEOUT, memory_limit=MAX_VIRTUAL_MEMORY, child_limit=0, allow_connections=False):
        safety_counter = 0
        skip = 0
        partial_result = []
        specific_results = []

        if type(base_command) == str:
            base_command = [base_command]

        while safety_counter < 32:
            safety_counter += 1
            if output_file.is_file():
                output_file.unlink()

            secret_location = Validation.get_secret(8)
            secret_key = Validation.get_secret(32)
            env = {secret_location: secret_key}
            secret_file = Path(self.tmp_dir, secret_location)

            exec_result = execution.execute(
                base_command + [output_file.absolute().as_posix(),
                str(skip), secret_location],
                self.tmp_dir,
                timeout=EXECUTABLE_TIMEOUT,
                env_add=env,
                child_limit=child_limit,
                allow_connections=allow_connections,
                memory_limit=memory_limit)
            self.print_verbose(exec_result)
            exec_result.sanitise_outputs(base_command[0], "tested_executable")

            try:
                if exec_result.retval != 0 and not exec_result.exception:
                    raise BadExecutionError(exec_result)
                if not output_file.is_file():
                    raise FileNotFoundError
                if self.check_validity and not Validation.validate_result_file(output_file, secret_file, secret_key):
                    raise FailedValidation
                with open(output_file) as json_file:
                    result = json.load(json_file)
            except FileNotFoundError:
                result = None
                if not partial_result:
                    raise FileNotFoundError
            except BadExecutionError as e:
                result = None
                if not partial_result:
                    raise e
                
            if not result:
                if skip < len(partial_result):
                    specific_results[skip] = exec_result
                    skip += 1
                    continue
                else:
                    break

            if len(partial_result) < len(result):
                partial_result = result
                specific_results = [None for _ in partial_result]
            else:
                partial_result[skip:] = result[skip:]

            if partial_result[-1]["mark"] != "":
                break

            try:
                failed = skip + next(i for i, r in enumerate(result[skip:]) if r["mark"] == "")
            except StopIteration:
                specific_results[-1] = exec_result
                break

            if failed > skip:
                skip = failed
            else:
                specific_results[skip] = exec_result
                skip = failed + 1

            if skip >= len(partial_result):
                specific_results[-1] = exec_result
                break
        
        for r, exception in zip(partial_result, specific_results):
            if r["mark"] == "":
                r["mark"] = "0"
                exception_message = self._get_exception_message(exception)
                r["feedback"] = f"{exception_message} : FAIL"

        return partial_result

    def _get_exception_message(self, result):
        default = "During execution an error occured"
        if result is None:
            return default

        exception_messages = {
            TimeoutExpired: "Execution timed out during this question",
            execution.ProcessOutOfMemoryError: "Execution ran out of memory. This could indicate a possible inefficiency or memory leak",
            execution.ProcessChildLimitHitError: "Execution interupted because too many child process were started",
            execution.ProcessOpenedSocketError: "Execution interupted because a socket connection was opened"
        }

        for exception_type, message in exception_messages.items():
            if isinstance(result.exception, exception_type):
                return message
        return f"{default}\n{result.stderr}"
