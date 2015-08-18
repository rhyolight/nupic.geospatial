#!/usr/bin/env python
# ----------------------------------------------------------------------
# Numenta Platform for Intelligent Computing (NuPIC)
# Copyright (C) 2013, Numenta, Inc.  Unless you have an agreement
# with Numenta, Inc., for a separate license for this software code, the
# following terms and conditions apply:
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Affero Public License for more details.
#
# You should have received a copy of the GNU Affero Public License
# along with this program.  If not, see http://www.gnu.org/licenses.
#
# http://numenta.org/licenses/
# ----------------------------------------------------------------------
import os
import sys
from optparse import OptionParser

from tools.preprocess_data import preprocess
from tools.anomaly_to_js_data import postprocess
from model.geospatial_anomaly import runGeospatialAnomaly

DEFAULT_OUTPUT_DIR = "output"
verbose = False
scriptDir = os.path.dirname(os.path.realpath(__file__))


parser = OptionParser(
  usage="%prog <path/to/input/file> [options]\n\nRun NuPIC on specified "
        "location file, which should already be in the proper format "
        "(downloaded from the simulator)."
)

parser.add_option(
  "-m",
  "--manual-sequence",
  action="store_true",
  default=False,
  dest="manualSequence",
  help="Automatically breaks into sequences based upon time gaps."
)
parser.add_option(
  "-t",
  "--time-encoders",
  action="store_true",
  default=False,
  dest="useTimeEncoders",
  help="Adds time of day encoder to model params."
)
parser.add_option(
  "-v",
  "--verbose",
  action="store_true",
  default=False,
  dest="verbose",
  help="Print debugging statements."
)
parser.add_option(
  "-o",
  "--output-dir",
  default=DEFAULT_OUTPUT_DIR,
  dest="outputDir",
  help="Where to write the output file."
)
parser.add_option(
  "-s",
  "--scale",
  default=False,
  dest="scale",
  help="Meter resolution for Geospatial Coordinate Encoder (default 5m)."
)


def run(inputPath, outputDir, useTimeEncoders, scale, autoSequence):

  outputPath = os.path.abspath(outputDir)
  if not os.path.exists(outputPath):
    os.makedirs(outputPath)

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

  run(
    input_path,
    options.outputDir,
    options.useTimeEncoders,
    options.scale,
    not options.manualSequence)
