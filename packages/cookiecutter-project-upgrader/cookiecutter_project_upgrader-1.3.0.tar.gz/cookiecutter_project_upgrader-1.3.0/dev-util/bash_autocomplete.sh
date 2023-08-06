#!/usr/bin/env bash

if [[ $0 == $BASH_SOURCE ]]; then
    echo "source this script!"
    exit 1
fi

eval "$(_COOKIECUTTER_PROJECT_UPGRADER_COMPLETE=source cookiecutter_project_upgrader)"

