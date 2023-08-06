#!/usr/bin/env bash
echo "CREATING USER"
adduser {} --no-create-home --disabled-password --gecos ""
echo "USER CREATED"

echo "INSTALLING DEPENDENCIES"
apt-get update
apt-get install -y python3.7 python3-pip python3-dev
apt-get install -y cloc cppcheck clang-format
echo "DEPENDENCIES INSTALLED"

echo "INSTALLING REQUIREMENTS"
pip3 install UoL-Autograder
echo "REQUIREMENTS INSTALLED"
