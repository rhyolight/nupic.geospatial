#!/usr/bin/env python
import sys
import os
import csv
import math
import time
from optparse import OptionParser

import gpxpy
import gpxpy.gpx

DEFAULT_OUTPUT_DIR = "output"
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


def distanceOnUnitSphereInMeters(point1, point2):
  lat1 = point1.latitude
  long1 = point1.longitude
  lat2 = point2.latitude
  long2 = point2.longitude

  # Convert latitude and longitude to
  # spherical coordinates in radians.
  degreesToRadians = math.pi/180.0

  # phi = 90 - latitude
  phi1 = (90.0 - lat1) * degreesToRadians
  phi2 = (90.0 - lat2) * degreesToRadians

  # theta = longitude
  theta1 = long1 * degreesToRadians
  theta2 = long2 * degreesToRadians

  cos = (math.sin(phi1) * math.sin(phi2) * math.cos(theta1 - theta2) +
         math.cos(phi1) * math.cos(phi2))
  arc = math.acos( cos )

  # Multiplied to get M
  return arc * 6373000


def run(inputPath, outputDir):

  gpxFile = open(inputPath, 'r')
  gpx = gpxpy.parse(gpxFile)

  outputFile = os.path.join(outputDir, "converted_gpx_output.csv")
  lastPoint = None

  with open(outputFile, 'w') as fileOut:
    writer = csv.writer(fileOut)
    for track in gpx.tracks:
      if verbose:
        print track.name
      for segment in track.segments:
        for point in segment.points:
          ts = int(time.mktime(point.time.timetuple()) * 1000)
          metersPerSecond = 0
          if lastPoint:
            distanceTravelled = distanceOnUnitSphereInMeters(lastPoint, point)
            msSinceLastPoint = ts - int(time.mktime(lastPoint.time.timetuple()) * 1000)
            if msSinceLastPoint > 0:
              metersPerSecond = distanceTravelled / (msSinceLastPoint / 1000)

          if verbose:
            print "{0}: ({1},{2})".format(point.time.__str__(), point.latitude, point.longitude)
          writer.writerow([track.name, ts, point.longitude, point.latitude, None, metersPerSecond, None, 1])
          lastPoint = point
  print "Wrote output file %s." % outputFile


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