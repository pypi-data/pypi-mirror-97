import argparse
import os
from . import run_test
from .general.util import save_feedback_file


parser = argparse.ArgumentParser(description="General purpose test evaluator", prog="feedback")
parser.add_argument('tested_file', type=str, help="file to be tested")
parser.add_argument('config_file', type=str, help="config for the test")
parser.add_argument('--verbose', '-v', action="store_true", help="Enable extra console logging")
parser.add_argument('--result_file', '-f', type=str, default="result.json", help="output file name")
parser.add_argument('--clear_cache', '-x', action="store_true", help="Remove all cached contents")
parser.add_argument('--copy_tmp', '-c', type=str, default=None, help="Copy tmp dir to specified location, before it's removed")
parser.add_argument('--disable_result_validation', '-d', action="store_true", help="Disable validation checking on result files")
parser.add_argument('--result_precision', '-p', type=int, default=4, help="Numeric precision of output scores")

# Primary entry point, with argument processing
def main():
    args = parser.parse_args()

    result = run_test(
        args.tested_file, 
        args.config_file, 
        {"clear_cache": args.clear_cache, "verbose": args.verbose, "check_validity": not args.disable_result_validation}, 
        args.copy_tmp,
        args.result_precision)
    
    save_feedback_file(result, args.result_file, verbose=args.verbose)

if __name__ == "__main__":      # Run main if ran directly
    main()
