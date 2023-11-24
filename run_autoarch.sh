#!/bin/bash

sudo pacman -Sy python-pip git
pip install plumbum
PYTHONPATH=$PWD python autoarch/os.py
PYTHONPATH=$PWD python autoarch/user.py
