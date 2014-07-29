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


def distance_on_unit_sphere_in_meters(point1, point2):
  lat1 = point1.latitude
  long1 = point1.longitude
  lat2 = point2.latitude
  long2 = point2.longitude

  # Convert latitude and longitude to
  # spherical coordinates in radians.
  degrees_to_radians = math.pi/180.0

  # phi = 90 - latitude
  phi1 = (90.0 - lat1)*degrees_to_radians
  phi2 = (90.0 - lat2)*degrees_to_radians

  # theta = longitude
  theta1 = long1*degrees_to_radians
  theta2 = long2*degrees_to_radians

  cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) +
         math.cos(phi1)*math.cos(phi2))
  arc = math.acos( cos )

  # Multiplied to get M
  return arc * 6373000


def run(input_path, output_dir):

  gpx_file = open(input_path, 'r')
  gpx = gpxpy.parse(gpx_file)

  output_file = os.path.join(output_dir, "converted_gpx_output.csv")
  last_point = None

  with open(output_file, 'w') as file_out:
    writer = csv.writer(file_out)
    for track in gpx.tracks:
      if verbose:
        print track.name
      for segment in track.segments:
        for point in segment.points:
          ts = int(time.mktime(point.time.timetuple()) * 1000)
          meters_per_second = 0
          if last_point:
            distance_travelled = distance_on_unit_sphere_in_meters(last_point, point)
            ms_since_last_point = ts - int(time.mktime(last_point.time.timetuple()) * 1000)
            if ms_since_last_point > 0:
              meters_per_second = distance_travelled / (ms_since_last_point / 1000)

          if verbose:
            print "{0}: ({1},{2})".format(point.time.__str__(), point.latitude, point.longitude)
          writer.writerow([track.name, ts, point.longitude, point.latitude, None, meters_per_second, None, 1])
          last_point = point
  print "Wrote output file %s." % output_file


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