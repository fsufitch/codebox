#!/bin/sh
virtualenv -p python3 .
bin/pip install -r requirements.txt
bin/python3 setup.py develop
