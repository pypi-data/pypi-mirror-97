import sys

LOOKUP_DIR = "lookup"

# linux, win32, cygwin, darwin
IS_WINDOWS = sys.platform.lower().startswith("win")
IS_LINUX = sys.platform.lower().startswith("linux")
EXECUTABLE_EXTENSION = ".exe" if IS_WINDOWS else ".out"
TMP_EXECUTABLE = "tmp.exe" if IS_WINDOWS else "tmp.out"
COMPILED_O = "cmp.o"
TMP_O = "tmp.o"
COMPILER = "g++" if IS_WINDOWS or IS_LINUX else "g++-9"
DEFAULT_CPP_STANDARD = "c++11"
SUPPORTED_CPP_STANDARDS = ["c++98", "c++03", "gnu++98", "gnu++03", "c++11", "gnu++11", "c++14", "gnu++14", "c++17", "gnu++17"]

JSON_HPP = "json.hpp"
CPP_EVAL_UTIL_CPP = "cpp_eval_util.cpp"
CPP_EVAL_UTIL_H = "cpp_eval_util.h"
EMPTY_MAIN = "empty_main.cpp"
CPP_EVAL_UTIL_O = "cpp_eval_util.o"

PY_RUNNER = sys.executable

FAIL = "fail"
PASS = "pass"

RUNNER_USER = "runner"

EXECUTABLE_TIMEOUT = 30  # seconds
MAX_VIRTUAL_MEMORY = 526 * 1024 * 1024  # 526 MB
