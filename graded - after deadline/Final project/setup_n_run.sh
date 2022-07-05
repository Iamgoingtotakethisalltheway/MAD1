#!/bin/bash

if [ -d ".final_project" ];
then
    echo "===================================="
    echo "SETTING UP LOCAL VIRTUAL ENVIRONMENT"
    echo "===================================="
    # Activate virutal env
    .   .final_project/bin/activate
else
    echo "==========================================="
    echo "CREATING AND ACTIVATING VIRTUAL ENVIRONMENT"
    echo "==========================================="
    python -m venv .final_project
    # Activate virutal env
    .   .final_project/bin/activate
fi

echo "===================================="
echo "INSTALLING PACKAGES AND DEPENDENCIES"
echo "===================================="
# Install packages and dependencies
pip install -r requirements.txt

export ENV=development
source export_secrets.sh
python main.py
deactivate

