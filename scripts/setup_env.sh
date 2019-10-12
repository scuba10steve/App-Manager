#!/usr/bin/env bash

type="venv"

if [[ $1 == "conda" ]]; then
    if [[ "$(conda env list)" == *"app-manager"* ]]; then
        conda env remove -n default
    fi

    if [[ -f environment.yml ]]; then
        conda env create -f=environment.yml
    fi
else
    if [[ $(which virtualenv) && ! -d ./venv ]]; then
        virtualenv ./venv
        if [[ -f ./venv/bin/activate ]]; then
            . ./venv/bin/activate
            pip install -r requirements.txt
        else 
            . ./venv/Scripts/activate
            pip install -r requirements.txt
        fi
    fi
fi