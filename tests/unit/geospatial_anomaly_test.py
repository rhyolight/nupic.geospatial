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

import unittest
from mock import Mock, patch



class TestGeoSpatialAnomaly(unittest.TestCase):


  def testAddEncodersToModelParams(self):
    # Mocks out the required nupic modules within geospatial_anomaly.py
    mockNuPICImport = Mock()
    mockModules = {
      "nupic": mockNuPICImport,
      "nupic.data": mockNuPICImport.data,
      "nupic.frameworks": mockNuPICImport.frameworks,
      "nupic.frameworks.opf": mockNuPICImport.frameworks.opf,
      "nupic.frameworks.opf.modelfactory": mockNuPICImport.frameworks.opf.modelfactory,
    }
    with patch.dict("sys.modules", mockModules):
      from model.geospatial_anomaly import addTimeEncoders

    mockParams = {
      "modelParams": {
        "sensorParams": {
          "encoders": {}
        }
      }
    }

    result = addTimeEncoders(mockParams)

    self.assertTrue("timestamp_timeOfDay" in
                    result["modelParams"]["sensorParams"]["encoders"],
                    "No new time encoer was added to model params.")


if __name__ == '__main__':
  unittest.main()
