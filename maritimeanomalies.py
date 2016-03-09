#!/usr/bin/env python

import os
import sys
from optparse import OptionParser

from run import run
from tools.convertion import convertion
from tools.anomaly_to_kml import anomalyrepresentation as KML

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

def maritimeanomalies(inputPath, outputDir, useTimeEncoders, scale, autoSequence):

  outputPath = os.path.abspath(outputDir)
  if not os.path.exists(outputPath):
    os.makedirs(outputPath)

  convertedOutputPath = os.path.join(outputPath, "converted_data.csv")
  if verbose: print "Converting %s..." % inputPath
  convertion(inputPath, convertedOutputPath)

  run(convertedOutputPath, outputPath, useTimeEncoders=useTimeEncoders, scale=scale, autoSequence=autoSequence, verbose=verbose)

  representationDataPath = os.path.join(outputPath, "anomaly_scores.csv")
  representationOutputPath = os.path.join(outputPath, "anomaly_representation.kml")
  if verbose: print "Creating visualization at %s..." % representationOutputPath
  KML(representationDataPath,representationOutputPath)


if __name__ == "__main__":
  (options, args) = parser.parse_args(sys.argv[1:])
  try:
    input_path = args.pop(0)
  except IndexError:
    parser.print_help(sys.stderr)
    sys.exit()

  verbose = options.verbose

  maritimeanomalies(
    input_path,
    options.outputDir,
    options.useTimeEncoders,
    options.scale,
    not options.manualSequence)
