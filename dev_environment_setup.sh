#!/bin/bash

sudo apt install python3-pip

pip3 install -r requirements.txt -t lib
PYTHONPATH=~/nz-river-level-alerts/lib