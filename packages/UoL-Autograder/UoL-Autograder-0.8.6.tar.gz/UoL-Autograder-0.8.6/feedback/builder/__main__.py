from . import build
import argparse

builder_parser = argparse.ArgumentParser(
    description="Create Autograder zip file",
    prog="feedback-builder")
builder_parser.add_argument('tested_file', type=str,
                            help="file to be tested")
builder_parser.add_argument('config_file', type=str,
                            help="config for the test")
builder_parser.add_argument('--verbose', '-v', action="store_true",
                            help="Enable extra console logging")
builder_parser.add_argument('--output_zip', '-o', type=str, default="autograder.zip",
                            help="Location of the generated zip")


def main():
    args = builder_parser.parse_args()

    build(args.tested_file, args.config_file,
          args.output_zip, verbose=args.verbose)


if __name__ == "__main__":
    main()
