import subprocess
import argparse
import os
from tempfile import TemporaryFile

from ..general.constants import COMPILER, DEFAULT_CPP_STANDARD
from ..general.util import decoder, read_from_start


def compile_cpp_to_o(cpp_file, out_file, working_dir=os.getcwd(), std=DEFAULT_CPP_STANDARD):
    if not out_file.endswith(".o"):
        extension = out_file.split(".")[-1]
        out_file = out_file.replace(f".{extension}", ".o")

    with TemporaryFile() as t:  # TODO: Use unified function
        run_params = [COMPILER, f'-std={std}', '-fnon-call-exceptions', '-c', cpp_file, '-o', out_file]
        # print(" ".join([param for param in run_params if param != ""]))
        subprocess.call([param for param in run_params if param != ""],
                        cwd=working_dir, stderr=t)              # Run compiler in the working directory and capture its contents to a file
        # Return to the start of the file, and read its contents
        content = read_from_start(t)
        output = decoder(content).replace(working_dir, "").split("\n")
    assert os.path.isfile(out_file), "Compilation failed with:\n{0}".format("\n".join(output))
    return out_file


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compile file to .o file")
    parser.add_argument('cpp_file', type=str, help="file to be compiled")
    parser.add_argument('out_file', type=str, help="target compiled file")

    args = parser.parse_args()
    compile_cpp_to_o(args.cpp_file, args.out_file)
