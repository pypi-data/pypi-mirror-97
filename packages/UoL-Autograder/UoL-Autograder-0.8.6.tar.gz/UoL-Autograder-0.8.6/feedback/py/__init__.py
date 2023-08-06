import json
import subprocess
import sys, os
import re
from collections import namedtuple
from tempfile import TemporaryFile
from pathlib import Path
import shutil
from pylint import epylint as lint
from ..general import util
from ..general import execution
from ..general import Runner
from ..general.constants import *
from ..general.result import CheckResult
from ..general.py_eval_util import get_eval_util_path

class PyLookup(util.Lookup):
    _runner_feedback = "py_runner_feedback.json"
    _eval_feedback = "py_eval_feedback.json"
    _static_feedback = "py_static_feedback.json"

class PyRunner(Runner):
    def __init__(self, tmp_files, run_args={}, runner_config=None):
        super().__init__(tmp_files, run_args, runner_config)
        self.py_lookup = PyLookup(tmp_files.lookup_dir)
        self.print_verbose(f"Working dir: {tmp_files.tmp_dir}")
        self._copy_py_eval_util()

        self._test_lookup["syntax"] = self.test_syntax
        self._test_lookup["functionality"] = self.test_functionality
        self._test_lookup["static_analysis"] = self.static_analysis

    def test_syntax(self, config):
        self.print_verbose("Testing syntax")
        # Here we check whether the code runs
        exec_result = execution.execute([PY_RUNNER, self.tested_path], self.tmp_dir, timeout=5)

        runs = exec_result.retval == 0 or exec_result.retval is None

        # Provide feedback
        with self.py_lookup.runner_feedback.open() as json_file:
            syntax_feedback = json.load(json_file)
        
        feedback = [syntax_feedback[PASS if exec_result.retval == 0 else FAIL]]
        if not runs:
            feedback.append(util.as_md_code(exec_result.stderr.split('\n')))
            self.print_verbose(f"Error output:\n{exec_result.stderr}")

        # create feedback dictionary file
        self.feedbacks.append(CheckResult(config, "syntax", 1 if exec_result.retval == 0 else 0, '\n'.join(feedback)))


    def test_functionality(self, config):
        self.print_verbose("Testing functionality")

        self._test_run_executable([PY_RUNNER, config.tester_file.absolute().as_posix(), self.tested_path], config)

    def static_analysis(self, config):
        self.print_verbose("Running static analysis")

        error_penalty = config.error_penalty if hasattr(config, "error_penalty") else 1
        warning_penalty = config.warning_penalty if hasattr(config, "warning_penalty") else 0.1
        convention_penalty = config.convention_penalty if hasattr(config, "convention_penalty") else 0.05
        refactor_penalty = config.refactor_penalty if hasattr(config, "refactor_penalty") else 0.05

        stdout, _ = lint.py_run(self.tested_path, return_std=True)
        result = stdout.getvalue().replace(self.tested_path, Path(self.tested_path).name)
        
        lines = result.split('\n')
        divider_index = next((i for i, l in enumerate(lines) if l.endswith('-----')), None)     # Get first or default
        relevant_lines = lines[1:divider_index] if divider_index else lines[1:]
        
        count = lambda lines, word: sum(word in line for line in lines)

        counts = [count(relevant_lines, word) for word in [" error ", " warning ", " convention ", " refactor "]]

        score = 1 - sum(c * p for c, p in zip(counts, [error_penalty, warning_penalty, convention_penalty, refactor_penalty]))
        clamped_score = min(1, max(0, score))

        with self.py_lookup.static_feedback.open() as json_file:
            static_feedback = json.load(json_file)

        if counts[0] > 0:
            feedback = static_feedback["result"]["errors"]
        elif sum(counts[1:]) > 0:
            feedback = static_feedback["result"]["warnings"]
        else:
            feedback = static_feedback["result"]["correct"]

        if sum(counts) > 0:
            feedback += "\n{0}".format("\n".join(relevant_lines))
            contextual_feedback = []
            for context, fb in static_feedback["contextual"].items():
                if any(context in line for line in lines):
                    contextual_feedback.append(fb)
            if any(contextual_feedback):
                feedback += "\n{0}".format('\n'.join(contextual_feedback))

        self.print_verbose("\n".join(relevant_lines))
        self.print_verbose(" ".join(f"{t}: {c}" for t, c in zip(["errors", "warnings", "conventions", "refactors"], counts)))
        
        self.feedbacks.append(CheckResult(config, "static analysis", clamped_score, feedback))
