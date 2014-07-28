#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: ./run_model.sh /path/to/processed_data.csv"
    exit
fi

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

HOUND=..
OUTPUT="output"
ANOMALY_SCORES=${OUTPUT}/anomaly_scores.csv
VISUALIZATION_DATA=${SCRIPT_DIR}/../static/js/data.js

mkdir -p ${OUTPUT}
${SCRIPT_DIR}/../model/geospatial_anomaly.py ${1} ${ANOMALY_SCORES}
rm $VISUALIZATION_DATA
${SCRIPT_DIR}/../tools/anomaly_to_js_data.py ${ANOMALY_SCORES} ${VISUALIZATION_DATA}
