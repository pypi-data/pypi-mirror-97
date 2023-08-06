#!/usr/bin/env bash

# Set up autograder files

cd /autograder/source

feedback "/autograder/submission/{}" "/autograder/source/config.json" -f "/autograder/results/results.json"