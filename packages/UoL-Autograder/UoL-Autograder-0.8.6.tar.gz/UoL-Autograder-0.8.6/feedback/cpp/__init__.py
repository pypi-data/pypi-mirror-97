import difflib
import json
import subprocess
import sys, os
import shutil
from tempfile import TemporaryFile, TemporaryDirectory
from pathlib import Path
from ..general import util
from ..general import execution
from ..general.constants import *
from ..general import Runner
from ..general.result import CheckResult
from ..general.validation import FailedValidation
from ..general.py_eval_util import get_eval_util_path
from .ocache import OCache


class CppLookup(util.Lookup):
    _compiler_warnings = "cpp_compiler_feedback.json"
    _static_warnings = "cpp_static_warnings.json"
    _style_feedback = "cpp_style_feedback.json"
    _eval_feedback = "cpp_eval_feedback.json"


class CppRunner(Runner):
    def __init__(self, tmp_files, run_args={}, runner_config=None):
        super().__init__(tmp_files, run_args, runner_config)
        self.cpp_lookup = CppLookup(tmp_files.lookup_dir)
        self.print_verbose(f"Working dir: {tmp_files.tmp_dir}")

        self.compiled_o_files = {}
        self.executables = {}

        self.cpp_std = runner_config.cpp_std if hasattr(runner_config, "cpp_std") else DEFAULT_CPP_STANDARD
        assert self.cpp_std in SUPPORTED_CPP_STANDARDS, f"Unsupported or unknown standard: {self.cpp_std}"

        self.o_cache = OCache(self.cpp_std)
        if "clear_cache" in run_args and run_args["clear_cache"]:
            self.o_cache.clear()

        self._test_lookup["compile"] = self.test_compile
        self._test_lookup["functionality"] = self.test_functionality
        self._test_lookup["functionality_executable"] = self.test_executable_functionality
        self._test_lookup["static"] = self.static_code_analysis
        self._test_lookup["style"] = self.test_code_style
        
        self._copy_cpp_files()
        self._copy_py_eval_util()

    def _copy_to_tmp(self, path):
        assert path.is_file()
        new_path = Path(self.tmp_dir, path.name).absolute().as_posix()
        shutil.copy(path.absolute().as_posix(), new_path)
        return new_path
    
    def _copy_cpp_files(self):
        my_dir = util.get_current_dir()

        self._copy_to_tmp(Path(my_dir, JSON_HPP))
        self._copy_to_tmp(Path(my_dir, CPP_EVAL_UTIL_H))
        self._copy_to_tmp(self.cpp_lookup.eval_feedback)
        self.eval_util_cpp = self._copy_to_tmp(Path(my_dir, CPP_EVAL_UTIL_CPP))
            

    def test_functionality(self, config):
        # Here we run the .exe and read in the inputs, generated outputs and expected outputs
        self.print_verbose("Testing functionality")

        executable, output = self._get_executable_tester(self.tested_path, config.tester_file.absolute().as_posix())

        if not executable:
            self.feedbacks.append(CheckResult(config, "functionality", 0, f"Test execution failed, failed to build with error:\n{output}"))
            return

        self._test_run_executable(executable, config)

    def test_executable_functionality(self, config):
        # Here we run the tester file, that runs the .exe
        self.print_verbose("Testing executable functionality")

        executable, output = self._get_executable_standalone(self.tested_path)

        if not executable:
            self.feedbacks.append(CheckResult(config, "functionality", 0, f"Test execution failed: {output}"))
            return

        self._test_run_executable([PY_RUNNER, config.tester_file.absolute().as_posix(), executable], config, child_limit=1)

    def _process_issues_output(self, lines):
        if IS_WINDOWS:
            issue_lines = [line
                           for line in lines
                           if line.startswith(self.tmp_dir)]
            issues = [(i + 1, issue_line.split(":")[2], ':'.join(issue_line.split(":")[5:]))
                      for i, issue_line in enumerate(issue_lines)]
        else:
            issue_lines = [line.replace("]", "")
                           for line in lines
                           if line.startswith("[")]
            issues = [(i + 1, issue_line.split(":")[1], issue_line.split(")")[1])
                      for i, issue_line in enumerate(issue_lines)]
        return issues
        
    def static_code_analysis(self, config):
        self.print_verbose("Running static code analysis")
        error_penalty = config.error_penalty if hasattr(config, "error_penalty") else 0.2

        exec_result = execution.execute(['cppcheck', self.tested_path], self.tmp_dir)
        self.print_verbose(f"Raw result:\n{exec_result}")
        # Use cppcheck for static code analysis
        lines = exec_result.stderr.replace('\r\n', '\n').split('\n')
        
        issues = self._process_issues_output(lines)

        n_issues = len(issues)

        with self.cpp_lookup.static_warnings.open() as json_file:
            static_feedback = json.load(json_file)

        fb = ""
        # build the feedback string
        n_issues_feedback = static_feedback['no_issues']
        n_issues_feedback.sort(key=lambda x: x['threshold'], reverse=True)

        for band in n_issues_feedback:
            if n_issues >= band['threshold']:
                fb += band["text"].format(n_issues)
                break

        contextual_feedback = static_feedback['contextual']
        if n_issues > 0:
            for issue_id, line_number, msg in issues:
                fb += (f"Issue {issue_id} on line {line_number}: `{msg}`\n\n")

                # loop through contextual feedback and add any relevant comments
                for key in contextual_feedback:
                    if key in msg:
                        fb += f'{contextual_feedback[key]}\n\n'

        self.feedbacks.append(CheckResult(config, "static analysis", max(1.0 - error_penalty * n_issues, 0), fb))

    def test_code_style(self, config):
        self.print_verbose("Testing code style")
        fixed_file = f"{self.tested_path}.fixed"
        
        selected_style = config.style if hasattr(config, "style") else "google"
        
        # Run clang-format
        with open(fixed_file, "w") as new_file:
            # Write output to file
            subprocess.call(['clang-format', f'-style={selected_style}', self.tested_path],
                            stdout=new_file)

        with open(fixed_file, "r") as f:
            fixed = f.readlines()
        with open(self.tested_path, "r") as f:
            orig = f.readlines()

        with open(self.cpp_lookup.style_feedback) as json_file:
            style_feedback = json.load(json_file)

        # This compares the fixed and original source files
        s = difflib.SequenceMatcher(None, fixed, orig)
        # value in the range 0.0 to 1.0
        score = s.ratio()

        # Generate feedback comments
        fb = [style_feedback['style_check'][PASS if score == 1.0 else FAIL]]
        
        if score < 1.0:
            # Now use diff to compare student file and clang tidied one
            exec_result = execution.execute(['diff', '-y', '-W', '180', '-T', '-t', self.tested_path, fixed_file], self.tmp_dir)
            fb.append(util.as_md_code(exec_result.stdout.replace("\r\n", "\n").split('\n')))

        fb.append(style_feedback['general'])

        self.feedbacks.append(CheckResult(config, "style", score, '\n\n'.join(fb)))

    def _compile_tester_to_o(self, tester_path):
        my_dir = util.get_current_dir()

        eval_util_cpp = Path(my_dir, CPP_EVAL_UTIL_CPP)

        cached_eval_util_o = self.o_cache.add_or_get(eval_util_cpp)
        cached_tester_o = self.o_cache.add_or_get(Path(tester_path))
        return self._copy_to_tmp(cached_tester_o), self._copy_to_tmp(cached_eval_util_o)

    def _compile_in_tmp(self, files, pedantic=False, link=True, output=None):
        run_params = [COMPILER, f'-std={self.cpp_std}', '-fnon-call-exceptions']
        if pedantic:
            run_params += ['-Wall', '-Wpedantic', '-Wextra']
        if not link:
            run_params += ["-c"]
        if output:
            run_params += ["-o", output]
        run_params += files
        
        exec_result = execution.execute([param for param in run_params if param != ""], self.tmp_dir)
        self.print_verbose(exec_result)
        return exec_result.stderr.replace(self.tmp_dir, "").split("\n"), output and os.path.isfile(output)

    def _failed_compilation_feedback(self, output):
        with self.cpp_lookup.compiler_warnings.open() as json_file:       # Load feedback file
            compiler_feedback = json.load(json_file)
        feedback = []
        feedback.append(compiler_feedback['compilation_result'][FAIL])   # Add comiplation failed feedback
        
        feedback.append(util.as_md_code(output))                               # Add compilation output to feedback
        error_feedback = compiler_feedback["contextual"]["error"]   # Get contextual feedback
        error_keys = set([key for key in error_feedback for line in output if key in line])
        feedback.append('\n\n'.join([f'`{key}`: {error_feedback[key]}' for key in error_keys]))    # analyse each error, and add each to the feedback
        return '\n'.join(feedback)

    def _warning_compilation_feedback(self, output, feedback, warning_penalty):
        with self.cpp_lookup.compiler_warnings.open() as json_file:       # Load feedback file
            compiler_feedback = json.load(json_file)
        # check if there were any warnings
        n_warnings = len([line for line in output if "warning" in line.lower()])
                
        score = max(1.0 - (n_warnings * warning_penalty), 0)     # Take points away for each warnig

        if n_warnings > 0:
            # add general feedback
            feedback.append(compiler_feedback['warning_check_result'][FAIL])
            
            # add the raw warnings to the feedback
            feedback.append(util.as_md_code(output))
            warning_feedback = compiler_feedback["contextual"]["warning"]
            warning_keys = set([key for key in warning_feedback for line in output if key in line])
            feedback.append('\n\n'.join([f'`{key}`: {warning_feedback[key]}' for key in warning_keys]))

        else:
            feedback.append(compiler_feedback['warning_check_result'][PASS])
        
        return '\n'.join(feedback), score

    def _compilation_result_template(self, score, config, feedback):
        return CheckResult(config, "compilation", score, '\n'.join(feedback) if type(feedback) == list else feedback)

    def _get_executable_standalone(self, tested_path):
        if (tested_path) in self.executables:
            return self.executables[(tested_path)], None

        tested_o = ""
        if tested_path in self.compiled_o_files:
            tested_o = self.compiled_o_files[tested_path]
        else:
            tested_o = os.path.join(self.tmp_dir, f"{Path(tested_path).stem}.o")
            output, compiled = self._compile_in_tmp([tested_path], link=False, output=tested_o)
            
            if not compiled:
                error = "Failed to compile {0}\n{1}".format(tested_path, '\n'.join(output))
                self.print_verbose(error)
                return None, error
            self.compiled_o_files[tested_path] = tested_o
        
        compiled_executable = os.path.join(self.tmp_dir, f"{Path(self.tested_path).stem}.{EXECUTABLE_EXTENSION.lstrip('.')}")
        output, compiled = self._compile_in_tmp([tested_o], output=compiled_executable)
        if not compiled:
            error = "Failed to link {0}\n{1}".format(tested_path, '\n'.join(output))
            self.print_verbose(error)
            return None, error
        self.executables[(tested_path)] = compiled_executable

        return compiled_executable, None

    def _get_executable_tester(self, tested_path, tester_path):
        if (tested_path, tester_path) in self.executables:
            return self.executables[(tested_path, tester_path)], ""

        tested_o = ""
        if tested_path in self.compiled_o_files:
            tested_o = self.compiled_o_files[tested_path]
        else:
            tested_o = os.path.join(self.tmp_dir, f"{Path(tested_path).stem}.o")
            output, compiled = self._compile_in_tmp([tested_path], link=False, output=tested_o)
            if not compiled:
                self.print_verbose(f"Failed to compile {tested_path}\n{output}")
                return None, output
            self.compiled_o_files[tested_path] = tested_o
        
        compiled_executable = os.path.join(self.tmp_dir, f"{Path(tested_path).stem}_{Path(tester_path).stem}.{EXECUTABLE_EXTENSION.lstrip('.')}")
        tester_path, eval_util_o = self._compile_tester_to_o(tester_path)
        output, compiled = self._compile_in_tmp([tested_o, tester_path, eval_util_o], output=compiled_executable)
        if not compiled:
            self.print_verbose(f"Failed to link {tested_o, tester_path, eval_util_o}\n{output}")
            return None, output

        self.executables[(tested_path, tester_path)] = compiled_executable

        return compiled_executable, ""

    def test_compile(self, config):
        self.print_verbose("Testing compilation")
        warning_penalty = config.warning_penalty if hasattr(config, "warning_penalty") else 0.2

        compiled_o = os.path.join(self.tmp_dir, f"{Path(self.tested_path).stem}.o")

        # see if file compiles
        output, compiled = self._compile_in_tmp([self.tested_path], link=False, output=compiled_o)

        # Check whether compilation was succesful
        if not compiled:
            self.print_verbose("Compilation failed")
            self.feedbacks.append(self._compilation_result_template(0, config, self._failed_compilation_feedback(output)))
            return

        self.compiled_o_files[self.tested_path] = compiled_o
        
        with self.cpp_lookup.compiler_warnings.open() as json_file:       # Load feedback file
            compiler_feedback = json.load(json_file)

        feedback = []
        feedback.append(compiler_feedback['compilation_result'][PASS])

        # now look for warnings, so re-compile with warnings switched on
        self.print_verbose("Pedantic recompile")
        output, _ = self._compile_in_tmp([self.tested_path], link=False, pedantic=True)
        feedback_result, score = self._warning_compilation_feedback(output, feedback, warning_penalty)
        
        # create feedback dictionary file
        self.feedbacks.append(self._compilation_result_template(score, config, feedback_result))

