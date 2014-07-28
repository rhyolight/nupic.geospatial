#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: ./run_complete.sh /path/to/data.csv"
    exit
fi

SCRIPT_DIR=$(dirname "${0}")

OUTPUT="output"
PROCESSED_DATA=${OUTPUT}/processed_data.csv

mkdir -p ${OUTPUT}

${SCRIPT_DIR}/preprocess_data.py ${1} ${PROCESSED_DATA}
${SCRIPT_DIR}/run_model.sh ${PROCESSED_DATA}
