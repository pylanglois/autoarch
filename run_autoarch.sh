#!/bin/bash

sudo pacman -Sy python-pip git
pip install plumbum
PYTHONPATH=$PWD autoarch/os.py
PYTHONPATH=$PWD autoarch/user.py
