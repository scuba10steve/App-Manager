#!/usr/bin/env bash

if [[ "$(conda env list)" == *"app-manager"* ]]; then
    conda env remove -n default
fi

if [[ -f environment.yml ]]; then
    conda env create -f=environment.yml
fi
