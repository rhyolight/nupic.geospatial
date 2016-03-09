#!/usr/bin/env python

import os
import sys

from tools.preprocess_data import preprocess
from tools.anomaly_to_js_data import postprocess
from model.geospatial_anomaly import runGeospatialAnomaly

verbose = False
scriptDir = os.path.dirname(os.path.realpath(__file__))

def run(inputPath, outputPath, useTimeEncoders, scale, autoSequence, verbose):

  preProcessedOutputPath = os.path.join(outputPath, "preprocessed_data.csv")
  if verbose: print "Pre-processing %s..." % inputPath
  preprocess(inputPath, preProcessedOutputPath, verbose=verbose)

  anomalyOutputPath = os.path.join(outputPath, "anomaly_scores.csv")
  if verbose: print "Running NuPIC on %s..." % preProcessedOutputPath
  runGeospatialAnomaly(preProcessedOutputPath,
                       anomalyOutputPath,
                       scale=scale,
                       autoSequence=autoSequence,
                       useTimeEncoders=useTimeEncoders,
                       verbose=verbose)

  visualizationOutputPath = os.path.join(scriptDir, "static/js/data.js")
  if verbose: print "Creating visualization at %s..." % visualizationOutputPath
  postprocess(anomalyOutputPath, visualizationOutputPath)


if __name__ == "__main__":
  (options, args) = parser.parse_args(sys.argv[1:])
  try:
    input_path = args.pop(0)
  except IndexError:
    parser.print_help(sys.stderr)
    sys.exit()

  verbose = options.verbose

  run(input_path, outputDir, useTimeEncoders, scale, manualSequence, verbose)
