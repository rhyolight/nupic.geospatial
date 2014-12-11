#!/usr/bin/env python
# ----------------------------------------------------------------------
# Numenta Platform for Intelligent Computing (NuPIC)
# Copyright (C) 2013, Numenta, Inc.  Unless you have purchased from
# Numenta, Inc. a separate commercial license for this software code, the
# following terms and conditions apply:
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses.
#
# http://numenta.org/licenses/
# ----------------------------------------------------------------------
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
hasElevation = False

parser = OptionParser(
  usage="%prog <path/to/gpx/data> [options]\n\nConvert GPX data file(s) into "
        "NuPIC input file for the Geospatial Tracking Application. You may "
        "specify a path to one GPX data file, or a directory containing many "
        "GPX data files, which will be processed and sorted by track start "
        "time."
)

parser.add_option(
  "-e",
  "--elevation",
  action="store_true",
  default=False,
  dest="hasElevation",
  help="Elevation data inside <ele> tags will be included in the output if it's present in the GPX file."
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

  # Return fast if points are in the same place
  if lat1 == lat2 and long1 == long2:
    return 0

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
  arc = math.acos(cos)

  # Multiplied to get M
  return arc * 6373000



def readGpxTracksFromFile(inputPath):
  if verbose:
    print "Reading GPX file %s" % inputPath
  inputFileName = os.path.splitext(os.path.basename(inputPath))[0]
  gpxFile = open(inputPath, 'r')
  gpx = gpxpy.parse(gpxFile)
  return inputFileName, gpx.tracks



def readTracksFromGpxFilesInDirectory(inputDir):
  if verbose:
    print "Reading GPX files in directory %s" % inputDir
  tracks = []
  dirName = inputDir.split("/").pop()
  for gpxFileName in os.listdir(inputDir):
    _, fileTracks = readGpxTracksFromFile(os.path.join(inputDir, gpxFileName))
    tracks = tracks + fileTracks
  return dirName, tracks



def sortTracksByDateAscending(tracks):
  return sorted(tracks, key=lambda track: track.segments[0].points[0].time)



def run(inputPath, outputDir):

  if os.path.isdir(inputPath):
    inputFileName, tracks = readTracksFromGpxFilesInDirectory(inputPath)
  else:
    inputFileName, tracks = readGpxTracksFromFile(inputPath)

  tracks = sortTracksByDateAscending(tracks)
  lastPoint = None
  outputRows = []

  for track in tracks:
    if verbose:
      print "Processing track %s..." % track.name
    for segment in track.segments:
      for point in segment.points:
        ts = int(time.mktime(point.time.timetuple()) * 1000)
        metersPerSecond = 0
        if lastPoint:
          distanceTravelled = distanceOnUnitSphereInMeters(lastPoint, point)
          msSinceLastPoint = ts - int(time.mktime(lastPoint.time.timetuple()) * 1000)
          if msSinceLastPoint > 0:
            metersPerSecond = distanceTravelled / (msSinceLastPoint / 1000)

        outputRows.append([track.name, ts, point.longitude, point.latitude, None, metersPerSecond, None, 1])
        lastPoint = point

  outputFile = os.path.join(outputDir, "%s.csv" % inputFileName)
  with open(outputFile, 'w') as fileOut:
    writer = csv.writer(fileOut)
    for row in outputRows:
      writer.writerow(row)

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