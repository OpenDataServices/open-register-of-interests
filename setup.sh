#!/bin/bash

virtualenv --python=python3 .ve
source .ve/bin/activate
pip install -r ./requirements.txt
