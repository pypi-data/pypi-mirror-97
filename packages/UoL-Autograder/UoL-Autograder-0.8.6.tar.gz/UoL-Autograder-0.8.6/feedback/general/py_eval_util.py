from inspect import getmembers, isfunction, signature, getfile, currentframe, isclass
import os, time, signal
import importlib
import importlib.util
import json
from pathlib import Path
import subprocess
from collections.abc import Iterable
from io import StringIO 
import sys
import argparse
import hashlib

PASS = "pass"
FAIL = "fail"
EXCEPTION = "exceptions"
EXCEPTION_TAG = "EXCEPTION:"
DURATION_SAMPLE_COUNT = 1000

def get_eval_util_path():
    return os.path.abspath(getfile(currentframe()))

def get_module_functions(module):
    # Get every function in a module
    return [f[1] for f in getmembers(module, isfunction)]

def get_module_classes(module):
    return [f[1] for f in getmembers(module, isclass)]

def levenshtein_ratio_and_distance(s, t, ratio_calc = False):
    """
    Source: https://www.datacamp.com/community/tutorials/fuzzy-string-python
    More on lev_distance: https://en.wikipedia.org/wiki/Levenshtein_distance

        levenshtein_ratio_and_distance:
        Calculates levenshtein distance between two strings.
        If ratio_calc = True, the function computes the
        levenshtein distance ratio of similarity between two strings
        For all i and j, distance[i,j] will contain the Levenshtein
        distance between the first i characters of s and the
        first j characters of t
    """
    # Initialize matrix of zeros
    rows = len(s)+1
    cols = len(t)+1
    distance = [[0 for i in range(cols)] for j in range(rows)]
    col, row = 0, 0
    
    # Populate matrix of zeros with the indeces of each character of both strings
    for i in range(1, rows):
        for k in range(1,cols):
            distance[i][0] = i
            distance[0][k] = k

    # Iterate over the matrix to compute the cost of deletions,insertions and/or substitutions    
    for col in range(1, cols):
        for row in range(1, rows):
            if s[row-1] == t[col-1]:
                cost = 0 # If the characters are the same in the two strings in a given position [i,j] then the cost is 0
            else:
                # In order to align the results with those of the Python Levenshtein package, if we choose to calculate the ratio
                # the cost of a substitution is 2. If we calculate just distance, then the cost of a substitution is 1.
                if ratio_calc == True:
                    cost = 2
                else:
                    cost = 1
            distance[row][col] = min(distance[row-1][col] + 1,      # Cost of deletions
                                 distance[row][col-1] + 1,          # Cost of insertions
                                 distance[row-1][col-1] + cost)     # Cost of substitutions
    if ratio_calc == True:
        # Computation of the Levenshtein Distance Ratio
        Ratio = ((len(s)+len(t)) - distance[row][col]) / (len(s)+len(t)) if (len(s) > 0 and len(t) > 0) or s == t else 0
        return Ratio
    else:
        # print(distance) # Uncomment if you want to see the matrix showing how the algorithm computes the cost of deletions,
        # insertions and/or substitutions
        # This is the minimum number of edits needed to convert string a to string b
        return distance[row][col]

def levenshtein_distance(s1, s2):
    # Calculate levenshtein distance between two strings
    return levenshtein_ratio_and_distance(s1, s2)

def levenshtein_ratio(s1, s2):
    # Calculate the similarity between two strings
    return levenshtein_ratio_and_distance(s1, s2, ratio_calc=True)


def result_to_dictionary(question, mark, weight, feedback):
    return {
        "question": question,
        "mark": mark,
        "weight": weight,
        "feedback": feedback
    }


def numbers_close(a, b, margin):
    return abs(a - b) < margin

def load_module(tested_file, load_as_main=False):
    spec = importlib.util.spec_from_file_location("__main__" if load_as_main else "tested_module", tested_file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def run_executable(executable, input_data=None, delay=0.2, timeout=10):
    # Run executable, wait a bit, than send input and return the decoded result split by line
    p = subprocess.Popen(executable, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(delay)
    try:
        result, _ = p.communicate(input=input_data, timeout=timeout)
    except subprocess.TimeoutExpired:
        # result = b""
        p.kill()
        result, _ = p.communicate()
    return result.decode('unicode_escape').replace("\r", "").split('\n')

class InputOverride(list):
    def __init__(self, arr=[]):
        if type(arr) == str:
            arr = [arr]
        self.arr = arr
        self.data = "\n".join(map(str, self.arr))
        self.too_many_reads = False

    def __enter__(self):
        self._stdin = sys.stdin
        self._stringio = StringIO()
        self._stringio.write(self.data)
        self._stringio.seek(0)
        sys.stdin = self._stringio
        return self

    def __exit__(self, exec_type, exec_value, traceback):
        self.extend(self.data[:self._stringio.tell()].splitlines())
        del self._stringio
        sys.stdin = self._stdin

        if exec_type and issubclass(exec_type, EOFError):
            self.too_many_reads = True
            return True

class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stdout = self._stdout

class CapturingErr(list):
    def __enter__(self):
        self._stderr = sys.stderr
        sys.stderr = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stderr = self._stderr


class RunnerTypes:
    code = 1
    executable = 2
    module = 3

class Evaluator:
    def __init__(self, strip_end_nl=True):
        parser = argparse.ArgumentParser(description="Test an exercise")
        parser.add_argument('tested', type=str, help="file to be tested")
        parser.add_argument('output_file', type=str, help="file to publish the result")
        parser.add_argument('skip', type=int, help="number of questions to skip")
        parser.add_argument('secret_location', type=str, default="", help="location of the secret value")
        self.args = parser.parse_args()

        self.strip_end_nl = strip_end_nl

        self._runner_type = None

        self._executable = None
        self._module = None
        self._input_provider = None
        self._name_provider = None
        self._result_provider = None
        self._score_provider = None
        self._feedback_provider = None
        self._combined_provider = None
        self._function_signature = None
        self._secret_key = self._get_secret()

    def _get_secret(self):
        secret_key = os.environ[self.args.secret_location]
        os.environ[self.args.secret_location] = ""
        return secret_key


    def run_executable(self, args=[]):
        if self._runner_type:
            raise EnvironmentError("Runner already defined. You may only use one run_ on the Evaluator")
        self._runner_type = RunnerTypes.executable
        self._executable = [self.args.tested] + args
        return self

    def run_module(self):
        if self._runner_type:
            raise EnvironmentError("Runner already defined. You may only use one run_ on the Evaluator")
        self._runner_type = RunnerTypes.module
        self._module = self.args.tested
        return self

    def with_input(self, input_provider):
        if self._runner_type != RunnerTypes.executable and self._runner_type != RunnerTypes.module:
            raise EnvironmentError("Can't use with_input in non executable/module evaluation. Use run_executable or run_module on the Evaluator first")
        self._input_provider = input_provider
        return self

    def with_name(self, name_provider):
        self._name_provider = name_provider
        return self

    def run_code(self, result_provider, signature=None):
        if self._runner_type:
            raise EnvironmentError("Runner already defined. You may only use one run_ on the Evaluator")
        self._runner_type = RunnerTypes.code
        self._result_provider = result_provider
        self._module = self.args.tested
        self._function_signature = signature
        return self

    def with_score(self, score_provider):
        self._score_provider = score_provider
        return self

    def with_feedback(self, feedback_provider):
        self._feedback_provider = feedback_provider
        return self

    def with_score_and_feedback(self, combined_provider):
        self._combined_provider = combined_provider
        return self

    def start(self):
        self._check_builder()
        # Discover number of questions
        n = 0
        try:
            while self._name_provider(n):
                n += 1
        except IndexError:
            pass

        results = [result_to_dictionary(self._name_provider(i), "", 1 / n, "") for i in range(n)]
        self._save_results(results)

        for i in range(self.args.skip, n):
            print(i)
            try:
                result, glob = self._get_result(i)
                score, feedback = self._get_score_and_feedback(i, result, glob)
            except Exception as e:
                score = 0
                feedback = f"During evaluation an error occured:\n{str(e)} : FAIL"
            results[i] = result_to_dictionary(self._name_provider(i), score, 1 / n, feedback)
            self._save_results(results)
        
        self._save_results(results)

    def _save_results(self, results):
        results_raw = json.dumps(results, indent=4)
        # print("Secret:", self.args.secret_location)
        with open(self.args.secret_location, "w") as f:
            h = hashlib.sha256()
            h.update(results_raw.encode("ascii", 'ignore'))
            h.update(self._secret_key.encode("ascii"))
            f.write(h.hexdigest())
        with open(self.args.output_file, "w") as f:
            f.write(results_raw)

    def _get_result(self, i):
        if self._runner_type == RunnerTypes.executable:
            exe_input = self._input_provider(i)
            r = run_executable(self._executable, self._handle_executable_input(exe_input))
            if r[-1] == "" and self.strip_end_nl:
                r.pop()
            return r, {}

        elif self._runner_type == RunnerTypes.code:
            module = load_module(self._module, load_as_main=False)
            if self._function_signature:
                func = self._find_element(module, self._function_signature, fuzzy_threshold=0.8)
                if not func:
                    raise Exception("Could not find function with requested signature")
                return self._result_provider(i, func), {}
            return self._result_provider(i, module), {}

        elif self._runner_type == RunnerTypes.module:
            mod_input = self._handle_module_input(self._input_provider(i))
            with Capturing() as output, InputOverride(mod_input) as consumed_input:
                load_module(self._module, load_as_main=True)
            return output, {"consumed_input": consumed_input}

    def _inject_globals(self, func, glob):
        for k,v in glob.items():
            func.__globals__[k] = v

    def _handle_executable_input(self, exe_input):
        if type(exe_input) == str:
            return exe_input.encode("utf-8")
        if isinstance(exe_input, Iterable):
            return '\n'.join(map(str, exe_input)).encode("utf-8")
        return str(exe_input).encode("utf-8")

    def _handle_module_input(self, mod_input):
        if not mod_input:
            return []
        if isinstance(mod_input, Iterable):
            return mod_input
        return [mod_input]

    def _get_score_and_feedback(self, i, result, glob):
        if self._combined_provider:
            self._inject_globals(self._combined_provider, glob)
            return self._combined_provider(i, result)
        else:
            self._inject_globals(self._score_provider, glob)
            score = self._score_provider(i, result)
            self._inject_globals(self._feedback_provider, glob)
            feedback = self._feedback_provider(i, result, score)
            return score, feedback

    def _check_builder(self):
        assert self._name_provider, "Name provider missing. You must call with_name on the Evaluator"
        assert self._score_provider or self._combined_provider, "Score provider missing. You must call with_score or with_score_and_feedback on the Evaluator"
        
        if not self._feedback_provider:
            self._feedback_provider = lambda i, j, k: ""

        if self._runner_type == RunnerTypes.code:
            assert self._result_provider, "Result provider missing. You must call run_code on the Evaluator"

        elif self._runner_type == RunnerTypes.executable:
            assert self._executable, "Executable missing. You must call run_executable on the Evaluator"
            if not self._input_provider:
                self._input_provider = lambda _: None

        elif self._runner_type == RunnerTypes.module:
            assert self._module, "Module missing. You must call run_module on the Evaluator"
            if not self._input_provider:
                self._input_provider = lambda _: None

        else:
            raise EnvironmentError("No runner specified. You must call one run_ function on the evaluator")

    def _find_element(self, module, target, fuzzy_threshold = 1):
        # Find a function in a module, that has the right signature, and the right name (or close to it)
        # fuzzy_threshold controlls how close the function names should match
        # target should have the same name, and parameters, as the expected function
        functions = get_module_functions(module) + get_module_classes(module)
        target_name = target.__name__.lower()
        target_arg_count = len(signature(target).parameters)

        for f in functions:
            if f.__name__.lower() == target_name and\
                len(signature(f).parameters) == target_arg_count:
                return f

        if fuzzy_threshold < 1:
            for f in functions:
                lev_ratio = levenshtein_ratio(target_name, f.__name__)
                if  lev_ratio > fuzzy_threshold and \
                        len(signature(f).parameters) == target_arg_count:
                    return f
        return None
