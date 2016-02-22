#!/usr/bin/env python
# ----------------------------------------------------------------------
# Numenta Platform for Intelligent Computing (NuPIC)
# Copyright (C) 2013, Numenta, Inc.  Unless you have purchased from
# Numenta, Inc. a separate commercial license for this software code, the
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
import sys
import os
import csv
import math
import time
import datetime
from optparse import OptionParser

import gpxpy
import gpxpy.gpx

DEFAULT_OUTPUT_DIR = "output"
verbose = False
hasElevation = False
elevationInFeet = False

parser = OptionParser(
  usage="%prog <path/to/gpx/data> [options]\n\nConvert GPX data file(s) into "
        "NuPIC input file for the Geospatial Tracking Application. You may "
        "specify a path to one GPX data file, or a directory containing many "
        "GPX data files, which will be processed and sorted by track start "
        "time."
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


def run(inputPath, outputDir):
  outputFile = os.path.join(outputDir, "out.csv")
  outFiles = {}

  with open(inputPath) as inputCsv:
    reader = csv.DictReader(inputCsv)
    for line in reader:
      animalName = line['individual-local-identifier']
      # event-id,visible,timestamp,location-long,location-lat,algorithm-marked-outlier,gps:hdop,gps:satellite-count,gps:vdop,ground-speed,heading,height-raw,sensor-type,individual-taxon-canonical-name,tag-local-identifier,individual-local-identifier,study-name,study-timezone,study-local-timestamp
      if not animalName in outFiles:
        outFiles[animalName] = []

      outFiles[animalName].append(line)

  for name in outFiles.keys():
    outputFile = os.path.join(outputDir, "%s.csv" % name)
    with open(outputFile, 'w') as fileOut:
      writer = csv.writer(fileOut)
      outputRows = outFiles[name]
      for row in outputRows:
        rowTime = datetime.datetime.strptime(row['timestamp'], "%Y-%m-%d %H:%M:%S.%f")
        timestamp = int(time.mktime(rowTime.timetuple()))
        # [track.name, ts, point.longitude, point.latitude, elevation, metersPerSecond, None, 1]
        writer.writerow([
          name,
          timestamp,
          row['location-long'],
          row['location-lat'],
          0,
          row['ground-speed'],
          None,
          1
        ])

    print "Wrote output file %s." % outputFile


if __name__ == "__main__":
  (options, args) = parser.parse_args(sys.argv[1:])
  try:
    inputPath = args.pop(0)
  except IndexError:
    parser.print_help(sys.stderr)
    sys.exit()

  verbose = options.verbose

  run(
    inputPath,
    options.output_dir)
