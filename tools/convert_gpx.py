#!/usr/bin/env python
import sys
import os
import csv
import time
from optparse import OptionParser

import gpxpy
import gpxpy.gpx

# INPUT = './data/Mon Jul 28 2014.gpx'
DEFAULT_OUTPUT_DIR = "output"
# OUTPUT = './data/convert_gpx_output.csv'
verbose = False

parser = OptionParser(
  usage="%prog <path/to/gpx/file> [options]\n\nConvert GPX data file into "
        "NuPIC input file for the Geospatial Tracking Application."
)

parser.add_option(
  "-o",
  "--output-dir",
  default=DEFAULT_OUTPUT_DIR,
  dest="output_dir",
  help="Output directory to write the resulting NuPIC input data file."
)
parser.add_option(
  "-v",
  "--verbose",
  action="store_true",
  default=False,
  dest="verbose",
  help="Print debugging statements."
)


def run(input_path, output_dir):

  gpx_file = open(input_path, 'r')
  gpx = gpxpy.parse(gpx_file)

  output_file = os.path.join(output_dir, "converted_gpx_output.csv")

  with open(output_file, 'w') as file_out:
    writer = csv.writer(file_out)
    for track in gpx.tracks:
      for segment in track.segments:
        for point in segment.points:
          ts = int(time.mktime(point.time.timetuple()) * 1000)
          if verbose:
            print "{0}: ({1},{2})".format(point.time.__str__(), point.latitude, point.longitude)
          writer.writerow(["testroute", ts, point.longitude, point.latitude, None, 0, None, 1])


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
    options.output_dir)